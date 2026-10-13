import sys,unittest,tempfile,datetime as dt,contextlib,io,json
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parents[1]))
import news_check as cli
from storage import resolve_storage
class NewsFreshnessTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);b=Path(self.tmp.name).resolve();m=b/'m';m.mkdir();i=b/'i';i.mkdir()
  def probe(m,i):return {'mount':str(m),'backing_image':str(i),'mount_verified':True,'encryption_verified':True,'filesystem':'apfs'}
  self.paths=resolve_storage(m/'state',mount=m,image=i,initialize=True,probe=probe,environ={})
  self.packet={'request_id':'same-id','observed_at':'2026-10-12T23:30:00+00:00','window':['2026-10-12T00:00:00-04:00','2026-10-13T00:00:00-04:00'],'status':'partial','headlines':[],'headline_count':0,'digest':'','digest_words':0,'coverage':{},'paid_calls':0,'fallback_required':[],'source_evidence':[],'civic_evidence':[]}
  self.packet['packet_sha256']=cli.digest(self.packet);self.path=self.paths.receipts/('news-'+cli.hashlib.sha256(b'same-id').hexdigest()+'.json');self.path.write_text(json.dumps(self.packet));self.path.chmod(0o600)
 def test_next_eastern_day_rejected_no_fetch_or_packet_change(self):
  before=self.path.read_bytes()
  with patch.object(cli,'acquire',side_effect=AssertionError('no fetch')) as acquire:
   with self.assertRaisesRegex(ValueError,'historical packet'):cli.check('same-id',paths=self.paths,now=dt.datetime(2026,10,13,5,tzinfo=dt.timezone.utc))
   acquire.assert_not_called()
  self.assertEqual(before,self.path.read_bytes())
 def test_same_eastern_day_across_utc_midnight_reuses_and_exposes_age(self):
  with patch.object(cli,'acquire',side_effect=AssertionError('no fetch')):
   p=cli.check('same-id',paths=self.paths,now=dt.datetime(2026,10,13,2,tzinfo=dt.timezone.utc))
  self.assertEqual(p,self.packet)
  with patch.object(cli,'build_context',side_effect=ValueError('fixture')):out=cli.delivery(p,now=dt.datetime(2026,10,13,2,tzinfo=dt.timezone.utc))
  self.assertEqual(out['packet_reuse_status'],'current_business_day');self.assertEqual(out['packet_age_seconds'],9000);self.assertEqual(out['packet_business_date'],'2026-10-12');self.assertEqual(out['observed_at'],p['observed_at']);self.assertEqual(out['window'],p['window'])
 def test_midnight_historical_delivery_suppresses_birthday_and_no_refetch(self):
  stdout=io.StringIO()
  with patch.object(sys,'argv',['news_check.py','--request-id','synthetic-run']),patch.object(cli,'check',return_value=self.packet) as check,patch.object(cli,'delivery',return_value={'packet_reuse_status':'historical_only'}) as delivery,patch.object(cli,'reuse_for_news') as shared,patch.object(cli,'acquire') as acquire,contextlib.redirect_stdout(stdout):code=cli.main()
  self.assertEqual(code,2);self.assertEqual(json.loads(stdout.getvalue())['reason'],'packet_crossed_business_date_boundary');check.assert_called_once();delivery.assert_called_once();shared.assert_not_called();acquire.assert_not_called()
 def test_literal_placeholder_stops_before_work(self):
  stdout=io.StringIO()
  with patch.object(sys,'argv',['news_check.py','--request-id','news-ACTUAL_UTC_RUN_TIME']),patch.object(cli,'check') as check,patch.object(cli,'delivery') as delivery,patch.object(cli,'reuse_for_news') as shared,contextlib.redirect_stdout(stdout):code=cli.main()
  self.assertEqual(code,2);check.assert_not_called();delivery.assert_not_called();shared.assert_not_called();self.assertEqual(json.loads(stdout.getvalue())['status'],'failed_closed');self.assertEqual(json.loads(stdout.getvalue())['reason'],'literal_request_timestamp_placeholder')
if __name__=='__main__':unittest.main()

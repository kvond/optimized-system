import sys,unittest,json,datetime as dt,hashlib,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from unittest.mock import patch
import shared_birthday as shared
from storage import resolve_storage
class SharedBirthdayTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);b=Path(self.tmp.name).resolve();m=b/'m';m.mkdir();i=b/'i';i.mkdir()
  def probe(m,i):return {'mount':str(m),'backing_image':str(i),'mount_verified':True,'encryption_verified':True,'filesystem':'apfs'}
  self.paths=resolve_storage(m/'state',mount=m,image=i,initialize=True,probe=probe,environ={});self.now=dt.datetime(2026,10,13,12,tzinfo=dt.timezone.utc)
  self.input=self.paths.root/shared.INPUT_NAME;self.input.write_bytes(b'fixture');self.input.chmod(0o600)
  self.packet=self.paths.receipts/'fixture.json';self.result={'business_date':'2026-10-13','fingerprint':'fp','input_sha256':hashlib.sha256(b'fixture').hexdigest(),'items':{'eligible':[{'event_id':'private','occurrence_date':'2026-10-19'},{'event_id':'private2','occurrence_date':'2026-11-10'}]},'reconciliation_status':'partial','scoped_hold_count':2};self.write()
  self.summary={'status':'complete','current_window_coverage_complete':True,'receipt_path':str(self.packet),'fingerprint':'fp','counts':{'eligible':2}}
 def write(self):self.packet.write_text(json.dumps({'result':self.result}));self.packet.chmod(0o600)
 def call(self):
  with patch.object(shared,'run',return_value=self.summary):return shared.reuse_for_news('fixture',paths=self.paths,now=self.now)
 def test_current_reuse_thresholds_private_packet(self):
  r=self.call();self.assertTrue(r['duplicate_source_read_skipped']);self.assertEqual(r['eligible_within21_days'],1);self.assertEqual(r['eligible_within7_days'],1);self.assertEqual(r['out_of_window_hold_count'],2);self.assertNotIn('private2',json.dumps(r))
 def test_stale_receipt(self):
  self.result['business_date']='2026-10-12';self.write()
  with self.assertRaises(ValueError):self.call()
 def test_input_tamper_and_fingerprint_conflict(self):
  self.input.write_bytes(b'tampered')
  with self.assertRaises(ValueError):self.call()
  self.input.write_bytes(b'fixture');self.summary['fingerprint']='different'
  with self.assertRaises(ValueError):self.call()
 def test_partial_unknown_never_zero(self):
  self.summary['status']='partial';r=self.call();self.assertIsNone(r['counts']);self.assertFalse(r['duplicate_source_read_skipped'])
if __name__=='__main__':unittest.main()

import contextlib,io,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parents[1]))
import news_check

class NewsBirthdayMainTests(unittest.TestCase):
 def execute(self,reuse=None,error=None):
  packet={'synthetic_packet':True}
  feed={'request_id':'synthetic-run','status':'partial','digest':'Synthetic public headline','headline_count':1,'paid_calls':0,'packet_sha256':'fixture-hash'}
  stream=io.StringIO()
  with patch.object(sys,'argv',['news_check.py','--request-id','synthetic-run']),patch.object(news_check,'check',return_value=packet) as check,patch.object(news_check,'delivery',return_value=feed.copy()) as delivery,patch.object(news_check,'reuse_for_news',return_value=reuse,side_effect=error) as shared,patch.object(news_check,'acquire',side_effect=AssertionError('no actual source access')),contextlib.redirect_stdout(stream):
   code=news_check.main()
  check.assert_called_once_with('synthetic-run');delivery.assert_called_once_with(packet);shared.assert_called_once_with('synthetic-run')
  return code,json.loads(stream.getvalue())
 def test_verified_same_day_birthday_reuse_follows_feed_packet(self):
  reuse={'status':'verified_reuse','business_date':'2026-10-13','counts':{'eligible':1},'duplicate_source_read_skipped':True,'api_reads':0,'ai_calls':0,'private_eligible_packet_path':'/synthetic-private/packet.json','news_thresholds_preserved':[21,7]}
  code,out=self.execute(reuse=reuse)
  self.assertEqual(code,0);self.assertEqual(out['birthday_source_reuse'],reuse)
  self.assertEqual(out['headline_count'],1);self.assertEqual(out['paid_calls'],0)
  self.assertEqual(out['delivery_sha256'],news_check.digest({k:v for k,v in out.items() if k!='delivery_sha256'}))
 def test_shared_source_failure_preserves_feed_and_unknown_birthday(self):
  code,out=self.execute(error=ValueError('synthetic unavailable'))
  self.assertEqual(code,0);self.assertEqual(out['digest'],'Synthetic public headline');self.assertEqual(out['packet_sha256'],'fixture-hash')
  self.assertEqual(out['birthday_source_reuse']['status'],'hold');self.assertIsNone(out['birthday_source_reuse']['counts'])
  self.assertFalse(out['birthday_source_reuse']['duplicate_source_read_skipped']);self.assertEqual(out['paid_calls'],0)
  self.assertIn('birthday_refresh',out['execution_notes'])
if __name__=='__main__':unittest.main()

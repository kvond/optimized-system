import sys,json,unittest,tempfile,datetime as dt
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from unittest.mock import patch
import birthday_check as cli
from storage import resolve_storage
class BirthdayCLITests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);base=Path(self.tmp.name).resolve();m=base/'mount';m.mkdir();i=base/'image';i.mkdir()
  def probe(m,i):return {'mount':str(m),'backing_image':str(i),'mount_verified':True,'encryption_verified':True,'filesystem':'apfs'}
  self.paths=resolve_storage(m/'state',mount=m,image=i,initialize=True,probe=probe,environ={});self.now=dt.datetime(2026,10,13,12,tzinfo=dt.timezone.utc)
  source={'source_id':'receipt','revision':'r1','complete':True,'available':True,'observed_at':self.now.isoformat()}
  self.data={'task_id':cli.TASK_ID,'calendar_id':'synthetic-calendar','project_id':'synthetic-project','scope':'home-birthday-gifts','normalization_complete':True,'family_bindings':[{'event_id':'opaque','history_task_id':'t1','source_receipt_id':'r1','verified':True}],'events':[{'event_id':'opaque','occurrence_date':'2026-10-20'}],'history':[],'calendar_source':source,'history_source':source,'source_receipt_path':'private source receipt'}
  self.file=self.paths.root/cli.INPUT_NAME;self.write()
 def write(self):
  self.file.write_text(json.dumps(self.data));self.file.chmod(0o600)
 def call(self,key='a'):
        context='Synthetic verified supplemental context'
        with patch.object(cli,'build_context',return_value={'context':context,'context_sha256':cli.hashlib.sha256(context.encode()).hexdigest(),'context_words':len(context.split())}),patch.object(cli,'CALENDAR_BINDING_SHA256',cli.hashlib.sha256(b'synthetic-calendar').hexdigest()),patch.object(cli,'PROJECT_BINDING_SHA256',cli.hashlib.sha256(b'synthetic-project').hexdigest()):return cli.run(key,paths=self.paths,now=self.now)
 def test_complete_readback_repeat_and_conflict(self):
  a=self.call();self.assertEqual(a['counts']['eligible'],1);self.assertNotIn('opaque',json.dumps(a));self.assertEqual(a,self.call())
  self.data['events'][0]['occurrence_date']='2026-10-21';self.write()
  with self.assertRaises(ValueError):self.call()
 def test_unknown_family_never_zero_or_eligible(self):
  self.data['family_bindings']=[];self.write();r=self.call();self.assertIsNone(r['counts']);self.assertEqual(r['status'],'blocked')
 def test_unrelated_excluded_scoped_hold_does_not_block_known_eligible(self):
  self.data['scoped_holds']=[{'history_task_id':'private-other','current_window':False,'reason':'crosswalk'}];self.write()
  r=self.call();self.assertEqual(r['counts']['eligible'],1);self.assertTrue(r['current_window_coverage_complete']);self.assertEqual(r['reconciliation_status'],'partial');self.assertNotIn('private-other',json.dumps(r))
  self.data['scoped_holds'][0]['current_window']=True;self.write();r=self.call('b');self.assertEqual(r['status'],'partial');self.assertFalse(r['current_window_coverage_complete']);self.assertEqual(r['counts']['eligible'],1)
 def test_stale_and_wrong_scope_hold(self):
  self.data['history_source']['observed_at']='2026-10-12T12:00:00+00:00';self.write();self.assertIsNone(self.call()['counts'])
  self.data['calendar_id']='other';self.write()
  with self.assertRaises(ValueError):self.call('b')
if __name__=='__main__':unittest.main()

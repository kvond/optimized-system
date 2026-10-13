import concurrent.futures, threading, copy, datetime as dt, json, pathlib, sys, tempfile, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from foundation import Store, UTC
from runner import Controller, SourceSnapshot, digest, validate_routes
class Adapter:
 def __init__(self,now):self.now=now;self.data={'a':{'revision':'1','content':{'value':2}},'b':{'revision':'1','content':{'value':5}}};self.calls=0
 def snapshot(self,id,partition,max_bytes):
  self.calls+=1;d=self.data[id];content=d['content']
  return SourceSnapshot(id,d['revision'],partition,d.get('authorized',True),d.get('readable',True),d.get('complete',True),d.get('observed_at',self.now()),content,d.get('hash',digest(content)))
class RunnerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.now=dt.datetime(2026,10,12,14,tzinfo=UTC);self.store=Store(pathlib.Path(self.tmp.name)/'private.sqlite',now=lambda:self.now)
  self.adapter=Adapter(lambda:self.now);self.effects=0
  self.config={'version':'1','routes':[{'name':'local','provider':'local','capability':0,'estimated_cost':'0','privacy_partitions':['synthetic'],'deterministic':True,'enabled':True}]}
  def handler(task,content,inputs):self.effects+=1;return {'double':content['value']*2}
  self.controller=Controller(self.store,adapter=self.adapter,routes=self.config,handlers={'local':handler})
  self.request={'request_id':'one','privacy_partition':'synthetic','contract_version':'1','inputs':{},'components':[{'component_id':i,'source_id':i,'source_revision':'1','task_type':'double','required_capability':0} for i in ['a','b']]}
 def tearDown(self):self.tmp.cleanup()
 def test_snapshot_taken_after_start_is_checked_against_post_read_clock(self):
  self.store.now=lambda:dt.datetime.now(UTC);self.adapter.now=self.store.now
  receipt=self.controller.execute(self.request);self.assertEqual(receipt['status'],'complete')
 def test_atomic_receipt_readback_and_identical_id_no_duplicate(self):
  first=self.controller.execute(self.request);self.assertEqual(first['status'],'complete');self.assertEqual(self.effects,2)
  self.assertEqual(first,self.controller.execute(self.request));self.assertEqual(self.effects,2);self.assertEqual(self.adapter.calls,4)
  self.assertIsNone(first['provider']);self.assertIsNone(first['model']);self.assertEqual(first['paid_dispatches'],0)
  self.assertEqual(self.controller.readback(first)['components']['a']['output'],{'double':4})
  self.now+=dt.timedelta(days=1)
  self.assertEqual(first,self.controller.execute(self.request));self.assertEqual(self.effects,4)
  conflict=copy.deepcopy(self.request);conflict['inputs']={'changed':True}
  with self.assertRaises(ValueError):self.controller.execute(conflict)
 def test_coverage_and_access_revalidated_before_cached_results(self):
  self.controller.execute(self.request);self.adapter.data['b']['complete']=False
  receipt=self.controller.execute(self.request);result=self.controller.readback(receipt)
  self.assertEqual(receipt['status'],'partial');self.assertEqual(result['components']['b']['reason'],'coverage_incomplete');self.assertEqual(self.effects,2)
  self.adapter.data['a']['authorized']=False
  receipt=self.controller.execute(self.request);self.assertEqual(self.controller.readback(receipt)['components']['a']['reason'],'access_denied')
 def test_changed_component_only_recomputed_for_new_revision(self):
  self.controller.execute(self.request);self.adapter.data['b']['revision']='2';self.adapter.data['b']['content']={'value':8}
  stale=copy.deepcopy(self.request);stale['request_id']='stale'
  receipt=self.controller.execute(stale);self.assertEqual(self.controller.readback(receipt)['components']['b']['reason'],'source_revision_changed');self.assertEqual(self.effects,2)
  changed=copy.deepcopy(self.request);changed['request_id']='two';changed['components'][1]['source_revision']='2'
  receipt=self.controller.execute(changed);self.assertEqual(receipt['status'],'complete');self.assertEqual(self.effects,3)
 def test_partial_repair_reuses_complete_component(self):
  self.adapter.data['b']['readable']=False;first=self.controller.execute(self.request);self.assertEqual(first['status'],'partial');self.assertEqual(self.effects,1)
  self.adapter.data['b']['readable']=True;second=self.controller.execute(self.request);self.assertEqual(second['status'],'complete');self.assertEqual(self.effects,2)
 def test_invalid_snapshot_hash_and_freshness_block(self):
  self.adapter.data['a']['hash']='incorrect';self.adapter.data['b']['observed_at']=self.now-dt.timedelta(seconds=301)
  receipt=self.controller.execute(self.request);result=self.controller.readback(receipt)
  self.assertEqual(result['components']['a']['reason'],'source_hash_mismatch');self.assertEqual(result['components']['b']['reason'],'source_observation_stale');self.assertEqual(self.effects,0)
 def test_paid_route_never_dispatched(self):
  config=copy.deepcopy(self.config);config['routes'][0].update(deterministic=False,estimated_cost='0.1',provider='unknown')
  controller=Controller(self.store,adapter=self.adapter,routes=config,handlers={'local':lambda *a:self.fail('AI dispatch')})
  receipt=controller.execute(self.request);self.assertEqual(receipt['status'],'partial');self.assertEqual(receipt['paid_dispatches'],0)
 def test_route_contract_change_requires_new_request_identity(self):
  self.controller.execute(self.request);changed=copy.deepcopy(self.config);changed['version']='2'
  controller=Controller(self.store,adapter=self.adapter,routes=changed,handlers={'local':lambda *a:self.fail('duplicate effect')})
  with self.assertRaises(ValueError):controller.execute(self.request)
 def test_runtime_route_validation_rejects_coercion_nan_privacy(self):
  for field,bad in [('enabled','true'),('deterministic',1),('capability',True),('estimated_cost','NaN'),('estimated_cost','-1'),('estimated_cost','1e-2'),('privacy_partitions',['synthetic',1])]:
   config=copy.deepcopy(self.config);config['routes'][0][field]=bad
   with self.subTest(field=field,bad=bad),self.assertRaises((ValueError,TypeError)):validate_routes(config)
 def test_receipt_readback_detects_tampering_before_any_reexecution(self):
  receipt=self.controller.execute(self.request)
  with self.store.transaction() as db:db.execute("UPDATE runner_requests SET result='{}'")
  with self.assertRaises(ValueError):self.controller.readback(receipt)
  with self.assertRaises(ValueError):self.controller.execute(self.request)
  self.assertEqual(self.effects,2)
 def test_blocked_adapter_does_not_hold_sqlite_writer(self):
  entered=threading.Event();release=threading.Event();original=self.adapter.snapshot
  def snapshot(*args):
   entered.set()
   if not release.wait(2):raise RuntimeError('test release missing')
   return original(*args)
  self.adapter.snapshot=snapshot
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   running=pool.submit(self.controller.execute,self.request)
   self.assertTrue(entered.wait(1))
   try:
    # A write must commit while the source callback is still blocked.
    writer=pool.submit(self.store.configure_budget,'synthetic','1')
    writer.result(timeout=.5)
    self.assertFalse(running.done())
   finally:release.set()
   self.assertEqual(running.result(timeout=1)['status'],'complete')
 def test_blocked_handler_does_not_hold_sqlite_writer(self):
  entered=threading.Event();release=threading.Event()
  def handler(task,content,inputs):
   entered.set()
   if not release.wait(2):raise RuntimeError('test release missing')
   return {'double':content['value']*2}
  self.controller.handlers={'local':handler}
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   running=pool.submit(self.controller.execute,self.request);self.assertTrue(entered.wait(1))
   try:pool.submit(self.store.configure_budget,'synthetic','1').result(timeout=.5)
   finally:release.set()
   self.assertEqual(running.result(timeout=1)['status'],'complete')
 def test_source_that_expires_during_computation_cannot_commit_success(self):
  request=copy.deepcopy(self.request);request['components']=request['components'][:1]
  def slow(task,content,inputs):
   self.now+=dt.timedelta(seconds=301);return {'value':2}
  self.controller.handlers={'local':slow}
  receipt=self.controller.execute(request);result=self.controller.readback(receipt)
  self.assertEqual(result['components']['a']['reason'],'source_observation_stale')
  with self.store.connection() as db:self.assertEqual(db.execute('SELECT COUNT(*) FROM cache').fetchone()[0],0)
 def test_expired_cache_recomputes_but_preserves_identical_receipt(self):
  first=self.controller.execute(self.request);self.assertEqual(self.effects,2)
  self.now+=dt.timedelta(seconds=301)
  second=self.controller.execute(self.request);self.assertEqual(first,second);self.assertEqual(self.effects,4)
  self.controller.execute(self.request);self.assertEqual(self.effects,4)
 def test_concurrent_pure_computation_commits_coherent_duplicate_receipts(self):
  with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:receipts=list(pool.map(lambda _:self.controller.execute(self.request),range(12)))
  self.assertTrue(all(r==receipts[0] for r in receipts));self.assertGreaterEqual(self.effects,2);self.assertLessEqual(self.effects,24)
if __name__=='__main__':unittest.main()

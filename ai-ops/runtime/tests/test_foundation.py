import concurrent.futures, datetime as dt, os, pathlib, sys, tempfile, time, unittest
from unittest.mock import patch, MagicMock
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from foundation import CacheContract, Store, Route, select_route, run_bounded, UTC
class FoundationTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.now=dt.datetime(2026,10,11,23,tzinfo=UTC)
  self.store=Store(pathlib.Path(self.tmp.name)/'state.sqlite',now=lambda:self.now)
 def tearDown(self): self.tmp.cleanup()
 def contract(self,**changes):
  data=dict(privacy_partition='school',source_id='deck',source_revision='r1',task_type='extract',contract_version='1',inputs={'question':3},route_version='1');data.update(changes);return CacheContract(**data)
 def test_source_revision_privacy_contract_and_expiry(self):
  self.store.put(self.contract(),{'value':7},self.now+dt.timedelta(seconds=5),succeeded=True)
  self.assertEqual(self.store.get(self.contract()),{'value':7})
  for c in [self.contract(source_revision='r2'),self.contract(privacy_partition='personal'),self.contract(contract_version='2'),self.contract(inputs={'question':4}),self.contract(route_version='2')]:self.assertIsNone(self.store.get(c))
  self.now+=dt.timedelta(seconds=5);self.assertIsNone(self.store.get(self.contract()))
 def test_failed_result_never_reusable_and_invalidation_partitioned(self):
  for partition in ('school','personal'):self.store.put(self.contract(privacy_partition=partition),{'ok':partition},self.now+dt.timedelta(days=1),succeeded=True)
  self.assertEqual(self.store.invalidate_source('school','deck'),1)
  self.assertIsNotNone(self.store.get(self.contract(privacy_partition='personal')))
  self.store.put(self.contract(),{'error':'timeout'},self.now+dt.timedelta(days=1),succeeded=False)
  self.assertIsNone(self.store.get(self.contract()))
 def test_budget_fail_closed_concurrent_and_idempotent_settlement(self):
  with self.assertRaises(PermissionError):self.store.reserve('school','0.1')
  self.store.configure_budget('school','1')
  def reserve(_):
   try:return self.store.reserve('school','0.1')
   except PermissionError:return None
  with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:ids=list(pool.map(reserve,range(30)))
  ids=[i for i in ids if i];self.assertEqual(len(ids),10)
  self.store.settle(ids[0],'0.1');self.store.settle(ids[0],'0.1')
  with self.assertRaises(ValueError):self.store.settle(ids[0],'0.2')
  with self.assertRaises(PermissionError):self.store.reserve('school','0.1')
  with self.assertRaises(PermissionError):self.store.cancel_unstarted(ids[1],execution_started=True)
  self.store.cancel_unstarted(ids[1],execution_started=False);self.store.reserve('school','0.1')
  with self.assertRaises(ValueError):self.store.configure_budget('school','0.9')
 def test_overrun_recorded_and_blocks_future_and_survives_reopen(self):
  self.store.configure_budget('school','1');r=self.store.reserve('school','0.5');self.store.settle(r,'1.1')
  reopened=Store(self.store.path,now=lambda:self.now)
  with self.assertRaises(PermissionError):reopened.reserve('school','0.01')
  for amount in ['NaN','-1','0.0000001']:
   with self.assertRaises(ValueError):self.store.reserve('school',amount)
 def test_lowest_cost_sufficient_and_deterministic_preferred(self):
  routes=[Route('large','vendor-a',3,'0.5',frozenset({'school'}),enabled=True),Route('small','vendor-b',1,'0.01',frozenset({'school'}),enabled=True),Route('other','vendor-c',3,'0.001',frozenset({'personal'}),enabled=True),Route('disabled','vendor-d',3,'0',frozenset({'school'})),Route('script','local',0,'0',frozenset({'school'}),deterministic=True,enabled=True)]
  self.assertEqual(select_route(routes,required_capability=0,partition='school').name,'script')
  self.assertEqual(select_route(routes,required_capability=1,partition='school').name,'small')
  self.assertEqual(select_route(routes,required_capability=2,partition='school').name,'large')
  with self.assertRaises(PermissionError):select_route(routes,required_capability=4,partition='school')
 def test_naive_clocks_rejected(self):
  with self.assertRaises(ValueError):self.store.put(self.contract(),{},dt.datetime(2027,1,1),succeeded=True)
  with self.assertRaises(ValueError):run_bounded([sys.executable,'-c','pass'],deadline=dt.datetime(2027,1,1))
 def test_deadline_stops_leader_and_descendant_before_work_continues(self):
  marker=pathlib.Path(self.tmp.name)/'escaped.txt'
  child="import time,pathlib;time.sleep(0.7);pathlib.Path(%r).write_text('alive')"%str(marker)
  leader="import subprocess,sys,time;subprocess.Popen([sys.executable,'-c',%r]);time.sleep(10)"%child
  start=time.monotonic();result=run_bounded([sys.executable,'-c',leader],deadline=dt.datetime.now(UTC)+dt.timedelta(seconds=.35),grace_seconds=.05)
  self.assertTrue(result['timed_out']);self.assertLess(time.monotonic()-start,.6)
  time.sleep(.8);self.assertFalse(marker.exists())
 def test_os_signal_denial_is_explicit_and_direct_child_reaped(self):
  with patch('foundation.os.killpg',side_effect=PermissionError('synthetic OS denial')):
   result=run_bounded([sys.executable,'-c','import time;time.sleep(10)'],deadline=dt.datetime.now(UTC)+dt.timedelta(seconds=.2),grace_seconds=.03)
  self.assertFalse(result['cleanup_confirmed']);self.assertTrue(result['signal_errors']);self.assertIsNotNone(result['returncode'])
 def test_final_kill_denial_in_receipt_and_reap_timeout_bounded(self):
  import foundation
  real_killpg=foundation.os.killpg
  def deny_final(group,sig):
   if sig==foundation.signal.SIGKILL:raise PermissionError('final cleanup denial')
   return real_killpg(group,sig)
  with patch('foundation.os.killpg',side_effect=deny_final):
   result=run_bounded([sys.executable,'-c','pass'],deadline=dt.datetime.now(UTC)+dt.timedelta(seconds=1),grace_seconds=.02)
  self.assertTrue(result['signal_errors']);self.assertFalse(result['cleanup_confirmed'])
  self.assertTrue(result['reap_confirmed'])
 def test_reap_wait_cannot_request_time_beyond_remaining_deadline(self):
  import subprocess
  fake=MagicMock();fake.pid=99999999;fake.returncode=None;fake.poll.return_value=None
  fake.wait.side_effect=subprocess.TimeoutExpired('synthetic',.01)
  with patch('foundation.subprocess.Popen',return_value=fake),patch('foundation.os.killpg'):
   result=run_bounded(['synthetic'],deadline=dt.datetime.now(UTC)+dt.timedelta(seconds=.15),grace_seconds=.02)
  self.assertFalse(result['reap_confirmed']);self.assertFalse(result['cleanup_confirmed'])
  self.assertEqual(fake.wait.call_count,1)
  self.assertGreater(fake.wait.call_args.kwargs['timeout'],0)
  self.assertLessEqual(fake.wait.call_args.kwargs['timeout'],.07)
 def test_reset_guard_uses_supported_grace(self):
  import runpy
  calls=[]
  def fake(command,**kwargs):
   calls.append(kwargs);return {'returncode':0,'cleanup_confirmed':True}
  script=pathlib.Path(__file__).resolve().parents[1]/'reset_guard.py'
  class BeforeCutoff(dt.datetime):
   @classmethod
   def now(cls,tz=None):return cls(2026,10,11,23,tzinfo=UTC)
  with patch('foundation.run_bounded',side_effect=fake),patch.object(sys,'argv',[str(script),'synthetic-command']),patch('datetime.datetime',BeforeCutoff):
   with self.assertRaises(SystemExit) as stop:runpy.run_path(str(script),run_name='__main__')
  self.assertEqual(stop.exception.code,0);self.assertEqual(calls[0]['grace_seconds'],.5)
 def test_finished_leader_cleans_background_child_and_past_deadline_no_launch(self):
  marker=pathlib.Path(self.tmp.name)/'escaped.txt';child="import time,pathlib;time.sleep(.4);pathlib.Path(%r).write_text('alive')"%str(marker)
  leader="import subprocess,sys;subprocess.Popen([sys.executable,'-c',%r])"%child
  result=run_bounded([sys.executable,'-c',leader],deadline=dt.datetime.now(UTC)+dt.timedelta(seconds=2),grace_seconds=.05)
  self.assertFalse(result['timed_out']);time.sleep(.6);self.assertFalse(marker.exists())
  with self.assertRaises(TimeoutError):run_bounded([sys.executable,'-c',"raise RuntimeError('launched')"],deadline=dt.datetime.now(UTC)-dt.timedelta(seconds=1))
if __name__=='__main__':unittest.main()

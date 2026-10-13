import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
import unittest,tempfile,datetime as dt,json,time,os,sqlite3,struct,multiprocessing as mp
from unittest.mock import patch
import doe_check as cli
from storage import resolve_storage
from doe_source import AdapterResult,GRANT
from vacancies import SourceRead

def hang(): time.sleep(10)
def successful_spawn(send):
    os.setsid()
    now=dt.datetime.now(dt.timezone.utc)
    send.send(AdapterResult(SourceRead(GRANT,'spawn-fixture',now,True,False,True,True,[]),None,{'posting_count':0}))
    send.close()
def failing_spawn(send):
    os.setsid()
    send.send({'worker_exception_class':'SyntheticStartupFailure'})
    send.close()
def partial_frame(send):
    os.setsid()
    os.write(send.fileno(), struct.pack('!i', 100000) + b'x')
    time.sleep(10)
class DOECheckTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        base=Path(self.temp.name).resolve();self.mount=base/'mount';self.mount.mkdir();self.image=base/'image';self.image.mkdir()
        def probe(m,i):return {'mount':str(m),'backing_image':str(i),'filesystem':'apfs','mount_verified':True,'encryption_verified':True}
        self.paths=resolve_storage(self.mount/'state',mount=self.mount,image=self.image,initialize=True,probe=probe,environ={})
    def result(self,complete=True):
        now=dt.datetime.now(dt.timezone.utc)
        records=[{'vacancy_id':'7','official_url':'https://www.applitrack.com/job?id=7','fields':{'title':'PUBLIC BODY SENTINEL'}}] if complete else []
        return AdapterResult(SourceRead(GRANT,'r1',now,True,False,complete,complete,records),None,{'posting_count':1 if complete else None})
    def test_real_spawn_transport_acceptance(self):
        result=cli.acquire(deadline=5,_worker_target=successful_spawn)
        self.assertTrue(result.read.complete)
        self.assertEqual(result.evidence['worker_start_method'],'spawn')
        self.assertTrue(result.evidence['worker_result_received'])
    def test_spawn_failure_has_sanitized_diagnostics(self):
        result=cli.acquire(deadline=5,_worker_target=failing_spawn)
        self.assertFalse(result.read.complete)
        self.assertEqual(result.evidence['worker_exception_class'],'SyntheticStartupFailure')
        self.assertIn('worker_exitcode',result.evidence)
    def test_seed_repeat_incomplete_preserves_and_no_bodies(self):
        with patch.object(cli,'acquire',return_value=self.result()):first=cli.check('seed',paths=self.paths)
        self.assertEqual(first['counts']['new'],1);self.assertNotIn('SENTINEL',json.dumps(first))
        with patch.object(cli,'acquire',side_effect=AssertionError('no refetch')):repeat=cli.check('seed',paths=self.paths)
        self.assertTrue(repeat['reused_request'])
        with patch.object(cli,'acquire',return_value=self.result()):fresh=cli.check('fresh',paths=self.paths)
        self.assertEqual(fresh['counts']['unchanged'],1)
        with patch.object(cli,'acquire',return_value=self.result(False)):blocked=cli.check('partial',paths=self.paths)
        self.assertTrue(all(v is None for v in blocked['counts'].values()))
        with sqlite3.connect(self.paths.root/'vacancies.sqlite') as db:self.assertEqual(db.execute('SELECT active FROM vacancy_current').fetchone()[0],1)
    def test_conflicting_artifact_detected(self):
        with patch.object(cli,'acquire',return_value=self.result()):r=cli.check('seed',paths=self.paths)
        p=Path(r['receipt_path']);d=json.loads(p.read_text());d['receipt']['request_id']='other';p.write_text(json.dumps(d))
        with self.assertRaises(ValueError):cli.check('seed',paths=self.paths)
    def test_actual_child_timeout_cleanup(self):
        started=time.monotonic()
        with patch.object(cli.doe_source,'read_source',hang):r=cli.acquire(deadline=.1,_context=mp.get_context('fork'))
        self.assertLess(time.monotonic()-started,3);self.assertFalse(r.read.complete);self.assertIsNone(r.evidence['posting_count'])
        self.assertTrue(r.evidence['child_cleanup_confirmed']);self.assertFalse((self.paths.root/'vacancies.sqlite').exists())
    def test_ejection_after_fetch_prevents_state_write(self):
        with patch.object(cli,'_resolve_again',side_effect=[self.paths,RuntimeError('ejected')]),patch.object(cli,'acquire',return_value=self.result()):
            with self.assertRaises(RuntimeError):cli.check('x',paths=self.paths)
        self.assertFalse((self.paths.root/'vacancies.sqlite').exists())
    def test_partial_frame_cannot_extend_acquisition(self):
        start=time.monotonic()
        with patch.object(cli,'_worker',partial_frame):r=cli.acquire(deadline=.1,_context=mp.get_context('fork'))
        self.assertLess(time.monotonic()-start,3)
        self.assertTrue(r.evidence['child_cleanup_confirmed'])
    def test_start_failure_closes_pipe_ends(self):
        context=mp.get_context('fork'); receive,send=context.Pipe(duplex=False)
        with patch.object(cli.mp,'get_context',return_value=context),patch.object(context,'Pipe',return_value=(receive,send)),patch.object(context,'Process') as factory:
            factory.return_value.pid=None
            factory.return_value.start.side_effect=OSError('start failed')
            with self.assertRaises(RuntimeError):cli.acquire(deadline=.1,_context=context)
        self.assertTrue(receive.closed);self.assertTrue(send.closed)
    def test_setsid_failure_is_cleaned(self):
        with patch.object(cli.os,'setsid',side_effect=PermissionError('setsid denied')):r=cli.acquire(deadline=.1,_context=mp.get_context('fork'))
        self.assertFalse(r.read.complete);self.assertTrue(r.evidence['child_cleanup_confirmed'])
    def test_group_permission_failure_falls_back_owned_pid(self):
        with patch.object(cli.doe_source,'read_source',hang),patch.object(cli.os,'killpg',side_effect=PermissionError('group denied')):r=cli.acquire(deadline=.1,_context=mp.get_context('fork'))
        self.assertTrue(r.evidence['child_cleanup_confirmed'])
    def test_both_signal_denials_still_close_and_join(self):
        context=mp.get_context('fork'); receive,send=context.Pipe(duplex=False)
        with patch.object(cli.mp,'get_context',return_value=context),patch.object(context,'Pipe',return_value=(receive,send)),patch.object(context,'Process') as factory,patch.object(cli.os,'getpgid',return_value=123),patch.object(cli.os,'killpg',side_effect=PermissionError('denied')):
            process=factory.return_value;process.pid=123;process.is_alive.return_value=True
            process.kill.side_effect=PermissionError('pid denied')
            with self.assertRaisesRegex(RuntimeError,'cleanup unconfirmed'):cli.acquire(deadline=.05,_context=context)
            process.join.assert_called_once_with(timeout=2)
        self.assertTrue(receive.closed);self.assertTrue(send.closed)
    def test_cleanup_unconfirmed_no_gate_write(self):
        with patch.object(cli,'acquire',side_effect=RuntimeError('cleanup unconfirmed')):
            with self.assertRaises(RuntimeError):cli.check('never-write',paths=self.paths)
        self.assertFalse((self.paths.root/'vacancies.sqlite').exists())
    def test_storage_revalidation_before_fetch(self):
        with patch.object(cli,'_resolve_again',side_effect=RuntimeError('ejected')),patch.object(cli,'acquire') as fetch:
            with self.assertRaises(RuntimeError):cli.check('x',paths=self.paths)
            fetch.assert_not_called()
if __name__=='__main__':unittest.main()

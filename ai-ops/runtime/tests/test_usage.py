import concurrent.futures
import datetime as dt
import importlib.util
from pathlib import Path
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('usage',Path(__file__).parents[1]/'usage.py');usage=importlib.util.module_from_spec(spec);spec.loader.exec_module(usage)

class UsageTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'usage.db';self.clock=dt.datetime(2026,10,12,3,59,tzinfo=dt.timezone.utc)
        self.ledger=usage.UsageLedger(self.path,business_timezone='America/New_York',now=lambda:self.clock)
        for s in ['combined','workflow:summary','provider:p']:
            self.ledger.configure(s,daily='1',monthly='2')
    def tearDown(self):self.tmp.cleanup()
    def reserve(self,ident,cost='0.5',ledger=None):return (ledger or self.ledger).reserve(request_id=ident,workflow='summary',provider='p',model='small',estimated_cost=cost)
    def test_atomic_concurrent_reservations(self):
        def job(i):
            try:return self.reserve(str(i))['new']
            except PermissionError:return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(job,range(8)))
        self.assertEqual(sum(results),2)
        self.assertEqual(len(self.ledger.receipts()),2)
    def test_pending_survives_midnight_reopen_and_unknown_prices(self):
        self.reserve('a','1');self.clock+=dt.timedelta(minutes=2)
        reopened=usage.UsageLedger(self.path,business_timezone='America/New_York',now=lambda:self.clock)
        with self.assertRaises(PermissionError):self.reserve('b','0.01',reopened)
        with self.assertRaises(ValueError):self.reserve('c',None,reopened)
        self.assertEqual(reopened.receipts()[0]['state'],'pending')
        with self.assertRaises(ValueError):usage.UsageLedger(self.path,business_timezone='UTC')
    def test_receipts_unknown_tokens_overrun_and_conflict(self):
        self.reserve('a')
        kw=dict(receipt_id='r',actual_cost='1.2',duration_seconds=2,status='failed',retry_state='blocked',error_code='provider.timeout')
        self.ledger.settle('a',**kw);self.clock+=dt.timedelta(seconds=2);self.ledger.settle('a',**kw)
        r=self.ledger.receipts()[0];self.assertIsNone(r['receipt']['input_tokens']);self.assertEqual(r['receipt']['actual_micros'],1200000);self.assertIsNotNone(r['settled_at'])
        with self.assertRaises(PermissionError):self.reserve('b','0.01')
        with self.assertRaises(ValueError):self.ledger.settle('a',receipt_id='r',actual_cost='1.1')
    def test_business_window_monthly_budget_and_alert_dedup(self):
        self.clock=dt.datetime(2026,11,1,3,59,tzinfo=dt.timezone.utc) # still October in New York
        self.reserve('a','0.8');self.ledger.settle('a',receipt_id='r1',actual_cost='0.8',input_tokens=10,cached_tokens=0,output_tokens=4)
        first=self.ledger.alerts();self.assertTrue(any(a['window']=='2026-10-31' and a['threshold']==80 for a in first))
        self.ledger.settle('a',receipt_id='r1',actual_cost='0.8',input_tokens=10,cached_tokens=0,output_tokens=4);self.assertEqual(first,self.ledger.alerts())
        self.clock+=dt.timedelta(minutes=2);self.reserve('b','1');self.ledger.settle('b',receipt_id='r2',actual_cost='1')
        self.clock+=dt.timedelta(hours=25);self.reserve('c','1');self.ledger.settle('c',receipt_id='r3',actual_cost='1')
        self.clock+=dt.timedelta(days=1)
        with self.assertRaises(PermissionError):self.reserve('d','0.01')
    def test_missing_scope_idempotency_and_metadata_validation(self):
        with self.assertRaises(PermissionError):self.ledger.reserve(request_id='x',workflow='other',provider='p',model='small',estimated_cost='0.1')
        self.reserve('a');self.assertFalse(self.reserve('a')['new'])
        with self.assertRaises(ValueError):self.reserve('a','0.6')
        with self.assertRaises(ValueError):self.ledger.settle('a',receipt_id='r',actual_cost='0.1',input_tokens=True)
        with self.assertRaises(ValueError):self.ledger.settle('a',receipt_id='r',actual_cost='0.1',error_code='raw private content')
        self.assertEqual(self.ledger.receipts()[0]['state'],'pending')
    def test_workflow_provider_caps_and_pending_old_month(self):
        self.ledger.configure('workflow:summary',daily='0.4',monthly='0.4')
        with self.assertRaises(PermissionError):self.reserve('a','0.5')
        self.ledger.configure('workflow:summary',daily='1',monthly='2')
        self.ledger.configure('provider:p',daily='1',monthly='0.6')
        self.clock=dt.datetime(2026,11,1,3,59,tzinfo=dt.timezone.utc)
        self.reserve('b','0.5');self.clock+=dt.timedelta(minutes=2)
        with self.assertRaises(PermissionError):self.reserve('c','0.2')
        self.assertEqual(len(self.ledger.receipts()),1)
        self.ledger.settle('b',receipt_id='r',actual_cost='0.1')
        self.reserve('c','0.2')
        with self.assertRaises(ValueError):self.ledger.settle('c',receipt_id='r',actual_cost='0.2')
        self.assertEqual(self.ledger.receipts()[1]['state'],'pending')

    def test_private_existing_database_required(self):
        self.path.chmod(0o644)
        with self.assertRaises(PermissionError):usage.UsageLedger(self.path,business_timezone='America/New_York')

if __name__=='__main__':unittest.main()

import concurrent.futures
import datetime as dt
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).parents[1]))
import vacancies as v
from storage import RuntimePaths,StorageError

class VacancyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.mount=Path(self.tmp.name).resolve();self.root=self.mount/'private';self.root.mkdir(mode=0o700);self.now=dt.datetime(2026,10,12,20,tzinfo=dt.timezone.utc);self.online=True
        def probe(mount,image):return {'mount_verified':self.online,'encryption_verified':self.online,'filesystem':'apfs','mount':str(mount),'backing_image':str(image)}
        self.paths=RuntimePaths(self.root,self.root/'cache.sqlite',self.root/'usage.sqlite',self.root/'receipts',{'mount':str(self.mount),'backing_image':str(self.mount/'image')},probe)
        self.grant=v.Grant('public-vacancies','synthetic-employer','synthetic-official','full-list-v1','https://jobs.example.test')
        self.gate=v.VacancyGate(self.paths,approvals={'daily':[self.grant],'weekly':[self.grant]},now=lambda:self.now)
    def tearDown(self):self.tmp.cleanup()
    def record(self,id='a',title='Science teacher',url=None):return {'vacancy_id':id,'official_url':url or 'https://jobs.example.test/jobs/'+id,'fields':{'title':title,'location':'Synthetic district'}}
    def read(self,records,revision='1',**kw):
        params=dict(grant=self.grant,revision=revision,observed_at=self.now,authorized=True,authenticated=True,available=True,complete=True,records=records);params.update(kw);return v.SourceRead(**params)
    def test_new_changed_unchanged_closed_and_history(self):
        r=self.gate.apply('daily','one',self.read([self.record()]));self.assertEqual(r['counts']['new'],1);self.assertEqual(self.gate.readback(r)['classification']['new'],['a'])
        self.now+=dt.timedelta(seconds=1);r=self.gate.apply('weekly','two',self.read([self.record()]));self.assertEqual(r['counts']['unchanged'],1)
        self.now+=dt.timedelta(seconds=1);r=self.gate.apply('daily','three',self.read([self.record(title='Revised title')],revision='2'));self.assertEqual(r['counts']['materially_changed'],1)
        self.now+=dt.timedelta(seconds=1);r=self.gate.apply('daily','four',self.read([],revision='3'));self.assertEqual(r['counts']['closed'],1)
        with self.gate.store.connection() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM vacancy_history').fetchone()[0],3);self.assertEqual(db.execute('SELECT active FROM vacancy_current').fetchone()[0],0)
    def test_partial_failure_unavailable_never_closes_or_means_no_new(self):
        self.gate.apply('daily','one',self.read([self.record()]))
        for i,flag in enumerate(['complete','authorized','authenticated','available']):
            r=self.gate.apply('daily','blocked'+str(i),self.read([],revision='2',**{flag:False}));self.assertEqual(r['status'],'blocked');self.assertIsNone(r['counts']['new']);self.assertIsNone(self.gate.readback(r)['classification']['closed'])
        with self.gate.store.connection() as db:self.assertEqual(db.execute('SELECT revision FROM vacancy_sources').fetchone()[0],'1')
    def test_coverage_scope_and_namespace_do_not_expand(self):
        other=v.Grant('public-vacancies','synthetic-employer','synthetic-official','filtered-list-v1','https://jobs.example.test')
        self.gate.apply('daily','one',self.read([self.record()]))
        with self.assertRaises(PermissionError):self.gate.apply('weekly','no-grant',self.read([],grant=other))
        gate=v.VacancyGate(self.paths,approvals={'weekly':[other]},now=lambda:self.now)
        r=gate.apply('weekly','filtered',self.read([],grant=other));self.assertEqual(r['counts']['closed'],0)
        with self.assertRaises(PermissionError):gate.readback(self.gate.apply('daily','two',self.read([self.record()])))
    def test_public_source_authentication_requirement_is_explicit(self):
        read=self.read([],authenticated=False)
        self.assertEqual(self.gate.apply('daily','protected',read)['reason'],'unauthenticated')
        public=v.Grant('public-vacancies','synthetic-employer','synthetic-official','full-list-v1','https://jobs.example.test',requires_authentication=False)
        gate=v.VacancyGate(self.paths,approvals={'daily':[public]},now=lambda:self.now)
        receipt=gate.apply('daily','public',self.read([self.record()],grant=public,authenticated=False))
        self.assertEqual(receipt['status'],'complete');self.assertEqual(receipt['counts']['new'],1)
        self.assertNotEqual(public.key(),self.grant.key())
        with self.assertRaises(ValueError):v.Grant('p','e','s','c','https://jobs.example.test',requires_authentication='false').key()

    def test_duplicate_ids_revision_conflict_and_observation_regression(self):
        with self.assertRaises(ValueError):self.gate.apply('daily','dupe',self.read([self.record(),self.record()]))
        self.gate.apply('daily','one',self.read([self.record()]))
        self.now+=dt.timedelta(seconds=1)
        with self.assertRaises(ValueError):self.gate.apply('daily','conflict',self.read([],revision='1'))
        r=self.gate.apply('daily','older',self.read([],revision='2',observed_at=self.now-dt.timedelta(seconds=2)));self.assertEqual(r['reason'],'observation_regression_or_conflict')
    def test_stale_future_private_fields_url_and_storage_fail_closed(self):
        for offset in [-301,1]:
            r=self.gate.apply('daily',str(offset),self.read([],observed_at=self.now+dt.timedelta(seconds=offset)));self.assertEqual(r['status'],'blocked')
        with self.assertRaises(ValueError):self.gate.apply('daily','host',self.read([self.record(url='https://other.example.test/a')]))
        record=self.record();record['fields']['candidate_profile']='disallowed'
        with self.assertRaises(ValueError):self.gate.apply('daily','profile',self.read([record]))
        self.online=False
        with self.assertRaises(StorageError):self.gate.apply('daily','offline',self.read([]))
    def test_atomic_concurrency_idempotent_receipt_and_conflicting_request(self):
        read=self.read([self.record()])
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:receipts=list(pool.map(lambda _:self.gate.apply('daily','same',read),range(5)))
        self.assertTrue(all(r==receipts[0] for r in receipts));self.assertEqual(receipts[0]['counts']['new'],1)
        with self.assertRaises(ValueError):self.gate.apply('daily','same',self.read([]))
        altered=dict(receipts[0],counts={'new':9})
        with self.assertRaises(ValueError):self.gate.readback(altered)
    def test_url_canonicalization_and_persistent_state(self):
        self.assertEqual(v.official_url('https://jobs.example.test/a?z=1&a=2#top',self.grant.official_origin),'https://jobs.example.test/a?a=2&z=1')
        with self.assertRaises(ValueError):v.official_url('https:///a','https:///')
        self.gate.apply('daily','one',self.read([self.record()]));gate=v.VacancyGate(self.paths,approvals={'daily':[self.grant]},now=lambda:self.now)
        self.assertEqual(gate.apply('daily','two',self.read([self.record()]))['counts']['unchanged'],1)

if __name__=='__main__':unittest.main()

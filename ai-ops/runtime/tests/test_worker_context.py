import hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from worker_context import PROFILES,build_context

class WorkerContextTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.directory=self.root/'ai-ops/knowledge';self.directory.mkdir(parents=True)
        self.private=self.root/'private-source.md';self.private.write_text('Synthetic source. No profile or private prompt.')
        self.rows=[]
        names={n for p in PROFILES.values() for n in p['paragraphs']}
        for name in sorted(names):
            prefixes=set(x for p in PROFILES.values() for x in p['paragraphs'].get(name,[]))
            body='# '+name+'\n\n'+'\n\n'.join(x+' — synthetic reviewed paragraph.' for x in sorted(prefixes))+'\n'
            (self.directory/name).write_text(body)
            self.rows.append({'bundle':name,'privacy_class':'private_operational','provenance':'synthetic verified source','bundle_sha256':hashlib.sha256(body.encode()).hexdigest(),'sources':[{'path':str(self.private),'scope':'local_only_source','sha256':hashlib.sha256(self.private.read_bytes()).hexdigest()}]})
        self.save()
    def tearDown(self):self.tmp.cleanup()
    def save(self):(self.directory/'manifest.json').write_text(json.dumps(self.rows))
    def test_each_worker_is_whole_paragraph_bounded_and_task_specific(self):
        for worker in PROFILES:
            r=build_context(worker,directory=self.directory)
            self.assertLessEqual(r['context_words'],400);self.assertLessEqual(r['bundle_count'],2)
            self.assertEqual(r['context_sha256'],hashlib.sha256(r['context'].encode()).hexdigest())
            self.assertFalse(r['ready_for_live_append']);self.assertEqual(r['paid_calls'],0)
            self.assertNotIn(str(self.private),r['context']);self.assertIn('retain the full original task',r['context'])
            self.assertEqual(build_context(worker,directory=self.directory)['provenance_fingerprint'],r['provenance_fingerprint'])
    def test_binding_requires_exact_existing_task_and_preservation(self):
        binding={'task_id':PROFILES['news']['task_id'],'original_prompt_sha256':'a'*64,'source_prompt_preserved':True,'destination_unchanged':True}
        self.assertTrue(build_context('news',directory=self.directory,binding=binding)['ready_for_live_append'])
        for key,value in [('task_id',PROFILES['birthday']['task_id']),('source_prompt_preserved',False),('destination_unchanged',False),('original_prompt_sha256','missing')]:
            invalid=dict(binding);invalid[key]=value
            with self.assertRaises(ValueError):build_context('news',directory=self.directory,binding=invalid)
        with self.assertRaises(ValueError):build_context('finance',directory=self.directory)
    def test_saved_context_cannot_bypass_changed_or_missing_private_source(self):
        saved=build_context('birthday',directory=self.directory)
        self.private.write_text('Changed synthetic source')
        with self.assertRaises(ValueError):build_context('birthday',directory=self.directory)
        self.private.unlink()
        with self.assertRaises(ValueError):build_context('birthday',directory=self.directory)
        self.assertTrue(saved['context']) # prior output exists, but never used as a verification bypass
    def test_tampered_bundle_changed_selection_and_hard_limit_fail_closed(self):
        target=self.directory/'workflow-preferences.md';target.write_text(target.read_text()+'changed')
        with self.assertRaises(ValueError):build_context('doe-watch',directory=self.directory)
        for r in self.rows:
            if r['bundle']=='workflow-preferences.md':r['bundle_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        target.write_text(target.read_text().replace('Prefer a filesystem path','Changed policy anchor'))
        for r in self.rows:
            if r['bundle']=='workflow-preferences.md':r['bundle_sha256']=hashlib.sha256(target.read_bytes()).hexdigest()
        self.save()
        with self.assertRaises(ValueError):build_context('doe-watch',directory=self.directory)
        with self.assertRaises(ValueError):build_context('writing-on-demand',directory=self.directory,max_words=1)

if __name__=='__main__':unittest.main()

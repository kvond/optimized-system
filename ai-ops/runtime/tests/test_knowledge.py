import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
spec=importlib.util.spec_from_file_location('knowledge',Path(__file__).parents[1]/'knowledge.py');k=importlib.util.module_from_spec(spec);spec.loader.exec_module(k)

class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name).resolve();self.docs=self.root/'ai-ops/knowledge';self.docs.mkdir(parents=True);self.source=self.root/'policy.md';self.source.write_text('Reviewed synthetic source policy.');self.rows=[]
        self.add('cost-routing.md','# Cost routing\n\nDeterministic work first. Use the cheapest sufficient model and budget cap.\n\nNo paid dispatch or savings claim is authorized.\n')
        self.add('writing-voice.md','# Writing voice\n\nPreserve prose and the author voice. Never invent a quotation.\n\nUse verified writing sources for Substack style.\n')
    def tearDown(self):self.tmp.cleanup()
    def add(self,name,body):
        (self.docs/name).write_text(body);self.rows.append({'bundle':name,'privacy_class':'private_operational','provenance':'synthetic reviewed rule','bundle_sha256':hashlib.sha256(body.encode()).hexdigest(),'sources':[{'path':'policy.md','sha256':hashlib.sha256(self.source.read_bytes()).hexdigest()}]});self.save()
    def save(self):(self.docs/'manifest.json').write_text(json.dumps(self.rows))
    def test_relevant_selection_and_provenance(self):
        r=k.retrieve(self.docs,'writing voice',max_words=65,max_bundles=1)
        self.assertEqual(r['sources'][0]['bundle'],'writing-voice.md');self.assertEqual(r['sources'][0]['sources'][0]['verification'],'sha256_matched');self.assertNotIn('cost-routing.md',r['context'])
    def test_receipt_belongs_to_ranked_bundle(self):
        cost_receipt=self.docs/'cost-receipt.json';cost_receipt.write_text('{"kind":"synthetic cost"}')
        self.rows[0]['live_source_receipts']=cost_receipt.name;self.save()
        r=k.retrieve(self.docs,'writing voice cost',max_words=300,max_bundles=2)
        self.assertEqual(r['sources'][0]['bundle'],'writing-voice.md')
        by_bundle={s['bundle']:s for s in r['sources']}
        self.assertIsNone(by_bundle['writing-voice.md']['live_receipt_path'])
        self.assertIsNone(by_bundle['writing-voice.md']['live_receipt_sha256'])
        self.assertEqual(by_bundle['cost-routing.md']['live_receipt_path'],cost_receipt.name)
        self.assertEqual(by_bundle['cost-routing.md']['live_receipt_sha256'],hashlib.sha256(cost_receipt.read_bytes()).hexdigest())
        self.assertIn('LIVE-RECEIPT cost-receipt.json',r['context'])
        voice_receipt=self.docs/'voice-receipt.json';voice_receipt.write_text('{"kind":"synthetic voice"}')
        self.rows[1]['live_source_receipts']=voice_receipt.name;self.save()
        r=k.retrieve(self.docs,'writing voice cost',max_words=300,max_bundles=2)
        by_bundle={s['bundle']:s for s in r['sources']}
        self.assertEqual(by_bundle['cost-routing.md']['live_receipt_path'],cost_receipt.name)
        self.assertEqual(by_bundle['writing-voice.md']['live_receipt_path'],voice_receipt.name)
        self.assertEqual(by_bundle['writing-voice.md']['live_receipt_sha256'],hashlib.sha256(voice_receipt.read_bytes()).hexdigest())
    def test_hard_word_cap_whole_paragraphs_and_cli(self):
        r=k.retrieve(self.docs,'cost',max_words=48,max_bundles=2)
        self.assertLessEqual(len(r['context'].split()),48)
        self.assertTrue(r['context'].endswith('.'))
        p=subprocess.run([sys.executable,str(Path(k.__file__)), 'cost','--directory',str(self.docs),'--max-words','48'],capture_output=True,text=True)
        self.assertEqual(p.returncode,0,p.stderr);self.assertLessEqual(len(p.stdout.split()),48)
        with self.assertRaises(ValueError):k.retrieve(self.docs,'cost',max_words=1)
    def test_tampered_bundle_and_source_fail_closed(self):
        p=self.docs/'writing-voice.md';p.write_text(p.read_text()+'Altered.\n')
        with self.assertRaises(ValueError):k.retrieve(self.docs,'voice')
        p.write_text('# Writing voice\n\nPreserve prose and the author voice. Never invent a quotation.\n\nUse verified writing sources for Substack style.\n');self.source.write_text('changed source')
        with self.assertRaises(ValueError):k.retrieve(self.docs,'cost')
    def test_explicit_historical_source_requires_exact_bytes(self):
        original=self.root/'original';original.mkdir();(original/'policy.md').write_bytes(self.source.read_bytes())
        self.source.write_text('different current source')
        with self.assertRaises(ValueError):k.retrieve(self.docs,'cost')
        r=k.retrieve(self.docs,'cost',source_root=original)
        self.assertEqual(r['sources'][0]['sources'][0]['verified_path'],str(original/'policy.md'))
        (original/'policy.md').write_text('also wrong')
        with self.assertRaises(ValueError):k.retrieve(self.docs,'cost',source_root=original)

    def test_private_eligibility_secret_and_escape_rejected(self):
        self.rows[0]['privacy_class']='raw_chat';self.save()
        with self.assertRaises(PermissionError):k.retrieve(self.docs,'cost')
        self.rows[0]['privacy_class']='private_operational';self.rows[0]['bundle']='../private.md';self.save()
        with self.assertRaises(ValueError):k.retrieve(self.docs,'cost')
        self.rows[0]['bundle']='cost-routing.md';body='sk-'+'x'*25;(self.docs/'cost-routing.md').write_text(body);self.rows[0]['bundle_sha256']=hashlib.sha256(body.encode()).hexdigest();self.save()
        with self.assertRaises(PermissionError):k.retrieve(self.docs,'cost')
    def test_missing_local_source_and_symlink_rejected(self):
        self.source.unlink()
        with self.assertRaises(ValueError):k.retrieve(self.docs,'cost')
        self.source.symlink_to(self.root/'missing.md')
        with self.assertRaises(ValueError):k.retrieve(self.docs,'cost')

if __name__=='__main__':unittest.main()

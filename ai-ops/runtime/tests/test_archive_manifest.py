import importlib.util
import json
import os
import stat
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('archive_manifest', Path(__file__).parents[1] / 'archive_manifest.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve(); self.source = self.root / 'source'; self.source.mkdir()
        (self.source / 'a').write_bytes(b'private content')
    def test_deterministic_bounded_inventory(self):
        a = m.inventory(self.source)
        self.assertEqual(m.manifest_json(a), m.manifest_json(m.inventory(self.source)))
        self.assertNotIn('private content', m.manifest_json(a))
        self.assertIsNone(a['platform']); self.assertEqual(a['privacy']['contains_secrets'], 'unknown')
        with self.assertRaises(ValueError): m.inventory(self.source, max_bytes=1)
        (self.source / 'b').write_bytes(b'b')
        with self.assertRaises(ValueError): m.inventory(self.source, max_files=1)
    def test_copy_never_overwrites(self):
        dest = self.root / 'copy'; r = m.verified_copy(self.source / 'a', dest)
        self.assertEqual(r['status'], 'verified')
        with self.assertRaises(FileExistsError): m.verified_copy(self.source / 'a', dest)
        self.assertEqual(dest.read_bytes(), b'private content')
    def test_symlink_rejected(self):
        (self.source / 'link').symlink_to(self.source / 'a')
        with self.assertRaises(ValueError): m.inventory(self.source)
        with self.assertRaises(ValueError): m.verified_copy(self.source / 'link', self.root / 'copy')
    def test_mutation_cleans_partial_copy(self):
        original = m._identity; calls = [0]
        def changed(p):
            value = original(p)
            if p == self.source / 'a':
                calls[0] += 1
                if calls[0] > 1: return value[:-1] + (value[-1]+1,)
            return value
        with patch.object(m, '_identity', changed):
            with self.assertRaises(ValueError): m.verified_copy(self.source / 'a', self.root / 'copy')
        self.assertFalse((self.root / 'copy').exists())
    def test_private_copy_under_public_umask(self):
        prior = os.umask(0o022)
        try:
            dest = self.root / 'private-copy'
            receipt = m.verified_copy(self.source / 'a', dest)
        finally:
            os.umask(prior)
        self.assertEqual(stat.S_IMODE(dest.stat().st_mode), 0o600)
        self.assertEqual(receipt['permission_mode'], '0600')
        self.assertEqual(receipt['encryption'], 'unknown')
    def test_fixture_replacement_between_identity_and_open(self):
        p = self.root / 'conversations.json'
        p.write_text(json.dumps([{'mapping': {}}]))
        original = Path.open
        replaced = [False]
        def swap(path, *args, **kwargs):
            if path == p and args and args[0] == 'rb' and not replaced[0]:
                replaced[0] = True
                replacement = self.root / 'replacement'
                replacement.write_text(json.dumps([{'mapping': {'new': {}}}]))
                os.replace(replacement, p)
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', swap):
            with self.assertRaisesRegex(ValueError, 'replaced'):
                m.inspect_export_fixture(p, platform='chatgpt')
    def test_explicit_export_fixture_structure(self):
        p = self.root / 'conversations.json'
        for platform, data in [('chatgpt',[{'mapping': {'x': {'message':'secret'}}}]), ('claude',[{'chat_messages':[{'text':'secret'}]}])]:
            p.write_text(json.dumps(data)); r = m.inspect_export_fixture(p, platform=platform)
            self.assertEqual(r['conversation_count'], 1); self.assertNotIn('secret', m.manifest_json(r))
            self.assertIsNone(r['account']); self.assertIsNone(r['date_range'])
        with self.assertRaises(ValueError): m.inspect_export_fixture(p, platform='chatgpt')

if __name__ == '__main__': unittest.main()

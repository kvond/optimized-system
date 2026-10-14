"""Fresh-process catalog validation and synthetic photo acceptance boundaries.

These tests never open real selections, accounts, native documents or photos.
"""
import csv
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[3]
DEFINITIONS = ROOT / 'ai-ops/workflow-contracts/definitions'
PHOTO = ROOT / 'skills/photo-album-reconcile/scripts/reconcile_picks.py'
VALIDATOR = ROOT / 'ai-ops/runtime/workflow_contract.py'


class NonSchoolCatalogTests(unittest.TestCase):
    def test_catalog_loads_in_fresh_process_without_private_bindings(self):
        files = sorted(p for p in DEFINITIONS.glob('*.json')
                       if p.name.startswith(('book-', 'photo-', 'higher-ed-', 'personal-', 'ai-ops-')))
        self.assertEqual(len(files), 13)
        ids = []
        for path in files:
            with self.subTest(path=path.name):
                result = subprocess.run([sys.executable, str(VALIDATOR), str(path)],
                                        cwd=ROOT, capture_output=True, text=True, timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                ids.append(json.loads(path.read_text())['workflow_id'])
        self.assertEqual(len(ids), len(set(ids)))


class PhotoReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.kids = self.root / 'selections'
        self.kids.mkdir()
        self.pick = self.kids / 'synthetic-album.txt'
        self.db = self.root / 'manifest.db'
        with sqlite3.connect(self.db) as con:
            con.execute('CREATE TABLE photos(path TEXT, is_dup INTEGER, event_id INTEGER, taken TEXT)')
        self.report = self.root / 'report.csv'
        self.resolved = self.root / 'resolved.csv'

    def photo(self, relative, duplicate=0, present=True):
        path = self.root / relative
        if present:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'synthetic file; no real image')
        with sqlite3.connect(self.db) as con:
            con.execute('INSERT INTO photos VALUES(?,?,?,?)', (str(path), duplicate, 1, '2026-01-02'))
        return path

    def run_cli(self, **overrides):
        args = dict(db=self.db, kids_dir=self.kids, report=self.report, resolved=self.resolved)
        args.update(overrides)
        command = [sys.executable, str(PHOTO)]
        for key, value in args.items():
            command.extend(['--' + key.replace('_', '-'), str(value)])
        return subprocess.run(command, cwd=self.root, capture_output=True, text=True, timeout=10)

    def rows(self):
        with self.report.open() as handle:
            return list(csv.DictReader(handle))

    def fingerprint(self, paths):
        return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

    def test_exact_match_readback_and_replay_preserve_sources(self):
        photo = self.photo('library/unique.jpg')
        self.pick.write_text('unique.jpg\n')
        before = self.fingerprint([photo, self.db, self.pick])
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows()[0]['t7_path'], str(photo))
        self.assertEqual(self.rows()[0]['status'], 'resolved')
        first = self.fingerprint([self.report, self.resolved])
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertEqual(first, self.fingerprint([self.report, self.resolved]))
        self.assertEqual(before, self.fingerprint([photo, self.db, self.pick]))

    def test_duplicate_basename_is_hold_even_when_hash_flag_prefers_one(self):
        self.photo('library-a/same.jpg')
        self.photo('library-b/same.jpg', duplicate=1)
        self.pick.write_text('same.jpg\n')
        result = self.run_cli()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(self.rows()[0]['status'], 'ambiguous')
        self.assertIn('STOP', result.stdout)

    def test_exact_absolute_path_disambiguates_basename(self):
        chosen = self.photo('library-a/same.jpg')
        self.photo('library-b/same.jpg')
        self.pick.write_text(str(chosen) + '\n')
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertEqual(self.rows()[0]['t7_path'], str(chosen))

    def test_missing_exact_path_never_falls_back_to_existing_basename(self):
        self.photo('library-a/same.jpg')
        self.pick.write_text(str(self.root / 'other/same.jpg') + '\n')
        self.assertEqual(self.run_cli().returncode, 1)
        self.assertEqual(self.rows()[0]['status'], 'missing')

    def test_stale_catalog_missing_file_is_hold(self):
        self.photo('removed/old.jpg', present=False)
        self.pick.write_text('old.jpg\n')
        self.assertEqual(self.run_cli().returncode, 1)
        self.assertEqual(self.rows()[0]['status'], 'missing')

    def test_unreadable_docx_preserves_prior_reports_and_sources(self):
        photo = self.photo('library/unique.jpg')
        self.pick.write_text('unique.jpg\n')
        damaged = self.kids / 'damaged.docx'
        damaged.write_bytes(b'not a zip')
        self.report.write_text('prior report')
        self.resolved.write_text('prior resolved')
        before = self.fingerprint([photo, self.db, self.pick, damaged, self.report, self.resolved])
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertEqual(before, self.fingerprint([photo, self.db, self.pick, damaged, self.report, self.resolved]))

    def test_docx_runs_are_joined_without_corrupting_filename(self):
        photo = self.photo('library/unique.jpg')
        self.pick.unlink(missing_ok=True)
        with zipfile.ZipFile(self.kids / 'synthetic.docx', 'w') as archive:
            archive.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>unique</w:t></w:r><w:r><w:t>.jpg</w:t></w:r></w:p></w:body></w:document>')
        self.assertEqual(self.run_cli().returncode, 0)
        self.assertEqual(self.rows()[0]['t7_path'], str(photo))

    def test_empty_or_unrecognized_selection_cannot_establish_all_clear(self):
        self.pick.write_text('Pending selection, no filenames yet.')
        self.assertEqual(self.run_cli().returncode, 2)
        self.assertFalse(self.report.exists())

    def test_missing_database_is_not_created(self):
        self.pick.write_text('unique.jpg\n')
        missing = self.root / 'absent.db'
        self.assertEqual(self.run_cli(db=missing).returncode, 2)
        self.assertFalse(missing.exists())

    def test_report_cannot_overwrite_database_selection_or_photo(self):
        photo = self.photo('library/unique.jpg')
        self.pick.write_text('unique.jpg\n')
        before = self.fingerprint([photo, self.db, self.pick])
        for target in (photo, self.db, self.pick):
            with self.subTest(target=target.name):
                self.assertEqual(self.run_cli(report=target).returncode, 2)
                self.assertEqual(before, self.fingerprint([photo, self.db, self.pick]))
        alias = self.root / 'hardlink.csv'
        os.link(photo, alias)
        self.assertEqual(self.run_cli(report=alias).returncode, 2)
        self.assertEqual(before, self.fingerprint([photo, self.db, self.pick]))


if __name__ == '__main__':
    unittest.main()

"""Fresh-process catalog validation and synthetic photo acceptance boundaries.

These tests never open real selections, accounts, native documents or photos.
"""
import csv
import copy
import datetime as dt
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
sys.path.insert(0, str(ROOT / 'ai-ops/runtime'))
from workflow_router import route_workflow


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


class NativePolicyAdmissionTests(unittest.TestCase):
    """Actual contracts, synthetic receipts: recovered policy is not execution proof."""
    now = dt.datetime(2026, 10, 15, 1, 0, tzinfo=dt.timezone.utc)

    def fixture(self, workflow_id):
        workflow = json.loads((DEFINITIONS / (workflow_id + '.json')).read_text())
        stamp = {'observed_at': self.now.isoformat(),
                 'expires_at': (self.now + dt.timedelta(seconds=120)).isoformat(),
                 'evidence_ref': 'synthetic:policy-admission-only'}
        operation = workflow['policy']['allowed_actions'][-1]
        request = {'schema_version': 1, 'request_id': 'synthetic-native-policy-test',
                   'workflow_id': workflow_id, 'domain': workflow['domain'],
                   'operation': operation, 'execution_kind': 'assisted',
                   'authorization': dict(stamp, state='authorized', allowed_actions=[operation]),
                   'ownership': dict(stamp, state='clear', owner_ref=workflow['owners']['execution_owner_ref']),
                   'receipt': dict(stamp, state='clear'),
                   'sources': [dict(source_ref=s['source_ref'], expected_revision='synthetic-v1',
                                    revision='synthetic-v1', coverage=s['coverage'],
                                    observed_at=self.now.isoformat(), evidence_ref='synthetic:source')
                               for s in workflow['sources']],
                   'dependencies': [dict(stamp, check=c, state='passed')
                                    for c in workflow['policy']['dependency_checks']]}
        execution = workflow['execution']
        evidence = {'schema_version': 1, 'routes': [dict(stamp,
                    route_ref='synthetic-private-reader', provider_ref='synthetic-no-provider',
                    executor_ref=execution['executor_ref'], resolved_executor_ref='synthetic-local',
                    account_refs=execution['account_refs'], domain=workflow['domain'],
                    privacy_partition=execution['privacy_partition'], operation=operation,
                    execution_kind='assisted', capabilities=execution['required_capabilities'],
                    resource_rank=0, estimated_cost='0', cost_basis_ref='synthetic:no-dispatch',
                    status='tested', identity_verified=True)]}
        return workflow, request, evidence

    def route(self, data):
        result = route_workflow(*data, now=self.now)
        self.assertFalse(result['execution_attempted'])
        return result

    def test_recovered_finance_policy_still_requires_budget_and_complete_ledger(self):
        baseline = self.fixture('personal-finance-brief')
        self.assertEqual(self.route(baseline)['status'], 'ready')
        for ref in ('private:finance-stored-budget', 'private:finance-month-to-date-ledger'):
            for condition in ('missing', 'partial'):
                with self.subTest(source=ref, condition=condition):
                    data = copy.deepcopy(baseline)
                    if condition == 'missing':
                        data[1]['sources'] = [s for s in data[1]['sources'] if s['source_ref'] != ref]
                    else:
                        next(s for s in data[1]['sources'] if s['source_ref'] == ref)['coverage'] = 'partial'
                    result = self.route(data)
                    self.assertEqual(result['reason'], 'source_unavailable_or_partial')
                    self.assertEqual(result['source_ref'], ref)

    def test_finance_classification_and_executor_are_independent_gates(self):
        data = self.fixture('personal-finance-brief')
        check = next(c for c in data[1]['dependencies'] if c['check'].startswith('Classify transfers'))
        check['state'] = 'unknown'
        self.assertEqual(self.route(data)['reason'], 'dependency_unverified')
        check['state'] = 'passed'
        data[2]['routes'][0]['status'] = 'unverified'
        self.assertEqual(self.route(data)['reason'], 'capability_unverified')

    def test_doe_component_cannot_replace_district_coverage_or_reported_history(self):
        baseline = self.fixture('personal-delaware-education-job-watch')
        self.assertEqual(self.route(baseline)['status'], 'ready')
        for ref in ('private:district-and-charter-current-source-evidence',
                    'private:task-specific-reported-vacancy-history'):
            data = copy.deepcopy(baseline)
            data[1]['sources'] = [s for s in data[1]['sources'] if s['source_ref'] != ref]
            result = self.route(data)
            self.assertEqual(result['reason'], 'source_unavailable_or_partial')
            self.assertEqual(result['source_ref'], ref)

    def test_morning_brief_unknown_class_boundary_or_iep_coverage_cannot_pass(self):
        baseline = self.fixture('personal-morning-school-brief')
        self.assertEqual(self.route(baseline)['status'], 'ready')
        for prefix in ('Identify actual classes', 'Explicitly resolve whether IEP'):
            data = copy.deepcopy(baseline)
            check = next(c for c in data[1]['dependencies'] if c['check'].startswith(prefix))
            check['state'] = 'unknown'
            self.assertEqual(self.route(data)['reason'], 'dependency_unverified')

    def test_review_policy_never_grants_gift_writes_or_news_finance_access(self):
        for workflow_id, operation in (
                ('personal-birthday-gift-review', 'update-todoist-gift-choice'),
                ('personal-news-briefing', 'change-carts'),
                ('personal-news-briefing', 'read-authorized-finance-sources')):
            with self.subTest(workflow=workflow_id, operation=operation):
                data = self.fixture(workflow_id)
                self.assertEqual(self.route(data)['status'], 'ready')
                data[1]['operation'] = operation
                data[1]['authorization']['allowed_actions'] = [operation]
                data[2]['routes'][0]['operation'] = operation
                self.assertEqual(self.route(data)['reason'], 'operation_not_allowed')


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

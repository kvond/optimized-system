"""Offline evidence-check tests; these never imply a live destination trial."""
import copy
import datetime as dt
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME))
from school_read_trial import compare_reads, save_summary, TrialError, REPOSITORY


class SchoolReadTrialTest(unittest.TestCase):
    def setUp(self):
        self.workflow = json.loads((RUNTIME.parent / 'workflow-contracts' / 'definitions' /
                                    'school-morning-report-resolution.json').read_text())
        self.source = 'private:existing-hub-tasks-checklist'
        self.now = dt.datetime(2026, 10, 14, 20, 0, tzinfo=dt.timezone.utc)
        self.binding = {'source_id': 'synthetic-file', 'link_id': 'synthetic-link',
                        'range': "'Task tab'!A1:D3"}
        self.before = {
            'tool': 'google_drive.get_spreadsheet_range',
            'request': {'spreadsheet_id': 'synthetic-file', 'link_id': 'synthetic-link',
                        'sheet_name': "'Task tab'", 'range': 'A1:D3'},
            'source_metadata': {'id': 'synthetic-file', 'mime_type': 'application/vnd.google-apps.spreadsheet'},
            'response': {'isError': False, 'structuredContent': {
                'range': "'Task tab'!A1:D3", 'majorDimension': 'ROWS',
                'values': [['Private sentinel'], ['Policy is not run proof'], ['Done', '#', 'Work', 'Evidence']]}},
            'observed_at': '2026-10-14T19:59:00Z',
        }
        self.after = copy.deepcopy(self.before)
        self.after['observed_at'] = '2026-10-14T19:59:30Z'

    def compare(self):
        return compare_reads(self.workflow, self.source, self.binding, self.before,
                             self.after, now=self.now)

    def test_matching_reads_never_promote_scope_or_disclose_source(self):
        result = self.compare()
        self.assertEqual(result['status'], 'matched')
        self.assertEqual(result['coverage'], 'bounded')
        for key in ('workflow_completed', 'destination_executor_tested',
                    'report_date_verified', 'account_identity_independently_verified'):
            self.assertIs(result[key], False)
        serialized = json.dumps(result)
        for private in ('Private sentinel', 'synthetic-file', 'synthetic-link', 'Task tab'):
            self.assertNotIn(private, serialized)

    def test_changed_content_holds_and_preserves_inputs(self):
        self.after['response']['structuredContent']['values'][0][0] = 'Changed sentinel'
        frozen = copy.deepcopy((self.before, self.after))
        result = self.compare()
        self.assertEqual(result['status'], 'held')
        self.assertIn('bounded_content_changed', result['problems'])
        self.assertEqual((self.before, self.after), frozen)

    def test_wrong_account_source_or_range_cannot_pass(self):
        changes = (
            ('request', 'link_id', 'other', 'account_link_mismatch'),
            ('request', 'spreadsheet_id', 'other', 'source_identity_mismatch'),
            ('source_metadata', 'id', 'other', 'source_identity_mismatch'),
            ('source_metadata', 'mime_type', 'other', 'source_identity_mismatch'),
            ('request', 'sheet_name', "'Other'", 'range_mismatch'),
        )
        for container, field, value, problem in changes:
            with self.subTest(field=field):
                original = self.after[container][field]
                self.after[container][field] = value
                self.assertIn(problem, self.compare()['problems'])
                self.after[container][field] = original

    def test_provider_error_and_empty_read_are_holds_not_missing_work(self):
        self.after['response']['isError'] = True
        self.after['response']['structuredContent']['values'] = []
        result = self.compare()
        self.assertEqual(result['status'], 'held')
        self.assertIn('provider_error', result['problems'])
        self.assertIn('empty_or_incomplete_read', result['problems'])
        self.after['response']['structuredContent']['values'] = [['', None]]
        self.assertIn('empty_or_incomplete_read', self.compare()['problems'])

    def test_stale_future_and_reverse_observations_hold(self):
        for stamp in ('2026-10-14T19:54:00Z', '2026-10-14T20:00:01Z'):
            self.after['observed_at'] = stamp
            self.assertIn('read_observation_stale_or_future', self.compare()['problems'])
        self.after['observed_at'] = '2026-10-14T19:58:30Z'
        self.assertIn('read_order_invalid', self.compare()['problems'])

    def test_oversized_request_is_held_even_when_response_is_small(self):
        for rectangle in ('A1:Z100', 'A:Z', 'D3:A1', 'A1:A51'):
            self.after['request']['range'] = rectangle
            self.assertIn('read_scope_exceeds_trial_bound', self.compare()['problems'])

    def test_unknown_source_or_non_school_contract_is_invalid(self):
        self.source = 'private:unknown-source'
        with self.assertRaises(TrialError):
            self.compare()
        self.source = 'private:existing-hub-tasks-checklist'
        self.workflow['domain'] = 'book'
        with self.assertRaises(TrialError):
            self.compare()

    def test_private_output_is_read_back_and_existing_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'evidence.json'
            digest = save_summary(self.compare(), path)
            self.assertEqual(len(digest), 64)
            self.assertEqual(os.stat(path).st_mode & 0o777, 0o600)
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                save_summary({'overwrite': True}, path)
            self.assertEqual(path.read_bytes(), original)

    def test_git_destination_and_symlink_are_rejected(self):
        with self.assertRaises(TrialError):
            save_summary(self.compare(), REPOSITORY / 'private-trial.json')
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'target'
            target.write_text('preserve')
            link = Path(directory) / 'link'
            link.symlink_to(target)
            with self.assertRaises(TrialError):
                save_summary(self.compare(), link)
            self.assertEqual(target.read_text(), 'preserve')


if __name__ == '__main__':
    unittest.main()

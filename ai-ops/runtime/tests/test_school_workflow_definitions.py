"""Requirement-regression checks, not school execution or capability tests."""
import json
from pathlib import Path
import re
import sys
import unittest

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME))
from workflow_contract import validate_workflow

CATALOG = RUNTIME.parent / 'workflow-contracts'
DEFINITIONS = CATALOG / 'definitions'
EXPECTED = {
    'school-morning-preparation-and-repair',
    'school-ic-higher-only-entry',
    'school-feedback-print-ready',
    'school-morning-report-resolution',
    'school-lesson-readiness',
    'school-assignment-setup',
    'school-friday-missed-lesson-notices',
}


class SchoolWorkflowDefinitionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contracts = {
            p.stem: json.loads(p.read_text(encoding='utf-8'))
            for p in DEFINITIONS.glob('school-*.json')
        }
        cls.runbook = (CATALOG / 'school-operations-runbook.md').read_text(encoding='utf-8')

    def test_complete_catalog_validates_and_has_exact_distinct_ids(self):
        self.assertEqual(set(self.contracts), EXPECTED)
        for name, contract in self.contracts.items():
            with self.subTest(workflow=name):
                checked = validate_workflow(contract)
                self.assertEqual(checked['workflow_id'], name)
                self.assertIsNot(checked, contract)
                self.assertIn('## ' + name, self.runbook)

    def test_only_existing_helper_can_enter_grades(self):
        write_actions = {'helper-enter-eligible-blank', 'helper-raise-lower-score',
                         'helper-save-reload-readback'}
        capable = []
        for name, contract in self.contracts.items():
            allowed = set(contract['policy']['allowed_actions'])
            if allowed & write_actions:
                capable.append(name)
                self.assertEqual(contract['execution']['executor_ref'], 'school-chrome-helper')
                self.assertTrue(write_actions <= allowed)
            else:
                self.assertIn('write-ic-grades', contract['policy']['prohibited_actions'])
        self.assertEqual(capable, ['school-ic-higher-only-entry'])
        helper = self.contracts[capable[0]]
        self.assertTrue({'lower-ic-score', 'change-exempt-flags-or-comments',
                         'retry-uncertain-grade-save', 'clear-helper-recovery-block',
                         'grade-from-provisional-filing-name',
                         'set-or-clear-missing-late-flags'} <= set(helper['policy']['prohibited_actions']))

    def test_all_workflows_preserve_provider_failures_and_uncertainty(self):
        for name, contract in self.contracts.items():
            with self.subTest(workflow=name):
                self.assertTrue({'infer-absence-from-provider-failure',
                                 'retry-uncertain-write',
                                 'clear-uncertainty-automatically'} <= set(contract['policy']['prohibited_actions']))
                self.assertEqual(contract['policy']['uncertain_write_policy'], 'stop_and_reconcile')
                self.assertLessEqual(contract['failure']['max_safe_read_retries'], 2)
                self.assertTrue(contract['failure']['continue_independent_work'])
                self.assertTrue(contract['failure']['report_next_step'])

    def test_all_workflows_preserve_teacher_marks_history_and_privacy(self):
        for name, contract in self.contracts.items():
            with self.subTest(workflow=name):
                self.assertTrue({'change-teacher-delivery-marks', 'copy-credentials-or-profiles',
                                 'broaden-sharing', 'delete-or-restore-source-history',
                                 'invent-identity-or-lesson-match'} <= set(contract['policy']['prohibited_actions']))
                self.assertEqual(contract['execution']['privacy_partition'], 'school-private')
                self.assertTrue(all(x['verification'] == 'content_and_destination_readback'
                                    for x in contract['outputs']))

    def test_morning_writers_and_cutoff_are_not_conflated(self):
        for name in ('school-morning-preparation-and-repair', 'school-morning-report-resolution'):
            contract = self.contracts[name]
            self.assertIn('mutate-source-after-cutoff', contract['policy']['prohibited_actions'])
            checks = ' '.join(contract['policy']['dependency_checks'])
            self.assertIn('07:00', checks)
            self.assertIn('source', checks.lower())
        prep = self.contracts['school-morning-preparation-and-repair']
        self.assertTrue({'generate-feedback', 'send-feedback-email'} <= set(prep['policy']['prohibited_actions']))
        followup = self.contracts['school-morning-report-resolution']
        self.assertTrue({'launch-competing-feedback-job', 'clear-helper-recovery-block',
                         'disable-weekday-helper-entry',
                         'certify-all-assignments-from-one-panel'} <= set(followup['policy']['prohibited_actions']))

    def test_exact_known_morning_registry_keys_preserved(self):
        expected = {
            'school-morning-preparation-and-repair': 'Local Codex::morning-roster-check-and-submission-tidy',
            'school-ic-higher-only-entry': 'School Chrome helper::kkficpedebnobolfpkpkpfagelofbmde',
            'school-feedback-print-ready': 'Local Codex::morning-student-feedback-and-print-checklist',
            'school-morning-report-resolution': 'Local Codex::resolve-morning-hub-report',
        }
        for name, key in expected.items():
            self.assertEqual(self.contracts[name]['trigger'], {'kind': 'existing_schedule', 'schedule_ref': key})
        for name in ('school-lesson-readiness', 'school-assignment-setup'):
            self.assertEqual(self.contracts[name]['trigger'], {'kind': 'on_demand'})

    def test_feedback_delivery_keeps_send_fence_and_current_override(self):
        c = self.contracts['school-feedback-print-ready']
        self.assertTrue({'retry-uncertain-email-send', 'retroactively-email-historical-baseline',
                         'retry-uncertain-model-call', 'physically-print',
                         'regenerate-unchanged-feedback', 'send-student-or-guardian-message'} <= set(c['policy']['prohibited_actions']))
        self.assertIn('send-teacher-only-outbox-batch-once', c['policy']['allowed_actions'])
        checks = ' '.join(c['policy']['dependency_checks'])
        for needed in ('send_allowed_once', 'expiry', 'SENT/raw MIME', 'claim token',
                       'ten newly eligible batches', 'Printed/Handed',
                       'override the older mandatory Hub Print direction'):
            self.assertIn(needed, checks)
        self.assertIn('private:school-only-email-mime-receipt', {x['output_ref'] for x in c['outputs']})
        for name, other in self.contracts.items():
            if name != c['workflow_id']:
                self.assertNotIn('send-teacher-only-outbox-batch-once', other['policy']['allowed_actions'])

    def test_questions_resume_without_whole_scope_certification(self):
        c = self.contracts['school-morning-report-resolution']
        self.assertTrue({'record-numbered-decision-question', 'resume-answered-issue',
                         'prepare-next-safe-window-repair'} <= set(c['policy']['allowed_actions']))
        checks = ' '.join(c['policy']['dependency_checks'])
        for needed in ('at most three numbered questions', 'resume without asking for another continue',
                       'continue independent work'):
            self.assertIn(needed, checks)
        self.assertIn('No reply is not approval.', self.runbook)
        self.assertIn('No questions for you', self.runbook)

    def test_friday_history_cannot_become_new_authority_or_current_capability(self):
        c = self.contracts['school-friday-missed-lesson-notices']
        self.assertEqual(c['trigger']['schedule_ref'], 'School Claude::trig_018b7U6kN8YegmEHuTsj8rQ9')
        self.assertTrue({'send-without-current-explicit-authority', 'send-duplicate-weekly-notice',
                         'guess-guardian-recipient', 'claim-guardian-read-from-saved-note'} <= set(c['policy']['prohibited_actions']))
        checks = ' '.join(c['policy']['dependency_checks'])
        self.assertIn('historical friday', checks.lower())
        self.assertIn('capability is untested', checks)
        self.assertIn('never grant new recurring send authority', checks)
        self.assertIn('at most three', checks)
        self.assertIn('private:current-friday-task-authority-and-owner', {x['source_ref'] for x in c['sources']})

    def test_missing_work_zero_and_window_require_authoritative_policy(self):
        for name in ('school-ic-higher-only-entry', 'school-feedback-print-ready',
                     'school-morning-report-resolution'):
            c = self.contracts[name]
            policy = [x for x in c['sources'] if x['source_ref'] ==
                      'private:current-deterministic-missing-work-and-eligibility-policy']
            self.assertEqual(len(policy), 1)
            self.assertTrue(policy[0]['required'])
            self.assertEqual(policy[0]['coverage'], 'complete')
            checks = ' '.join(c['policy']['dependency_checks'])
            for required in ('eligible automatic zeros', 'two-week submission-window',
                             'complete-coverage', 'original-event',
                             'Photosynthesis empty intake still waits'):
                self.assertIn(required, checks)
            self.assertIn('infer-absence-from-provider-failure', c['policy']['prohibited_actions'])

    def test_setup_and_lesson_acceptance_require_native_factors(self):
        setup = self.contracts['school-assignment-setup']
        self.assertTrue({'submit-fake-student-work', 'publish-private-response-links',
                         'create-recurring-setup-job'} <= set(setup['policy']['prohibited_actions']))
        self.assertIn('Form-only repair cannot pass', ' '.join(setup['policy']['dependency_checks']))
        lesson = self.contracts['school-lesson-readiness']
        self.assertIn('treat-code-count-as-visual-completion', lesson['policy']['prohibited_actions'])
        self.assertIn('independent lesson implementation', ' '.join(lesson['policy']['dependency_checks']))
        self.assertIn('image-only', ' '.join(lesson['policy']['dependency_checks']))

    def test_new_catalog_contains_references_not_private_resolved_values(self):
        # Not a universal DLP guarantee: catches accidental raw exports/locators in these files.
        texts = [self.runbook]
        for c in self.contracts.values():
            texts.append(json.dumps(c))
            self.assertTrue(all(s['source_ref'].startswith('private:') for s in c['sources']))
            self.assertTrue(all(o['output_ref'].startswith('private:') for o in c['outputs']))
            self.assertNotIn('enabled', c)
            self.assertNotIn('completed', c)
            self.assertNotIn('approved', c)
        combined = '\n'.join(texts)
        self.assertIsNone(re.search(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', combined))
        for forbidden in ('/Users/', 'docs.google.com/', 'drive.google.com/', 'run.app/',
                          'client_secret', 'access_token', 'refresh_token', '-----BEGIN PRIVATE KEY'):
            self.assertNotIn(forbidden, combined)


if __name__ == '__main__':
    unittest.main()

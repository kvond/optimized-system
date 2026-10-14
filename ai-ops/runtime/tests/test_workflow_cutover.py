import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from workflow_cutover import (CutoverError, digest, invocation, json_digest,
                              pin_file, transition, verify_bundle,
                              verify_coverage, verify_prompt_only_change)


class InvocationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        source = Path(__file__).resolve().parents[2] / 'workflow-contracts/definitions/personal-calendar-school-email-review.json'
        definition = json.loads(source.read_text())
        self.workflow = definition['workflow_id']
        self.schedule = definition['trigger']['schedule_ref']
        (self.root / 'contract.json').write_text(json.dumps(definition))
        (self.root / 'runbook.md').write_text('# Procedure\nComplete native readback.')
        self.prompt = 'Read exact sources.\n\nRetain delivery history.'
        (self.root / 'policy.txt').write_text(self.prompt)
        (self.root / 'backup.toml').write_bytes(b'original definition')
        (self.root / 'native.toml').write_bytes(b'original definition')
        (self.root / 'bindings.json').write_text('{}')
        self.coverage = [dict(paragraph=i, source_sha256=digest(p.encode()), disposition='covered',
                              targets=['runbook.md#Procedure'], review_note='Synthetic reviewed rule')
                         for i, p in enumerate(self.prompt.split('\n\n'), 1)]
        owner = {'account_or_local_owner': 'synthetic-owner'}
        record = {'schedule_ref': self.schedule, 'workflow_id': self.workflow, 'system': 'Local Codex',
                  'enabled_state': {'native_status': 'ACTIVE'}, 'owner': owner,
                  'source_contract_ref': {'path': str(self.root/'native.toml'),
                                          'definition_sha256': digest(b'original definition')}}
        self.registry = {'records': [record]}
        (self.root/'registry.json').write_text(json.dumps(self.registry))
        self.candidate = {'schema_version': 1, 'operation': 'same-owner-prompt-conversion',
                          'workflow_id': self.workflow, 'contract_version': definition['contract_version'],
                          'schedule_ref': self.schedule, 'contract': pin_file(self.root, 'contract.json'),
                          'procedures': [pin_file(self.root, 'runbook.md')],
                          'registry_path': str(self.root/'registry.json'), 'owner_sha256': json_digest(owner),
                          'canonical_checkout': str(self.root), 'coverage': self.coverage,
                          'policy_backup_path': str(self.root/'policy.txt'),
                          'original': {'path': str(self.root/'native.toml'),
                                       'backup_path': str(self.root/'backup.toml'),
                                       'sha256': digest(b'original definition'),
                                       'prompt_sha256': digest(self.prompt.encode())},
                          'bindings': {'path': str(self.root/'bindings.json'), 'sha256': digest(b'{}')}}

    def verify(self, candidate=None, workflow=None, expected_hash=None):
        return verify_bundle(candidate or self.candidate, self.root, workflow or self.workflow,
                             expected_hash or self.candidate['contract']['sha256'])

    def test_valid_artifacts_do_not_grant_execution(self):
        result = self.verify()
        self.assertTrue(result['validation_only'])
        self.assertFalse(result['execution_authorized'])

    def test_invocation_is_deterministic_and_bound_to_hash(self):
        a = invocation(self.candidate, self.root/'candidate.json')
        self.assertEqual(a, invocation(copy.deepcopy(self.candidate), self.root/'candidate.json'))
        changed = copy.deepcopy(self.candidate)
        changed['contract']['sha256'] = 'a'*64
        self.assertNotEqual(a, invocation(changed, self.root/'candidate.json'))
        with self.assertRaises(CutoverError): self.verify(expected_hash='a'*64)
        with self.assertRaises(CutoverError): self.verify(workflow='unrelated-workflow')

    def test_changed_contract_and_procedure_reject_stale_pin(self):
        for path in ('contract.json', 'runbook.md'):
            before = (self.root/path).read_bytes()
            (self.root/path).write_bytes(before + b' ')
            with self.assertRaises(CutoverError): self.verify()
            (self.root/path).write_bytes(before)

    def test_changed_or_missing_policy_cannot_keep_coverage(self):
        with self.assertRaises(CutoverError): verify_coverage(self.prompt+' altered', self.coverage, self.root)
        with self.assertRaises(CutoverError): verify_coverage(self.prompt, self.coverage[:-1], self.root)
        invalid = copy.deepcopy(self.coverage)
        invalid[1] = invalid[0]
        with self.assertRaises(CutoverError): verify_coverage(self.prompt, invalid, self.root)
        invalid = copy.deepcopy(self.coverage)
        invalid[0]['targets'] = ['runbook.md#Missing heading']
        with self.assertRaises(CutoverError): verify_coverage(self.prompt, invalid, self.root)

    def test_no_duplicate_registry_binding_or_changed_owner(self):
        self.registry['records'].append(copy.deepcopy(self.registry['records'][0]))
        (self.root/'registry.json').write_text(json.dumps(self.registry))
        with self.assertRaises(CutoverError): self.verify()
        self.registry['records'].pop()
        self.registry['records'][0]['owner']['account_or_local_owner'] = 'replacement'
        (self.root/'registry.json').write_text(json.dumps(self.registry))
        with self.assertRaises(CutoverError): self.verify()

    def test_preserved_backup_and_binding_tamper_blocks(self):
        for path in ('backup.toml', 'policy.txt', 'bindings.json', 'native.toml'):
            before = (self.root/path).read_bytes()
            (self.root/path).write_bytes(before+b' changed')
            with self.assertRaises(CutoverError): self.verify()
            (self.root/path).write_bytes(before)

    def test_no_path_escape(self):
        with self.assertRaises(CutoverError): pin_file(self.root, '../elsewhere')

    def test_schedule_readback_preserves_unknown_fields_and_notifications(self):
        old = {'prompt': 'old', 'target_thread_id': 'synthetic', 'notification_policy': 'failed_runs_only',
               'status': 'ACTIVE', 'rrule': 'existing', 'future_backend_setting': 'preserve'}
        new = dict(old, prompt='new', updated_at=2)
        verify_prompt_only_change(old, new)
        for key in ('target_thread_id', 'notification_policy', 'status', 'rrule', 'future_backend_setting'):
            changed = dict(new, **{key: 'changed'})
            with self.assertRaises(CutoverError): verify_prompt_only_change(old, changed)


class OwnershipTests(unittest.TestCase):
    def setUp(self):
        self.checks = dict.fromkeys(('published', 'exact_artifacts', 'source_unchanged', 'coverage_reviewed',
                                   'current_bindings', 'current_authority', 'accepted_trial', 'no_running_job'), True)

    def act(self, action, old='ACTIVE', new='PAUSED', **kwargs):
        return transition(action, old_state=old, new_state=new, checks=self.checks, **kwargs)

    def test_prompt_conversion_keeps_same_owner(self):
        self.assertEqual(self.act('update_prompt', new='ABSENT')['new'], 'ABSENT')
        with self.assertRaises(CutoverError): self.act('update_prompt')

    def test_disable_then_readback_before_enable(self):
        self.assertEqual(self.act('disable_old')['old'], 'PAUSED')
        with self.assertRaises(CutoverError): self.act('enable_new', old='PAUSED')
        self.checks['old_disabled_readback'] = True
        self.assertEqual(self.act('enable_new', old='PAUSED')['new'], 'ACTIVE')
        with self.assertRaises(CutoverError): self.act('enable_new')

    def test_each_missing_gate_and_truthy_string_blocks(self):
        for key in list(self.checks):
            self.checks[key] = 'true'
            with self.assertRaises(CutoverError): self.act('disable_old')
            self.checks[key] = True

    def test_unknown_readback_never_enables_or_restores(self):
        self.checks.update(old_disabled_readback=True, new_disabled_readback=True, rollback_source_verified=True)
        for action in ('enable_new', 'rollback'):
            for old, new in (('UNKNOWN', 'PAUSED'), ('PAUSED', 'UNKNOWN')):
                with self.assertRaises(CutoverError): self.act(action, old=old, new=new)

    def test_rollback_requires_replacement_disabled_and_original_verified(self):
        with self.assertRaises(CutoverError): self.act('rollback', old='PAUSED')
        self.checks.update(new_disabled_readback=True, rollback_source_verified=True)
        self.assertEqual(self.act('rollback', old='PAUSED')['old'], 'ACTIVE')
        with self.assertRaises(CutoverError): self.act('rollback', old='PAUSED', new='ACTIVE')

    def test_lost_write_response_never_retries_or_rolls_back_side_effect(self):
        self.checks.update(new_disabled_readback=True, rollback_source_verified=True)
        for action in ('disable_old', 'rollback', 'update_prompt'):
            with self.assertRaises(CutoverError): self.act(action, uncertain_write=True)


if __name__ == '__main__':
    unittest.main()

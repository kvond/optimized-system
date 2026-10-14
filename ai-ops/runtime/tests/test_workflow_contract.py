import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME))
from workflow_contract import ContractError, validate_workflow


def example():
    return {
        'schema_version': 1, 'workflow_id': 'synthetic-review',
        'contract_version': '1', 'title': 'Synthetic review', 'domain': 'technical',
        'owners': {'execution_owner_ref': 'operator:test', 'maintenance_owner_ref': 'maintainer:test'},
        'execution': {'executor_ref': 'executor:local', 'account_refs': [],
                      'required_capabilities': ['local-read'], 'privacy_partition': 'synthetic',
                      'concurrency_key': 'synthetic-review-writer'},
        'trigger': {'kind': 'on_demand'},
        'sources': [{'source_ref': 'source:fixture', 'required': True, 'coverage': 'complete', 'max_age_seconds': 300}],
        'outputs': [{'output_ref': 'output:fixture', 'kind': 'report', 'verification': 'content_and_destination_readback'}],
        'policy': {'allowed_actions': ['read-fixture'], 'prohibited_actions': ['network-write'],
                   'dependency_checks': ['Synthetic fixture hash verified'], 'uncertain_write_policy': 'stop_and_reconcile'},
        'success_checks': ['Saved output has exact expected fixture content'],
        'failure': {'max_safe_read_retries': 1, 'continue_independent_work': True, 'report_next_step': True},
        'provenance': {'contract_refs': ['test:synthetic-review']}}


class WorkflowContractTests(unittest.TestCase):
    def reject(self, value):
        with self.assertRaises(ContractError):
            validate_workflow(value)

    def test_returns_independent_validated_definition(self):
        source = example()
        result = validate_workflow(source)
        self.assertEqual(source, result)
        result['execution']['required_capabilities'].append('new-capability')
        self.assertEqual(source['execution']['required_capabilities'], ['local-read'])

    def test_schedule_binding_preserves_inventory_key(self):
        source = example()
        source['trigger'] = {'kind': 'existing_schedule', 'schedule_ref': 'Local Codex::example-task'}
        self.assertEqual(validate_workflow(source), source)
        source['trigger'].pop('schedule_ref')
        self.reject(source)

    def test_cannot_smuggle_activation_grants_or_inline_account_data(self):
        for location, key, bad_value in [
                ((), 'enabled', True), (('execution',), 'api_key', 'DO-NOT-ECHO'),
                (('sources', 0), 'content', {'private': 'DO-NOT-ECHO'}),
                (('trigger',), 'schedule_ref', 'not-an-on-demand-schedule'),
                (('failure',), 'retry_uncertain_writes', True)]:
            source = example()
            container = source
            for part in location:
                container = container[part]
            container[key] = bad_value
            self.reject(source)

    def test_unknown_or_boolean_versions_are_rejected(self):
        for version in (True, 0, 2, '1'):
            source = example()
            source['schema_version'] = version
            self.reject(source)

    def test_retry_bounds_and_types(self):
        for retries in (True, -1, 4, 1.0, '1'):
            source = example()
            source['failure']['max_safe_read_retries'] = retries
            self.reject(source)

    def test_failed_write_policy_and_next_step_cannot_be_relaxed(self):
        source = example()
        source['policy']['uncertain_write_policy'] = 'retry'
        self.reject(source)
        source = example()
        source['failure']['report_next_step'] = False
        self.reject(source)

    def test_inconsistent_action_permissions_are_rejected(self):
        source = example()
        source['policy']['allowed_actions'].append('network-write')
        self.reject(source)

    def test_duplicate_references_and_capabilities_are_rejected(self):
        for key, ref in (('sources', 'source_ref'), ('outputs', 'output_ref')):
            source = example()
            duplicate = copy.deepcopy(source[key][0])
            if key == 'sources':
                duplicate['max_age_seconds'] += 1
            else:
                duplicate['kind'] = 'artifact'
            source[key].append(duplicate)
            self.reject(source)
        source = example()
        source['execution']['required_capabilities'].append('local-read')
        self.reject(source)

    def test_source_coverage_and_freshness_are_explicit(self):
        for key, value in (('coverage', 'unknown'), ('max_age_seconds', True),
                           ('max_age_seconds', 0), ('required', 1)):
            source = example()
            source['sources'][0][key] = value
            self.reject(source)

    def test_empty_silent_failure_or_absent_success_evidence_rejected(self):
        for key in ('success_checks', 'sources', 'outputs'):
            source = example()
            source[key] = []
            self.reject(source)

    def test_cli_does_not_echo_private_payload_or_dispatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'fixture.json'
            source = example()
            path.write_text(json.dumps(source))
            command = [sys.executable, str(RUNTIME / 'workflow_contract.py'), str(path)]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0)
            self.assertIn('execution not attempted', result.stdout)
            source['password'] = 'DO-NOT-ECHO'
            path.write_text(json.dumps(source))
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('DO-NOT-ECHO', result.stdout + result.stderr)
            self.assertNotIn(str(path), result.stdout + result.stderr)

    def test_duplicate_json_fields_cannot_override_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'fixture.json'
            body = json.dumps(example())
            path.write_text(body.replace('"max_safe_read_retries": 1',
                                         '"max_safe_read_retries": 1, "max_safe_read_retries": 2'))
            result = subprocess.run([sys.executable, str(RUNTIME / 'workflow_contract.py'), str(path)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn('duplicate object fields', result.stderr)

    def test_schema_is_well_formed_and_example_has_all_declared_fields(self):
        schema_path = RUNTIME.parent / 'workflow-contracts' / 'workflow.schema.json'
        schema = json.loads(schema_path.read_text())
        self.assertEqual(set(example()), set(schema['required']))
        self.assertFalse(schema['additionalProperties'])
        # The optional library is QA only; production validation is stdlib.
        if importlib.util.find_spec('jsonschema'):
            from jsonschema import Draft202012Validator
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(example())


if __name__ == '__main__':
    unittest.main()

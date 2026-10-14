"""Behavioral synthetic tests; no private bindings or live provider requests."""
import copy
import datetime as dt
import json
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME))
from workflow_router import (RoutingError, route_workflow, resolve_intent,
                             resume_intent, build_handoff, load_rules)

NOW = dt.datetime(2026, 10, 14, 20, 0, tzinfo=dt.timezone.utc)


def stamp():
    return {'observed_at': (NOW - dt.timedelta(seconds=10)).isoformat(),
            'expires_at': (NOW + dt.timedelta(seconds=240)).isoformat(),
            'evidence_ref': 'synthetic:checked'}


def fixture(domain='technical', executor='home-codex', kind='deterministic', operation='read-fixture'):
    workflow = {
        'schema_version': 1, 'workflow_id': 'synthetic-review', 'contract_version': '1',
        'title': 'Synthetic review', 'domain': domain,
        'owners': {'execution_owner_ref': 'synthetic-owner', 'maintenance_owner_ref': 'synthetic-maintainer'},
        'execution': {'executor_ref': executor, 'account_refs': ['synthetic-account'],
                      'required_capabilities': ['synthetic-read'], 'privacy_partition': 'synthetic-private',
                      'concurrency_key': 'synthetic-shared-sources'},
        'trigger': {'kind': 'on_demand'},
        'sources': [{'source_ref': 'synthetic:source', 'required': True, 'coverage': 'complete', 'max_age_seconds': 300}],
        'outputs': [{'output_ref': 'synthetic:output', 'kind': 'report', 'verification': 'content_and_destination_readback'}],
        'policy': {'allowed_actions': [operation], 'prohibited_actions': ['ungranted-write'],
                   'dependency_checks': ['Synthetic exact identity confirmed'], 'uncertain_write_policy': 'stop_and_reconcile'},
        'success_checks': ['Synthetic saved output verified'],
        'failure': {'max_safe_read_retries': 1, 'continue_independent_work': True, 'report_next_step': True},
        'provenance': {'contract_refs': ['synthetic:canonical-contract']}}
    request = {'schema_version': 1, 'request_id': 'synthetic-request', 'workflow_id': workflow['workflow_id'],
               'domain': domain, 'operation': operation, 'execution_kind': kind,
               'authorization': dict(stamp(), state='authorized', allowed_actions=[operation]),
               'ownership': dict(stamp(), state='clear', owner_ref='synthetic-owner'),
               'receipt': dict(stamp(), state='clear'),
               'sources': [{'source_ref': 'synthetic:source', 'expected_revision': 'v1', 'revision': 'v1',
                            'coverage': 'complete', 'observed_at': stamp()['observed_at'], 'evidence_ref': 'synthetic:source-check'}],
               'dependencies': [dict(stamp(), check='Synthetic exact identity confirmed', state='passed')]}
    evidence = {'schema_version': 1, 'routes': [dict(stamp(), route_ref='synthetic-tool', provider_ref='synthetic-local',
                executor_ref=executor, resolved_executor_ref=executor, account_refs=['synthetic-account'], domain=domain,
                privacy_partition='synthetic-private', operation=operation, execution_kind=kind,
                capabilities=['synthetic-read'], resource_rank=1, estimated_cost='0', cost_basis_ref='synthetic:measured-cost',
                status='tested', identity_verified=True)]}
    return workflow, request, evidence


class RouterTests(unittest.TestCase):
    def route(self, data=None, **kwargs):
        return route_workflow(*(data or fixture()), now=NOW, **kwargs)

    def test_representative_domains_remain_exact_and_read_only(self):
        for domain in ('school', 'book', 'higher-ed', 'photo', 'personal', 'ai-ops'):
            with self.subTest(domain=domain):
                data = fixture(domain)
                before = copy.deepcopy(data)
                decision = self.route(data)
                self.assertEqual(decision['status'], 'ready')
                self.assertEqual(decision['resolved_executor_ref'], 'home-codex')
                self.assertFalse(decision['execution_attempted'])
                self.assertEqual(data, before)
                self.assertEqual(decision['valid_until'], stamp()['expires_at'])

    def test_higher_ed_cannot_use_school_evidence(self):
        data = fixture('higher-ed')
        data[2]['routes'][0]['domain'] = 'school'
        self.assertEqual(self.route(data)['reason'], 'no_verified_route')

    def test_account_partition_operation_and_executor_are_independent(self):
        for key, value in [('account_refs', ['other-account']), ('privacy_partition', 'public'),
                           ('operation', 'other-operation'), ('executor_ref', 'school-google')]:
            with self.subTest(key=key):
                data = fixture()
                data[2]['routes'][0][key] = value
                self.assertEqual(self.route(data)['status'], 'blocked')

    def test_symbolic_executor_resolves_without_changing_contract(self):
        data = fixture(executor='private:existing-executor:synthetic')
        data[2]['routes'][0]['resolved_executor_ref'] = 'home-codex'
        result = self.route(data)
        self.assertEqual(result['status'], 'ready')
        self.assertEqual(result['executor_ref'], 'private:existing-executor:synthetic')
        self.assertEqual(result['resolved_executor_ref'], 'home-codex')

    def test_unresolved_executor_reference_does_not_create_capability(self):
        data = fixture(executor='existing-owner')
        self.assertEqual(self.route(data)['reason'], 'executor_binding_unresolved')

    def test_expired_future_untested_and_blocked_capabilities_do_not_route(self):
        for edit, expected in [({'expires_at': NOW.isoformat()}, 'capability_evidence_stale'),
                               ({'observed_at': (NOW + dt.timedelta(seconds=1)).isoformat()}, 'capability_evidence_stale'),
                               ({'status': 'unverified'}, 'capability_unverified'),
                               ({'status': 'blocked'}, 'capability_unverified'),
                               ({'identity_verified': False}, 'capability_unverified')]:
            data = fixture()
            data[2]['routes'][0].update(edit)
            self.assertEqual(self.route(data)['reason'], expected)

    def test_old_capability_cannot_extend_itself_with_distant_expiry(self):
        data = fixture()
        data[2]['routes'][0]['observed_at'] = (NOW - dt.timedelta(days=2)).isoformat()
        self.assertEqual(self.route(data)['reason'], 'capability_evidence_stale')

    def test_missing_required_capability_blocks(self):
        data = fixture()
        data[0]['execution']['required_capabilities'].append('synthetic-write')
        self.assertEqual(self.route(data)['reason'], 'capability_insufficient')

    def test_unknown_cost_is_not_a_free_route(self):
        data = fixture()
        data[2]['routes'][0]['estimated_cost'] = None
        self.assertEqual(self.route(data)['reason'], 'cost_input_missing')
        data[2]['routes'][0]['estimated_cost'] = '0'
        data[2]['routes'][0]['cost_basis_ref'] = None
        self.assertEqual(self.route(data)['reason'], 'cost_input_missing')

    def test_cheapest_sufficient_route_and_rank_tiebreak_use_supplied_values(self):
        data = fixture()
        first = data[2]['routes'][0]
        first.update(estimated_cost='0.03', resource_rank=5)
        second = dict(first, route_ref='second', estimated_cost='0.01', resource_rank=9)
        third = dict(first, route_ref='third', estimated_cost='0.01', resource_rank=2)
        data[2]['routes'] += [second, third]
        self.assertEqual(self.route(data)['route_ref'], 'third')

    def test_assisted_work_prefers_exact_sufficient_deterministic_tool(self):
        data = fixture(kind='assisted')
        first = data[2]['routes'][0]
        second = dict(first, route_ref='deterministic-tool', execution_kind='deterministic', estimated_cost='0.02')
        data[2]['routes'].append(second)
        self.assertEqual(self.route(data)['route_ref'], 'deterministic-tool')
        self.assertEqual(self.route(data)['execution_kind'], 'deterministic')

    def test_coding_stays_with_codex_even_if_other_account_can_code(self):
        data = fixture(executor='ud-claude-home', kind='coding')
        self.assertEqual(self.route(data)['reason'], 'coding_owner_required')
        data = fixture(kind='coding')
        self.assertEqual(self.route(data)['status'], 'ready')

    def test_school_claude_needs_verified_bounded_browser_kind(self):
        data = fixture('school', executor='school-claude', kind='browser')
        data[2]['routes'][0]['status'] = 'unverified'
        self.assertEqual(self.route(data)['status'], 'blocked')
        data[2]['routes'][0]['status'] = 'tested'
        self.assertEqual(self.route(data)['status'], 'ready')
        data[1]['execution_kind'] = data[2]['routes'][0]['execution_kind'] = 'assisted'
        self.assertEqual(self.route(data)['reason'], 'executor_kind_not_allowed')

    def test_helper_is_exclusive_grade_writer(self):
        for operation in load_rules()['exclusive_operation_executors']:
            data = fixture('school', kind='browser', operation=operation)
            self.assertEqual(self.route(data)['reason'], 'exclusive_writer_required')
            data[0]['execution']['executor_ref'] = 'school-chrome-helper'
            data[2]['routes'][0].update(executor_ref='school-chrome-helper', resolved_executor_ref='school-chrome-helper')
            self.assertEqual(self.route(data)['status'], 'ready')
        data = fixture('school', kind='browser')
        data[0]['execution']['required_capabilities'].append('school-ic-helper-write')
        data[2]['routes'][0]['capabilities'].append('school-ic-helper-write')
        self.assertEqual(self.route(data)['reason'], 'exclusive_writer_required')

    def test_uncertain_receipt_prevents_fallback_or_duplicate_write(self):
        data = fixture('school', kind='browser')
        data[1]['receipt']['state'] = 'uncertain'
        data[2]['routes'].append(dict(data[2]['routes'][0], route_ref='fallback'))
        self.assertEqual(self.route(data)['reason'], 'receipt_reconciliation_required')
        self.assertNotIn('route_ref', self.route(data))

    def test_unknown_receipt_and_competing_or_unknown_owner_hold(self):
        for key, state, expected in [('receipt', 'unknown', 'receipt_reconciliation_required'),
                                      ('ownership', 'competing', 'ownership_unresolved'),
                                      ('ownership', 'unknown', 'ownership_unresolved')]:
            data = fixture()
            data[1][key]['state'] = state
            self.assertEqual(self.route(data)['reason'], expected)
        data = fixture()
        data[1]['ownership']['owner_ref'] = 'another-owner'
        self.assertEqual(self.route(data)['reason'], 'ownership_unresolved')

    def test_capability_does_not_grant_authority(self):
        data = fixture()
        data[1]['authorization']['state'] = 'unknown'
        self.assertEqual(self.route(data)['reason'], 'authorization_missing')
        data[1]['authorization']['state'] = 'authorized'
        data[1]['authorization']['allowed_actions'] = []
        self.assertEqual(self.route(data)['reason'], 'authorization_missing')

    def test_prohibited_or_wrong_workflow_never_routes(self):
        for key, value, expected in [('operation', 'ungranted-write', 'operation_not_allowed'),
                                     ('workflow_id', 'another-workflow', 'intent_mismatch'),
                                     ('domain', 'another-domain', 'intent_mismatch')]:
            data = fixture()
            data[1][key] = value
            self.assertEqual(self.route(data)['reason'], expected)

    def test_stale_authority_owner_receipt_and_dependency_hold(self):
        for key in ('authorization', 'ownership', 'receipt'):
            data = fixture()
            data[1][key]['expires_at'] = NOW.isoformat()
            self.assertEqual(self.route(data)['reason'], key + '_evidence_stale')
        data = fixture()
        data[1]['dependencies'][0]['expires_at'] = NOW.isoformat()
        self.assertEqual(self.route(data)['reason'], 'dependency_evidence_stale')

    def test_unverified_or_missing_dependency_is_actionable(self):
        data = fixture()
        data[1]['dependencies'] = []
        result = self.route(data)
        self.assertEqual(result['reason'], 'dependency_unverified')
        self.assertEqual(result['dependency_index'], 0)
        self.assertTrue(result['next_step'])

    def test_source_partial_is_not_empty_or_complete(self):
        for coverage in ('partial', 'unavailable', 'bounded'):
            data = fixture()
            data[1]['sources'][0]['coverage'] = coverage
            self.assertEqual(self.route(data)['status'], 'blocked')
        data = fixture()
        data[0]['sources'][0]['coverage'] = 'bounded'
        data[1]['sources'][0]['coverage'] = 'bounded'
        self.assertEqual(self.route(data)['status'], 'ready')

    def test_changed_missing_or_stale_revision_is_held(self):
        for edit, expected in [({'revision': 'v2'}, 'source_revision_changed'),
                               ({'revision': None}, 'source_revision_missing'),
                               ({'observed_at': (NOW - dt.timedelta(seconds=300)).isoformat()}, 'source_evidence_stale')]:
            data = fixture()
            data[1]['sources'][0].update(edit)
            self.assertEqual(self.route(data)['reason'], expected)

    def test_optional_unavailable_source_is_explicit_in_decision(self):
        data = fixture()
        data[0]['sources'][0]['required'] = False
        data[1]['sources'] = []
        result = self.route(data)
        self.assertEqual(result['status'], 'ready')
        self.assertEqual(result['unavailable_sources'], [{'source_ref': 'synthetic:source', 'reason': 'source_unavailable_or_partial'}])

    def test_conflicting_actual_executor_binding_cannot_compete_on_cost(self):
        data = fixture()
        data[2]['routes'].append(dict(data[2]['routes'][0], route_ref='other', resolved_executor_ref='another-runtime'))
        self.assertEqual(self.route(data)['reason'], 'executor_binding_conflict')
        data[2]['routes'][1]['estimated_cost'] = None
        self.assertEqual(self.route(data)['reason'], 'executor_binding_conflict')

    def test_duplicate_evidence_and_sources_are_rejected(self):
        for index, key in ((2, 'routes'), (1, 'sources'), (1, 'dependencies')):
            data = fixture()
            data[index][key].append(copy.deepcopy(data[index][key][0]))
            with self.assertRaises(RoutingError):
                self.route(data)

    def test_bool_price_nan_extra_fields_and_naive_time_rejected(self):
        for key, value in [('estimated_cost', True), ('estimated_cost', 'NaN'), ('resource_rank', True),
                           ('identity_verified', 1), ('observed_at', '2026-10-14T20:00:00')]:
            data = fixture()
            data[2]['routes'][0][key] = value
            with self.assertRaises(RoutingError):
                self.route(data)
        data = fixture()
        data[1]['secret'] = 'DO-NOT-ECHO'
        with self.assertRaises(RoutingError):
            self.route(data)

    def test_unknown_and_ambiguous_intent_return_one_question_no_execution(self):
        first = fixture('book')[0]
        second = copy.deepcopy(first)
        second['workflow_id'] = 'another-book'
        intent = {'workflow_id': None, 'domain': 'book', 'operation': 'read-fixture'}
        pending = resolve_intent([first, second], intent)
        self.assertEqual(pending['status'], 'question')
        self.assertEqual(pending['candidates'], ['synthetic-review', 'another-book'])
        self.assertFalse(pending['execution_attempted'])
        self.assertEqual(resume_intent([first, second], pending, None), pending)
        answer = dict(intent, workflow_id='another-book')
        self.assertEqual(resume_intent([first, second], pending, answer)['status'], 'resolved')
        unknown = resolve_intent([first], dict(intent, domain='school'))
        self.assertEqual(unknown['reason'], 'unknown_intent')

    def test_answer_does_not_expand_scope_or_reuse_changed_contract(self):
        workflow = fixture('book')[0]
        pending = resolve_intent([workflow], {'workflow_id': None, 'domain': 'book', 'operation': None})
        with self.assertRaises(RoutingError):
            resume_intent([workflow], pending, {'workflow_id': 'synthetic-review', 'domain': 'school', 'operation': 'read-fixture'})
        workflow['contract_version'] = '2'
        with self.assertRaises(RoutingError):
            resume_intent([workflow], pending, {'workflow_id': 'synthetic-review', 'domain': 'book', 'operation': 'read-fixture'})

    def test_handoff_contains_canonical_progress_and_next_owner_no_transfer(self):
        workflow, _, _ = fixture()
        result = build_handoff(workflow, decision=self.route(), canonical_source_ref='synthetic:canonical',
                               completed=[{'action': 'read-fixture', 'receipt_ref': 'synthetic:receipt'}],
                               remaining=[], output_refs=['synthetic:output-v1'], next_owner_ref='synthetic-owner',
                               next_step='Read the saved output before the next operation.')
        self.assertEqual(result['canonical_source_ref'], 'synthetic:canonical')
        self.assertEqual(result['completed'][0]['receipt_ref'], 'synthetic:receipt')
        self.assertFalse(result['ownership_transferred'])
        schema = json.loads((RUNTIME.parents[1] / 'skills/ai-operations-router/references/handoff.schema.json').read_text())
        self.assertEqual(set(result), set(schema['required']))
        if importlib.util.find_spec('jsonschema'):
            from jsonschema import Draft202012Validator
            Draft202012Validator.check_schema(schema)
            Draft202012Validator(schema).validate(result)
        with self.assertRaises(RoutingError):
            build_handoff(workflow, decision=self.route(), canonical_source_ref='synthetic:canonical', completed=[],
                          remaining=['read-fixture'], output_refs=[], next_owner_ref='other-owner', next_step='Continue')

    def test_handoff_cannot_claim_completed_work_without_output_or_receipt(self):
        workflow, _, _ = fixture()
        args = dict(decision=self.route(), canonical_source_ref='synthetic:canonical',
                    completed=[{'action': 'read-fixture', 'receipt_ref': 'synthetic:receipt'}],
                    remaining=[], output_refs=[], next_owner_ref='synthetic-owner', next_step='Verify output.')
        with self.assertRaises(RoutingError):
            build_handoff(workflow, **args)
        args['output_refs'] = ['synthetic:output']
        args['completed'][0]['receipt_ref'] = ''
        with self.assertRaises(RoutingError):
            build_handoff(workflow, **args)

    def test_cli_fresh_process_ready_blocked_and_private_error(self):
        with tempfile.TemporaryDirectory() as temp:
            paths = [Path(temp) / name for name in ('workflow.json', 'request.json', 'evidence.json')]
            data = fixture()
            for path, value in zip(paths, data):
                path.write_text(json.dumps(value))
            command = [sys.executable, str(RUNTIME / 'workflow_router.py'), *(str(p) for p in paths), '--now', NOW.isoformat()]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'ready')
            data[1]['receipt']['state'] = 'uncertain'
            paths[1].write_text(json.dumps(data[1]))
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(json.loads(result.stdout)['reason'], 'receipt_reconciliation_required')
            data[1]['secret'] = 'DO-NOT-ECHO'
            paths[1].write_text(json.dumps(data[1]))
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('DO-NOT-ECHO', result.stderr + result.stdout)
            self.assertNotIn(str(paths[1]), result.stderr + result.stdout)
            self.assertEqual(set(Path(temp).iterdir()), set(paths))


if __name__ == '__main__':
    unittest.main()

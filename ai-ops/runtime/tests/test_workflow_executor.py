"""Offline executor failures with private temporary state and real catalog reads."""
import copy
import datetime as dt
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME))
from runner import Controller, digest
from storage import StorageError
from workflow_executor import (WorkflowExecutor, CatalogValidationAdapter,
                               OPERATION, CAPABILITY, EXECUTOR, LEASE_CHECK)

NOW = dt.datetime(2026, 10, 14, 20, 0, tzinfo=dt.timezone.utc)


def catalog_workflow():
    return {
        'schema_version': 1, 'workflow_id': 'local-catalog-acceptance', 'contract_version': '1',
        'title': 'Local catalog validation acceptance', 'domain': 'technical',
        'owners': {'execution_owner_ref': 'local-test-owner', 'maintenance_owner_ref': 'local-test-owner'},
        'execution': {'executor_ref': EXECUTOR, 'account_refs': [], 'required_capabilities': [CAPABILITY],
                      'privacy_partition': 'synthetic', 'concurrency_key': 'local-catalog-acceptance'},
        'trigger': {'kind': 'on_demand'},
        'sources': [{'source_ref': 'source:canonical-workflow-catalog', 'required': True,
                     'coverage': 'complete', 'max_age_seconds': 300}],
        'outputs': [{'output_ref': 'output:catalog-validation', 'kind': 'report',
                     'verification': 'content_and_destination_readback'}],
        'policy': {'allowed_actions': [OPERATION], 'prohibited_actions': ['external-write'],
                   'dependency_checks': [LEASE_CHECK], 'uncertain_write_policy': 'stop_and_reconcile'},
        'success_checks': ['Saved runner receipt and exact catalog digest read back'],
        'failure': {'max_safe_read_retries': 1, 'continue_independent_work': True, 'report_next_step': True},
        'provenance': {'contract_refs': ['test:bounded-local-catalog-acceptance']}}


class EvidenceResolver:
    """Synthetic gate evidence for tests, never a live account capability claim."""
    def __init__(self, workflow, revision, now, request_id='test-request'):
        self.workflow, self.revision, self.now, self.request_id = workflow, revision, now, request_id
        self.calls = 0
        self.edit = lambda call, request, evidence: None

    def __call__(self, lease):
        self.calls += 1
        w = self.workflow
        stamp = {'observed_at': self.now().isoformat(),
                 'expires_at': (self.now() + dt.timedelta(seconds=120)).isoformat(),
                 'evidence_ref': 'test:bounded-local-evidence'}
        request = {'schema_version': 1, 'request_id': self.request_id, 'workflow_id': w['workflow_id'],
                   'domain': w['domain'], 'operation': OPERATION, 'execution_kind': 'deterministic',
                   'authorization': dict(stamp, state='authorized', allowed_actions=[OPERATION]),
                   'ownership': dict(stamp, state='clear', owner_ref=w['owners']['execution_owner_ref']),
                   'receipt': dict(stamp, state='clear'),
                   'sources': [{'source_ref': w['sources'][0]['source_ref'], 'expected_revision': self.revision,
                                'revision': self.revision, 'coverage': 'complete',
                                'observed_at': self.now().isoformat(), 'evidence_ref': 'test:catalog-read'}],
                   'dependencies': [dict(stamp, check=LEASE_CHECK, state='passed' if lease else 'unknown')]}
        evidence = {'schema_version': 1, 'routes': [dict(stamp, route_ref='local-catalog-validator',
                    provider_ref='local', executor_ref=EXECUTOR, resolved_executor_ref=EXECUTOR, account_refs=[],
                    domain=w['domain'], privacy_partition=w['execution']['privacy_partition'], operation=OPERATION,
                    execution_kind='deterministic', capabilities=[CAPABILITY], resource_rank=0, estimated_cost='0',
                    cost_basis_ref='test:local-no-provider-dispatch', status='tested', identity_verified=True)]}
        self.edit(self.calls, request, evidence)
        return request, evidence


class WorkflowExecutorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve())
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.state = self.root / 'state'
        self.state.mkdir(mode=0o700)
        self.file = self.root / 'catalog.json'
        self.workflow = catalog_workflow()
        self.file.write_text(json.dumps(self.workflow))
        self.clock = NOW
        self.adapter = CatalogValidationAdapter([self.file])
        self.executor = WorkflowExecutor(self.adapter, acceptance_directory=self.state, now=lambda: self.clock)
        self.resolver = EvidenceResolver(self.workflow, digest(self.adapter.read()), lambda: self.clock)
        self.deadline = NOW + dt.timedelta(seconds=60)

    def run_it(self, *, workflow=None, resolver=None, executor=None):
        return (executor or self.executor).execute(workflow or self.workflow, resolver or self.resolver, deadline=self.deadline)

    def change_file(self):
        changed = copy.deepcopy(self.workflow)
        changed['title'] = 'Changed catalog source'
        self.file.write_text(json.dumps(changed))

    def state_rows(self):
        with self.executor.store.connection() as db:
            return db.execute('SELECT state FROM workflow_execution_state ORDER BY request_key').fetchall()

    def test_real_local_adapter_saves_existing_runner_receipt_and_reads_back(self):
        result = self.run_it()
        self.assertEqual(result['status'], 'complete')
        self.assertEqual(result['readback']['components']['catalog']['output']['validated_count'], 1)
        self.assertEqual(result['runner_receipt']['result_location']['table'], 'runner_requests')
        self.assertEqual(result['runner_receipt']['paid_dispatches'], 0)
        self.assertFalse(result['production_storage_verified'])
        self.assertEqual(self.state_rows(), [('complete',)])
        self.assertEqual(self.executor.database.stat().st_mode & 0o077, 0)

    def test_idempotent_replay_only_reads_saved_output(self):
        first = self.run_it()
        self.clock += dt.timedelta(seconds=5)
        with patch.object(Controller, 'execute', side_effect=AssertionError('must not dispatch again')):
            second = self.run_it()
        self.assertTrue(second['reused_request'])
        self.assertEqual(first['runner_receipt'], second['runner_receipt'])

    def test_same_request_changed_revision_never_overwrites_output(self):
        first = self.run_it()
        self.change_file()
        self.resolver.revision = digest(self.adapter.read())
        result = self.run_it()
        self.assertEqual(result['reason'], 'request_identity_conflict')
        with self.executor.store.connection() as db:
            self.assertEqual(db.execute('SELECT COUNT(*) FROM runner_requests').fetchone()[0], 1)
        self.assertEqual(first['status'], 'complete')

    def test_actual_source_change_after_claim_blocks_before_dispatch(self):
        def edit(call, request, evidence):
            if call == 2:
                self.change_file()
        self.resolver.edit = edit
        result = self.run_it()
        self.assertEqual(result['reason'], 'source_revision_changed')
        self.assertFalse(result['execution_attempted'])
        self.assertEqual(self.state_rows(), [('blocked',)])

    def test_source_change_during_dispatch_stops_scope_and_new_id_cannot_retry(self):
        original = Controller.execute
        def changed(controller, request):
            receipt = original(controller, request)
            self.change_file()
            return receipt
        with patch.object(Controller, 'execute', changed):
            first = self.run_it()
        self.assertEqual(first['reason'], 'source_changed_after_dispatch')
        self.assertEqual(first['status'], 'stopped')
        self.resolver.request_id = 'new-id-cannot-clear-hold'
        self.resolver.revision = digest(self.adapter.read())
        with patch.object(Controller, 'execute', side_effect=AssertionError('must not retry')):
            again = self.run_it()
        self.assertEqual(again['reason'], 'scope_reconciliation_required')

    def test_lost_native_readback_is_durable_stop_without_retry(self):
        with patch.object(Controller, 'readback', side_effect=OSError('readback lost')):
            first = self.run_it()
        self.assertEqual(first['status'], 'stopped')
        self.assertEqual(first['reason'], 'save_or_readback_uncertain')
        reloaded = WorkflowExecutor(self.adapter, acceptance_directory=self.state, now=lambda: self.clock)
        with patch.object(Controller, 'execute', side_effect=AssertionError('must not retry')):
            second = self.run_it(executor=reloaded)
        self.assertEqual(second['reason'], 'scope_reconciliation_required')
        self.assertEqual(self.state_rows(), [('stopped',)])

    def test_completed_output_lost_readback_never_regenerates(self):
        self.run_it()
        with self.executor.store.transaction() as db:
            db.execute('DELETE FROM runner_requests')
        with patch.object(Controller, 'execute', side_effect=AssertionError('must not regenerate')):
            result = self.run_it()
        self.assertEqual(result['reason'], 'completed_readback_lost')
        self.assertEqual(self.state_rows(), [('stopped',)])

    def test_interruption_after_dispatch_marker_survives_restart(self):
        with patch.object(Controller, 'execute', side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.run_it()
        self.assertEqual(self.state_rows(), [('running',)])
        result = self.run_it()
        self.assertEqual(result['reason'], 'scope_reconciliation_required')

    def test_pre_dispatch_interruption_resumes_safely(self):
        original = self.executor._record
        def interrupt(key, scope, fp, state, record):
            original(key, scope, fp, state, record)
            if state == 'prepared':
                raise KeyboardInterrupt
        with patch.object(self.executor, '_record', interrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.run_it()
        self.assertEqual(self.state_rows(), [('prepared',)])
        self.assertEqual(self.run_it()['status'], 'complete')

    def test_concurrent_same_scope_is_nonblocking_and_dispatches_once(self):
        entered, release = threading.Event(), threading.Event()
        errors, results = [], []
        def edit(call, request, evidence):
            if call == 2:
                entered.set()
                if not release.wait(3):
                    raise RuntimeError('test release timeout')
        self.resolver.edit = edit
        def run_first():
            try:
                results.append(self.run_it())
            except BaseException as error:
                errors.append(error)
        worker = threading.Thread(target=run_first)
        worker.start()
        try:
            self.assertTrue(entered.wait(3))
            second_resolver = EvidenceResolver(self.workflow, self.resolver.revision, lambda: self.clock, 'other-request')
            second = self.run_it(resolver=second_resolver)
            self.assertEqual(second['reason'], 'scope_busy')
            self.assertFalse(second['execution_attempted'])
        finally:
            release.set()
            worker.join(3)
        self.assertFalse(worker.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(results[0]['status'], 'complete')
        self.assertEqual(self.state_rows(), [('complete',)])

    def test_independent_scope_remains_usable_after_stop(self):
        with patch.object(Controller, 'readback', side_effect=OSError):
            self.run_it()
        independent = copy.deepcopy(self.workflow)
        independent['workflow_id'] = 'independent-catalog-check'
        independent['execution']['concurrency_key'] = 'independent-catalog-check'
        resolver = EvidenceResolver(independent, self.resolver.revision, lambda: self.clock)
        self.assertEqual(self.run_it(workflow=independent, resolver=resolver)['status'], 'complete')
        self.assertCountEqual(self.state_rows(), [('complete',), ('stopped',)])

    def test_provider_unavailable_after_claim_never_dispatches(self):
        def edit(call, request, evidence):
            if call >= 2:
                evidence['routes'][0]['status'] = 'blocked'
        self.resolver.edit = edit
        with patch.object(Controller, 'execute', side_effect=AssertionError('no provider fallback')):
            result = self.run_it()
        self.assertEqual(result['reason'], 'capability_unverified')
        self.assertFalse(result['execution_attempted'])

    def test_competing_owner_after_claim_never_dispatches(self):
        def edit(call, request, evidence):
            if call >= 2:
                request['ownership']['state'] = 'competing'
        self.resolver.edit = edit
        self.assertEqual(self.run_it()['reason'], 'ownership_unresolved')

    def test_existing_uncertain_receipt_never_dispatches(self):
        self.resolver.edit = lambda call, request, evidence: request['receipt'].update(state='uncertain')
        self.assertEqual(self.run_it()['reason'], 'receipt_reconciliation_required')
        self.assertEqual(self.state_rows(), [])

    def test_deadline_expiry_before_claim_never_dispatches(self):
        self.clock = self.deadline
        self.assertEqual(self.run_it()['reason'], 'deadline_expired')
        self.assertEqual(self.state_rows(), [('blocked',)])

    def test_deadline_expiry_before_dispatch_never_calls_runner(self):
        def edit(call, request, evidence):
            if call == 3:
                self.clock = self.deadline
        self.resolver.edit = edit
        with patch.object(Controller, 'execute', side_effect=AssertionError('deadline passed')):
            result = self.run_it()
        self.assertEqual(result['reason'], 'deadline_expired')
        self.assertFalse(result['execution_attempted'])

    def test_expired_ready_decision_after_running_marker_is_stopped(self):
        original = self.executor._record
        def advance(key, scope, fp, state, record):
            original(key, scope, fp, state, record)
            if state == 'running':
                self.clock += dt.timedelta(seconds=121)
        with patch.object(self.executor, '_record', advance), patch.object(Controller, 'execute', side_effect=AssertionError):
            result = self.run_it()
        self.assertEqual(result['status'], 'stopped')
        self.assertEqual(result['reason'], 'deadline_expired')

    def test_safe_source_reads_retry_only_within_declared_limit(self):
        actual = self.adapter.read
        calls = 0
        def transient():
            nonlocal calls
            calls += 1
            if calls == 1:
                raise OSError('temporary safe read error')
            return actual()
        with patch.object(self.adapter, 'read', transient):
            self.assertEqual(self.run_it()['status'], 'complete')
        self.assertEqual(calls, 4)  # One retry, pre-dispatch recheck, post-save recheck.
        self.resolver.request_id = 'read-failure-request'
        with patch.object(self.adapter, 'read', side_effect=OSError) as failed:
            result = self.run_it()
        self.assertEqual(failed.call_count, 2)
        self.assertEqual(result['reason'], 'source_read_failed')

    def test_unsupported_school_remote_or_account_adapter_never_dispatches(self):
        self.workflow['domain'] = 'school'
        result = self.run_it()
        self.assertEqual(result['reason'], 'adapter_binding_not_supported')
        self.assertFalse(result['execution_attempted'])

    def test_no_arbitrary_adapter_registry_or_nonprivate_state(self):
        with self.assertRaises(ValueError):
            WorkflowExecutor(object(), acceptance_directory=self.state)
        self.state.chmod(0o755)
        with self.assertRaises(StorageError):
            WorkflowExecutor(self.adapter, acceptance_directory=self.state)

    def test_symlink_source_and_oversized_payload_fail_closed(self):
        other = self.root / 'other.json'
        other.write_text(self.file.read_text())
        self.file.unlink()
        self.file.symlink_to(other)
        self.assertEqual(self.run_it()['reason'], 'source_validation_failed')
        self.file.unlink()
        self.file.write_text(' ' * 65537)
        self.assertEqual(self.run_it()['reason'], 'source_validation_failed')

    def test_production_mount_unavailable_does_not_fall_back(self):
        with patch('workflow_executor.resolve_storage', side_effect=StorageError('mount absent')):
            with self.assertRaises(StorageError):
                WorkflowExecutor(self.adapter)
        self.assertFalse((self.root / 'cache.sqlite').exists())


if __name__ == '__main__':
    unittest.main()

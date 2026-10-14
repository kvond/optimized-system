"""Bounded local catalog execution through the existing router and Controller.

This module has one trusted adapter, no command/model/plugin dispatch, and no
school writer. Coordinator state references runner_requests receipts; it is not
a second grade, mail, feedback or domain-result ledger.
"""
from __future__ import annotations

import contextlib
import copy
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import stat
import uuid

from foundation import Store, canonical, timestamp, utcnow
from runner import Controller, SourceSnapshot, digest
from storage import StorageError, resolve_storage
from workflow_contract import validate_workflow, _unique_json_keys
from workflow_router import route_workflow

OPERATION = 'validate-workflow-catalog'
CAPABILITY = 'local-catalog-validation'
EXECUTOR = 'local-deterministic-runtime'
LEASE_CHECK = 'Local catalog execution lease held'
MAX_FILES = 64
MAX_FILE_BYTES = 65536


class ExecutionBlocked(RuntimeError):
    def __init__(self, reason, next_step):
        self.reason, self.next_step = reason, next_step
        super().__init__(reason)


def _private(path, *, directory=False):
    path = Path(path)
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise StorageError('symlink state paths rejected')
    mode = path.stat().st_mode
    if mode & 0o077 or not (stat.S_ISDIR(mode) if directory else stat.S_ISREG(mode)):
        raise StorageError('private state permissions required')


def _bounded_file(path):
    flags = os.O_RDONLY | os.O_NONBLOCK | getattr(os, 'O_NOFOLLOW', 0)
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('symlink source rejected')
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_FILE_BYTES:
            raise ValueError('bounded regular source required')
        body = stream.read(MAX_FILE_BYTES + 1)
        after = os.fstat(stream.fileno())
    if len(body) > MAX_FILE_BYTES or (before.st_ino, before.st_size, before.st_mtime_ns) != (after.st_ino, after.st_size, after.st_mtime_ns):
        raise ValueError('source changed during bounded read')
    return body


class CatalogValidationAdapter:
    """Fixed pure adapter; trusted configuration binds exact local JSON files.

    Only IDs, versions and content hashes enter Controller snapshots. No source
    bodies, account configuration, shell argv, network or paid calls are saved.
    """
    def __init__(self, files, *, source_ref='source:canonical-workflow-catalog',
                 output_ref='output:catalog-validation'):
        self.files = tuple(sorted((Path(p).absolute() for p in files), key=str))
        if not 1 <= len(self.files) <= MAX_FILES or len(set(self.files)) != len(self.files):
            raise ValueError('bounded unique catalog file allowlist required')
        self.source_ref, self.output_ref = source_ref, output_ref
        self.binding = digest({'adapter': 'catalog-validation-v1', 'files': [str(p) for p in self.files],
                               'source_ref': source_ref, 'output_ref': output_ref})

    def read(self):
        records = []
        for path in self.files:
            body = _bounded_file(path)
            workflow = validate_workflow(json.loads(body, object_pairs_hook=_unique_json_keys))
            records.append({'workflow_id': workflow['workflow_id'],
                            'contract_version': workflow['contract_version'],
                            'sha256': hashlib.sha256(body).hexdigest()})
        if len({r['workflow_id'] for r in records}) != len(records):
            raise ValueError('duplicate workflow identity')
        return {'validated_count': len(records), 'definitions': sorted(records, key=lambda r: r['workflow_id'])}

    def check_binding(self, workflow, decision, *, acceptance):
        execution = workflow['execution']
        if (workflow['domain'] != 'technical' or decision.get('execution_kind') != 'deterministic'
                or decision.get('resolved_executor_ref') != EXECUTOR
                or decision.get('provider_ref') != 'local'
                or decision.get('estimated_cost') != '0'
                or execution['account_refs'] or execution['required_capabilities'] != [CAPABILITY]
                or workflow['policy']['allowed_actions'] != [OPERATION]
                or len(workflow['sources']) != 1 or not workflow['sources'][0]['required']
                or workflow['sources'][0]['coverage'] != 'complete'
                or workflow['sources'][0]['source_ref'] != self.source_ref
                or len(workflow['outputs']) != 1 or workflow['outputs'][0]['output_ref'] != self.output_ref
                or (acceptance and execution['privacy_partition'] != 'synthetic')):
            raise ExecutionBlocked('adapter_binding_not_supported',
                'Keep the existing workflow owner; this bridge implements only exact local catalog validation.')


class _FrozenSource:
    def __init__(self, snapshot):
        self.value = snapshot

    def snapshot(self, source_id, privacy_partition, max_bytes):
        if source_id != self.value.source_id or privacy_partition != self.value.privacy_partition:
            raise PermissionError('frozen source binding mismatch')
        return copy.deepcopy(self.value)


def _catalog_result(task, content, inputs):
    if task != OPERATION or inputs != {}:
        raise ValueError('fixed operation and empty inputs required')
    return copy.deepcopy(content)


class WorkflowExecutor:
    """Use one existing private Store and cooperative local flock per scope.

    resolve(lease_or_none) -> (request, capability_evidence) is trusted bounded
    read-only integration code. It must reread authority/native ownership/receipt
    evidence; it may attest LEASE_CHECK only while the supplied lease is held.
    A lease here does not fence independent browser, remote or external writers.
    Those adapters are deliberately absent. No clear-stop or retry-write API.
    """
    def __init__(self, adapter, *, paths=None, acceptance_directory=None, now=utcnow):
        if type(adapter) is not CatalogValidationAdapter:
            raise ValueError('only the fixed catalog adapter is allowlisted')
        if paths is not None and acceptance_directory is not None:
            raise ValueError('choose production storage or explicit offline acceptance')
        self.adapter, self.now = adapter, now
        self.acceptance = acceptance_directory is not None
        if self.acceptance:
            self.root = Path(acceptance_directory).absolute()
            # Never initialize a second Git-backed state location or relax modes.
            if any((p / '.git').exists() for p in (self.root, *self.root.parents)):
                raise StorageError('acceptance state must be outside Git')
            _private(self.root, directory=True)
            self.paths = None
            self.database = self.root / 'cache.sqlite'
        else:
            self.paths = paths or resolve_storage(initialize=True)
            self.root, self.database = self.paths.root, self.paths.cache
        self._storage_check()
        self.store = Store(self.database, now=now)
        self._storage_check()
        with self.store.connection() as db:
            db.execute('''CREATE TABLE IF NOT EXISTS workflow_execution_state(
                request_key TEXT PRIMARY KEY, scope_key TEXT NOT NULL,
                fingerprint TEXT NOT NULL, state TEXT NOT NULL,
                record TEXT NOT NULL)''')

    def _storage_check(self):
        if self.paths is not None:
            resolve_storage(self.paths.root, mount=self.paths.proof['mount'],
                            image=self.paths.proof['backing_image'], probe=self.paths.probe, environ={})
        _private(self.root, directory=True)
        if self.database.exists() or self.database.is_symlink():
            _private(self.database)

    @contextlib.contextmanager
    def _lease(self, scope):
        self._storage_check()
        path = self.root / ('workflow-lease-' + scope + '.lock')
        fd = os.open(path, os.O_RDWR | os.O_CREAT | getattr(os, 'O_NOFOLLOW', 0), 0o600)
        try:
            _private(path)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise ExecutionBlocked('scope_busy', 'Wait for the current local scope owner; do not start a competing run.') from None
            yield {'scope_key': scope, 'token': uuid.uuid4().hex, 'local_only': True}
        finally:
            # Never unlink lock files: another waiter could hold the old inode.
            os.close(fd)

    def _record(self, key, scope, fp, state, record):
        self._storage_check()
        with self.store.transaction() as db:
            row = db.execute('SELECT fingerprint,state FROM workflow_execution_state WHERE request_key=?', (key,)).fetchone()
            if row and row[0] != fp:
                raise ExecutionBlocked('request_identity_conflict', 'Use the original request input or a new explicit request ID.')
            if state == 'blocked' and row and row[1] not in ('prepared', 'blocked'):
                return  # A post-unlock diagnostic must never erase newer progress or a stop.
            db.execute('INSERT OR REPLACE INTO workflow_execution_state VALUES (?,?,?,?,?)',
                       (key, scope, fp, state, canonical(record)))
        with self.store.connection() as db:
            saved = db.execute('SELECT state,record FROM workflow_execution_state WHERE request_key=?', (key,)).fetchone()
        if saved != (state, canonical(record)):
            raise StorageError('execution state readback mismatch')

    def _report(self, request_id, workflow_id, reason, next_step, *, attempted=False, state='blocked', **extra):
        return dict(schema_version=1, request_id=request_id, workflow_id=workflow_id,
                    status=state, reason=reason, next_step=next_step,
                    execution_attempted=attempted, production_storage_verified=not self.acceptance,
                    local_lease_only=True, **extra)

    def _deadline(self, deadline):
        if timestamp(self.now()) >= timestamp(deadline):
            raise ExecutionBlocked('deadline_expired', 'Start a fresh bounded request after verifying current source and owner evidence.')

    def _read(self, workflow, deadline):
        for attempt in range(workflow['failure']['max_safe_read_retries'] + 1):
            self._deadline(deadline)
            try:
                result = self.adapter.read()
                self._deadline(deadline)
                return result
            except OSError:
                if attempt == workflow['failure']['max_safe_read_retries']:
                    raise ExecutionBlocked('source_read_failed', 'Restore the exact local source and retry only its safe read.') from None
            except (ValueError, UnicodeError):
                raise ExecutionBlocked('source_validation_failed', 'Repair or resolve the exact catalog source; no output execution was attempted.') from None

    @staticmethod
    def _identity(workflow, request, binding):
        return digest({'workflow': workflow, 'binding': binding,
                       'request': {k: request[k] for k in ('request_id', 'workflow_id', 'domain', 'operation', 'execution_kind')},
                       'sources': sorted([(s['source_ref'], s['expected_revision']) for s in request['sources']])})

    def execute(self, workflow, resolve, *, deadline):
        """One bounded attempt; replay only rereads a known completed runner receipt.

        A pre-dispatch interruption resumes from prepared. Once running is saved,
        any interruption/uncertain save/readback blocks the whole local scope
        durably. Repeating a request or inventing a new ID cannot clear that hold.
        """
        workflow = validate_workflow(workflow)
        timestamp(deadline)
        request, evidence = resolve(None)
        decision = route_workflow(workflow, request, evidence, now=self.now())
        request_id = request['request_id']
        scope = digest(workflow['execution']['concurrency_key'])
        key = digest([workflow['execution']['privacy_partition'], workflow['workflow_id'], request_id])
        fp = self._identity(workflow, request, self.adapter.binding)
        report = lambda reason, next_step, **kw: self._report(request_id, workflow['workflow_id'], reason, next_step,
            owner_ref=workflow['owners']['execution_owner_ref'], concurrency_key=workflow['execution']['concurrency_key'],
            execution_state_location={'database': str(self.database), 'table': 'workflow_execution_state', 'request_key': key}, **kw)
        # The exact local lease dependency can only pass after acquiring it.
        lease_pending = (decision['status'] == 'blocked' and decision['reason'] == 'dependency_unverified'
                         and workflow['policy']['dependency_checks'][decision['dependency_index']] == LEASE_CHECK)
        if decision['status'] != 'ready' and not lease_pending:
            return report(decision['reason'], decision['next_step'], route_decision=decision)
        try:
            self._deadline(deadline)
            with self._lease(scope) as lease:
                with self.store.connection() as db:
                    held = db.execute("SELECT request_key,state FROM workflow_execution_state WHERE scope_key=? AND state IN ('running','stopped') LIMIT 1", (scope,)).fetchone()
                    prior = db.execute('SELECT fingerprint,state,record FROM workflow_execution_state WHERE request_key=?', (key,)).fetchone()
                if held:
                    return report('scope_reconciliation_required', 'Existing owner must inspect the saved runner receipt and source; never automatically retry or clear this stop.', state='stopped', held_request_key=held[0])
                if prior and prior[0] != fp:
                    return report('request_identity_conflict', 'Preserve the original request and use a new explicit ID only for new, authorized inputs.')
                request2, evidence2 = resolve(copy.deepcopy(lease))
                decision2 = route_workflow(workflow, request2, evidence2, now=self.now())
                if self._identity(workflow, request2, self.adapter.binding) != fp:
                    raise ExecutionBlocked('request_changed_after_claim', 'Resolve the changed request/source scope before a new attempt.')
                if decision2['status'] != 'ready':
                    raise ExecutionBlocked(decision2['reason'], decision2['next_step'])
                self.adapter.check_binding(workflow, decision2, acceptance=self.acceptance)
                if decision['status'] == 'ready' and decision['route_ref'] != decision2['route_ref']:
                    raise ExecutionBlocked('route_changed_after_claim', 'Verify the new exact route with its current owner before a fresh attempt.')
                content = self._read(workflow, deadline)
                revision = digest(content)
                if any(s['revision'] != revision or s['expected_revision'] != revision for s in request2['sources']):
                    raise ExecutionBlocked('source_revision_changed', 'Reread the catalog and explicitly bind the new source revision before execution.')
                partition = workflow['execution']['privacy_partition']
                source = SourceSnapshot(self.adapter.source_ref, revision, partition, True, True, True, self.now(), content, digest(content))
                controller = Controller(self.store, adapter=_FrozenSource(source),
                    routes={'version': 'workflow-catalog-v1', 'routes': [{'name': decision2['route_ref'], 'provider': 'local',
                    'capability': 0, 'estimated_cost': '0', 'privacy_partitions': [partition], 'deterministic': True, 'enabled': True}]},
                    handlers={decision2['route_ref']: _catalog_result}, freshness_seconds=min(300, workflow['sources'][0]['max_age_seconds']))
                if prior and prior[1] == 'complete':
                    saved = json.loads(prior[2])
                    try:
                        result = controller.readback(saved['runner_receipt'])
                    except Exception:
                        stopped = report('completed_readback_lost', 'Reconcile the existing runner receipt; do not regenerate or retry automatically.',
                                         state='stopped', runner_result_location=saved['runner_receipt']['result_location'])
                        self._record(key, scope, fp, 'stopped', stopped)
                        return stopped
                    self._deadline(deadline)
                    return dict(saved, reused_request=True, readback=result)
                self._record(key, scope, fp, 'prepared', report('prepared', 'Revalidate before one exact deterministic invocation.'))
                # Read-only source recheck and fresh authority/provider evidence immediately before dispatch.
                if digest(self._read(workflow, deadline)) != revision:
                    raise ExecutionBlocked('source_changed_before_dispatch', 'Resolve the changed catalog revision; no runner dispatch occurred.')
                request3, evidence3 = resolve(copy.deepcopy(lease))
                decision3 = route_workflow(workflow, request3, evidence3, now=self.now())
                if self._identity(workflow, request3, self.adapter.binding) != fp:
                    raise ExecutionBlocked('request_changed_before_dispatch', 'Resolve the changed scope before a new bounded attempt.')
                if decision3['status'] != 'ready':
                    raise ExecutionBlocked(decision3['reason'], decision3['next_step'])
                self.adapter.check_binding(workflow, decision3, acceptance=self.acceptance)
                if decision3['route_ref'] != decision2['route_ref']:
                    raise ExecutionBlocked('route_changed_before_dispatch', 'Resolve the current route before a fresh bounded attempt.')
                action_deadline = min(deadline, dt.datetime.fromisoformat(decision3['valid_until']))
                self._deadline(action_deadline)
                runner_location = {'storage': 'sqlite', 'database': str(self.database.resolve()), 'table': 'runner_requests',
                                   'request_key': digest([partition, 'workflow-' + key])}
                running = report('dispatch_started', 'Read back the existing runner result before any recovery action.',
                                 attempted=True, state='running', runner_result_location=runner_location)
                self._record(key, scope, fp, 'running', running)
                runner_request = {'request_id': 'workflow-' + key, 'privacy_partition': partition,
                    'contract_version': workflow['contract_version'], 'inputs': {}, 'components': [{'component_id': 'catalog',
                    'source_id': self.adapter.source_ref, 'source_revision': revision, 'task_type': OPERATION, 'required_capability': 0}]}
                try:
                    self._deadline(action_deadline)
                    receipt = controller.execute(runner_request)
                    self._deadline(action_deadline)
                    result = controller.readback(receipt)
                    if receipt['status'] != 'complete' or result['status'] != 'complete':
                        raise ExecutionBlocked('runner_incomplete', 'Inspect the saved runner component result before any new execution.')
                    if digest(self._read(workflow, action_deadline)) != revision:
                        raise ExecutionBlocked('source_changed_after_dispatch', 'Reconcile the saved output with the changed source; do not auto-retry.')
                    complete = report('output_readback_verified', 'Validated local catalog output is saved; this does not migrate a schedule or prove a school workflow.',
                        attempted=True, state='complete', runner_receipt=receipt, output_ref=self.adapter.output_ref,
                        source_revision=revision, route_decision=decision3, reused_request=False)
                    self._record(key, scope, fp, 'complete', complete)
                    return dict(complete, readback=result)
                except Exception as error:
                    reason = error.reason if isinstance(error, ExecutionBlocked) else 'save_or_readback_uncertain'
                    stopped = report(reason, 'Existing owner must reconcile the saved runner result and source; no automatic retry or stop clearing.',
                                     attempted=True, state='stopped', runner_result_location=runner_location)
                    self._record(key, scope, fp, 'stopped', stopped)
                    return stopped
        except ExecutionBlocked as error:
            blocked = report(error.reason, error.next_step)
            # Pre-action blocks are safe to retry after fresh evidence; never overwrite a completed record.
            if error.reason != 'scope_busy':
                with self.store.connection() as db:
                    row = db.execute('SELECT state FROM workflow_execution_state WHERE request_key=?', (key,)).fetchone()
                if not row or row[0] in ('prepared', 'blocked'):
                    self._record(key, scope, fp, 'blocked', blocked)
            return blocked

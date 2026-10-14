"""Pure evidence-gated workflow routing. No network, execution, grants or leases.

Inputs come from trusted private resolvers. A ready decision is a short-lived
proposal, never authority or proof of completed work. Re-evaluate after claiming
the existing runtime's lease and immediately before acting.
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import json
import re
from pathlib import Path

from foundation import Route, canonical, micros, select_route, timestamp, UTC
from workflow_contract import validate_workflow, _unique_json_keys

RULES_PATH = Path(__file__).resolve().parents[2] / 'skills' / 'ai-operations-router' / 'references' / 'routing-rules.json'
STAMP_KEYS = {'observed_at', 'expires_at', 'evidence_ref'}


class RoutingError(ValueError):
    """Validation messages name fields, never submitted values."""


def _object(value, keys, path):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise RoutingError(f'{path}: exact declared fields required')


def _text(value, path, nullable=False):
    if nullable and value is None:
        return
    if not isinstance(value, str) or not value.strip() or len(value) > 1024 or '\n' in value or '\r' in value:
        raise RoutingError(f'{path}: bounded single-line text required')


def _strings(value, path, *, empty=False):
    if not isinstance(value, list) or not (0 if empty else 1) <= len(value) <= 100:
        raise RoutingError(f'{path}: bounded list required')
    for item in value:
        _text(item, path)
    if len(value) != len(set(value)):
        raise RoutingError(f'{path}: duplicate entries prohibited')


def _enum(value, choices, path):
    if not isinstance(value, str) or value not in choices:
        raise RoutingError(f'{path}: supported value required')


def _date(value, path):
    _text(value, path)
    try:
        result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        timestamp(result)
    except (ValueError, TypeError):
        raise RoutingError(f'{path}: timezone-aware ISO datetime required') from None
    return result


def _stamp(value, path):
    _text(value['evidence_ref'], f'{path}.evidence_ref')
    start = _date(value['observed_at'], f'{path}.observed_at')
    end = _date(value['expires_at'], f'{path}.expires_at')
    if end <= start:
        raise RoutingError(f'{path}: expiry must follow observation')


def _fresh(value, now, max_age):
    start = _date(value['observed_at'], 'observed_at')
    end = min(_date(value['expires_at'], 'expires_at'), start + dt.timedelta(seconds=max_age))
    return start <= now < end, end


def _digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def _iso(value):
    return value.astimezone(UTC).isoformat()


def load_rules():
    return validate_rules(json.loads(RULES_PATH.read_text(), object_pairs_hook=_unique_json_keys))


def validate_rules(value):
    _object(value, {'schema_version', 'rule_version', 'execution_kinds', 'coding_executor_refs',
                    'executor_kind_limits', 'exclusive_capability_executors',
                    'exclusive_operation_executors', 'max_capability_age_seconds',
                    'max_context_age_seconds'}, 'rules')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise RoutingError('rules.schema_version: version 1 required')
    _text(value['rule_version'], 'rules.rule_version')
    _strings(value['execution_kinds'], 'rules.execution_kinds')
    if set(value['execution_kinds']) != {'deterministic', 'coding', 'browser', 'assisted'}:
        raise RoutingError('rules.execution_kinds: fixed execution kinds required')
    _strings(value['coding_executor_refs'], 'rules.coding_executor_refs')
    for key in ('executor_kind_limits', 'exclusive_capability_executors', 'exclusive_operation_executors'):
        if not isinstance(value[key], dict) or len(value[key]) > 100:
            raise RoutingError(f'rules.{key}: bounded mapping required')
        for name, choices in value[key].items():
            _text(name, f'rules.{key}')
            _strings(choices, f'rules.{key}')
            if key == 'executor_kind_limits' and not set(choices) <= set(value['execution_kinds']):
                raise RoutingError('rules.executor_kind_limits: unknown execution kind')
    for key in ('max_capability_age_seconds', 'max_context_age_seconds'):
        if type(value[key]) is not int or not 1 <= value[key] <= 86400:
            raise RoutingError(f'rules.{key}: integer within one day required')
    return copy.deepcopy(value)


def _validate_request(value, kinds):
    _object(value, {'schema_version', 'request_id', 'workflow_id', 'domain', 'operation',
                    'execution_kind', 'authorization', 'ownership', 'receipt',
                    'sources', 'dependencies'}, 'request')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise RoutingError('request.schema_version: version 1 required')
    for key in ('request_id', 'workflow_id', 'domain', 'operation'):
        _text(value[key], f'request.{key}')
    _enum(value['execution_kind'], kinds, 'request.execution_kind')
    for key, extra, states in (
            ('authorization', {'allowed_actions'}, {'authorized', 'unknown'}),
            ('ownership', {'owner_ref'}, {'clear', 'competing', 'unknown'}),
            ('receipt', set(), {'clear', 'uncertain', 'unknown'})):
        entry = value[key]
        _object(entry, STAMP_KEYS | {'state'} | extra, f'request.{key}')
        _enum(entry['state'], states, f'request.{key}.state')
        _stamp(entry, f'request.{key}')
    _strings(value['authorization']['allowed_actions'], 'request.authorization.allowed_actions', empty=True)
    _text(value['ownership']['owner_ref'], 'request.ownership.owner_ref')
    for key, fields, unique in (
            ('sources', {'source_ref', 'expected_revision', 'revision', 'coverage', 'observed_at', 'evidence_ref'}, 'source_ref'),
            ('dependencies', STAMP_KEYS | {'check', 'state'}, 'check')):
        if not isinstance(value[key], list) or len(value[key]) > 100:
            raise RoutingError(f'request.{key}: bounded list required')
        seen = set()
        for entry in value[key]:
            _object(entry, fields, f'request.{key}')
            _text(entry[unique], f'request.{key}.{unique}')
            if entry[unique] in seen:
                raise RoutingError(f'request.{key}: duplicate references prohibited')
            seen.add(entry[unique])
            if key == 'dependencies':
                _enum(entry['state'], {'passed', 'held', 'unknown'}, 'request.dependencies.state')
                _stamp(entry, 'request.dependencies')
            else:
                for name in ('expected_revision', 'revision'):
                    _text(entry[name], f'request.sources.{name}', nullable=True)
                _enum(entry['coverage'], {'complete', 'bounded', 'partial', 'unavailable'}, 'request.sources.coverage')
                _text(entry['evidence_ref'], 'request.sources.evidence_ref')
                _date(entry['observed_at'], 'request.sources.observed_at')


def _validate_evidence(value, kinds):
    _object(value, {'schema_version', 'routes'}, 'evidence')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise RoutingError('evidence.schema_version: version 1 required')
    if not isinstance(value['routes'], list) or len(value['routes']) > 100:
        raise RoutingError('evidence.routes: bounded list required')
    seen = set()
    fields = STAMP_KEYS | {'route_ref', 'provider_ref', 'executor_ref', 'resolved_executor_ref',
                          'account_refs', 'domain', 'privacy_partition', 'operation', 'execution_kind',
                          'capabilities', 'resource_rank', 'estimated_cost', 'cost_basis_ref',
                          'status', 'identity_verified'}
    for entry in value['routes']:
        _object(entry, fields, 'evidence.routes')
        for key in ('route_ref', 'provider_ref', 'executor_ref', 'resolved_executor_ref', 'domain',
                    'privacy_partition', 'operation'):
            _text(entry[key], f'evidence.routes.{key}')
        if entry['route_ref'] in seen:
            raise RoutingError('evidence.routes: duplicate route references prohibited')
        seen.add(entry['route_ref'])
        _strings(entry['account_refs'], 'evidence.routes.account_refs', empty=True)
        _strings(entry['capabilities'], 'evidence.routes.capabilities')
        _enum(entry['execution_kind'], kinds, 'evidence.routes.execution_kind')
        _enum(entry['status'], {'tested', 'unverified', 'blocked'}, 'evidence.routes.status')
        if type(entry['identity_verified']) is not bool:
            raise RoutingError('evidence.routes.identity_verified: boolean required')
        if type(entry['resource_rank']) is not int or not 0 <= entry['resource_rank'] <= 1000000:
            raise RoutingError('evidence.routes.resource_rank: nonnegative bounded integer required')
        if entry['estimated_cost'] is not None:
            if not isinstance(entry['estimated_cost'], str) or not re.fullmatch(r'(0|[1-9][0-9]*)(\.[0-9]{1,6})?', entry['estimated_cost']):
                raise RoutingError('evidence.routes.estimated_cost: fixed-point nonnegative amount required')
            micros(entry['estimated_cost'])
        _text(entry['cost_basis_ref'], 'evidence.routes.cost_basis_ref', nullable=True)
        _stamp(entry, 'evidence.routes')


def route_workflow(workflow, request, capability_evidence, *, now, rules=None):
    """Return a ready/blocked decision without acquiring state or executing work.

    The exact declared executor binding is preserved. Evidence may resolve its
    private reference to an actual runtime, but cannot change the workflow owner.
    Every required capability and dependency is required conservatively even when
    routing just one allowed operation. Supply updated evidence on every call.
    """
    timestamp(now)
    workflow = validate_workflow(workflow)
    rules = load_rules() if rules is None else validate_rules(rules)
    _validate_request(request, rules['execution_kinds'])
    _validate_evidence(capability_evidence, rules['execution_kinds'])
    base = {'schema_version': 1, 'request_id': request['request_id'],
            'workflow_id': workflow['workflow_id'], 'contract_version': workflow['contract_version'],
            'contract_sha256': _digest(workflow), 'request_sha256': _digest(request),
            'evidence_sha256': _digest(capability_evidence), 'rules_sha256': _digest(rules),
            'rule_version': rules['rule_version'], 'validated_at': _iso(now),
            'execution_attempted': False, 'owner_ref': workflow['owners']['execution_owner_ref']}

    def blocked(reason, next_step, **detail):
        return dict(base, status='blocked', reason=reason, next_step=next_step, **detail)

    if request['workflow_id'] != workflow['workflow_id'] or request['domain'] != workflow['domain']:
        return blocked('intent_mismatch', 'Resolve the exact workflow ID and domain before routing.')
    if request['operation'] not in workflow['policy']['allowed_actions']:
        return blocked('operation_not_allowed', 'Choose an operation explicitly allowed by this contract.')
    expiry = []
    for key in ('receipt', 'ownership', 'authorization'):
        entry = request[key]
        fresh, until = _fresh(entry, now, rules['max_context_age_seconds'])
        if not fresh:
            return blocked(f'{key}_evidence_stale', f'Read current {key} evidence for this exact workflow.')
        expiry.append(until)
        if key == 'receipt' and entry['state'] != 'clear':
            return blocked('receipt_reconciliation_required', 'Reconcile the existing native receipt with its current owner; do not retry or select a fallback.')
        if key == 'ownership' and (entry['state'] != 'clear' or entry['owner_ref'] != base['owner_ref']):
            return blocked('ownership_unresolved', 'Resolve the current owner and any external writer before claiming this workflow.')
        if key == 'authorization' and (entry['state'] != 'authorized' or request['operation'] not in entry['allowed_actions']):
            return blocked('authorization_missing', 'Resolve authority for this exact operation from the existing user instruction.')
    declared = {s['source_ref']: s for s in workflow['sources']}
    sources = {s['source_ref']: s for s in request['sources']}
    if set(sources) - set(declared):
        return blocked('undeclared_source', 'Remove the undeclared input and resolve the contract source references.')
    unavailable = []
    for ref, spec in declared.items():
        source = sources.get(ref)
        issue = None
        if source is None or source['coverage'] in ('unavailable', 'partial'):
            issue = 'source_unavailable_or_partial'
        elif spec['coverage'] == 'complete' and source['coverage'] != 'complete':
            issue = 'source_coverage_incomplete'
        elif source['revision'] is None or source['expected_revision'] is None:
            issue = 'source_revision_missing'
        elif source['revision'] != source['expected_revision']:
            issue = 'source_revision_changed'
        else:
            observed = _date(source['observed_at'], 'sources.observed_at')
            until = observed + dt.timedelta(seconds=spec['max_age_seconds'])
            if not observed <= now < until:
                issue = 'source_evidence_stale'
            else:
                expiry.append(until)
        if issue:
            unavailable.append({'source_ref': ref, 'reason': issue})
            if spec['required']:
                return blocked(issue, 'Obtain a fresh complete permitted source read and verify its expected revision.', source_ref=ref)
    dependencies = {v['check']: v for v in request['dependencies']}
    for index, check in enumerate(workflow['policy']['dependency_checks']):
        item = dependencies.get(check)
        if item is None or item['state'] != 'passed':
            return blocked('dependency_unverified', 'Verify the referenced contract dependency before this operation.', dependency_index=index)
        fresh, until = _fresh(item, now, rules['max_context_age_seconds'])
        if not fresh:
            return blocked('dependency_evidence_stale', 'Refresh the referenced contract dependency evidence.', dependency_index=index)
        expiry.append(until)
    execution = workflow['execution']
    required = set(execution['required_capabilities'])
    matching = []
    resolved_bindings = set()
    ineligible = []
    for route in capability_evidence['routes']:
        if not (route['executor_ref'] == execution['executor_ref']
                and set(route['account_refs']) == set(execution['account_refs'])
                and route['domain'] == workflow['domain']
                and route['privacy_partition'] == execution['privacy_partition']
                and route['operation'] == request['operation']
                and (route['execution_kind'] == request['execution_kind']
                     or request['execution_kind'] == 'assisted' and route['execution_kind'] == 'deterministic')):
            continue
        actual = route['resolved_executor_ref']
        reason = None
        fresh, until = _fresh(route, now, rules['max_capability_age_seconds'])
        if route['status'] != 'tested' or not route['identity_verified']:
            reason = 'capability_unverified'
        elif not fresh:
            reason = 'capability_evidence_stale'
        elif not required <= set(route['capabilities']):
            reason = 'capability_insufficient'
        elif actual.startswith(('existing-', 'private:')):
            reason = 'executor_binding_unresolved'
        elif route['execution_kind'] == 'coding' and actual not in rules['coding_executor_refs']:
            reason = 'coding_owner_required'
        elif actual in rules['executor_kind_limits'] and route['execution_kind'] not in rules['executor_kind_limits'][actual]:
            reason = 'executor_kind_not_allowed'
        elif any(cap in required and actual not in owners for cap, owners in rules['exclusive_capability_executors'].items()):
            reason = 'exclusive_writer_required'
        elif request['operation'] in rules['exclusive_operation_executors'] and actual not in rules['exclusive_operation_executors'][request['operation']]:
            reason = 'exclusive_writer_required'
        if reason is None:
            resolved_bindings.add(actual)
            if route['estimated_cost'] is None or route['cost_basis_ref'] is None:
                reason = 'cost_input_missing'
        if reason:
            ineligible.append({'route_ref': route['route_ref'], 'reason': reason})
        else:
            matching.append((route, until))
    if len(resolved_bindings) > 1:
        return blocked('executor_binding_conflict', 'Resolve the single current executor binding before choosing a tool.')
    if not matching:
        reason = ineligible[0]['reason'] if ineligible and len({x['reason'] for x in ineligible}) == 1 else 'no_verified_route'
        return blocked(reason, 'Keep the current owner; resolve fresh exact executor, account, capability and cost evidence for this operation.', ineligible_routes=ineligible)
    choices = [Route(r['route_ref'], r['provider_ref'], r['resource_rank'], r['estimated_cost'],
                     frozenset([r['privacy_partition']]), r['execution_kind'] == 'deterministic', True)
               for r, _ in matching]
    selected = select_route(choices, required_capability=0, partition=execution['privacy_partition'])
    route, until = next((r, end) for r, end in matching if r['route_ref'] == selected.name)
    expiry.append(until)
    return dict(base, status='ready', reason='verified_route', route_ref=route['route_ref'],
                executor_ref=execution['executor_ref'], resolved_executor_ref=route['resolved_executor_ref'],
                provider_ref=route['provider_ref'], account_refs=execution['account_refs'],
                operation=request['operation'], execution_kind=route['execution_kind'],
                privacy_partition=execution['privacy_partition'], required_capabilities=sorted(required),
                concurrency_key=execution['concurrency_key'], valid_until=_iso(min(expiry)),
                estimated_cost=route['estimated_cost'], cost_basis_ref=route['cost_basis_ref'],
                unavailable_sources=unavailable, capability_evidence_ref=route['evidence_ref'],
                next_step='Verify the existing runtime lease, revalidate this evidence, then invoke the exact authorized adapter; require native output readback.')


def resolve_intent(workflows, intent):
    """Resolve exact domain/operation/ID only. Never guess from request keywords."""
    _object(intent, {'workflow_id', 'domain', 'operation'}, 'intent')
    for key in intent:
        _text(intent[key], f'intent.{key}', nullable=True)
    catalog = [validate_workflow(w) for w in workflows]
    ids = [w['workflow_id'] for w in catalog]
    if len(set(ids)) != len(ids) or len(catalog) > 100:
        raise RoutingError('catalog: bounded unique workflow definitions required')
    candidates = [w for w in catalog if (intent['workflow_id'] is None or w['workflow_id'] == intent['workflow_id'])
                  and (intent['domain'] is None or w['domain'] == intent['domain'])
                  and (intent['operation'] is None or intent['operation'] in w['policy']['allowed_actions'])]
    catalog_sha = _digest(sorted(catalog, key=lambda w: w['workflow_id']))
    if len(candidates) == 1 and intent['operation'] is not None and intent['domain'] is not None:
        return {'status': 'resolved', 'workflow_id': candidates[0]['workflow_id'], 'domain': intent['domain'],
                'operation': intent['operation'], 'catalog_sha256': catalog_sha, 'execution_attempted': False}
    return {'status': 'question', 'question_id': _digest({'intent': intent, 'catalog': catalog_sha}),
            'intent': copy.deepcopy(intent), 'catalog_sha256': catalog_sha,
            'candidates': [w['workflow_id'] for w in candidates], 'execution_attempted': False,
            'reason': 'ambiguous_or_incomplete_intent' if candidates else 'unknown_intent',
            'next_step': '1. Identify the exact workflow, domain and allowed operation from the canonical catalog.'}


def resume_intent(workflows, pending, answer):
    """An answer resolves intent only; all routing evidence must then be reread."""
    _object(pending, {'status', 'question_id', 'intent', 'catalog_sha256', 'candidates',
                      'execution_attempted', 'reason', 'next_step'}, 'pending')
    original = resolve_intent(workflows, pending['intent'])
    if original != pending or pending['status'] != 'question':
        raise RoutingError('pending: question changed or catalog must be reread')
    if answer is None:
        return copy.deepcopy(pending)
    _object(answer, {'workflow_id', 'domain', 'operation'}, 'answer')
    for key, value in answer.items():
        _text(value, f'answer.{key}')
        if pending['intent'][key] is not None and pending['intent'][key] != value:
            raise RoutingError('answer: existing scope cannot change during continuation')
    return resolve_intent(workflows, answer)


def build_handoff(workflow, *, decision, canonical_source_ref, completed, remaining,
                  output_refs, next_owner_ref, next_step):
    """Build a reference-only handoff, not a message, execution or ownership transfer.

    Completed entries are {action, receipt_ref}; only verified work belongs here.
    Existing uncertain receipts must be reconciled by the existing owner.
    """
    workflow = validate_workflow(workflow)
    if not isinstance(decision, dict) or decision.get('status') not in ('ready', 'blocked'):
        raise RoutingError('decision: routing proposal required')
    if decision.get('execution_attempted') is not False:
        raise RoutingError('decision: proposal must not claim execution')
    _text(decision.get('reason'), 'decision.reason')
    if decision.get('workflow_id') != workflow['workflow_id'] or decision.get('contract_sha256') != _digest(workflow):
        raise RoutingError('decision: exact workflow fingerprint required')
    for key, value in (('canonical_source_ref', canonical_source_ref), ('next_owner_ref', next_owner_ref), ('next_step', next_step)):
        _text(value, key)
    _strings(remaining, 'remaining', empty=True)
    _strings(output_refs, 'output_refs', empty=True)
    if not isinstance(completed, list) or len(completed) > 100:
        raise RoutingError('completed: bounded list required')
    actions = []
    for item in completed:
        _object(item, {'action', 'receipt_ref'}, 'completed')
        _text(item['receipt_ref'], 'completed.receipt_ref')
        if item['action'] not in workflow['policy']['allowed_actions']:
            raise RoutingError('completed.action: declared action required')
        actions.append(item['action'])
    if len(set(actions)) != len(actions) or set(actions) & set(remaining):
        raise RoutingError('handoff: completed and remaining actions must be distinct')
    if not set(remaining) <= set(workflow['policy']['allowed_actions']):
        raise RoutingError('remaining: declared actions required')
    if next_owner_ref != workflow['owners']['execution_owner_ref']:
        raise RoutingError('next_owner_ref: preserve current owner until an authorized contract cutover')
    if completed and not output_refs:
        raise RoutingError('output_refs: completed work needs a saved output reference')
    return {'schema_version': 1, 'workflow_id': workflow['workflow_id'],
            'contract_version': workflow['contract_version'], 'contract_sha256': _digest(workflow),
            'canonical_source_ref': canonical_source_ref, 'completed': copy.deepcopy(completed),
            'remaining': list(remaining), 'output_refs': list(output_refs), 'next_owner_ref': next_owner_ref,
            'next_step': next_step, 'route_status': decision['status'], 'route_reason': decision['reason'],
            'execution_attempted': False, 'ownership_transferred': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workflow', type=Path)
    parser.add_argument('request', type=Path)
    parser.add_argument('evidence', type=Path)
    parser.add_argument('--now', help='Explicit aware ISO clock for reproducible offline tests')
    args = parser.parse_args(argv)
    try:
        values = [json.loads(p.read_text(), object_pairs_hook=_unique_json_keys)
                  for p in (args.workflow, args.request, args.evidence)]
        now = _date(args.now, 'now') if args.now else dt.datetime.now(UTC)
        decision = route_workflow(*values, now=now)
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        detail = str(error) if isinstance(error, RoutingError) else type(error).__name__
        parser.exit(1, f'Routing input invalid: {detail}\n')
    print(json.dumps(decision, sort_keys=True, indent=2))
    return 0 if decision['status'] == 'ready' else 2


if __name__ == '__main__':
    raise SystemExit(main())

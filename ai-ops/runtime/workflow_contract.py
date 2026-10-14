"""Validate sanitized workflow definitions; never dispatch work or resolve access.

The definition is a portable requirements catalog, not the runtime execution
request or a grant. This standard-library validator implements the accompanying
v1 schema plus cross-field uniqueness and action-conflict checks.
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path


class ContractError(ValueError):
    """Messages contain field paths, never submitted values."""


def _object(value, keys, path):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise ContractError(f"{path}: exact declared fields required")


def _string(value, path, *, slug=False):
    limit = 128 if slug else 256
    if (not isinstance(value, str) or not value.strip() or len(value) > limit
            or '\r' in value or '\n' in value):
        raise ContractError(f"{path}: bounded nonempty single-line string required")
    if slug and not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', value):
        raise ContractError(f"{path}: lowercase hyphen-separated identifier required")


def _integer(value, path, minimum, maximum):
    if type(value) is not int or not minimum <= value <= maximum:
        raise ContractError(f"{path}: integer in permitted bounds required")


def _boolean(value, path):
    if type(value) is not bool:
        raise ContractError(f"{path}: boolean required")


def _array(value, path, *, minimum=0):
    if not isinstance(value, list) or not minimum <= len(value) <= 100:
        raise ContractError(f"{path}: bounded array required")


def _strings(value, path, *, minimum=0, slug=False):
    _array(value, path, minimum=minimum)
    for index, item in enumerate(value):
        _string(item, f"{path}[{index}]", slug=slug)
    if len(set(value)) != len(value):
        raise ContractError(f"{path}: duplicate entries prohibited")


def validate_workflow(value):
    """Return a separate validated definition. No files, network or state writes.

    Callers must independently resolve authority, account and capability evidence,
    acquire the concurrency lease, freeze verified source versions, and use the
    existing execution-request/runtime and receipt contracts before acting.
    """
    _object(value, ('schema_version', 'workflow_id', 'contract_version', 'title',
                   'domain', 'owners', 'execution', 'trigger', 'sources', 'outputs',
                   'policy', 'success_checks', 'failure', 'provenance'), '$')
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        raise ContractError('schema_version: supported version is 1')
    for key in ('workflow_id', 'domain'):
        _string(value[key], key, slug=True)
    for key in ('contract_version', 'title'):
        _string(value[key], key)
    owners = value['owners']
    _object(owners, ('execution_owner_ref', 'maintenance_owner_ref'), 'owners')
    for key in owners:
        _string(owners[key], f'owners.{key}')
    execution = value['execution']
    _object(execution, ('executor_ref', 'account_refs', 'required_capabilities',
                        'privacy_partition', 'concurrency_key'), 'execution')
    for key in ('executor_ref', 'concurrency_key'):
        _string(execution[key], f'execution.{key}')
    _string(execution['privacy_partition'], 'execution.privacy_partition', slug=True)
    _strings(execution['account_refs'], 'execution.account_refs')
    _strings(execution['required_capabilities'], 'execution.required_capabilities',
             minimum=1, slug=True)
    trigger = value['trigger']
    if not isinstance(trigger, dict) or trigger.get('kind') not in ('on_demand', 'existing_schedule'):
        raise ContractError('trigger.kind: supported kind required')
    if trigger['kind'] == 'existing_schedule':
        _object(trigger, ('kind', 'schedule_ref'), 'trigger')
        _string(trigger['schedule_ref'], 'trigger.schedule_ref')
    else:
        _object(trigger, ('kind',), 'trigger')
    for key, ref_key, fields in (
            ('sources', 'source_ref', ('source_ref', 'required', 'coverage', 'max_age_seconds')),
            ('outputs', 'output_ref', ('output_ref', 'kind', 'verification'))):
        entries = value[key]
        _array(entries, key, minimum=1)
        refs = set()
        for index, entry in enumerate(entries):
            path = f'{key}[{index}]'
            _object(entry, fields, path)
            _string(entry[ref_key], f'{path}.{ref_key}')
            if entry[ref_key] in refs:
                raise ContractError(f'{key}: duplicate reference prohibited')
            refs.add(entry[ref_key])
            if key == 'sources':
                _boolean(entry['required'], f'{path}.required')
                if entry['coverage'] not in ('complete', 'bounded'):
                    raise ContractError(f'{path}.coverage: supported coverage required')
                _integer(entry['max_age_seconds'], f'{path}.max_age_seconds', 1, 31536000)
            elif (entry['kind'] not in ('artifact', 'report', 'receipt')
                  or entry['verification'] != 'content_and_destination_readback'):
                raise ContractError(f'{path}: supported kind and readback requirement required')
    policy = value['policy']
    _object(policy, ('allowed_actions', 'prohibited_actions', 'dependency_checks',
                     'uncertain_write_policy'), 'policy')
    for key in ('allowed_actions', 'prohibited_actions'):
        _strings(policy[key], f'policy.{key}', minimum=1, slug=True)
    if set(policy['allowed_actions']) & set(policy['prohibited_actions']):
        raise ContractError('policy: allowed and prohibited actions overlap')
    _strings(policy['dependency_checks'], 'policy.dependency_checks', minimum=1)
    if policy['uncertain_write_policy'] != 'stop_and_reconcile':
        raise ContractError('policy.uncertain_write_policy: stop_and_reconcile required')
    _strings(value['success_checks'], 'success_checks', minimum=1)
    failure = value['failure']
    _object(failure, ('max_safe_read_retries', 'continue_independent_work', 'report_next_step'), 'failure')
    _integer(failure['max_safe_read_retries'], 'failure.max_safe_read_retries', 0, 3)
    _boolean(failure['continue_independent_work'], 'failure.continue_independent_work')
    if failure['report_next_step'] is not True:
        raise ContractError('failure.report_next_step: true required')
    _object(value['provenance'], ('contract_refs',), 'provenance')
    _strings(value['provenance']['contract_refs'], 'provenance.contract_refs', minimum=1)
    return copy.deepcopy(value)


def _unique_json_keys(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ContractError('JSON: duplicate object fields prohibited')
        value[key] = item
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', type=Path)
    args = parser.parse_args(argv)
    for path in args.paths:
        try:
            value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=_unique_json_keys)
            validate_workflow(value)
        except (OSError, UnicodeError, ValueError) as error:
            # Exception type only for external errors: no private path or body.
            detail = str(error) if isinstance(error, ContractError) else type(error).__name__
            parser.exit(1, f'Workflow definition invalid: {detail}\n')
    print(f'Validated {len(args.paths)} workflow definition(s); execution not attempted.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

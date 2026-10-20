"""Read-only scheduler conversion checks. Never dispatch or mutate a schedule.

The private candidate is an artifact, not a second scheduler registry. Human
semantic coverage review and native trial receipts remain required separately.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from workflow_contract import validate_workflow


class CutoverError(ValueError):
    """Safe errors identify failed checks without echoing private contents."""


def digest(blob):
    return hashlib.sha256(blob).hexdigest()


def json_digest(value):
    return digest(json.dumps(value, sort_keys=True, separators=(',', ':')).encode())


def pin_file(root, relative):
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if not relative or target == root or root not in target.parents:
        raise CutoverError('artifact path must stay in checkout')
    return {'path': relative, 'sha256': digest(target.read_bytes())}


def verify_pins(root, pins):
    if not pins or len({p['path'] for p in pins}) != len(pins):
        raise CutoverError('unique artifact pins required')
    for pin in pins:
        if pin_file(root, pin['path']) != pin:
            raise CutoverError('artifact hash changed')


def verify_coverage(prompt, coverage, root):
    """Require one reviewed mapping for every exact source paragraph.

    This checks that no reviewed block disappeared or changed. It cannot decide
    semantic equivalence: the reviewer must actually compare the linked rules.
    """
    blocks = prompt.split('\n\n')
    if len(coverage) != len(blocks):
        raise CutoverError('source coverage incomplete')
    for number, (block, item) in enumerate(zip(blocks, coverage), 1):
        if item.get('paragraph') != number or item.get('source_sha256') != digest(block.encode()):
            raise CutoverError('source coverage identity changed')
        if item.get('disposition') not in ('covered', 'superseded') or not item.get('review_note'):
            raise CutoverError('unreviewed source policy')
        if not item.get('targets'):
            raise CutoverError('source policy has no target')
        for target in item['targets']:
            path, _, heading = target.partition('#')
            pin_file(root, path)
            if heading and heading not in (Path(root) / path).read_text():
                raise CutoverError('coverage target missing')


def verify_bundle(candidate, checkout, workflow_id, contract_sha256):
    """Validate one exact invocation, returning paths to read; no execution."""
    if candidate.get('schema_version') != 1 or candidate.get('operation') != 'same-owner-prompt-conversion':
        raise CutoverError('supported local conversion required')
    if candidate['workflow_id'] != workflow_id or candidate['contract']['sha256'] != contract_sha256:
        raise CutoverError('invocation identity mismatch')
    pins = [candidate['contract']] + candidate['procedures']
    verify_pins(checkout, pins)
    pinned_paths = {pin['path'] for pin in pins}
    definition = validate_workflow(json.loads((Path(checkout) / candidate['contract']['path']).read_text()))
    if (definition['workflow_id'] != workflow_id or
            definition['contract_version'] != candidate['contract_version'] or
            definition['trigger'].get('schedule_ref') != candidate['schedule_ref']):
        raise CutoverError('contract identity mismatch')
    registry = json.loads(Path(candidate['registry_path']).read_text())
    records = [r for r in registry['records'] if r['schedule_ref'] == candidate['schedule_ref']]
    if len(records) != 1 or records[0]['workflow_id'] != workflow_id:
        raise CutoverError('single canonical registry binding required')
    record = records[0]
    if record['system'] != 'Local Codex' or record['enabled_state']['native_status'] != 'ACTIVE':
        raise CutoverError('current local owner not active')
    if json_digest(record['owner']) != candidate['owner_sha256']:
        raise CutoverError('owner changed')
    expected_source = record['source_contract_ref']
    if (expected_source['path'] != candidate['original']['path'] or
            expected_source['definition_sha256'] not in
            (candidate['original']['sha256'], candidate.get('accepted_definition_sha256'))):
        raise CutoverError('registry source changed; reconcile existing record')
    if digest(Path(expected_source['path']).read_bytes()) != expected_source['definition_sha256']:
        raise CutoverError('native definition changed since registry readback')
    backup = Path(candidate['original']['backup_path']).read_bytes()
    if digest(backup) != candidate['original']['sha256']:
        raise CutoverError('rollback source changed')
    policy = Path(candidate['policy_backup_path']).read_text()
    if digest(policy.encode()) != candidate['original']['prompt_sha256']:
        raise CutoverError('preserved policy changed')
    for item in candidate['coverage']:
        for target in item.get('targets', []):
            if target.partition('#')[0] not in pinned_paths:
                raise CutoverError('coverage target is not pinned')
    verify_coverage(policy, candidate['coverage'], checkout)
    bindings = Path(candidate['bindings']['path']).read_bytes()
    if digest(bindings) != candidate['bindings']['sha256']:
        raise CutoverError('private binding source changed')
    return {'workflow_id': workflow_id, 'contract_version': definition['contract_version'],
            'contract_path': str(Path(checkout) / candidate['contract']['path']),
            'procedure_paths': [str(Path(checkout) / p['path']) for p in candidate['procedures']],
            'registry_path': candidate['registry_path'], 'bindings_path': candidate['bindings']['path'],
            'validation_only': True, 'execution_authorized': False}


def verify_prompt_only_change(before, after):
    """Check the whole definition, allowing only prompt and backend timestamp."""
    if before.get('prompt') == after.get('prompt'):
        raise CutoverError('prompt did not change')
    excluded = {'prompt', 'updated_at'}
    if {k: v for k, v in before.items() if k not in excluded} != {
            k: v for k, v in after.items() if k not in excluded}:
        raise CutoverError('non-prompt schedule field changed')


def transition(action, *, old_state, new_state, checks, uncertain_write=False):
    """Pure review gate; caller supplies independently read native evidence.

    No truthy string may count as evidence. UNKNOWN readback never means paused.
    There is intentionally no scheduler API, persistence or automatic retry here.
    """
    states = {'ACTIVE', 'PAUSED', 'ABSENT', 'UNKNOWN'}
    if old_state not in states or new_state not in states:
        raise CutoverError('invalid owner state')
    if uncertain_write:
        raise CutoverError('reconcile original uncertain write; never resend')
    if 'UNKNOWN' in (old_state, new_state):
        raise CutoverError('native state readback required before further mutation')
    required = {'published', 'exact_artifacts', 'source_unchanged', 'coverage_reviewed',
                'current_bindings', 'current_authority', 'accepted_trial', 'no_running_job'}
    if action != 'rollback':
        if any(checks.get(key) is not True for key in required):
            raise CutoverError('conversion acceptance evidence incomplete')
    if action == 'update_prompt' and old_state == 'ACTIVE' and new_state == 'ABSENT':
        return {'old': 'ACTIVE', 'new': 'ABSENT', 'next': 'read-back-entire-same-definition'}
    if action == 'disable_old' and old_state == 'ACTIVE' and new_state == 'PAUSED':
        return {'old': 'PAUSED', 'new': 'PAUSED', 'next': 'native-old-paused-readback'}
    if action == 'enable_new' and old_state == 'PAUSED' and new_state == 'PAUSED':
        if checks.get('old_disabled_readback') is not True:
            raise CutoverError('old disabled readback required')
        return {'old': 'PAUSED', 'new': 'ACTIVE', 'next': 'native-both-states-and-output-readback'}
    if action == 'rollback' and old_state in {'PAUSED', 'ACTIVE'} and new_state in {'PAUSED', 'ABSENT'}:
        # Pausing a schedule does not establish that an earlier invocation has
        # stopped. Current authority and idle/fenced native writers are still
        # required before restoring the original owner.
        if any(checks.get(key) is not True for key in ('current_authority', 'no_running_job')):
            raise CutoverError('current rollback authority and idle writer evidence required')
        if checks.get('rollback_source_verified') is not True or checks.get('new_disabled_readback') is not True:
            raise CutoverError('verified rollback and replacement-disabled readback required')
        return {'old': 'ACTIVE', 'new': new_state, 'next': 'native-original-state-readback'}
    raise CutoverError('transition risks duplicate owners or requires reconciliation')


def invocation(candidate, candidate_path):
    """Render a short exact local invocation; no cloud-local-path fallback."""
    import shlex
    root = candidate['canonical_checkout']
    command = ['python3', str(Path(root) / 'ai-ops/runtime/workflow_cutover.py'),
               'verify', '--candidate', str(candidate_path), '--checkout', root,
               '--workflow-id', candidate['workflow_id'],
               '--contract-sha256', candidate['contract']['sha256']]
    binding_rule = (
        "Resolve the current spreadsheet, verified report/source records and Claude catch-up ownership from private bindings. Use prompts/school-spreadsheet-feedback.md; route saved-report packet assembly independently of generation, Hub, email and IC availability. "
        if candidate['workflow_id'] == 'school-feedback-print-ready' else ''
    )
    return (
        f"Run the existing {candidate['workflow_id']} workflow, contract {candidate['contract_version']}, "
        "in this same chat on the current home Mac. Its existing America/New_York cadence, owner and notification preference remain in force. "
        f"Use the accessible canonical checkout {root}. First run this read-only identity check:\n\n"
        + shlex.join(command) + "\n\n"
        "Then read its returned contract, procedures and private bindings; resolve current authority, native source revisions, capability and shared ownership from the single referenced private registry and existing records. "
        + binding_rule +
        "The check itself grants no write. Follow the versioned procedure through actual native output readback. "
        "Resume exact pending questions immediately when Katherine answers after rereading sources; keep independent work moving. "
        "Preserve existing grade/email ownership and uncertain-write holds; never resend or retry an uncertain save. "
        "If the checkout, pin, binding or executor is unavailable, hold only dependent work and report the exact next safe check; do not substitute a cloud-only local path, create a job or change schedules."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['verify'])
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--checkout', required=True)
    parser.add_argument('--workflow-id', required=True)
    parser.add_argument('--contract-sha256', required=True)
    args = parser.parse_args()
    try:
        candidate = json.loads(Path(args.candidate).read_text())
        checkout = Path(args.checkout).resolve()
        if checkout != Path(candidate['canonical_checkout']).resolve():
            raise CutoverError('canonical checkout mismatch')
        remote = subprocess.check_output(['git', '-C', str(checkout), 'remote', 'get-url', 'origin'], text=True).strip()
        if remote != candidate['canonical_remote']:
            raise CutoverError('canonical repository mismatch')
        result = verify_bundle(candidate, checkout, args.workflow_id, args.contract_sha256)
    except (CutoverError, ValueError, KeyError, OSError, subprocess.SubprocessError) as error:
        # Never echo arbitrary parser exceptions or values from private files.
        parser.exit(2, (str(error) if isinstance(error, CutoverError) else 'candidate verification failed') + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

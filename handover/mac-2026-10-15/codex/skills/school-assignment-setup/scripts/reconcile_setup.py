#!/usr/bin/env python3
"""Reconcile current setup evidence; no network access or remote mutations."""
import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

IDENTITY = ('course_id', 'lesson_id', 'marking_period', 'source_id', 'form_id',
            'upload_folder_id', 'schoology_folder_id', 'schoology_page_id', 'class_option')
GATES = ('agenda_identity', 'source_content', 'form_owner', 'published_accepting',
         'student_responder', 'required_identity_fields', 'upload_configuration',
         'folder_owner', 'hub_reader', 'schoology_route', 'schoology_placement')
FORM_PAGE_GATES = ('form_owner', 'published_accepting', 'student_responder',
                   'required_identity_fields', 'upload_configuration', 'folder_owner',
                   'schoology_route')
MAX_CLOCK_SKEW = timedelta(seconds=120)


def timestamp(value):
    try:
        result = datetime.fromisoformat(str(value).replace('Z', '+00:00'))
        return result if result.tzinfo else None
    except (ValueError, TypeError):
        return None


def evidenced(check):
    return isinstance(check, dict) and check.get('ok') is True and bool(check.get('evidence'))


def reconcile(data, *, now=None):
    now = datetime.now(timezone.utc) if now is None else timestamp(now)
    if now is None:
        raise ValueError('now must be timezone-aware')
    latest_allowed = now + MAX_CLOCK_SKEW
    started = timestamp(data.get('run_started_at'))
    global_issues = []
    scope = data.get('scope', {})
    scope_time = timestamp(scope.get('checked_at'))
    if not data.get('run_id') or not started:
        global_issues.append('Missing run identity or timezone-aware run_started_at')
    if started and started > latest_allowed:
        global_issues.append('run_started_at is in the future beyond allowed clock skew')
    if not (scope.get('complete') is True and scope.get('evidence') and
            started and scope_time and started <= scope_time <= latest_allowed):
        global_issues.append('Selected class/marking-period scope is not freshly evidenced complete')
    expected = data.get('expected', [])
    if not expected and not (scope.get('no_assignments') is True and scope.get('evidence')):
        global_issues.append('Expected assignment set is empty without a verified no-assignment scope')
    keys = [r.get('key') for r in expected]
    if None in keys or len(set(keys)) != len(keys):
        global_issues.append('Missing or duplicate expected assignment keys')

    by_key = defaultdict(list)
    for receipt in data.get('receipts', []):
        by_key[receipt.get('key')].append(receipt)
    shared = defaultdict(list)
    destinations = defaultdict(list)
    for row in expected:
        if row.get('status', 'assigned') == 'assigned' and row.get('form_id'):
            shared[row['form_id']].append(row)
            if row.get('upload_folder_id'):
                destinations[row['upload_folder_id']].append(row)
    unapproved_shared = set()
    for uses in shared.values():
        if len({r.get('lesson_id') for r in uses}) > 1:
            groups = {r.get('shared_form_group') for r in uses}
            if len(groups) != 1 or not next(iter(groups)) or not all(r.get('shared_form_evidence') for r in uses):
                unapproved_shared.update(r['key'] for r in uses)
    unapproved_destinations = set()
    for uses in destinations.values():
        if len({r['form_id'] for r in uses}) > 1:
            groups = {r.get('shared_destination_group') for r in uses}
            if len(groups) != 1 or not next(iter(groups)) or not all(r.get('shared_destination_evidence') for r in uses):
                unapproved_destinations.update(r['key'] for r in uses)

    results = []
    for row in expected:
        key = row.get('key')
        status = row.get('status', 'assigned')
        if status == 'not_applicable':
            if row.get('exception_reason') and row.get('exception_evidence'):
                results.append({'key': key, 'status': 'not_applicable', 'reason': row['exception_reason']})
                continue
            results.append({'key': key, 'status': 'needs_work', 'issues': ['Unproven exclusion']})
            continue
        issues = []
        if status != 'assigned':
            issues.append('Unknown status; future assigned lessons remain assigned')
        candidates = by_key.get(key, [])
        current = [r for r in candidates if r.get('run_id') == data.get('run_id')]
        candidates = current or candidates
        if any(timestamp(r.get('observed_at')) is None for r in candidates):
            issues.append('Malformed receipt timestamp prevents reliable latest-state selection')
        receipt = max(enumerate(candidates), key=lambda pair: (
                      timestamp(pair[1].get('observed_at')) or datetime.min.replace(tzinfo=timezone.utc),
                      pair[0]), default=(-1, {}))[1]
        observed = receipt.get('observed', {})
        observed_at = timestamp(receipt.get('observed_at'))
        agenda_at = timestamp(row.get('agenda_checked_at'))
        fresh = bool(receipt.get('run_id') == data.get('run_id') and started and agenda_at
                     and observed_at and started <= agenda_at <= observed_at <= latest_allowed
                     and row.get('agenda_fingerprint')
                     and receipt.get('agenda_fingerprint') == row['agenda_fingerprint'])
        if not fresh:
            issues.append('Missing/stale/future receipt or changed Agenda fingerprint')
        identity_ok = True
        for field in IDENTITY:
            if not row.get(field) or observed.get(field) != row[field]:
                issues.append(f'Unverified or mismatched {field}')
                identity_ok = False
        if key in unapproved_shared:
            issues.append('Shared Form spans different lessons without evidenced approved grouping')
        if key in unapproved_destinations:
            issues.append('Different Forms share an upload folder without evidenced approved destination grouping')
        gates = receipt.get('gates', {})
        for gate in GATES:
            if not evidenced(gates.get(gate)):
                reason = gates.get(gate, {}).get('reason', 'missing successful evidence')
                issues.append(f'{gate}: {reason}')
        if row.get('student_material_requirement') == 'digital':
            if not row.get('student_material_id') or observed.get('student_material_id') != row['student_material_id']:
                issues.append('Missing/wrong intended student material ID')
            if not evidenced(gates.get('student_material')):
                issues.append('Student lesson link/access/content not verified')
        elif row.get('student_material_requirement') == 'teacher_confirmed_no_digital':
            if not row.get('student_material_exception_evidence'):
                issues.append('No evidence for omitting a student lesson link')
        else:
            issues.append('Student material requirement unresolved; Form-only is not full setup')
        form_page_only = bool(issues and fresh and identity_ok and key not in unapproved_shared
                              and key not in unapproved_destinations
                              and all(evidenced(gates.get(g)) for g in FORM_PAGE_GATES))
        results.append({'key': key, 'status': 'ready' if not issues else 'needs_work',
                        'form_page_only': form_page_only, 'issues': issues})
    counts = {s: sum(r['status'] == s for r in results) for s in ('ready', 'needs_work', 'not_applicable')}
    counts['form_page_only'] = sum(r.get('form_page_only', False) for r in results)
    return {'run_id': data.get('run_id'), 'all_ready': not global_issues and counts['needs_work'] == 0,
            'counts': counts, 'global_issues': global_issues, 'assignments': results,
            'note': 'Evidence reconciliation only; this helper does not inspect or change live services.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--output', type=Path, help='Optional private JSON result path')
    args = parser.parse_args()
    try:
        result = reconcile(json.loads(args.manifest.read_text()))
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(f'Invalid setup manifest: {exc}', file=sys.stderr)
        return 2
    encoded = json.dumps(result, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(encoded, encoding='utf-8')
        args.output.chmod(0o600)
    else:
        print(encoded, end='')
    return 0 if result['all_ready'] else 1


if __name__ == '__main__':
    sys.exit(main())

"""Compare two bounded school connector reads; never dispatch school work.

Input captures and frozen bindings are private, trusted operator evidence. This
helper cannot authenticate them, test a destination account, certify a report
date, or complete the governing workflow. It writes only a new local summary.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re

from workflow_contract import validate_workflow, _unique_json_keys

REPOSITORY = Path(__file__).resolve().parents[2]


class TrialError(ValueError):
    """Errors name fields only, never private input values."""


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     ensure_ascii=False).encode()).hexdigest()


def _time(value):
    try:
        result = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.tzinfo is None or result.utcoffset() is None:
            raise ValueError()
        return result
    except (AttributeError, TypeError, ValueError):
        raise TrialError('observed_at: aware ISO datetime required') from None


def _bounded_rectangle(value):
    match = re.fullmatch(r'([A-Z]{1,3})([1-9][0-9]*):([A-Z]{1,3})([1-9][0-9]*)', value)
    if not match:
        return False
    left, top, right, bottom = match.groups()
    def column(label):
        number = 0
        for char in label:
            number = number * 26 + ord(char) - ord('A') + 1
        return number
    width = column(right) - column(left) + 1
    height = int(bottom) - int(top) + 1
    return width > 0 and 0 < height <= 50 and width * height <= 200


def compare_reads(workflow, source_ref, binding, before, after, *, now):
    """Return a body-free comparison, not router capability/receipt evidence.

    Captures wrap the actual get_spreadsheet_range request, structured response,
    source metadata response, and observation time. No network is performed.
    """
    definition = validate_workflow(workflow)
    sources = {s['source_ref']: s for s in definition['sources']}
    if definition['domain'] != 'school' or source_ref not in sources:
        raise TrialError('source_ref: existing school definition source required')
    if not isinstance(binding, dict) or set(binding) != {'source_id', 'link_id', 'range'}:
        raise TrialError('binding: exact frozen source_id, link_id and range required')
    if any(not isinstance(v, str) or not v.strip() for v in binding.values()):
        raise TrialError('binding: nonempty values required')
    now = _time(now.isoformat())
    maximum_age = min(300, sources[source_ref]['max_age_seconds'])
    problems, hashes, times = [], [], []
    for capture in (before, after):
        if not isinstance(capture, dict) or set(capture) != {
                'tool', 'request', 'source_metadata', 'response', 'observed_at'}:
            raise TrialError('capture: exact fields required')
        if capture['tool'] != 'google_drive.get_spreadsheet_range':
            raise TrialError('capture.tool: supported bounded read required')
        stamp = _time(capture['observed_at'])
        times.append(stamp)
        if not 0 <= (now - stamp).total_seconds() <= maximum_age:
            problems.append('read_observation_stale_or_future')
        request = capture['request']
        metadata = capture['source_metadata']
        response = capture['response']
        if not all(isinstance(x, dict) for x in (request, metadata, response)):
            raise TrialError('capture: request, metadata and response objects required')
        if request.get('link_id') != binding['link_id']:
            problems.append('account_link_mismatch')
        if (request.get('spreadsheet_id') != binding['source_id'] or
                metadata.get('id') != binding['source_id'] or
                metadata.get('mime_type') != 'application/vnd.google-apps.spreadsheet'):
            problems.append('source_identity_mismatch')
        if response.get('isError') or response.get('error'):
            problems.append('provider_error')
        data = response.get('structuredContent', {})
        if not isinstance(data, dict):
            raise TrialError('response.structuredContent: object required')
        # Compare the complete native returned range to the frozen range. The
        # tool request must independently identify its exact tab and rectangle.
        sheet = request.get('sheet_name')
        rectangle = request.get('range')
        if not isinstance(sheet, str) or not isinstance(rectangle, str):
            raise TrialError('request: exact sheet_name and range required')
        if not _bounded_rectangle(rectangle):
            problems.append('read_scope_exceeds_trial_bound')
        if f'{sheet}!{rectangle}' != binding['range'] or data.get('range') != binding['range']:
            problems.append('range_mismatch')
        values = data.get('values')
        if (data.get('majorDimension') != 'ROWS' or not isinstance(values, list)
                or not values or any(not isinstance(row, list) for row in values)
                or not any(cell not in ('', None) for row in values
                           if isinstance(row, list) for cell in row)):
            problems.append('empty_or_incomplete_read')
        if isinstance(values, list) and (len(values) > 50 or
                sum(len(row) for row in values if isinstance(row, list)) > 200):
            problems.append('read_scope_exceeds_trial_bound')
        hashes.append(_digest(data))
    if times[1] < times[0]:
        problems.append('read_order_invalid')
    if hashes[0] != hashes[1]:
        problems.append('bounded_content_changed')
    problems = list(dict.fromkeys(problems))
    return {
        'kind': 'bounded-read-comparison',
        'workflow_id': definition['workflow_id'],
        'contract_version': definition['contract_version'],
        'source_ref': source_ref,
        'existing_owner_ref': definition['owners']['execution_owner_ref'],
        'status': 'matched' if not problems else 'held',
        'problems': problems,
        'observed_at': [stamp.isoformat() for stamp in times],
        'payload_sha256': hashes,
        'binding_sha256': _digest(binding),
        'coverage': 'bounded',
        'report_date_verified': False,
        'account_identity_independently_verified': False,
        'destination_executor_tested': False,
        'workflow_completed': False,
        'next_step': ('Attach this comparison to the existing private evidence; verify report date, '
                      'account identity and remaining workflow dependencies separately.' if not problems
                      else 'Preserve prior complete evidence; resolve the exact held read before dependent work.'),
    }


def save_summary(summary, output):
    """Create a private local artifact once, then read back its actual bytes."""
    output = Path(output)
    resolved = output.resolve()
    if resolved == REPOSITORY or REPOSITORY in resolved.parents:
        raise TrialError('output: private destination outside repository required')
    if output.is_symlink():
        raise TrialError('output: symlinks prohibited')
    payload = (json.dumps(summary, indent=2, sort_keys=True) + '\n').encode()
    # O_EXCL preserves existing artifacts and refuses symlink races.
    fd = os.open(str(output), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    if output.read_bytes() != payload:
        raise TrialError('output: saved readback mismatch; preserve artifact for reconciliation')
    return hashlib.sha256(payload).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workflow', required=True, type=Path)
    parser.add_argument('--source-ref', required=True)
    parser.add_argument('--binding', required=True, type=Path)
    parser.add_argument('--before', required=True, type=Path)
    parser.add_argument('--after', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args(argv)
    try:
        def read(path):
            return json.loads(path.read_text(), object_pairs_hook=_unique_json_keys)
        result = compare_reads(read(args.workflow), args.source_ref, read(args.binding),
                               read(args.before), read(args.after), now=dt.datetime.now(dt.timezone.utc))
        digest = save_summary(result, args.output)
    except (OSError, ValueError, TypeError, KeyError) as error:
        detail = str(error) if isinstance(error, TrialError) else type(error).__name__
        parser.exit(1, f'Read comparison failed: {detail}\n')
    print(json.dumps({'status': result['status'], 'saved_output_sha256': digest,
                      'local_output_readback_verified': True, 'workflow_completed': False}))
    return 0 if result['status'] == 'matched' else 2


if __name__ == '__main__':
    raise SystemExit(main())

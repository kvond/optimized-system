"""Render the existing reference-only classroom map. No network or work execution."""
import argparse
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'ai-ops/architecture/system-state.json'
OUTPUT = ROOT / 'ai-ops/architecture/overview.md'
STATES = {'verified_done': 'Verified done', 'in_progress': 'In progress',
          'still_needed': 'Still needed', 'blocked': 'Blocked',
          'no_longer_needed': 'No longer needed', 'unverified': 'Unverified'}
TRUNKS = {'ic': 'IC interactions', 'hub': 'Teaching Hub', 'slides': 'Lesson Slides'}


def instant(value):
    if not isinstance(value, str):
        raise ValueError('Timestamp must include a timezone.')
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.utcoffset() is None:
            raise ValueError()
        return result.astimezone(timezone.utc)
    except (ValueError, TypeError):
        raise ValueError('Timestamp must include a timezone.') from None


def text(value):
    if not isinstance(value, str) or not value.strip() or len(value) > 700 or any(ord(c) < 32 for c in value):
        raise ValueError('Expected bounded, nonempty plain text.')
    return value


def url(value):
    value = text(value)
    if re.search(r'[\s<>()\[\]`"\\]', value):
        raise ValueError('Unsafe evidence URL characters.')
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or parsed.username or parsed.password or parsed.port
            or parsed.query or parsed.netloc not in {'github.com', 'answerableteaching.slack.com'}):
        raise ValueError('Evidence must use a canonical GitHub or public Slack reference.')
    if (any(part in {'.', '..'} for part in parsed.path.split('/')) or '//' in parsed.path
            or (parsed.fragment and not re.fullmatch(r'[A-Za-z0-9_-]{1,160}', parsed.fragment))):
        raise ValueError('Unsafe evidence path or fragment.')
    if parsed.netloc == 'github.com':
        if not re.fullmatch(r'/kvond/(?:optimized-system|school-workflow-hub)(?:/[A-Za-z0-9_./-]+)?', parsed.path):
            raise ValueError('Unrecognized repository reference.')
    elif not re.fullmatch(r'/archives/C[A-Z0-9]+/p[0-9]+', parsed.path):
        raise ValueError('Evidence must use an original Slack permalink.')
    return value


def validate(data):
    if not isinstance(data, dict) or set(data) != {'schema', 'updated_at', 'trunks', 'nodes', 'dependencies', 'costs', 'my_actions'} or data['schema'] != 'classroom-map/v1':
        raise ValueError('Invalid classroom map schema.')
    updated = instant(data['updated_at'])
    if data['trunks'] != TRUNKS:
        raise ValueError('Keep the three canonical trunks.')
    if not isinstance(data['nodes'], list) or not 3 <= len(data['nodes']) <= 30:
        raise ValueError('Expected bounded map nodes.')
    ids = set()
    for node in data['nodes']:
        if not isinstance(node, dict) or set(node) != {'id', 'trunk', 'label', 'state', 'owner', 'observed_at', 'evidence', 'recovery_ref', 'next_action', 'teacher_action', 'blocker'}:
            raise ValueError('Invalid node fields.')
        ident = node['id']
        if not isinstance(ident, str) or not re.fullmatch(r'[a-z][a-z0-9_]{0,40}', ident) or ident in ids:
            raise ValueError('Invalid or duplicate node id.')
        ids.add(ident)
        if node['trunk'] not in TRUNKS or node['state'] not in STATES:
            raise ValueError('Invalid trunk or state.')
        for key in ('label', 'owner', 'recovery_ref', 'next_action', 'teacher_action', 'blocker'):
            text(node[key])
        if instant(node['observed_at']) > updated:
            raise ValueError('An observation cannot be newer than the snapshot.')
        if not isinstance(node['evidence'], list) or not 1 <= len(node['evidence']) <= 5:
            raise ValueError('Every state needs reference evidence, including unknown/held states.')
        for item in node['evidence']:
            if not isinstance(item, dict) or set(item) != {'label', 'url'}:
                raise ValueError('Invalid evidence fields.')
            text(item['label']); url(item['url'])
    if not set(TRUNKS).issubset(ids) or any(n['id'] in TRUNKS and n['id'] != n['trunk'] for n in data['nodes']):
        raise ValueError('Every trunk needs its own state node.')
    if not isinstance(data['dependencies'], list) or len(data['dependencies']) > 50:
        raise ValueError('Invalid dependency list.')
    pairs = set()
    for edge in data['dependencies']:
        if not isinstance(edge, dict) or set(edge) != {'from', 'to', 'state', 'reason'}:
            raise ValueError('Invalid dependency fields.')
        pair = (edge['from'], edge['to'])
        if pair[0] not in ids or pair[1] not in ids or pair[0] == pair[1] or pair in pairs or edge['state'] not in STATES:
            raise ValueError('Dangling, duplicate or invalid dependency.')
        pairs.add(pair); text(edge['reason'])
    if not isinstance(data['costs'], dict) or set(data['costs']) != {'API', 'Google Cloud', 'Subscriptions'}:
        raise ValueError('Keep all three cost categories explicit.')
    for value in data['costs'].values(): text(value)
    text(data['my_actions'])
    return data


def md(value):
    return re.sub(r'([\\`*_{}\[\]()#+.!|>~-])', r'\\\1', html.escape(value))


def label(value):
    return json.dumps(html.escape(value), ensure_ascii=False)


def render(data):
    validate(data)
    lines = ['# Classroom system: evidence and next steps', '',
        f"Snapshot: **{data['updated_at']}**. These are dated observations, not a live health check or an execution grant.", '',
        '## My actions', '', md(data['my_actions']), '',
        '## Dependency map', '', 'Red arrows identify held dependencies; the exact blocker is written on the arrow and below. Clickable evidence and recovery references follow the diagram.', '',
        '```mermaid', 'flowchart TB', '  classroom["Classroom system"]']
    for node in data['nodes']:
        lines.append(f"  {node['id']}[{label(node['label'] + ' — ' + STATES[node['state']])}]")
    links = 0
    for trunk in TRUNKS:
        lines.append(f'  classroom --> {trunk}'); links += 1
    for node in data['nodes']:
        if node['id'] not in TRUNKS:
            lines.append(f"  {node['trunk']} --- {node['id']}"); links += 1
    held = []
    for edge in data['dependencies']:
        lines.append(f"  {edge['from']} -->|{label(edge['reason'])}| {edge['to']}")
        if edge['state'] == 'blocked': held.append(links)
        links += 1
    lines.extend(['  classDef verified_done fill:#e8f5e9,stroke:#2e7d32,color:#163d20;',
        '  classDef in_progress fill:#e3f2fd,stroke:#1565c0,color:#123b62;',
        '  classDef blocked fill:#ffebee,stroke:#b42318,color:#7a1910;',
        '  classDef still_needed fill:#fff8e1,stroke:#8d6e00,color:#514000;',
        '  classDef unverified fill:#f1f3f5,stroke:#6b7280,color:#30343b;',
        '  classDef no_longer_needed fill:#f1f3f5,stroke:#9ca3af,color:#535963;'])
    for node in data['nodes']: lines.append(f"  class {node['id']} {node['state']};")
    if held: lines.append('  linkStyle ' + ','.join(map(str, held)) + ' stroke:#b42318,stroke-width:3px;')
    lines.extend(['```', '', '## Owners, evidence and remaining work', ''])
    for trunk, title in TRUNKS.items():
        lines.extend([f'### {title}', '', '| Item / state | Existing owner | Evidence observed | Recovery / remaining action | Katherine action |',
                      '| --- | --- | --- | --- | --- |'])
        for node in (n for n in data['nodes'] if n['trunk'] == trunk):
            evidence = '; '.join(f"[{md(e['label'])}]({e['url']})" for e in node['evidence'])
            recovery = f"{md(node['recovery_ref'])}. Next: {md(node['next_action'])}. Hold: {md(node['blocker'])}"
            lines.append(f"| {md(node['label'])}<br>**{STATES[node['state']]}** | {md(node['owner'])} | {node['observed_at']}<br>{evidence} | {recovery} | {md(node['teacher_action'])} |")
        lines.append('')
    lines.extend(['## Costs', '', '| Category | Measurement |', '| --- | --- |'])
    lines.extend(f'| {key} | {md(value)} |' for key, value in data['costs'].items())
    lines.extend(['', 'Unknown usage is unavailable, never zero or proof of savings. Existing API caps, billing scope and subscriptions remain unchanged.', '',
        '## Update the same map with code', '',
        'Canonical input: [system-state.json](system-state.json). Renderer: [architecture_map.py](../runtime/architecture_map.py). Tests: [test_architecture_map.py](../runtime/tests/test_architecture_map.py).', '',
        'After reading the original evidence, update only the sanitized observations and their timestamps. Preserve private records in their canonical systems; this map stores references, not grades, student work, credentials or raw receipts.', '',
        '```sh', 'python3 ai-ops/runtime/architecture_map.py', 'python3 ai-ops/runtime/architecture_map.py --check',
        "python3 -m unittest discover -s ai-ops/runtime/tests -p 'test_architecture_map.py' -v", '```', '',
        '`--check` returns 0 only for a matching document and a snapshot no older than 24 hours; stale or future snapshots and drift return 2. Invalid input returns 1. Updating the clock field alone does not refresh evidence. The renderer never fetches sources, invokes AI, posts to Slack, starts work, acquires a lease or changes a schedule.', '',
        'Dot can invoke this checked-in renderer after a verified evidence update, check the result, and submit changed source through the existing reviewed PR path. Link this same overview in the existing project thread. No automatic Dot refresh or daily report execution is established by publishing this implementation.', '',
        '## Authorities and boundaries', '',
        'This is the existing architecture overview, updated in place. It is a reference projection, not a second posting log, checklist or execution authority. See the [current handoff](../HANDOFF.md), [ownership guide](../worker-registry/roles-and-schedules.md), [workflow contracts](../workflow-contracts/INDEX.md), [routing interface](../runtime/README.md), and [review/merge policy](../review-and-merge.md).', '',
        'The existing Chrome helper remains the sole IC writer. Current source revisions, exact identities, private mappings, ownership, uncertainty fences and native destination readback remain mandatory. A map status, source publication, PR, deployment, visible browser tab or helper queue cannot establish a saved grade, refreshed feedback, physical delivery or classroom learning.', '',
        'Canonical content and private recovery records remain in their existing authorized systems. Keep the provider-neutral deterministic runtime and existing private-state/storage contracts; no new always-on platform, service, API budget, public asset release, schedule or student-data store is created here.', ''])
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=DATA)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.data.read_text())
        rendered = render(data)
        age = (datetime.now(timezone.utc) - instant(data['updated_at'])).total_seconds()
        if args.check:
            if age < 0 or age > 24 * 3600 or not args.output.exists() or args.output.read_text() != rendered:
                print('Map stale, future-dated, missing, or differs from its evidence input.', file=sys.stderr)
                return 2
            print('Map matches validated evidence input; source freshness still requires the evidence owner.')
        else:
            args.output.write_text(rendered)
            print('Rendered the reference map; no sources checked or workflows executed.')
        return 0
    except (ValueError, OSError, TypeError, KeyError) as error:
        print('Map input invalid or unavailable: ' + type(error).__name__, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

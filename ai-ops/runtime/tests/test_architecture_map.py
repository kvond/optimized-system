"""Deterministic public-reference map: evidence boundaries, drift and stale input."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

PATH = Path(__file__).resolve().parents[1] / 'architecture_map.py'
spec = importlib.util.spec_from_file_location('architecture_map', PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ArchitectureMapTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(module.DATA.read_text())
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name) / 'state.json'
        self.output = Path(self.temp.name) / 'map.md'

    def invoke(self, check=False):
        self.source.write_text(json.dumps(self.data))
        args = ['--data', str(self.source), '--output', str(self.output)]
        if check: args.append('--check')
        with patch('sys.stdout', new_callable=io.StringIO), patch('sys.stderr', new_callable=io.StringIO):
            return module.main(args)

    def test_canonical_map_has_three_trunks_real_links_and_conditional_actions(self):
        document = module.render(self.data)
        for title in module.TRUNKS.values(): self.assertIn(title, document)
        self.assertIn('## My actions', document)
        self.assertIn('None newly required', document)
        self.assertIn('classroom --> my_actions', document)
        self.assertIn('Schoology', document)
        self.assertIn('linkStyle', document)
        self.assertIn('Usage unavailable', document)
        self.assertIn('not a live health check', document)
        self.assertIn('not a second posting log', document)

    def test_unchanged_render_is_reproducible_and_check_is_read_only(self):
        self.assertEqual(self.invoke(), 0)
        original = self.output.read_bytes()
        self.assertEqual(self.invoke(check=True), 0)
        self.assertEqual(self.output.read_bytes(), original)
        self.assertEqual(module.render(self.data), module.render(deepcopy(self.data)))

    def test_drift_or_missing_output_never_claims_updated_or_rewrites_it(self):
        self.assertEqual(self.invoke(check=True), 2)
        self.assertFalse(self.output.exists())
        self.output.write_text('Teacher review text')
        self.assertEqual(self.invoke(check=True), 2)
        self.assertEqual(self.output.read_text(), 'Teacher review text')

    def test_old_and_future_snapshots_hold_even_when_document_matches(self):
        for change in (timedelta(days=-2), timedelta(days=1)):
            data = deepcopy(self.data)
            stamp = datetime.now(timezone.utc) + change
            self.data['updated_at'] = stamp.isoformat()
            for node in self.data['nodes']: node['observed_at'] = stamp.isoformat()
            self.assertEqual(self.invoke(), 0)
            before = self.output.read_bytes()
            self.assertEqual(self.invoke(check=True), 2)
            self.assertEqual(self.output.read_bytes(), before)
            self.data = data

    def test_unknown_grade_state_is_not_promoted_by_a_verified_deployment(self):
        document = module.render(self.data)
        self.assertEqual(next(n for n in self.data['nodes'] if n['id'] == 'ic')['state'], 'unverified')
        self.assertIn('Current saved', document)
        self.assertIn('Changed', document)
        self.assertIn('Class notes: deployed and readable', document)
        self.assertIn('verified_done', document)
        self.assertIn('no live report acceptance', document)

    def test_missing_evidence_invalid_status_and_foreign_trunk_are_refused(self):
        for key, value in [('evidence', []), ('state', 'probably_done'), ('trunk', 'new_platform')]:
            data = deepcopy(self.data); data['nodes'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): module.render(data)

    def test_duplicate_nodes_and_dangling_or_duplicate_edges_are_refused(self):
        changes = [lambda d: d['nodes'].append(deepcopy(d['nodes'][0])),
                   lambda d: d['nodes'][0].update(id='classroom'),
                   lambda d: d['dependencies'][0].update(to='missing'),
                   lambda d: d['dependencies'].append(deepcopy(d['dependencies'][0]))]
        for change in changes:
            data = deepcopy(self.data); change(data)
            with self.assertRaises(ValueError): module.render(data)

    def test_url_guard_rejects_credentials_active_schemes_and_query_payloads(self):
        for address in ['javascript:alert(1)', 'https://github.com@evil.example/kvond/optimized-system',
                        'https://user:password@github.com/kvond/optimized-system',
                        'https://github.com/kvond/optimized-system?token=private',
                        'https://github.com/kvond/optimized-system/../../someone/another-repo',
                        'https://github.com/kvond/optimized-system#x)![remote](https://example.invalid/pixel)',
                        'https://github.com/kvond/optimized-system#space fragment',
                        'https://github.com/kvond/optimized-system//ambiguous',
                        'https://drive.google.com/file/d/private', 'file:///private/history',
                        'https://answerableteaching.slack.com/client/private']:
            data = deepcopy(self.data); data['nodes'][0]['evidence'][0]['url'] = address
            with self.subTest(address=address), self.assertRaises(ValueError): module.render(data)

    def test_text_cannot_inject_markup_or_new_mermaid_statements(self):
        data = deepcopy(self.data)
        data['nodes'][0]['label'] = '<script>alert("x")</script> [another] | link'
        document = module.render(data)
        self.assertNotIn('<script>', document)
        self.assertIn('&lt;script&gt;', document)
        data['nodes'][0]['label'] = 'title\nnew_node["hidden"]'
        with self.assertRaises(ValueError): module.render(data)

    def test_future_observation_naive_timestamp_and_unknown_payload_fields_hold(self):
        changes = [lambda d: d['nodes'][0].update(observed_at='2099-01-01T00:00:00Z'),
                   lambda d: d.update(updated_at='2026-10-25T00:00:00'),
                   lambda d: d.update(student_rows=[])]
        for change in changes:
            data = deepcopy(self.data); change(data)
            with self.assertRaises(ValueError): module.render(data)

    def test_invalid_source_cannot_replace_an_existing_map(self):
        self.output.write_text('Existing verified map')
        self.data['nodes'][0]['evidence'] = []
        self.assertEqual(self.invoke(), 1)
        self.assertEqual(self.output.read_text(), 'Existing verified map')


if __name__ == '__main__':
    unittest.main()

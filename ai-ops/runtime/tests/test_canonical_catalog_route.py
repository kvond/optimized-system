"""The published catalog must expose its actual bounded execution adapter."""
import json
from pathlib import Path
import sys
import unittest

RUNTIME = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RUNTIME))
from workflow_contract import validate_workflow
from workflow_executor import CatalogValidationAdapter, EXECUTOR
from workflow_router import resolve_intent


class CanonicalCatalogRouteTests(unittest.TestCase):
    def test_exact_canonical_operation_resolves_and_matches_real_adapter(self):
        files = sorted((RUNTIME.parent / 'workflow-contracts/definitions').glob('*.json'))
        catalog = [validate_workflow(json.loads(p.read_text())) for p in files]
        resolution = resolve_intent(catalog, {'workflow_id': None, 'domain': 'technical',
                                             'operation': 'validate-workflow-catalog'})
        self.assertEqual(resolution['status'], 'resolved')
        self.assertEqual(resolution['workflow_id'], 'technical-catalog-validation')
        workflow = next(w for w in catalog if w['workflow_id'] == resolution['workflow_id'])
        adapter = CatalogValidationAdapter(files)
        adapter.check_binding(workflow, {'execution_kind': 'deterministic',
                              'resolved_executor_ref': EXECUTOR, 'provider_ref': 'local',
                              'estimated_cost': '0'}, acceptance=False)
        self.assertEqual(adapter.read()['validated_count'], len(files))
        self.assertEqual(workflow['execution']['account_refs'], [])
        self.assertEqual(workflow['policy']['allowed_actions'], ['validate-workflow-catalog'])


if __name__ == '__main__':
    unittest.main()

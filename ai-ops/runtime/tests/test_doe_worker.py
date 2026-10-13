import contextlib,datetime as dt,io,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import doe_worker as worker
from doe_source import AdapterResult,GRANT
from storage import resolve_storage
from vacancies import SourceRead

class DOEWorkerTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        base=Path(self.temp.name).resolve();mount=base/'mount';mount.mkdir();image=base/'image';image.mkdir()
        def probe(m,i):return {'mount':str(m),'backing_image':str(i),'filesystem':'apfs','mount_verified':True,'encryption_verified':True}
        self.paths=resolve_storage(mount/'state',mount=mount,image=image,initialize=True,probe=probe,environ={})
        self.context={'context':'Synthetic verified compact worker context.','context_sha256':'a'*64}
        self.addCleanup(patch.stopall)
        patch.object(worker,'resolve_storage',return_value=self.paths).start()
        patch.object(worker,'build_context',return_value=self.context).start()
    def source(self,ids=('7','8'),complete=True):
        records=[{'vacancy_id':key,'official_url':'https://www.applitrack.com/job?id='+key,'fields':{'title':'Synthetic public opening '+key,'description':'SYNTHETIC_DETAIL_ONLY '+key+' '+('Public responsibilities. '*30)}} for key in ids] if complete else []
        return AdapterResult(SourceRead(GRANT,'revision-'+''.join(ids)+str(complete),dt.datetime.now(dt.timezone.utc),True,False,complete,complete,records),None,{'posting_count':len(records) if complete else None})
    def packet(self,request,ids=('7','8'),complete=True):
        with patch.object(worker.doe_check,'acquire',return_value=self.source(ids,complete)):
            return worker.packet(request)
    def test_unchanged_active_listings_are_not_already_reviewed_or_reported(self):
        first=self.packet('seed');repeat=self.packet('fresh-repeat')
        self.assertEqual(first['counts']['new'],2);self.assertEqual(repeat['counts']['unchanged'],2)
        self.assertEqual({x['vacancy_id'] for x in repeat['listings']},{'7','8'})
        self.assertFalse(repeat['candidate_review_history_verified'])
        self.assertIn('verified task-specific reviewed/reported history',repeat['candidate_history_rule'])
        self.assertNotIn('already_reported_ids',repeat);self.assertFalse(repeat['statewide_coverage'])
        self.assertEqual(repeat['ai_calls'],0);self.assertEqual(repeat['context'],self.context['context'])
    def test_default_packet_preserves_all_ids_hashes_but_omits_descriptions(self):
        result=self.packet('metadata-only')
        self.assertFalse(result['full_description_included'])
        self.assertEqual({x['vacancy_id'] for x in result['listings']},{'7','8'})
        self.assertNotIn('SYNTHETIC_DETAIL_ONLY',json.dumps(result))
        for listing in result['listings']:
            self.assertNotIn('description',listing['fields'])
            self.assertRegex(listing['public_listing_sha256'],r'^[0-9a-f]{64}$')
        self.assertFalse(result['candidate_review_history_verified'])
    def test_exact_id_detail_uses_same_immutable_snapshot_without_refetch(self):
        metadata=self.packet('metadata-first')
        with patch.object(worker.doe_check,'acquire',side_effect=AssertionError('detail read must not refetch')):
            detail=worker.packet('metadata-first','7')
            with self.assertRaises(ValueError):worker.packet('metadata-first','unknown')
        self.assertTrue(detail['full_description_included']);self.assertTrue(detail['reused_request'])
        self.assertEqual(len(detail['listings']),1);self.assertEqual(detail['listings'][0]['vacancy_id'],'7')
        self.assertIn('SYNTHETIC_DETAIL_ONLY 7',detail['listings'][0]['fields']['description'])
        self.assertEqual(detail['source_revision'],metadata['source_revision'])
        self.assertEqual(detail['source_observed_utc'],metadata['source_observed_utc'])
        self.assertEqual(worker.hashed(detail['listings'][0]),metadata['listings'][0]['public_listing_sha256'])
        self.assertFalse(detail['candidate_review_history_verified']);self.assertEqual(detail['ai_calls'],0)
    def test_same_request_reuse_retains_observation_and_requires_freshness_check(self):
        first=self.packet('same-request')
        self.assertFalse(first['reused_snapshot_requires_freshness_check'])
        with patch.object(worker.doe_check,'acquire',side_effect=AssertionError('same request must not refetch')):
            reused=worker.packet('same-request')
        self.assertTrue(reused['reused_request']);self.assertTrue(reused['reused_snapshot_requires_freshness_check'])
        self.assertEqual(reused['source_observed_utc'],first['source_observed_utc'])
        self.assertEqual(reused['checked_at_utc'],first['checked_at_utc'])
        self.assertEqual(reused['listings'],first['listings'])
        self.assertFalse(reused['candidate_review_history_verified'])
        self.assertEqual(reused['ai_calls'],0)
    def test_complete_packet_contains_all_active_records_and_excludes_withdrawn(self):
        self.packet('seed');changed=self.packet('closed-one',ids=('7',))
        self.assertEqual(changed['source_classification']['closed'],['8'])
        self.assertEqual(changed['source_classification']['unchanged'],['7'])
        self.assertEqual([x['vacancy_id'] for x in changed['listings']],['7'])
    def test_partial_source_is_nullable_hold_not_no_new_matches(self):
        self.packet('seed');blocked=self.packet('partial',complete=False)
        self.assertEqual(blocked['status'],'blocked');self.assertIsNone(blocked['listings'])
        self.assertTrue(all(v is None for v in blocked['counts'].values()))
        self.assertFalse(blocked['candidate_review_history_verified']);self.assertEqual(blocked['ai_calls'],0)
    def test_context_failure_stops_source_storage_and_emits_zero_call_hold(self):
        with patch.object(worker,'build_context',side_effect=ValueError('missing private source')),patch.object(worker,'resolve_storage') as storage,patch.object(worker.doe_check,'check') as source,patch.object(sys,'argv',['doe_worker','--request-id','no-dispatch']):
            capture=io.StringIO()
            with contextlib.redirect_stdout(capture):code=worker.main()
            result=json.loads(capture.getvalue());self.assertEqual(code,2);self.assertIsNone(result['listings'])
            self.assertEqual(result['ai_calls'],0);self.assertEqual(result['status'],'failed_closed')
            storage.assert_not_called();source.assert_not_called()
    def test_artifact_listing_tamper_cannot_change_valid_receipt_packet(self):
        report=self.packet('seed');artifact=Path(report['receipt_path']);saved=json.loads(artifact.read_text())
        saved['public_listings'][0]['fields']['title']='Changed artifact outside bound source snapshot'
        artifact.write_text(json.dumps(saved))
        with patch.object(worker.doe_check,'acquire',side_effect=AssertionError('no refetch')):
            with self.assertRaises(ValueError):worker.packet('seed')

if __name__=='__main__':unittest.main()

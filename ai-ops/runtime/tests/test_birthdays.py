import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
import unittest,datetime as dt,json
from birthdays import reconcile,public_summary
class BirthdayTests(unittest.TestCase):
    def setUp(self):
        self.now=dt.datetime(2026,12,31,23,0,tzinfo=dt.timezone.utc)
        self.source={'source_id':'approved-calendar','revision':'v1','complete':True,'available':True,'observed_at':self.now.isoformat()}
        self.args=dict(scope='private-birthday-owner',now=self.now,timezone='America/New_York',lookahead_days=7,calendar_source=self.source,history_source={**self.source,'source_id':'approved-history'},events=[{'event_id':'private-id','occurrence_date':'2027-01-07'}],history=[])
    def test_inclusive_window_and_year_boundary(self):
        r=reconcile(**self.args);self.assertEqual(r['counts']['eligible'],1)
        self.args['events'].append({'event_id':'later','occurrence_date':'2027-01-08'})
        self.assertEqual(reconcile(**self.args)['counts']['outside_window'],1)
    def test_exact_occurrence_only_verified_history(self):
        self.args['history']=[{'event_id':'private-id','occurrence_date':'2026-01-07','status':'handled','receipt_id':'old','verified':True,'saved_at':self.now.isoformat()}]
        self.assertEqual(reconcile(**self.args)['counts']['eligible'],1)
        self.args['history'][0]['occurrence_date']='2027-01-07';self.args['history'][0]['verified']=False
        self.assertEqual(reconcile(**self.args)['counts']['eligible'],1)
        self.args['history'][0]['verified']=True
        self.assertEqual(reconcile(**self.args)['counts']['handled'],1)
    def test_incomplete_preserves_unknown_and_no_false_no_work(self):
        self.args['history_source']={**self.args['history_source'],'complete':False}
        r=reconcile(**self.args);self.assertIsNone(r['counts']);self.assertIsNone(r['items']);self.assertFalse(r['no_work_conclusion_permitted'])
    def test_timezone_and_stale_evidence(self):
        self.args['now']=dt.datetime(2027,1,1,2,0,tzinfo=dt.timezone.utc)
        self.assertEqual(reconcile(**self.args)['business_date'],'2026-12-31')
        self.args['now']=dt.datetime(2027,1,2,2,0,tzinfo=dt.timezone.utc)
        self.assertEqual(reconcile(**self.args)['status'],'blocked')
    def test_determinism_privacy_and_policy_identity(self):
        a=reconcile(**self.args);self.assertEqual(a,reconcile(**self.args))
        self.assertNotIn('private-id',json.dumps(public_summary(a)))
        self.args['lookahead_days']=6;self.assertNotEqual(a['fingerprint'],reconcile(**self.args)['fingerprint'])
    def test_no_inferred_leap_day_or_duplicate(self):
        self.args['events']=[{'event_id':'a','occurrence_date':'2027-02-29'}]
        with self.assertRaises(ValueError):reconcile(**self.args)
        self.args['events']=[{'event_id':'a','occurrence_date':'2027-01-01'}]*2
        with self.assertRaises(ValueError):reconcile(**self.args)
if __name__=='__main__':unittest.main()

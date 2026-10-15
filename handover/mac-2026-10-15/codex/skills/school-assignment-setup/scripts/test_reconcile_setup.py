import copy
import unittest
from reconcile_setup import GATES, IDENTITY, reconcile as reconcile_at


def reconcile(data):
    return reconcile_at(data, now='2026-10-14T12:05:00Z')


def fixture():
    expected = {field: field + '-one' for field in IDENTITY}
    expected.update(key='component-one', agenda_checked_at='2026-10-14T12:01:00Z',
                    agenda_fingerprint='fresh-row-hash', student_material_requirement='digital',
                    student_material_id='student-copy-one')
    receipt = dict(key=expected['key'], run_id='current-run', agenda_fingerprint='fresh-row-hash',
                   observed_at='2026-10-14T12:02:00Z', observed={k: expected[k] for k in IDENTITY},
                   gates={g: {'ok': True, 'evidence': 'private-proof'} for g in (*GATES, 'student_material')})
    receipt['observed']['student_material_id'] = 'student-copy-one'
    return dict(run_id='current-run', run_started_at='2026-10-14T12:00:00Z',
                scope={'complete': True, 'evidence': 'fresh-full-agenda', 'checked_at': '2026-10-14T12:01:00Z'},
                expected=[expected], receipts=[receipt])


class ReconcileTests(unittest.TestCase):
    def test_full_current_chain(self):
        self.assertTrue(reconcile(fixture())['all_ready'])

    def test_links_only_does_not_hide_missing_hub_or_lesson(self):
        d = fixture()
        del d['receipts'][0]['gates']['hub_reader']
        del d['receipts'][0]['gates']['student_material']
        r = reconcile(d)
        self.assertFalse(r['all_ready'])
        self.assertEqual(r['counts']['ready'], 0)
        self.assertEqual(r['counts']['form_page_only'], 1)

    def test_wrong_upload_destination_or_marking_period(self):
        for field in ('upload_folder_id', 'marking_period', 'source_id'):
            with self.subTest(field=field):
                d = fixture(); d['receipts'][0]['observed'][field] = 'different'
                self.assertFalse(reconcile(d)['all_ready'])

    def test_old_run_and_changed_agenda_are_not_reusable_passes(self):
        for field in ('run_id', 'agenda_fingerprint'):
            d = fixture(); d['receipts'][0][field] = 'old'
            self.assertFalse(reconcile(d)['all_ready'])

    def test_newer_failure_supersedes_saved_success(self):
        d = fixture(); newer = copy.deepcopy(d['receipts'][0]); newer['observed_at'] = '2026-10-14T12:03:00Z'
        newer['gates']['published_accepting']['ok'] = False
        d['receipts'].append(newer)
        self.assertFalse(reconcile(d)['all_ready'])

    def test_latest_receipt_compares_actual_time_not_timezone_text(self):
        d = fixture(); newer = copy.deepcopy(d['receipts'][0])
        newer['observed_at'] = '2026-10-14T08:03:00-04:00'
        newer['gates']['folder_owner']['ok'] = False
        d['receipts'].append(newer)
        self.assertFalse(reconcile(d)['all_ready'])

    def test_equal_timestamp_last_appended_failure_supersedes_success(self):
        d = fixture(); newer = copy.deepcopy(d['receipts'][0])
        newer['gates']['published_accepting']['ok'] = False
        d['receipts'].append(newer)
        r = reconcile(d)
        self.assertFalse(r['all_ready'])
        self.assertEqual(r['counts']['ready'], 0)

    def test_future_evidence_is_refused_with_injected_clock(self):
        for location, field in (('run', 'run_started_at'), ('scope', 'checked_at'),
                                ('expected', 'agenda_checked_at'), ('receipt', 'observed_at')):
            with self.subTest(location=location):
                d = fixture()
                target = {'run': d, 'scope': d['scope'], 'expected': d['expected'][0],
                          'receipt': d['receipts'][0]}[location]
                target[field] = '2099-01-01T00:00:00Z'
                self.assertFalse(reconcile(d)['all_ready'])
        d = fixture()
        d['run_started_at'] = d['scope']['checked_at'] = d['expected'][0]['agenda_checked_at'] = d['receipts'][0]['observed_at'] = '2099-01-01T00:00:00Z'
        self.assertFalse(reconcile(d)['all_ready'])

    def test_clock_skew_boundary_is_bounded(self):
        d = fixture(); d['receipts'][0]['observed_at'] = '2026-10-14T12:07:00Z'
        self.assertTrue(reconcile(d)['all_ready'])
        d['receipts'][0]['observed_at'] = '2026-10-14T12:07:01Z'
        self.assertFalse(reconcile(d)['all_ready'])

    def test_different_forms_cannot_silently_share_destination(self):
        d = fixture(); second = copy.deepcopy(d['expected'][0])
        second.update(key='component-two', lesson_id='different-lesson', form_id='different-form')
        receipt = copy.deepcopy(d['receipts'][0]); receipt['key'] = second['key']
        receipt['observed'].update(lesson_id=second['lesson_id'], form_id=second['form_id'])
        d['expected'].append(second); d['receipts'].append(receipt)
        r = reconcile(d)
        self.assertFalse(r['all_ready'])
        self.assertEqual(r['counts']['ready'], 0)
        self.assertEqual(r['counts']['form_page_only'], 0)
        for row in d['expected']:
            row.update(shared_destination_group='deliberate-shared-destination',
                       shared_destination_evidence='verified-current-routing-decision')
        self.assertTrue(reconcile(d)['all_ready'])
        del d['expected'][1]['shared_destination_evidence']
        self.assertFalse(reconcile(d)['all_ready'])

    def test_multiple_lesson_shared_form_requires_explicit_binding(self):
        d = fixture(); second = copy.deepcopy(d['expected'][0]); second.update(key='component-two', lesson_id='different-lesson')
        receipt = copy.deepcopy(d['receipts'][0]); receipt['key'] = second['key']; receipt['observed']['lesson_id'] = second['lesson_id']
        d['expected'].append(second); d['receipts'].append(receipt)
        self.assertFalse(reconcile(d)['all_ready'])
        for row in d['expected']: row.update(shared_form_group='approved-components', shared_form_evidence='live-approved-binding')
        self.assertTrue(reconcile(d)['all_ready'])

    def test_future_or_grading_excluded_work_still_needs_setup(self):
        d = fixture(); d['expected'][0].update(future=True, submissions=0, grading_excluded=True)
        d['receipts'] = []
        self.assertFalse(reconcile(d)['all_ready'])

    def test_unproven_material_omission_is_not_ready(self):
        d = fixture(); d['expected'][0]['student_material_requirement'] = 'teacher_confirmed_no_digital'
        self.assertFalse(reconcile(d)['all_ready'])
        d['expected'][0]['student_material_exception_evidence'] = 'teacher-paper-assignment-choice'
        self.assertTrue(reconcile(d)['all_ready'])

    def test_retired_exception_is_explicit(self):
        d = fixture(); d['expected'][0].update(status='not_applicable', exception_reason='Retired by teacher')
        self.assertFalse(reconcile(d)['all_ready'])
        d['expected'][0]['exception_evidence'] = 'explicit-decision'
        r = reconcile(d); self.assertTrue(r['all_ready']); self.assertEqual(r['counts']['not_applicable'], 1)

    def test_incomplete_scope_cannot_pass(self):
        d = fixture(); d['scope']['complete'] = False
        self.assertFalse(reconcile(d)['all_ready'])


if __name__ == '__main__':
    unittest.main()

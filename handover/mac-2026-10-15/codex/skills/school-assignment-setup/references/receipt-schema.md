# Reconciliation receipts

Run locally after completing or refreshing actual observations:

```bash
python3 ~/.codex/skills/school-assignment-setup/scripts/reconcile_setup.py /absolute/private/setup-run.json --output /absolute/private/setup-result.json
```

Exit 0 means all expected records pass their evidenced factors (or have explicit exclusions); 1 means work remains; 2 means malformed input. This is not a live probe. Never populate a successful gate merely to make the checker green.

The JSON object has:

- `run_id`, timezone-aware `run_started_at`.
- `scope`: `complete`, `evidence`, `checked_at`; identify the selected courses/marking periods and complete live Agenda enumeration in that evidence. An entirely empty scope also needs `no_assignments: true`.
- `expected`: one record per real component. Fields: `key`, `course_id`, `lesson_id`, `marking_period`, `source_id`, `form_id`, `upload_folder_id`, `schoology_folder_id`, `schoology_page_id`, `class_option`, `agenda_checked_at`, `agenda_fingerprint`. The fingerprint should cover the live authoritative row's topic, daily plans, dates, source IDs and routing—not only its week label. Unknown target IDs remain unresolved until established by creation/reuse and fresh readback; update the binding while retaining before evidence.
- `student_material_requirement`: `digital` plus `student_material_id`, or `teacher_confirmed_no_digital` plus `student_material_exception_evidence`. Missing/unavailable/private material is not an exemption. A paper-only assignment can be an evidenced exemption.
- Different `lesson_id` records reusing one Form need the same nonempty `shared_form_group` and `shared_form_evidence` on each record. A single canonical lesson continuing across weeks/sections can retain its same lesson ID; class option and route must still match each section.
- Different Form IDs using one upload folder need the same nonempty `shared_destination_group` and `shared_destination_evidence` on every affected record. Verify that this is deliberate current routing; accidental template destination reuse must not pass.
- `status` defaults to `assigned`, including future assignments requested in an annual setup. `not_applicable` requires `exception_reason` and `exception_evidence` (e.g. actual no-class slot, explicitly retired material, preserved closed historical work). Grading exclusions belong in an independent optional field; no-submission counts cannot create an exclusion.
- `receipts`: append observations rather than erasing failed/history evidence. Each has `key`, `run_id`, `agenda_fingerprint`, timezone-aware `observed_at`, `observed` (the exact identity fields above and student material ID when applicable), and `gates`. The latest timestamped receipt in the current run wins; if timestamps tie, the last appended receipt wins. A later failed receipt supersedes an earlier success.
- All run/scope/Agenda/receipt timestamps must be no later than the current clock plus 120 seconds of allowed skew. Unit fixtures can inject timezone-aware `now` into `reconcile`; manifests cannot override the clock.

Every gate is `{ "ok": true|false, "evidence": "private artifact/location", "reason": "concrete failure if any" }`.

| Gate | Evidence required |
|---|---|
| agenda_identity | Fresh exact course, component, dates, MP, authoritative plans and resolved topic |
| source_content | Actual current source folder/file, not trashed, readable and content matched; current student copy derives from the intended lesson |
| form_owner | Exact school-owned/authorized Form read as owner or authorized collaborator; identity and preserved history confirmed |
| published_accepting | Published and Accepting responses verified after writes/restoration |
| student_responder | Intended students can respond under current published responder audience; not merely owner preview |
| required_identity_fields | Required student name and correct required class choice, including A4 BIOLOGY for Biology |
| upload_configuration | Existing required upload question, suitable accepted types and observed file limits; same question preserved when editing |
| folder_owner | Actual upload-question destination exists, correct owner/parent, owner-readable and not trashed |
| hub_reader | Actual Hub identity can read/list the exact destination required for ingestion; permission merely proposed is failure |
| schoology_route | Correct saved page/body Form href and publish/availability state; short-link final target resolved |
| schoology_placement | Correct course, parent lesson folder, marking period, week/date label and chronological ordering saved/read back |
| student_material | Exact intended student link saved on page, readable by audience, current and content-matched, without teacher answers |

`ready` requires every applicable factor. `form_page_only` explicitly indicates partial work and never contributes to `ready`. Keep UI tests, Form configuration verification and Hub reader access distinct in the supporting receipts. This checker validates consistency of the supplied proof; it cannot establish its truth or replace live readback.

# Portable school operations

These seven definitions preserve the current school procedures for a fresh
executor. They are requirements, not a dispatcher, active schedule, credential
store, new permission grant or proof of completed school work. They extend the
existing `school-current.json` and historical task contracts without rewriting
those snapshots. The October 14 persisted preparation/follow-up prompts and
October 13 teacher-email/science-writing amendments take precedence over older
text copied into those snapshots.

Use the existing deployed Hub and its deterministic preview/apply/verify
contracts. Do not reimplement grading, create a second job or use a general
model to calculate completion in a chat. Before implementation repairs, read the
current canonical Hub checkout's `docs/START_HERE.md` and repository instructions.
This operations repository is not the Hub source or its private configuration.

## Invocation and private resolution

1. Select the exact definition by `workflow_id`. Read this procedure and the
   current governing references in `provenance.contract_refs` before acting.
2. Resolve `private:` references from the existing private runtime registry,
   current school records and relevant saved task. Resolve actual account,
   endpoint, folder, assignment and recipient identities there, never from Git.
   Missing resolution blocks only dependent work; do not invent a locator.
3. Verify the executor's current capability for this exact account and operation.
   `home-codex` is the present repair owner; `school-chrome-helper` is the sole
   grade writer. `existing-lesson-workflow-owner`,
   `existing-assignment-setup-owner` and `existing-school-notice-owner` require
   current owner/capability resolution and are not invitations to start a second
   executor. A school Google login is a data identity, not a coding capability.
4. Read the private scheduler registry and existing execution/receipt state.
   Resolve `school-shared-browser-and-sources` to the actual global lease and
   source writer ownership, including independently running sessions. A schema
   key does not implement a lock. A missing receipt does not prove a writer idle.
5. Freeze the selected scope, actual source versions and intended output key.
   Use existing workflow-specific stable idempotency keys and receipt stores;
   do not create a second receipt ledger. The declared source ages are maximum
   freshness requirements, not proof of freshness. Reread and compare revisions
   immediately before any mutation even within the age limit.
6. Run only actions allowed by the exact workflow and current authorization.
   Verify saved content and native destination, then update the existing private
   records/checklist with actual results. A validator pass never dispatches a job.

The four morning registry references resolve existing 06:30 preparation,
07:00 helper, 07:30 feedback and 08:00 follow-up owners in America/New_York.
This catalog does not change their cadence, timezone, host or account. The
historical Friday task reference preserves a known task, but its current
native state/capability is unverified. Manual lesson/setup definitions remain
on demand; do not add schedules for them.

Private source families resolve as follows:

| Reference family | Required resolution |
|---|---|
| `hub-today-system-notes`, `existing-hub-tasks-checklist` | Current dated Today/System report, teacher Notes revision and existing shared checklist; preserve teacher content. |
| `current-agenda-*`, `current-teaching-manual-*` | Exact live selected class/week/component cells, registered pointers and current applicable manual tabs; cached titles are locators only. |
| `ic-current-*`, `ic-assignment-*` | Complete current course/section or exact assignment membership/flags from canonical IC, with completeness and revision evidence. |
| `registered-intake-coverage`, `complete-current-submission-coverage` | Actual exact Form responses/file references, upload folder, registered folders, approved shared/earlier routes, real unsorted intake and original index links. |
| `archive-configuration`, `feedback-catalog-and-checklist` | Current deployed private destinations, existing stable student folders, index, report IDs, history and teacher marks. |
| `print-ready-email-outbox`, `approved-feedback-adapter-config` | Existing canonical outbox, pinned trusted adapter/runtime, immutable manifests and reserved/uncertain/confirmed state; never extract secrets. |
| `*-ownership`, `*-owner-*`, `*-authority*`, `*-decisions` | Existing actual owner, exact current teacher authority, accepted decisions, exclusions and unfinished recovery scope; configuration is not execution evidence. |
| All `output_ref` values | Existing private native destination or receipt, not a request to create a parallel artifact tree. |

## Shared evidence and recovery rules

IC is canonical for current class/section and assignment membership. Biology,
both Forensics sections and Anatomy/A&P are instructional. The verified Study
Hall course/sections remain roster-only and separate from submission/grade
matching. Only complete fresh membership evidence and an authorized verified
synchronizer permit roster changes. Otherwise report status. Partial scans
preserve the last complete roster and cannot imply mass departures. Verified
withdrawn/Hub-only students leave current operations while originals, work,
prior grades and private Former students history remain preserved.

One fresh batched Hub overview with roster and Agenda bookends is preferable to
repeated whole-roster reads per assignment. Failed, partial, changed or
rate-limited reads are availability failures. Discard unverified names, preserve
prior complete state and allow at most two safe-read retries. Do not convert a
read failure into a teacher identity question, missing work or a zero. Do not
repeatedly poll an unchanged provider/authentication block. If Desktop Commander
is quota-exhausted, use an authorized working native/API alternative without
retrying/reconnecting that provider. For expired IC, existing school Google SSO
and autofill may be used without inspecting credentials; a new authentication
hurdle stops dependent work, not unrelated work.

Identity evidence is not interchangeable. A fresh unique full name or approved
nickname/initial within a complete course/section roster may support deployed
private filing only. It never authorizes a grade or new assessment. Preserve a
stronger existing identity and student folder rather than merging histories.
Exact source content, canonical identity and registered assignment binding govern
grading. Filenames, similar titles or cached links alone prove none of these.

Before calling work missing, inspect complete selected intake coverage. Distinguish
verified empty intake, no Form responses, unresolved work elsewhere and incomplete
coverage. Keep actual untrashed IDs/parents/versions and original Form event dates.
Read supported native Slides/PowerPoint without requiring conversion. Never
restore a trashed/retired file, substitute a same-title copy, move wrong-Form
originals, change student answers, broaden access or delete history merely to
clear an alert. Previews, shortcuts, copied files and saved notes alone do not
prove a source/binding repair.

Preserve the exact accepted current decisions. Investigative Processes and Types
of Evidence may share their verified folder; their brainstorm/partner comparison
count as received Notes. Supplied examples such as Carbon's Grass do not count.
The current year excludes Week 01 cases and the exact Forensics Inductive and
Deductive Reasoning lesson; this must not swallow Week 01 Lab Safety or unrelated
work. Read the private current rule scope before acting rather than generalizing
from a number or title.

Readable identified/matched received work is counted under the deterministic
found-work policy. Notes/Concept Bank and Revision remain distinct; retain coded
required blanks in their denominators; zero denominator means N/A. Missing
codes/scores, mistakes or unfinished work alone do not hold grades. Access,
identity, wrong-lesson and genuinely ambiguous response evidence remain distinct
safeguards. Do not borrow absent/newer teacher tasks. The exact registered Biology
Photosynthesis exception is repair-first; Cellular Respiration and generic raw
links do not inherit it. Empty intake waits without a score check, invented copy
repair or zero. Existing distributed copies may still exist: resolve them through
the authorized Agenda-page-one path, preserve answers/history, verify additive
code repairs and exact saved revisions, then follow normal scoring/helper
verification. Keep that final checklist step pending until verified.

After uncertain writes, stop the dependent write path. Never retry a grade save,
email, model operation or publish merely because a response was lost. Preserve
intent, reservation, source revisions and native receipt. Reconcile the exact
existing destination; no router/fallback may clear uncertainty automatically.
For uncertain IC saving, give one precise scope: class/section, assignment,
component, affected exact cells, what is saved/read back and what remains unknown.
The safe next step is to inspect those cells, correct/save only if wrong, reload
to verify, then use the helper's verification control only after its full required
scope is checked. Never ask for another Save after a verified save, or certify
all assignments from one checked panel.

## school-morning-preparation-and-repair

1. Verify current date, selected Agenda week, school account and sole ownership.
   Read current Today/System, teacher Notes and actual grade/feedback state.
2. Obtain complete IC roster evidence first. Reconcile through only the verified
   authorized synchronizer; otherwise record status, exact stale/inaccessible
   source and preserved complete baseline. Continue independent verified work.
3. Gather one fresh selected Agenda/intake overview with bookends. Inspect exact
   source IDs, original events, shared routes and current folder inventory.
   Investigate holds before labeling student work. Known accepted shared-folder
   decisions require no new teacher question.
4. Apply already-authorized exact stale-link/source-binding/folder repairs only
   through existing preview/apply/verify contracts. Preserve original Form
   upload locations and all versions. Loose-file moves require proven identity,
   destination and unchanged access. Private archive filing uses deployed rules
   and content-verified copies of each distinct revision in existing folders.
5. Finish all source/content/binding mutations before 07:00 Eastern. At cutoff,
   stop those writes even if unfinished, record exact remaining scope in the
   existing checklist for the next safe window and continue independent reads or
   non-racing UI/code repair. This routine neither enters grades nor generates
   feedback, sends email/messages or prints.
6. For a technical issue, use the current Hub code/release workflow, appropriate
   tests and deployed behavior checks. Keep native source/destination proof
   separate from code/deployment readiness.
7. Verify changed source/destination IDs, revision/content, private access and
   index; update the same Hub/checklist with guarded Notes readback. Report actual
   checked/filed/unchanged/held scope, roster state, before-07:00 completion,
   actual helper evidence and exact remaining actions. A successful single class
   or changed configuration cannot complete all-class source/IC requests.

## school-ic-higher-only-entry

This is a contract for the existing helper, not a new Codex grade writer.

1. Verify exact installed helper, enabled weekday setting, correct signed-in
   school origins and current IC assignment session. The setting alone proves
   no run. Resolve any recovery block before new writes; never clear it
   automatically. Keep external source and browser writers away from frozen work.
2. Freeze current complete source revisions and exact IC school year, section,
   term, assignment, component, roster and ten-point bindings. Use verified Hub
   arithmetic and current exclusions, never chat/model grading.
3. For each mapped eligible cell, preserve Exempt flags/comments and higher
   existing grades. Fill a verified eligible blank or raise a lower value only.
   No per-assignment teacher approval is necessary under standing authority.
   This catalog neither toggles entry nor starts a manual duplicate run.
4. Save, reload and read back the exact destination cells against frozen source
   evidence. Any uncertain save/readback halts further helper writes, retains
   its block and produces the exact recovery scope above.
5. Reconcile actual native receipts. Report entered, raised, kept and left
   per class/assignment/component, distinct from unattempted/unconfirmed scope.
   Ready, an open popup, Save indicator or delivered receipt is not verification.

## school-feedback-print-ready

1. Read current outbox status before generation; eligible already verified new
   documents can progress independently of a source/model hold. Verify the
   existing trusted adapter and pinned runtime through private configuration.
   Do not replace its baseline, forge authentication or force checks to pass.
2. For each class's latest closed lesson/newly completed eligible revision,
   verify current Agenda Prompt 2, exact received source, canonical membership
   and assessment identity. Reuse unchanged verified drafts/PDFs without another
   model call. Preserve prior reports and any interrupted provider/save receipt.
3. Create only the approved source-backed report types. Critical-aspect feedback
   keeps its approved one-page format, attributed evidence, one focused question,
   reflection instruction and writing space. Biology science-writing remains
   separate, covering vocabulary, concepts, evidence and reasoning. Do not infer
   chronology from first/revised boxes, filenames or file creation dates.
4. The current science-writing amendment uses saved attributed observations,
   not an unrequested rerating. Show one point per distinct reviewed piece in
   each of four graphs, including distinct same-lesson pieces and explicit
   unrated gaps. Do not average them into lesson points or call one point a
   trend. Its separate practice page supplies three reviewed science facts and
   an accessible CER with lines; supplied practice facts are not student evidence.
   Paper practice is unassessed until returned paper is actually reviewed.
5. Derive supportive missing-work contracts only from complete fresh coverage,
   current roster/flags and factual due dates. Exclude Exempt, unassigned, newly
   joined, future-due and extended work. Located work closes the corresponding
   contract. If extension state is unavailable use a dated factual work-not-located
   invitation, never an asserted missing-work finding or grade change. Combine
   that student's current lessons on one page; old contracts cannot prove absence.
6. Save each new exact report version once in the existing private student/class
   folder beside actual copied work. Verify complete content, destination/access
   and index. A filing failure preserves the saved report; do not regenerate it.
   Keep Biology DTGSS class data without named evidence, separate private student
   writing analysis and teacher action reports. Preserve teacher plans/notes.
7. Update the existing index and four-class checklist. `Made` requires saved
   exact student/report/revision readback. `Made this run` means actual new/revised
   individually filed work, not recompilation of history. Keep report groups,
   dates, source links and historical revisions; never reset/infer Printed or
   Handed out, including after email.
8. Finalize the immutable all-class packet for the actual Eastern saved-feedback
   date. Include verified student critical-aspect, science-writing and eligible
   current-work-contract reports; exclude teacher analyses and only suppress
   proven duplicates. Read the entire saved PDF, page order, manifest and private
   destination; link the exact packet in existing Today/current Agenda records.
9. Drain the canonical teacher-only outbox using its existing adapter and exact
   school Gmail sender/recipient resolved privately. No CC/BCC or student/guardian
   delivery. Prepare one immutable incremental packet of eligible unsent versions,
   verify complete bytes/hash/manifest and preserve the activation baseline and
   existing confirmed corrected-report receipt. If that baseline/setup proof is
   absent, hold rather than resend historical work.
10. Immediately before one send, obtain the first successful `begin_send` reply
    with `send_allowed_once`, preserve its claim privately, record durable intent
    and compare current UTC to the returned expiry. Status or a repeat claim
    readback is not new send authority. Send the exact prepared subject/attachment
    once. Read actual Gmail SENT/raw MIME and verify exact sender, recipient,
    subject, bytes/hash and source manifest before `confirm_sent`. Lost response,
    expired evidence or uncertain delivery calls `hold_uncertain` when possible
    and stops all sending. Never auto-retry, re-bill or reconstruct a reservation.
11. Prepare the next eligible incremental batch only after confirmation, at most
    ten batches per run. An A-to-A+B expansion sends only B; teacher marks never
    deduplicate email. The existing normal limit is 200 reports/10 MB; when split,
    number the body parts without changing the outbox's exact subject. Report
    partial coverage if the bound leaves pending items. No empty email.
12. Read outbox again. Confirmed delivery points the teacher to the emailed
    attachment; it overrides older directions to click Hub Print. Only genuine
    delivery failure or a requested reprint uses exact dated Hub recovery.
    Do not print physically or claim handing-out. Notify only actionable change.

## school-morning-report-resolution

1. At the existing 08:00 follow-up, inspect current Today/System/Notes, actual run
   dates and the existing private checklist/Agenda. Grade receipt, feedback file,
   email and archive/index completion are separate facts.
2. Investigate current source and code before asking the teacher. Repair already
   authorized link/date/display/reader/receipt defects using the existing release
   and native verification path. Preserve notes/history; a revision conflict
   requires a fresh read rather than overwriting another writer.
3. Keep source/content/binding changes that require the before-07:00 window as
   prepared exact repairs in the existing 06:30 record. At 08:00 perform only
   safe independent work, never touching frozen helper inputs/panels or racing
   feedback. No second grade/feedback/email writer and no auto-cleared recovery.
4. Use the question-and-resume contract below for real undecidable choices. Keep
   working on every independent issue. Apply returned answers after rereading
   current evidence; if the safe window has passed, prepare the dependent write
   for the already-existing window and do not create another job.
5. Read back repaired deployed behavior and actual native outputs. Update the
   existing Today/checklist with verified fixes, unresolved scope, owner and
   smallest next action. Keep this repair owner on home Codex until an explicitly
   coordinated destination trial and one-owner cutover succeed.

## school-lesson-readiness

This preserves the existing manual school procedure. A separate live lesson
project may already own its sources; catalog completion is not completion of
that project or evidence the School Claude destination can execute it.

1. Resolve the current exact task owner, bounded class/lesson/cycle and applicable
   authority. Read live Agenda, all applicable current teaching-manual tabs and
   actual original/current native decks. Historical task receipts are locators,
   not current complete acceptance. Honor narrowly documented source restrictions.
2. Preserve native originals and compare every original/current slide, including
   pictures/image-only slides, videos, diagrams, examples and speaker notes.
   Restore authorized omitted material before eligible enhancement. Preserve
   purposeful repetition and response regions; a VT filename proves nothing.
3. Follow existing enhancement/accept-and-fix workflow only on eligible lecture
   content. Do not re-enhance completed/protected response, diagnostic, Concept
   Bank or opening/protected-marker slides. Inspect native results and actual
   visuals; no native-master PowerPoint round trip.
4. Integrate VT/revision support in the real lesson sequence. Read current Skill 3
   and Appendix B for exact code syntax/semantics. Preserve valid existing IDs,
   pair Notes/Draft by question identity, place small code text outside answers,
   prevent duplicates and update native inventories without altering work.
5. Genuine meaningful added response/note text boxes count toward Notes, separate
   from required baseline and Revision. Exclude prompts/template/decorative/empty
   objects; preserve stable slide/object evidence and avoid replay duplicates.
   Do not invent when an object was added if baseline provenance is unavailable.
6. Confirm actual parser acceptance separately. Prompt/native code repair does
   not deploy a parser. Required cases include baseline plus two genuine Notes
   additions, no decorative/empty additions, replay without duplicates and no
   Revision denominator change. Keep exact Photosynthesis repair-first scope.
7. Recheck source/manual revision before every change, then verify saved native
   objects, rendered appearance, complete original coverage and retained answers.
   Use the assignment-chain contract for exact Form/upload/Schoology readiness.
   Report completed versus unverified teaching, code, visual and routing factors.

## school-assignment-setup

Use the installed `school-assignment-setup` skill and its native-workflow and
receipt-schema references as the maintained detailed setup procedure. This is
bounded one-time setup, not a new recurring task or grading path.

1. Discover existing receipts/connections and read actual selected Agenda tabs,
   dates, daily plans, exact folders/links. Include Study Hall in requested
   all-class scope without inventing assignments in empty courses/slots.
2. Build one record per actual assignment/component with course/section, term,
   dates and current content. Same-week lessons stay separate; approved shared
   Forms retain exact mappings. A grading exclusion does not cancel future setup.
3. Verify every factor: lesson identity/material; exact Form published/accepting
   state, intended student audience and required upload/class questions; actual
   upload-question View folder, parent/existence/access; true Hub-reader list/read;
   saved Schoology page identity/parent/order/published body links; intended
   student-copy content/access without teacher answers. No title, HTTP200 or copy
   suffix substitutes for these checks.
4. Apply smallest authorized correction, preserving original Form/page/folder IDs,
   history and originals. Permission/sharing changes need their existing specific
   authorization and tool rules; the catalog does not grant them. Do not restore
   retired Forms or publish response/student-file links to a class page.
5. Resume the first unverified factor, re-reading before any save/create retry.
   Do not submit fake student responses for testing. Reconcile expected scope
   against fresh saved native evidence using the skill's gate checker; the
   checker is not itself a live verifier. Separate full setup from Form-only
   interim repair and name exact remaining factors.

## school-friday-missed-lesson-notices

The historical contract records a Friday 14:15 Eastern task and its old native
save/readback. The portable `existing_schedule` key preserves that known task;
it does not claim the task is active now, verify the destination or create new
send authority. Before execution verify its actual native owner, cadence,
timezone, capability and current explicit teacher authorization for affected
students and verified guardians. If any is unavailable, retain the existing
contract and private draft, report that exact blocker and perform no send.

1. Verify current school year/class/section roster and Friday cutoff. Establish
   actual taught/due lessons, current exemptions/extensions and corrections from
   complete fresh submission coverage; reuse valid current receipts and read
   changes rather than rescanning unrelated history.
2. Blank/zero grades, absent Missing flags, overall grades and partial sources
   cannot prove a missed lesson. Future/not-due, exempt, unreadable/unmatched and
   submitted-awaiting-assessment work do not qualify.
3. Choose at most three most recent confirmed missed lessons by authoritative
   due date, fewer when fewer qualify, none means no notice. Draft neutral lesson
   names, dates and smallest turn-in action; omit unrequested private commentary.
4. Verify actual student/guardian audience in iTracker. Do not guess from a
   household label, change guardians, broaden access or broadcast details.
   Verify exact composed note and audience immediately before authorized publish.
5. Check the private duplicate key for Friday date, student, exact selected
   lessons and recipient identities. Persist intent, publish once only under
   current authority and read back the saved note and audience. Uncertain save
   stops that action without automatic retry. A saved note is not a read receipt.
6. Record aggregate eligibility/published/readback/held counts and concrete
   blockers privately. Never store bodies/recipient identifiers in Git or call a
   configured schedule operational without its actual execution evidence.

## Questions and answer-to-resume contract

Technical conflicts are investigated and repaired within existing authority;
only genuine teaching/identity/lesson choices or necessary access actions become
questions. Keep normally no more than three numbered questions in one short
message. Each gives exact class/section/lesson and verified affected scope,
canonical link/slide number when verified, what was checked, the blocking cause
and two or three concrete choices with a recommendation if supported. Explicitly
state unverified identity/link/slides; do not invent details to fill a template.
Known accepted decisions, Exempt, not-yet-submitted work, provider failures and
routine roster churn are not new teacher choices. Say **No questions for you**
when none are needed.

Store each unresolved question once in the existing private checklist/System
record using its stable issue reference and current revision. Continue independent
work. When an answer arrives, resolve it to that exact issue, reread sources,
apply it within the current safe write window and verify the outcome without
asking for another “continue.” No reply is not approval. A stale answer/source
requires the smallest new clarifying fact only; preserve the prior answer and
never repeat the whole decision list unchanged.

## Acceptance and maintenance

Run catalog checks after integration:

```sh
python3 ai-ops/runtime/workflow_contract.py ai-ops/workflow-contracts/definitions/school-*.json
python3 -m unittest discover -s ai-ops/runtime/tests -p test_school_workflow_definitions.py -v
```

These tests detect requirement regressions and private-data leakage patterns;
they do not simulate school writes or prove capability. Live acceptance remains
workflow-specific and must use actual sources and native saved readback.

| Failure fixture | Required result |
|---|---|
| Partial IC roster or rate-limited intake | Preserve prior complete state; no missing-work/zero/departure inference; independent work may continue. |
| Preparation reaches 07:00 with one source repair left | Hold exact source write in existing 06:30 record; continue non-racing reads, not a new schedule. |
| Helper times out after Save | Stop all helper writes; retain recovery block and reconcile exact cells/receipt without retry. |
| Feedback generation held but outbox has verified new work | Process eligible existing outbox separately under its send fence; no model retry or duplicate email. |
| Email claim exists but Gmail readback is uncertain | Hold batch and stop sending; neither repeat claim nor later schedule grants another send. |
| PDF emailed or unchanged history recompiled | No Printed/Handed change and no false Made-this-run claim. |
| Teacher answers one of two pending questions | Resume only that exact refreshed issue and independent work; preserve unanswered issue once. |
| Friday task seen only in historical saved receipt | Preserve known scheduler key; current capability/authority/owner remains a prerequisite, with no publish or new scheduler. |
| Form-only page saved but intended student material inaccessible | Partial setup; do not claim complete chain. |
| Native lesson codes count correctly but image-only originals absent | Visual/content readiness remains unfinished. |

When current teacher instructions change, update only the affected portable
contract/procedure, preserve private source revision evidence and rerun relevant
checks. Coordinator alone changes active schedules or shared releases. Never
replace the working owner with an untested destination to satisfy a migration
checkbox. Rollback for this catalog is reverting its scoped commit; no runtime
or native school rollback is needed because publishing these definitions makes
no school changes.

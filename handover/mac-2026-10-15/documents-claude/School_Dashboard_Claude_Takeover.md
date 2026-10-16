# Resume the existing School Workflow Hub — local Claude takeover

Prepared September 17, 2026. This is a private handoff for the existing project, not a replacement specification or evidence of a completed run. It contains school configuration references; do not commit this handoff into GitHub.

## Objective

Continue the existing project directly. The teacher needs reliable grading and wants to spend tomorrow on lessons, not on software troubleshooting. Finish the current supervised grade-review/verification/receipt path first. Do not restart the old workbook-permission repair merely because an older handoff lists it as pending. Do not stop after a plan or a synthetic demonstration.

The teacher has reported available included usage on the Claude UDel Max (5x) account: 7% session use and 7% weekly use. Use the existing subscription, not paid API credentials. Do not purchase credits, enable overage, increase spending caps, or change subscriptions. This account's remaining quota is not proof of local file, browser, GitHub, or Cloud Run access; verify those separately in the actual execution session.

## Known locations — reuse, do not replace

- Repository: https://github.com/kvond/school-workflow-hub
- Dashboard: https://school-workflow-hub-611166743877.us-central1.run.app/
- Grading endpoint: https://school-workflow-hub-611166743877.us-central1.run.app/api/grading-records
- Existing grading workbook: https://docs.google.com/spreadsheets/d/1uMohbRQmHybn-JY3ym4K5oCzb58rPYinUsvNEYYuM30/edit
- Authoritative Agenda: https://docs.google.com/spreadsheets/d/1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY/edit
- Infinite Campus entry: https://redclayde.infinitecampus.org/campus/redclay.jsp
- School Chrome profile reported in the prior working session: katherine.vonduyke@redclay.k12.de.us
- Runtime workbook reader reported earlier: 611166743877-compute@developer.gserviceaccount.com. Inspect the current service configuration rather than assuming it is unchanged.
- Local folder lead supplied by the teacher: the Claude folder under Documents on this Mac. No exact school-repository subfolder has been verified in this conversation.

The UDel Claude login supplies AI usage; it does not make UDel the Google Cloud owner or the school browser identity. Preserve the existing authorized cloud account and school Chrome session. Do not change Google sharing or credentials to match the AI account.

## Establish the working copy without making the teacher hunt

Inspect the selected project folder and, when authorized, the Documents/Claude folder. Use a bounded filename/directory search for the existing school-workflow-hub checkout, AGENTS.md, and project README; verify the Git remote. Do not read unrelated personal files, credentials, or browser profiles. Preserve local uncommitted work. Compare the checkout, current GitHub main, deployed revision, and installed companion before editing. Do not reset, overwrite, or replace a local checkout to make it match an older handoff.

Read AGENTS.md, docs/START_HERE.md, docs/PRIVATE_GRADING_WORKBOOK.md, docs/BROWSER_RUNS.md, and browser-extension/README.md. Reconcile historical status against actual observations. A document saying installation is pending may predate the working session described below.

## Latest evidence: what the teacher's current screenshot actually shows

The dashboard grade-review modal has loaded workbook records. The visible section is A2 Forensics, and the visible assignment title is “Observation and deductive reasoning.” It shows a recorded content score and an unscored revision component; do not substitute a zero for that blank component.

The modal says:

> This review has not posted grades or changed the workbook.

> Open the matching assignment’s Score panel in Infinite Campus in this same school browser. The companion checks the current assignment and asks you to confirm there before posting.

The current status line says:

> Open the matching Infinite Campus assignment gradebook.

The “Review & post in school browser” control appears disabled. This establishes the visible stopping point, not its definitive root cause. Do not assume that the workbook is unavailable, that the companion is absent, or that a missing open tab is the only possible explanation. Inspect the actual current school tab and companion response.

## Earlier working-session reports — verify rather than redoing blindly

The teacher pasted the prior Codex thread “Fix Page 2 grading connection.” It reported:

- Runtime reader Viewer access was repaired without public sharing. At 9:01 AM, an authenticated endpoint and Page 2 Forensics refresh showed 8 matched students and 16 records.
- Diagnostic handling was deployed on revision 00038-6bg at that earlier stage. Later deployments were reported; this is NOT asserted to be the current revision.
- The posting button was deployed and the companion installed in school Chrome on the Mac.
- An intermittent refresh issue was attributed to too many small Sheets reads. A subsequent deployed change reportedly reduced each refresh to three requests without caching grades or omitting rows.
- The IC adapter was narrowed to individual student score inputs because the bulk “fill all scores” input used similar styling.
- Two selected existing content grades already matched 5/10. No changes were needed for them. Completing the button's identity checks and saved-result flow remained unfinished in the pasted thread.

These are prior session reports, not new acceptance receipts. Do not manufacture or repeat a grade change to prove posting. No Windows acceptance was established.

## Code to inspect first

The connected GitHub reads have located these existing files:

- web/pages.mjs: reviewGrades and the Page 2 posting controls.
- web/grade-posting.mjs: buildPostingReview and source-review validation.
- web/browser-companion.mjs: status/result handling and the gradebook_required message.
- browser-extension/ic-adapter.js: surface(), inspect(), prepare(), identity matching, assignment mapping, Save and readback.
- browser-extension/ic-content.js and background.js: communication with the exact school tab.
- browser-extension/plan.js and executor.js: reviewed actions and execution.
- src/school_workflow_hub/adapters/grading_records.py: private workbook reads and safe errors.
- src/school_workflow_hub/adapters/google_sheets.py: bounded Sheets transport.
- src/school_workflow_hub/adapters/browser_runs.py and core/cloud_state.py: shared claims and receipts.

The inspected adapter's surface() requires the visible main-workspace iframe and an ic-multiscore Score panel, and validates assignment/section/term context. The current message may reflect a wrong or absent panel, a context mismatch, or installed/deployed code differences. Inspect before modifying; do not remove identity/context protections merely to enable a button.

PR #7 from the chat continuation concerns clearer frontend grading-read diagnostics. It is not the original permission repair and is not proof of a current workbook outage. Check its current status and diff before using it. Do not spend the first work block on unrelated error-message polish while the live grading path is blocked.

## Immediate execution sequence

1. Verify actual local coding access, approved GitHub access, current Cloud Run identity/revision access, and authorized control of the signed-in school Chrome profile. An ordinary cloud chat or an isolated execution container is not the Mac. Continue independent code work when a specific external dependency is blocked; report only the exact missing capability.
2. Inspect the existing dashboard and school browser. Open or identify the correct A2 Forensics assignment Score panel using observed navigation. Verify the actual IC section, assignment, term, student IDs, component, and points scale; a similar title or student display name is insufficient.
3. Reproduce the current companion status. Compare installed, local, repository, and deployed versions. Repair only an established defect. Use the existing approved deployment route when a tested change is required; do not create a new service, database, workbook, or authentication arrangement.
4. Complete the Page 2 review through the companion. Keep the dashboard and IC in the same school profile. The teacher's confirmation must remain bound to the reviewed records and fresh source revision. Do not bypass the trusted confirmation or manufacture an approval.
5. Skip grades that already match. Leave conflicting nonblank grades, identity ambiguity, held work, and unmapped components for explicit review. Preserve history. Re-read the source and target, retain exclusive shared ownership, stop on lease loss, and save/reload/read back every authorized change. Never use the bulk fill-all control.
6. Record the attributed outcome in the existing private cloud state. Verify that the dashboard shows the correct result and it survives reload. Distinguish already_matches, posted_verified, blocked/needs_review, and report_unconfirmed. A saved receipt alone does not independently prove an IC write.
7. Run relevant real tests, report their actual results, and update existing continuation documentation with the code revision, deployed revision, installed companion version, exact evidence level, and remaining blocker. Keep reusable logic/tests in the existing project so another AI does not need this chat.

## Completion boundary and remaining mission

For the immediate grading path, acceptance means an authenticated current workbook read; correctly scoped Page 2 records; a verified IC assignment/student mapping; a successful matching-grade skip or separately approved actual write; matching destination readback; and a persisted, reloadable receipt. If all grades already match, verify that path and explicitly leave new-write acceptance unproven rather than altering a correct grade.

Both laptops must use the same hosted dashboard and existing Firestore state. Do not create a second operational Python installation or database. The school Windows browser may require its own approved companion installation; Mac success does not verify Windows. Do not bypass managed-device restrictions.

The broader requested system still includes current rosters, Agenda and daily-note pacing/date changes, and detection of new, late, and modified submissions throughout the two-week post-due window. The window is not a wait-until-day-14 batch. Preserve cumulative submission history and prior assessments. Failed/partial scans do not establish missing work; keep missing work unscored through the full grace period and respect individual extensions. Use current Agenda prompts for completion, feedback, and class summaries. Do not confuse completing the posting button with completing these other workflows or activate duplicate schedules. Put remaining ordered human actions and exact blockers in the existing dashboard/private task system.

## Boundaries and communication

Do not change workbook contents, grades outside the selected reviewed scope, sharing, authentication protections, billing, or recurring schedules without the necessary authorization. Never move student data, browser sessions, passwords, tokens, or runtime identifiers into GitHub or another account simply because the AI account changed. Verify the processing context is approved before inspecting private student records.

Use one browser executor, not competing agents. Stop on an uncertain write and reconcile before retrying. No claim of background progress without an actual running authorized task.

Do the implementation and investigation directly. Ask the teacher for one precise action only when authentication, approved local access, a required confirmation, or a genuine permission decision blocks the next operation. Include the exact target/account in that request. Do not ask her to locate old chats, re-explain the system, sort the Documents folder, run diagnostic commands, or rebuild the architecture.

This handoff does not establish that Claude has begun work or has the required access. Start by testing the actual execution context, then proceed from the observed live blocker.

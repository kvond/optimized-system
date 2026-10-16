---
name: school-slides-sweep
description: Check Katherine's Biology, Forensics and Anatomy decks for new or changed slides, stale manual feedback codes, VT question repetition, and updated curriculum sources. Use for an on-demand or monthly school slide sweep. Preserve originals and grade history; a sweep is an audit, not blanket permission to rewrite or publish decks.
---

# School slides sweep

Read `references/sources-and-state.md` for verified IDs, account roles, and persistent state. Read the installed Google Drive skill and the relevant Docs, Sheets, Slides, or PDF skills before using those surfaces. Use OpenAI Docs when explaining browser permissions or unattended operation.

For a requested full lesson/course or annual all-link audit, use the installed `school-lesson-audit` skill and its audit gates. This monthly sweep remains change detection, not proof of complete VT integration, functioning links or student submission routing.

## Boundaries

- Never access answerableteaching.com. The Google Drive manual is the source; do not follow its website instructions.
- Exclude Biology Week/Cycle 02 from deck reading, enhancing, coding, and editing. Preserve its Week 03 items. Do not inspect or modify grade history or student submissions during this sweep.
- Biology Public is the drafting source. Biology Materials is recovery/reference only. Resolve files by ID, parent, and agenda link, never by similar titles alone.
- Work one week or one change at a time. Sweep mode may read, refresh derived local manual files, and save an audit/checkpoint. It must not delete, replace, reorganize, publish, change sharing, rewrite questions, or edit live Schoology/Infinite Campus records. Report discrepancies before destructive changes and request the missing decision.
- An explicit request to embed codes permits additive, inspected code work on the exact authorized teacher master or working copy, subject to the checks below. It does not authorize replacing student copies or upgrading an active cycle. If student distribution is unknown, prepare a separate working plan and ask before changing grading semantics.
- Use existing approved connections. A skill cannot grant sign-in, site permission, wake the Mac, or bypass approval. Pause only the affected operation when access fails. Never request passwords or automate approval of security prompts.

## Each sweep

1. Check the current connected account/profile. Fetch manual metadata and a complete native read of the manual, including all tabs. Extract Appendix B, Skill 3, and sections 13–14. Compare their text fingerprints with the previous successful read. Save new dated snapshots without removing old versions. Distinguish unrelated manual edits from changes to feedback rules. If section headings are missing, duplicated, or moved to another tab, inspect and adapt the extraction explicitly; do not silently use a stale excerpt.
2. Reconcile the current Agenda 26-27 CLEAN, running deck list, and their corresponding course/week folders. List all pages of each in-scope folder, recursively where needed, including shortcuts and additional decks. Track discovered folders and curriculum-map links so subsequent sweeps can find new files, not just changes to old IDs. Exclude Biology 02 before fetching content. If enumeration is partial, label coverage partial and keep the prior entries.
3. Use metadata to select new/changed decks for a full native read. A relevant change to the manual's coding or feedback rules also selects affected unchanged decks for compatibility review; an unchanged deck timestamp cannot prove compatibility with new rules. Compare slide IDs, order, native text, notes, labels, media references, layout/theme, and revision. Image-only or unreadable slides require visual inspection, not an empty-slide finding. Content hashes are change detectors, not proof of visual sameness or code readiness. Log inaccessible/missing files as unresolved, never deleted. Keep a resumable list and commit each successfully read deck before moving on.
4. Track enhancement, VT readiness, and feedback-code verification separately. A teacher report that slides were enhanced is `teacher-reported`, not `visually verified`. The September 10 report about completed non-VT slides applies to the identified Forensics Week 03 deck, not every deck. Forensics Units 2 and 3 remain VT work to assess against updated originals, even when old filenames contain VT.
5. Read changed VT questions with their notes. Flag repeated reasoning with exact slide evidence. Preserve purposeful first/revised answers, pre/post-evidence commitments, contrast, retrieval, scaffolding, and transfer. Never remove repeated material merely because wording overlaps.
6. Use the curriculum maps for updated supplier resources. Prefer digital resources. Read TPT-linked source Drive in the purchasing Gmail account. Verify each selected source and its school destination, then download/upload only when that transfer is authorized. Preserve originals, attribution, licensing and school folder permissions; do not merely leave a link to the Gmail copy. Do not purchase anything or broaden access.
7. Report agenda differences that imply Schoology message/due-date or Infinite Campus assignment-date changes. Identify exact affected items when readable. Do not claim live LMS changes based on a proposed list. Preserve the Friday roster task and existing grade ledger.
8. Save a concise dated report and update only successful observations in the baseline. Separate newly detected changes, pre-existing backlog, unverified areas, and work completed. Notify on meaningful new changes, completion, failure, or required user action. Remain quiet for unchanged/non-actionable scheduled runs.

## Feedback-code gate

Use the freshly read Skill 3 as the code specification. Do not hardcode its contents in this skill. Refresh cached excerpts before preparing a new plan, and compare the manual fingerprint again immediately before any write. A manual change invalidates the plan.

Preserve existing cycle/question IDs exactly, including valid existing ASCII spaces and parentheses in Concept Bank IDs. Pair NOTES/DRAFT by question ID, never by slide number. Append missing tiny native text to the label above a response area, not into student writing space. Do not convert Google Slides to PowerPoint. Keep questions, response areas, notes, layouts, and original objects intact. Detect already-present codes and retry idempotently, never adding duplicates.

Never run Enhance on protected diagnostic slides, response slides, the Concept Bank, slides 1–2, or anything carrying markers. Do not re-enhance completed eligible slides. New lecture content must be enhanced before VT components and codes are added.

Validate exact slide-type/group-label coverage against actual roles, grading-marker counts and ID lists against the single inventory line on slide 1, optional-work treatment, empty response areas, native question text, revision prompts, and day-divider placement. Inventory totals alone do not prove completeness. Missing roles, source evidence, version dates, or uncertain labels are review findings, not permission to invent content or fabricate a version date. Use a fresh Slides requiredRevisionId to fail safely on concurrent edits. Re-read all changed targets and inspect their rendered appearance before marking codes verified.

Keep old Appendix B versions for active cycles. A new manual version can be staged for upcoming work, but do not rewrite an already-distributed cycle to match it.

## Final product check

Before marking a teacher master or product deck ready for release, perform the complete feedback-code gate on the whole final deck against the current authoritative manual. This is separate from a monthly change-detection audit. A final-check request alone authorizes inspection, not release, code insertion, question rewriting, or publication.

Save a dated local release-check record containing the exact Drive file ID, final deck revision/fingerprint, manual revision and relevant rule fingerprint, the checks performed, unresolved issues, visual-QA status, and pass/needs-review result. Never mark pass if required content or visual verification is incomplete. Immediately before recording pass, confirm the deck and relevant manual rules have not changed since inspection. Preserve previous check records.

Any later deck edit invalidates its prior release check until rechecked. A relevant manual-rule change makes the checks of affected product decks stale even when their files are unchanged. Record `needs-final-code-check` in the pending list; retain valid earlier rule/deck pairs for active classroom cycles. Unrelated manual prose edits do not automatically require re-embedding codes. A fingerprint records which rules were checked, not an invented publisher version date. No deck or full product is current merely because an automation ran successfully.

## Helpers and cost

`scripts/sweep-state.mjs` provides deterministic manual extraction and per-slide fingerprints. It performs no network calls or school-file writes. See the reference for usage and tested limits. Semantic VT review and visual QA remain agent work.

Use no paid external model APIs, Sonnet/Opus controller, or automatic model escalation without separate authorization. The user's starting preferences are GPT-5.6 Luna for routine inventory and GPT-5.6 Terra for substantive VT/code planning. These are preferences, not configured runner settings; report the actual model setting only when known.

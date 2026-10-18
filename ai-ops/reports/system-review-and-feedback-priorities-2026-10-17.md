# System review and feedback work order — October 17, 2026

Reviewed current `kvond/optimized-system` main at `88a118c`, current GitHub issue/PR state, a fresh Teaching Hub source checkout, and the October 17 public #feedback-pipeline status. This is a source and backlog review. Live Agenda prompts, school identity, deployed configuration, student reports and morning-run receipts were not independently verified in this review.

## Resolved: “What if?” difference

The difference is intentional, not an outstanding synchronization bug. Active lint behavior was corrected in commit `0e6b02a`: `What if?` counts as the canonical diagnostic marker; `What if…` produces `H-MARKER-BROKEN` with slide and repair guidance. The extractor recognizes broader headings for structural classification. The October 15 retirement record explicitly preserves the extractor unchanged and states that exclusions are independently owned. Do not make the tuples identical merely for parity.

Added a synthetic cross-script regression; all six marker tests pass. No production grading behavior changed. [Retirement PR #22](https://github.com/kvond/optimized-system/pull/22) merged October 15, despite the October 17 Slack status being unable to verify it.

## Recommended order

| Rank | Work | Why / completion evidence |
|---|---|---|
| 1 | Accept one real feedback path in the existing Teaching Hub | Highest direct reduction in teacher repair. Extend [Hub #115, workstream B](https://github.com/kvond/school-workflow-hub/issues/115); verify intake, assessment, saved/reopened report, readable PDF, checklist, exact teacher-only outbox receipt, unchanged rerun and later revision. Do not count fixture success as live acceptance. |
| 1a | Resolve intake identity and isolate genuine holds | Gate for feedback. Recheck [Hub #37](https://github.com/kvond/school-workflow-hub/issues/37): collected email + uploaded lesson evidence + roster; typed answers are cross-checks. Count readable correctly matched work even when other scores are missing; preserve true identity/source holds. Do not apply a September observation as proof of today's state. |
| 2 | Complete lesson-renewal pilots and final-artifact checks | Finish [optimized-system #33](https://github.com/kvond/optimized-system/issues/33) before course batches. Verify current final revision, markers, lesson content, Agenda/Schoology destinations and media. Fix the two superseded Agenda references in the VT skill through a separately reviewed change. |
| 3 | Reconcile Anatomy calendar | [#35](https://github.com/kvond/optimized-system/issues/35) tracks remaining calendar conflicts. Preserve the verified Blood Typing move; resolve each remaining date/meeting conflict against current sources. |
| 4 | Simplify ownership documentation and verify schedule replacements | Handoff/roles still propose retired B1 checks. Define monitoring against the current Hub source revision, run and output, distinguishing no eligible work, delayed/unreadable, failed and missing. Reuse current outbox and teacher delivery records. Preserve existing jobs until replacement execution/readback is proved; the October 22 Thursday cloud run is still a future acceptance checkpoint. |
| 5 | Close confirmed bookkeeping gaps; keep manuscript work separate | #31 appears superseded by merged PR #32; verify then close through normal issue maintenance. [#37 manuscript author review](https://github.com/kvond/optimized-system/issues/37) remains its own author-review task. Channel/Drive-folder retirement can wait until replacement consumers and preservation are established. |

## Feedback coordination work order

Codex should own implementation and technical verification in `kvond/school-workflow-hub`; the existing school-feedback-print-ready contract already assigns execution/maintenance to home Codex. Claude can independently review a bounded proposal or draft PR when Katherine explicitly authorizes messaging that chat. This document is a reference handoff, not a transfer of ownership or a new schedule.

1. Inspect current live Prompt 00/0, Prompt 1, Prompt 2 and the current Feedback Guide. Record source revisions privately. Resolve the reported three-level/four-level scale conflict from authoritative instructions; do not invent or convert scales.
2. Identify the already approved native feedback author/adapter and test its actual capability and deployment binding. A renderer, enabled task or healthy provider is insufficient.
3. Select one current class, section and lesson; privately bind each source revision and identity. Separate critical-aspect feedback from science-writing feedback. Unassessed work remains unassessed.
4. Run the existing core operation through saved report/PDF/private destination/index readback. Preserve history and teacher-controlled Printed/Handed marks. Reuse unchanged verified output.
5. Where the standing teacher-only delivery contract applies, verify the canonical outbox claim and exact SENT/raw-MIME attachment receipt once. An uncertain send stops for reconciliation; no automatic resend.
6. Rerun unchanged inputs: no new model call, report or email. Then prove that one substantial student revision creates only the required new version, preserving previous work and delivery history.
7. Compare manual and scheduled paths. Add deterministic exception monitoring to this operation only after the path is accepted. Keep IC entry under the existing school Chrome helper's separate contract.

Acceptance receipt should name the exact class/section and lesson privately, source/report revisions, saved artifact readbacks, outbox state, reuse result and the exact remaining blocked step. Public/Git reports contain no student data.

The old exact-quote and prompt-drift checks are useful requirements, but inspect existing replacements before porting. Current Hub native feedback already includes exact-quote validators and relevant synthetic tests. Prompt compatibility must bind to current Agenda source versions. Rebuilding the retired Feedback Pipeline would create competing work.

## Boundaries

No school writes, messages, emails, schedule changes, merges, channel archival or Drive retirement occurred in this review. The draft regression change is reviewable separately. Configuration and historical receipts do not establish today's live feedback completion.

## Technical verification and specific candidates

Fresh Teaching Hub source: `0077251ab518d13c31e3dea6d341e4f3d86fbb65`. Five relevant suites passed: **140 tests** covering native feedback, delivery state, daily packets, science-writing display and print-ready email. These are targeted synthetic tests, not the full Hub PR gate or live teacher-path acceptance.

A specific candidate for the feedback implementation batch is `src/hub_v2/native_feedback.py:145-161`: whole-scope problems, another row's selection problem, or a late selected row may block feedback. Audit those conditions against current source/eligibility policy. Independent readable correctly matched work should progress; genuine identity/source ambiguity still holds. This is a code-review finding, not a confirmed live incident.

Detailed evidence and acceptance criteria are in `feedback-technical-review.md` beside this report.

## Coordination dependencies

- Hub draft [PR #164](https://github.com/kvond/school-workflow-hub/pull/164) already owns the Today `app.js` changes. Review that work before starting overlapping interface changes for #166; keep the first feedback acceptance slice focused on the existing operation.
- Sunday Weekly Lesson Preflight should be designed to consume the saved Thursday Hub preflight result and inspect fresh changes, rather than duplicate collection. This remains a proposal until result freshness, source coverage and ownership are verified.
- The configured Sunday System Review stays with Claude Code. This requested parallel Codex audit does not replace its schedule.

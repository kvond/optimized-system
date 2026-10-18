# Workflow ownership and schedule guide

Updated 2026-10-18. This file is the operational ownership/schedule source. Standards themselves live in the pinned Slack posts and the Claude Doc `Classroom System Standards — Slides, Grades, Rosters`; do not duplicate them here.

## Standing boundaries
- Canonical names: `ai-ops/NAMES.md`.
- Decisions: Slack `#decisions`.
- Code, skills, prompts, scheduled jobs: this repository.
- No student names, grades, or feedback text in Slack.
- No publishing, sending, grading into IC, deleting, or changing a canonical file without a standing rule or Katherine's approval.
- Claude/Codex use draft PRs on prefixed branches. Routine reversible technical work within Katherine's stated goals has standing authorization through independent review, current checks and merge under [review and merge](../review-and-merge.md). Katherine reviews results after the fact; per-PR or batch permission is not required.
- District Claude organization has no browser use; IC entry and I-Tracker notes remain hand-triggered.

## Current recurring ownership
| Routine | Owner | When | Boundary |
|---|---|---|---|
| Home and school day review | Local Codex | Daily 04:30 Eastern | Read/brief only within its existing contract. |
| Roster and submission tidy | Local Codex | Weekdays 06:30 Eastern | Preparation/repair; no IC write. |
| Eligible IC entry | School Chrome helper | Weekdays 07:00 standing contract | Hand-triggered/opt-in; IC write stays here. |
| Feedback/print-ready | Local Codex | Weekdays 07:30 Eastern | Prepare/file outputs; physical printing/delivery remains Katherine. |
| Teaching Hub report follow-up | Local Codex | Weekdays 08:00 Eastern | Reconcile receipts; no inferred success. |
| Friday I-Tracker | School Claude organization | Friday 14:15 Eastern displayed | Browser blocked in district Claude; I-Tracker note remains hand-triggered. |
| System Review | Claude Code scheduled task (Pro plan) | Weekly Sunday night Eastern | Proposes only. Prompt: `prompts/system-review.md`. |
| Hub week-ahead check and Monday packet | Cloud Run Job `hub-weekly-preflight`, started by Cloud Scheduler `hub-weekly-preflight-thursday` (project school-workflow-hub-54879) | Thursdays 15:00 Eastern | Deterministic: no AI, no browser, no teacher sign-in. Added 2026-10-16 (Hub PR #168). Replaces the Mac's Thursday Claude Code task, which stays on until the 22 Oct cloud run is verified. |
| Book-ops inventory and monthly full sweep | GitHub Action `.github/workflows/book-ops.yml` in this repo | Sundays 03:00 Eastern; full sweep on the first Sunday | Deterministic: no AI, no Roam writes; results committed to `book-ops/`. Added 2026-10-16 (PRs #26, #27). Replaces two Cowork tasks on the Mac, which are still to be switched off. |

The private scheduler registry remains the inventory of provider-level schedule records. This file defines ownership and intended cadence; a configured schedule is not proof of a successful run.

## Next background jobs
### Weekly Lesson Preflight — Sunday
Owner: ChatGPT (Katherine's decision, 2026-10-15), not a Claude Code scheduled task. Proposed Sunday run before Monday preparation. Uses the school Drive. Claude reviews its outputs and PRs against these rules; it does not run Preflight.

Needs access to: `kvond/lesson-preflight`; school Drive; Master Agenda `Agenda 26-27 CLEAN`; `📤 Turn it in_Google Forms`; next-week VT decks and lesson materials; Schoology read access or a current exported/readable source. It may inspect and report readiness but does not publish or change canonical files without a standing rule/approval.

**Overlap for ChatGPT to decide (2026-10-16):** the Thursday Hub job above already runs the Hub's own week-ahead check and rebuilds the Monday packet. Either the Sunday Preflight reads that saved result (the Hub's `GET /v2/api/weekly-preflight`) instead of re-running it, or one of the two is dropped. Until decided, both stay as they are.

Acceptance: source IDs resolve; next-week scope is explicit; output distinguishes missing/unreadable from absent; no student data is sent to Slack; report lands in `#lesson-preflight` or an approved private artifact with a Slack pointer.

### Feedback Pipeline B1-output check — daily
Owner: deterministic check first; Claude Code only for exceptions/judgment.

Needs access to: school Drive location where Workflow B1 outputs land; the B1 run/output identifier or expected-output rule; read access to the corresponding upstream run state. It checks that expected B1 output landed and reports exceptions only. It does not send feedback, grade into IC, or write I-Tracker notes.

Acceptance: each expected B1 run can be paired to its output without student data in Slack; missing output is distinguished from delayed/unreadable; successful days can stay silent or emit a non-student-data receipt.

## Historical state
Detailed October 12–14 observations, old schedules, prior names, and acceptance receipts remain in Git history and `ai-ops/reports/`. They are evidence, not current instructions. Do not restore retired routines from history without a new decision.

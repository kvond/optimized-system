# Workflow ownership and schedule guide

Updated 2026-10-15. This file is the operational ownership/schedule source. Standards themselves live in the pinned Slack posts and the Claude Doc `Classroom System Standards — Slides, Grades, Rosters`; do not duplicate them here.

## Standing boundaries
- Canonical names: `ai-ops/NAMES.md`.
- Decisions: Slack `#decisions`.
- Code, skills, prompts, scheduled jobs: this repository.
- No student names, grades, or feedback text in Slack.
- No publishing, sending, grading into IC, deleting, or changing a canonical file without a standing rule or Katherine's approval.
- Claude/Codex changes are draft PRs on their own prefixed branches; neither merges.
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
| System Review | Claude Code primary; GitHub Action fallback | Weekly Sunday primary; fallback later | Judgment routine proposes only. Same prompt contract for both paths. |

The private scheduler registry remains the inventory of provider-level schedule records. This file defines ownership and intended cadence; a configured schedule is not proof of a successful run.

## Next background jobs
### Weekly Lesson Preflight — Sunday
Owner: Claude Code, with deterministic reads delegated where possible. Proposed Sunday run before Monday preparation.

Needs access to: `kvond/lesson-preflight`; school Drive; Master Agenda `Agenda 26-27 CLEAN`; `📤 Turn it in_Google Forms`; next-week VT decks and lesson materials; Schoology read access or a current exported/readable source. It may inspect and report readiness but does not publish or change canonical files without a standing rule/approval.

Acceptance: source IDs resolve; next-week scope is explicit; output distinguishes missing/unreadable from absent; no student data is sent to Slack; report lands in `#lesson-preflight` or an approved private artifact with a Slack pointer.

### Feedback Pipeline B1-output check — daily
Owner: deterministic check first; Claude Code only for exceptions/judgment.

Needs access to: school Drive location where Workflow B1 outputs land; the B1 run/output identifier or expected-output rule; read access to the corresponding upstream run state. It checks that expected B1 output landed and reports exceptions only. It does not send feedback, grade into IC, or write I-Tracker notes.

Acceptance: each expected B1 run can be paired to its output without student data in Slack; missing output is distinguished from delayed/unreadable; successful days can stay silent or emit a non-student-data receipt.

## Historical state
Detailed October 12–14 observations, old schedules, prior names, and acceptance receipts remain in Git history and `ai-ops/reports/`. They are evidence, not current instructions. Do not restore retired routines from history without a new decision.

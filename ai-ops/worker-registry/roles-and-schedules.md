# Workflow ownership and schedule guide

Updated 2026-10-17 for home IC helper and Weekly Lesson Preflight ownership. This file is the operational ownership/schedule source. Standards themselves live in the pinned Slack posts and the Claude Doc `Classroom System Standards — Slides, Grades, Rosters`; do not duplicate them here.

## Standing boundaries
- Canonical names: `ai-ops/NAMES.md`.
- Decisions: Slack `#decisions`.
- Code, skills, prompts, scheduled jobs: this repository.
- No student names, grades, or feedback text in Slack.
- No publishing, sending, grading into IC, deleting, or changing a canonical file without a standing rule or Katherine's approval.
- Claude/Codex changes are draft PRs on their own prefixed branches; neither merges.
- District Claude browser limits and the school computer's unavailable IC helper do not describe Katherine's home Mac. The existing Chrome helper on the home Mac remains the sole IC score writer. I-Tracker remains separate.

## Current recurring ownership
| Routine | Owner | When | Boundary |
|---|---|---|---|
| Home and school day review | Local Codex | Daily 04:30 Eastern | Read/brief only within its existing contract. |
| Roster and submission tidy | Local Codex | Weekdays 06:30 Eastern | Preparation/repair; no IC write. |
| Eligible IC entry | Existing Chrome helper in the school profile on Katherine's home Mac | Weekdays 07:00 Eastern standing contract | Automatic path requires the helper's saved weekday-morning opt-in; no repeated per-assignment approval. Preserve exact mapping, keep-higher, flags and save/reload/readback limits. Manual recovery stays with the same helper. Current readiness and actual execution must be verified separately. |
| Feedback/print-ready | Local Codex | Weekdays 07:30 Eastern | Prepare/file outputs; physical printing/delivery remains Katherine. |
| Teaching Hub report follow-up | Local Codex | Weekdays 08:00 Eastern | Reconcile receipts; no inferred success. |
| Friday I-Tracker | School Claude organization | Friday 14:15 Eastern displayed | Browser blocked in district Claude; I-Tracker note remains hand-triggered. |
| System Review | Claude Code scheduled task (Pro plan) | Weekly Sunday night Eastern | Proposes only. Prompt: `prompts/system-review.md`. |
| Hub week-ahead check and Monday packet | Cloud Run Job `hub-weekly-preflight`, started by Cloud Scheduler `hub-weekly-preflight-thursday` (project school-workflow-hub-54879) | Thursdays 15:00 Eastern | Deterministic: no AI, no browser, no teacher sign-in. Added 2026-10-16 (Hub PR #168). Replaces the Mac's Thursday Claude Code task, which stays on until the 22 Oct cloud run is verified. |
| Book-ops inventory and monthly full sweep | GitHub Action `.github/workflows/book-ops.yml` in this repo | Sundays 03:00 Eastern; full sweep on the first Sunday | Deterministic: no AI, no Roam writes; results committed to `book-ops/`. Added 2026-10-16 (PRs #26, #27). Replaces two Cowork tasks on the Mac, which are still to be switched off. |

The private scheduler registry remains the inventory of provider-level schedule records. This file defines ownership and intended cadence; a configured schedule is not proof of a successful run.

### Home-computer IC recovery
Katherine's [October 17 clarification](https://answerableteaching.slack.com/archives/C0C8ZJ4FTAT/p1792285329701299) confirms the home Mac as the expected host, including when she requests recovery from her phone. Verify that host is awake/reachable, the school Chrome profile and helper opt-in are current, and no competing writer or unresolved uncertainty block is present. An open Hub tab or remote connection alone proves none of those facts.

If IC signs out, the helper stops. An authorized host agent may select Google SSO and Katherine's school account, letting the browser's saved-password autofill complete sign-in. Do not read, reveal, export or copy credentials. If sign-in needs an interactive challenge or the tool requires a permission prompt, report that exact step; standing task authorization does not prove a remote tool session is already connected. Do not promise that phone pairing or Desktop Commander approval persists indefinitely without checking the actual client/session.

Continue through the existing helper only within its registered time, opt-in and recovery rules. Fill eligible blanks or raise lower scores; preserve higher scores, exempt/other flags and teacher comments. Save, reload and read back each result. An uncertain save stops further writes and is reconciled before any retry; reauthentication does not clear that block. The operative constraints are [the helper contract](../workflow-contracts/definitions/school-ic-higher-only-entry.json) and [Hub AGENTS.md](https://github.com/kvond/school-workflow-hub/blob/main/AGENTS.md). This clarification changes no schedule, permission setting or grade.

## Next background jobs
### Weekly Lesson Preflight — Sunday
Owner: ChatGPT (Katherine's decision, 2026-10-15), not a Claude Code scheduled task. Proposed Sunday run before Monday preparation. Uses the school Drive. Claude reviews its outputs and PRs against these rules; it does not run Preflight.

Implementation home: `kvond/school-workflow-hub`, currently `src/hub_v2/weekly_preflight.py`. Needs access to the existing private Hub result and its source baseline, school Drive, Master Agenda `Agenda 26-27 CLEAN`, `📤 Turn it in_Google Forms`, next-week VT decks and lesson materials, and Schoology read access or a current exported/readable source. Keep distinct lessons separate even when they share a week or folder. It may inspect and report readiness but does not publish or change canonical files without a standing rule/approval.

**Resolved division:** the Thursday Hub job remains the sole Monday-packet producer. Sunday checks freshness and classroom access, reuses the existing packet when inputs are unchanged, and reports changed inputs for a scoped refresh by the same producer. It does not render/send a second packet or create another listener, cache or schedule. This was recorded in the [PR16 review](https://github.com/kvond/optimized-system/pull/16#issuecomment-6227862177); PR16 is now merged, but that is not Sunday activation evidence.

Acceptance before Sunday activation: source IDs resolve and the intended Monday is explicit; compare the saved baseline against current Agenda scope, source identities/revisions, folder membership, Form bindings, roster quantities and rules/packet versions. `GET /v2/api/weekly-preflight` reads saved state and cannot itself prove freshness. Unavailable/incomplete sources stay unresolved rather than falling back to an older success; unchanged inputs keep the same packet with no render/send. Verify the structured result and artifact, not exit status alone. Report in `#lesson-preflight` with no student data and private artifact pointers where needed. Keep the October 22 cloud-run retirement gate unchanged.

### Separate preflight repository retirement
Katherine [approved decommissioning conditionally on the Hub handling the work](https://answerableteaching.slack.com/archives/C0C8ZJ4FTAT/p1792285329701299). `kvond/lesson-preflight` is a retirement candidate, not a second implementation home. It was empty and unarchived when checked October 17; that fact alone does not establish replacement coverage.

Before retirement, verify the Hub's intended coverage and actual result for the reported gaps: G1 teaching dates against student slides; G2 link destinations and duplicate/misleading labels; G3 Notes/DRAFT due dates against each distinct lesson's revision/last teaching day; G4 slide-number reference drift; G5 missing worksheet documents and duplicate copies. Reuse the existing proposal/tests at Hub commit `30189ea` where appropriate, with separate implementation ownership; do not count a proposed port as completed. Preserve required source/history, check callers and schedules, record the replacement receipt in `#decomission`, then retire only the proven redundant component. No deletion, archive or schedule change is performed by this documentation update.

### Feedback Pipeline B1-output check — daily
Owner: deterministic check first; Claude Code only for exceptions/judgment.

Needs access to: school Drive location where Workflow B1 outputs land; the B1 run/output identifier or expected-output rule; read access to the corresponding upstream run state. It checks that expected B1 output landed and reports exceptions only. It does not send feedback, grade into IC, or write I-Tracker notes.

Acceptance: each expected B1 run can be paired to its output without student data in Slack; missing output is distinguished from delayed/unreadable; successful days can stay silent or emit a non-student-data receipt.

## Historical state
Detailed October 12–14 observations, old schedules, prior names, and acceptance receipts remain in Git history and `ai-ops/reports/`. They are evidence, not current instructions. Do not restore retired routines from history without a new decision.

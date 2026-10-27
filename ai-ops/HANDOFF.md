# Classroom system — current handoff

Updated 2026-10-20. This section is the current source; older state is Git history, not an active instruction.

## Homes
- Decisions: Slack `answerableteaching.slack.com`. `#decisions` is the decision log; area channels are `#system-review`, `#feedback-pipeline`, `#teaching-hub`, `#lesson-preflight`, `#vt-decks`, `#class-reports`. Standards for an area are the pinned post in that channel. No student names, grades, or feedback text in Slack.
- Code, skills, prompts, and scheduled jobs: `kvond/optimized-system`. Canonical names: `ai-ops/NAMES.md`. Agent rules: `AGENTS.md` and `CLAUDE.md`.
- Full classroom standards: Claude Doc `Classroom System Standards — Slides, Grades, Rosters`. Do not copy those standards into another file; operational files point to it.
- `ai-ops/decision-log/` is history only.

## Operating rules
- Claude decides operational choices within standing rules and logs decisions in `#decisions`.
- Consent boundary: no publishing, sending, grading into IC, deleting, or changing a canonical file without a standing rule or Katherine's approval.
- Claude and Codex use prefixed branches and draft PRs. Routine reversible technical work within Katherine's stated goals is standing-authorized through testing, independent review and merge; do not require per-PR or batch permission. Katherine reviews results after the fact and may reject them. Follow [review and merge](review-and-merge.md), including latest-head checks and targeted tested reversions.
- Use only canonical names from `ai-ops/NAMES.md` and Katherine's terms and measures.

## Shared working agreements — 2026-10-26

The current shared agreements live in [Kathy and Dot](https://answerableteaching.slack.com/archives/C0CC18AGYR0/p1792975896161269); [October 26 additions](https://answerableteaching.slack.com/archives/C0CC18AGYR0/p1793018609938099) extend them. This is their matching GitHub backup, not another standards hierarchy. These explicit current instructions govern over conflicting older general wording above. Project procedures and course-specific rules remain in their existing skills. A repository update does not prove the Slack edit or pin succeeded.

1. **Katherine governs the program.** Consult these agreements and the relevant project skill before starting a job. Retain earlier applicable instructions and respect current corrections.
2. **Overview first.** Review existing outcomes and evidence, then identify only remaining gaps. Reuse verified work instead of rebuilding it or generating duplicates.
3. **No invented gates.** Reuse applicable bounded approvals. Do not add optional approval holds Katherine has not requested. Respect a declined optional gate and do not ask again without material change. Required safety, privacy, source and identity checks remain.
4. **Useful, concise communication.** Give enough context and relevant links, concrete choices for genuine decisions, and the smallest next step. Do not repeatedly surface unchanged information or completed items.
5. **Keep completed work closed.** Reopen only when new material evidence changes it. Computer records do not establish what Katherine has done offline. Unknown is not “not done.”
6. **Diagnose the system proactively.** Look for communication, workflow, tool or skill causes rather than relying on Katherine to diagnose them. Recommend a concrete preventive fix with expected benefit, risk and a verification plan.
7. **Verify product names and capabilities.** Consult current official product documentation before asserting a product name, missing feature or blocker. Verify how it is used and actual access/state. Do not diagnose from workflow labels or assumptions. Say when state cannot be verified. Looking up the Google Slides Gemini workflow is Dot’s responsibility, not Katherine’s job to teach it.
8. **Use one consistent name.** Keep the established name for the same thing across discussion, skills, files and reports. Do not proliferate aliases. Katherine’s rule: “Words are categories, and categories are filing systems.” Changing the words changes the filing system.
9. **Finish actual outcomes.** Distinguish verified user outcomes from code, deployment or infrastructure milestones. Record the exact blocker, owner and next step for open outcomes. Instruction captured means documented, not that its underlying work is done.
10. **One home for each kind of rule.** These shared agreements belong here. Project procedures stay in their current project skills, with matching GitHub backups where applicable. Do not create competing names, skill copies or trackers. Keep private records and student information out of public channels.
11. **When assigned jobs finish, look for the next useful work.** If nothing is on deck, scan Slack for outstanding work, prioritizing useful cloud/background work. Check existing ownership and completed outcomes before acting. Dot does the bulk of the work; conserve Claude’s smaller subscription and delegate only architecture/agent-design problems or capability-specific needs.
12. **Do not duplicate Claude’s routine.** Katherine reported on October 25/26 that Claude would check Slack hourly that night. That report is not independently verified execution and is not a request to create another Claude automation.
13. **Self-audit only after priority work.** After priority student work is complete, carry out the requested read-only system audit, then follow through on bounded repairs within existing authorization. Present broader changes as proposals; obtain any genuinely required additional approval. A first pass is estimated at 30–60 minutes, excluding repairs, not guaranteed.
14. **Keep skills pinned and backed up.** Whenever a skill changes, update its matching GitHub backup and keep the current skill pinned in its relevant Slack channel. Reuse the canonical skill rather than competing standards. Verify publication, pinning and GitHub synchronization separately; a posted message does not prove either of the latter.
15. **Use Claude Code for stalled reviews.** An unfinished independent review that stalls overnight may use Claude Code as an authorized fallback within the existing task scope and limited usage. Do not repeat completed reviews, duplicate an active reviewer or bypass denied operations or genuine safeguards.
16. **Respect the purpose of the Roster.** The Roster is for Katherine to print, not assistant record keeping. Internal Hub processing and reconciliation records belong at the back of the existing Feedback Checklist, separate from teacher-facing printable views.
17. **Act on diagnosed problems.** Before morning Hub reporting, freshly read these agreements and relevant channel updates. A checklist missing-IC flag requires checking the actual latest eligible work and saved IC evidence, diagnosing the Hub/Helper/IC or reporting break, and carrying out authorized recoverable fixes—not returning the same obstacle to Katherine. Preserve accepted manual completions and required safeguards; report genuine remaining decisions accurately.

Instruction captured is not execution completed. Review these agreements and relevant current channel/thread instructions freshly before the morning report as well as before work.

## Scheduled-task source of truth — October 26

The actual saved scheduled task is canonical for its deployed instructions,
schedule, owner and target. GitHub is its matching backup; do not create or
maintain a Slack copy of a scheduled-task prompt. This exception applies only to
scheduled tasks: project skills and shared agreements keep their existing
channel-first homes and matching GitHub backups.

Read the actual task before replacing its prompt. Preserve cadence, timezone,
owner, target and unrelated rules unless separately authorized. Read back the
saved task and compare exact prompt content or hash before labeling this backup
synchronized. A repository merge is not deployment. New teacher instructions
remain authoritative requirements to reconcile into the runtime task; a stale
saved prompt is not permission to ignore them.

## October 27 working-instructions reference

Before acting or reporting, consult the [current Teaching Hub workflow update](https://answerableteaching.slack.com/archives/C0C9E488BAN/p1793108553190989) and its [matching runbook backup](workflow-contracts/school-operations-runbook.md#current-workflow-update--october-27-2026). It governs conflicting older Hub/Helper-only assumptions while preserving source, privacy, scoring, sole-writer and existing completed-work safeguards. Reuse current evidence and approvals; limit repetitive reads, broad scans and parallel work. Stop unproductive loops, reassess and choose the simplest authorized route. The separate student-work architecture is an approved target in read-only shadow testing, not a verified cutover. This reference changes no runtime schedule, pin or production state.

## Current owners and limits
- System Review: weekly Claude Code scheduled task on Katherine's Pro plan (Sunday night ET), using `prompts/system-review.md`. No GitHub Action, Anthropic API key or Slack webhook.
- The school computer cannot run the IC helper. Use Katherine's home Mac and its authenticated school Chrome profile for the existing helper; district Claude browser limits do not prohibit that separate executor. The weekday 07:00 opt-in path has standing authority, subject to its exact mapping, keep-higher, flag and saved-readback limits. A phone request can initiate work on the home Mac; the phone is not a second IC writer. See the current home-computer recovery rule in `ai-ops/worker-registry/roles-and-schedules.md`. I-Tracker remains a separate workflow and gains no authority from this clarification.
- Katherine authorized the October 20 daily-task split: [Hub operations](../prompts/school-hub-operations.md) at 06:30 and [Spreadsheet feedback](../prompts/school-spreadsheet-feedback.md) at 07:30 weekdays Eastern, reusing the two existing task IDs/threads. Claude retains its active spreadsheet catch-up until exact scope handback. The working extension, sole 07:00 IC helper and separate follow-up remain unchanged. Saved scheduler readback and first execution remain distinct from these definitions. See `ai-ops/worker-registry/roles-and-schedules.md`.

## Remote connection evidence
- An open app/process does not establish usable remote-channel access. At the start of an active remote task, obtain a fresh device listing and one authorized read-only metadata result before reporting the connection as usable.
- When a device is Offline, record the observation time and device/tool state separately from local Codex or Chrome state. Continue already-authorized local work when available; do not infer that a local open app kept the remote channel connected.
- Report observed failures without a speculative cause. Do not copy credentials or browser profiles, create a watcher, or restart a healthy device to manufacture connection evidence.

## Open gaps
- The morning-tabs userscript points at a missing Sheet (`1XGcv-SCueqJrSIsiMC6Y_9LpAGoeTIhnb7NSNpp3q-A`).
- The Hub owns the Weekly Lesson Preflight implementation and Thursday packet production. The proposed Sunday ChatGPT check is read-only freshness/access validation, not another packet producer. Its activation and the separate repository's retirement still require the acceptance gates in `ai-ops/worker-registry/roles-and-schedules.md`.

## Source pointers
- Names: `ai-ops/NAMES.md`
- Ownership/schedules: `ai-ops/worker-registry/roles-and-schedules.md`
- Technical authorization, independent review and merge: `ai-ops/review-and-merge.md`
- Workflow contracts: `ai-ops/workflow-contracts/INDEX.md`
- Historical evidence: `ai-ops/reports/` and Git history
- Current human clarification: [Katherine's October 17 home-computer and preflight answers](https://answerableteaching.slack.com/archives/C0C8ZJ4FTAT/p1792285329701299).

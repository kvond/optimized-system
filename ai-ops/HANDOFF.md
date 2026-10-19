# Classroom system — current handoff

Updated 2026-10-18. This section is the current source; older state is Git history, not an active instruction.

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

## Current owners and limits
- System Review: weekly Claude Code scheduled task on Katherine's Pro plan (Sunday night ET), using `prompts/system-review.md`. No GitHub Action, Anthropic API key or Slack webhook.
- The school computer cannot run the IC helper. Use Katherine's home Mac and its authenticated school Chrome profile for the existing helper; district Claude browser limits do not prohibit that separate executor. The weekday 07:00 opt-in path has standing authority, subject to its exact mapping, keep-higher, flag and saved-readback limits. A phone request can initiate work on the home Mac; the phone is not a second IC writer. See the current home-computer recovery rule in `ai-ops/worker-registry/roles-and-schedules.md`. I-Tracker remains a separate workflow and gains no authority from this clarification.
- Existing 06:30/07:30/08:00 school routines and the 07:00 IC helper remain separate until explicitly changed. See `ai-ops/worker-registry/roles-and-schedules.md`.

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

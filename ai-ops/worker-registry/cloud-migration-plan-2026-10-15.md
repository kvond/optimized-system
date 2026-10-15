# Moving the recurring jobs off the MacBook Air

Proposal, 15 October 2026. Nothing here is switched on. Each row needs Katherine's approval before it changes, and `roles-and-schedules.md` stays the source of truth until it does.

## Why

The MacBook Air is being erased. Four active Codex automations, the Slack worker, the Thursday preflight and the Cowork tasks all run on it, and three of the Codex jobs read code from inside run folders under `~/Documents/Claude` rather than from a repository. On erase day every one of them stops. The next machine has 32 GB, but the direction is to put more of the work on APIs and the cloud, not on any laptop.

## The rule for placing a job

1. **Deterministic first, on a schedule that costs nothing.** If the job is a fixed check or a fixed transformation, it runs as code: Cloud Scheduler calling a Teaching Hub endpoint (the Hub is already on Cloud Run), a GitHub Action, or a Google Apps Script time trigger in the account that owns the data.
2. **A model only for judgment or exceptions.** When a step needs reading and deciding, the deterministic job calls the Claude API for that step alone, under the budget in `ai-ops/cost-routing/budget.md` ($1/day, $20/month ceiling).
3. **A full agent session only for open-ended work.** That means a Claude Code cloud routine on `kvond/optimized-system`, which now loads the skills through `.claude/skills` (PR #23).
4. **A browser only where no API exists.** Infinite Campus entry and I-Tracker stay hand-triggered on whatever machine Katherine is at.

## Job by job

| Job | Today | Proposed home | Model use | Needs first |
|---|---|---|---|---|
| Calendar and school email review (daily 04:30) | Codex on the Mac, running `workflow_cutover.py` from a run-folder checkout | Claude Code cloud routine on this repo, using the Gmail and Calendar connectors; the contract and runtime are already in `ai-ops/` | Yes, reading and summarising | Confirm connectors reach cloud sessions; move the private candidate binding out of the run folder |
| Roster check and submission tidy (weekdays 06:30) | Codex on the Mac | Cloud Scheduler → a Teaching Hub repair endpoint; Claude API only on exceptions | Exceptions only | A Hub endpoint that runs the existing checks without a browser |
| Feedback and print-ready (weekdays 07:30) | Codex on the Mac, running `email_outbox_worker.py` from a run folder with a run-folder venv | Move `email_outbox_worker.py` into `school-workflow-hub`; Cloud Scheduler → Cloud Run job | None for sending; exceptions only | The worker in the repo with tests; Gmail send scope on the school account |
| Teaching Hub report follow-up (weekdays 08:00) | Codex on the Mac | Same Cloud Run job as the 07:30 run, second step | Exceptions only | As above |
| Nightly Slack worker (daily 21:00) | Codex on the Mac | Slack gateway on Cloud Run (already staged) triggering a Claude Code cloud routine | Yes | Gateway live; the routine's permissions written down |
| Weekly lesson preflight (Thursday afternoon) | Claude Code scheduled task driving Chrome | Cloud Scheduler → the Hub's own preflight endpoint; post the result to `#lesson-preflight` | None | The preflight callable without the browser (the Hub already does the checking) |
| Book-ops inventory rebuild (weekly) | Cowork task | GitHub Action running `build_inventory.py` with the Roam read token as a repository secret | None | Token stored as a secret, not in a folder file |
| Book-ops monthly full sweep | Cowork task | GitHub Action for `dedup_sweep.py`; candidates written to the `[[book-ops review]]` page | None for matching | As above |
| Daily Spanish lesson | Cowork task (paused) | Claude Code cloud routine with the Roam MCP in `.mcp.json`, token from the environment | Yes | Roam token in the cloud environment |
| Book distill 1–4 and 2nd-brain distill | Cowork, manual trigger | Stay on demand; run from any machine or a cloud session | Yes | Nothing; they are not scheduled |
| IC entry (Chrome helper) and Friday I-Tracker | Browser | Stay hand-triggered on the current machine | No | Nothing |
| System Review (weekly) | Claude Code scheduled task (planned) | Claude Code cloud routine | Yes | Already planned this way |

## Order

1. **Before erase day, keep the morning school jobs alive.** Move `email_outbox_worker.py` and the cutover checkout into repositories and point the automations at the repositories, not the run folders. Five paths in `~/Documents/Claude` are being kept only for this.
2. **Put the zero-model jobs on Cloud Scheduler and GitHub Actions**: the preflight, the inventory rebuild and the full sweep. These cost nothing to run.
3. **Move the Hub jobs** (roster tidy, feedback, report follow-up) to Cloud Run with the model only on exceptions.
4. **Move the agent jobs** (calendar and email, Slack worker, Spanish) to cloud routines, after confirming that connectors and the Roam token reach cloud sessions.
5. **Retire the Codex automations one at a time** as each replacement produces a verified run. A configured schedule is not proof of a run.

## Machine setup that keeps the next laptop light

- **One clone per repository** under `~/code`, with work on git worktrees removed when the PR merges. No clones inside `~/Documents`.
- **Run and scratch folders stay outside iCloud-synced Desktop and Documents.**
- **Secrets in a password manager or cloud secret store, never in folder files.** That covers `.roam_token`, `~/.roam/edit_token` and the Hub API key.
- **One agent app open at a time** for long runs.

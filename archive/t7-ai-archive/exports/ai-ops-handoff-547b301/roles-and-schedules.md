# Which AI does what, and when

Main working account: **UD (`kvond@udel.edu`)** for ChatGPT/Codex and retained Claude. **Source kvond12 accounts are for preserving earlier work**; they have not been retired. Checked October 12, 2026. Active schedules mean configured, not proof a run completed. The full local Codex automation directory currently contains only the two school TOMLs below. Personal coverage is the five verified UD tasks; other accounts, cloud schedulers and older task systems are not a global completeness claim. No current local daily-brief-2 or monthly slide-audit TOML was found.

## Current recurring jobs

Times below are Eastern where verified. Personal ChatGPT times are displayed in the UI; their backend timezone is still unverified.

| Worker / job | State | When | App and device needed | What remains unverified |
|---|---|---|---|---|
| UD ChatGPT — Daily News Briefing | Active | Every day, 4:30 a.m. displayed | Cloud task: laptop may be off; connected service tabs generally need not be open ([OpenAI](https://learn.chatgpt.com/docs/automations)) | Backend timezone, full source coverage and private delivery |
| UD ChatGPT — Daily Finance Brief | Active | Every day, 4:30 a.m. displayed | Cloud task: laptop may be off; connected service tabs generally need not be open ([OpenAI](https://learn.chatgpt.com/docs/automations)) | Backend timezone, input access and successful delivery |
| UD ChatGPT — Delaware Education Job Watch | Active; Katherine’s educator search | Daily monitoring recorded; clock not exposed | Cloud task: laptop may be off; connected service tabs generally need not be open ([OpenAI](https://learn.chatgpt.com/docs/automations)) | Exact cadence/clock/timezone and last successful receipt |
| UD ChatGPT — Birthday Gift Workflow | Active | Monday morning; exact clock not exposed | Cloud task: laptop may be off; connected service tabs generally need not be open ([OpenAI](https://learn.chatgpt.com/docs/automations)) | Exact clock/timezone, delivery and conflicting cart rules |
| UD ChatGPT — Weekly Job Scan | Active; separate production/management candidate | Wednesday, 7:00 a.m. displayed | Cloud task: laptop may be off; connected service tabs generally need not be open ([OpenAI](https://learn.chatgpt.com/docs/automations)) | Backend timezone and successful delivery; separate resume/tracker/profile, no shared approvals |
| Codex + Remote Desktop Commander — school roster/tidy | Active | Weekdays, 6:30 a.m. Eastern | Awake Mac, Codex desktop running, project on disk ([OpenAI](https://learn.chatgpt.com/use-cases/manage-your-inbox)); school Chrome/Hub/IC available | Complete source/roster coverage and actual filing receipts |
| Chrome school helper — eligible IC grades | Existing separate helper; current loaded setting unverified | Weekdays, 7:00 a.m. standing contract | Awake connected Mac; Chrome school profile, loaded helper and signed-in Hub/IC | Current extension setting/loading and exact saved-grade readback |
| Codex + Remote Desktop Commander — student feedback | Active | Weekdays, 7:30 a.m. Eastern | Awake Mac, Codex desktop running, project on disk ([OpenAI](https://learn.chatgpt.com/docs/automations)); school Chrome/Hub available | Eligible source coverage and verified newly saved private feedback |

No physical printing is scheduled by these jobs. Katherine controls Printed and Handed out marks. The helper alone owns automatic IC entry; roster/tidy finishes source mutations before 7:00.

## Worker roles available or proposed

| Worker | Job | State / timing | What to open |
|---|---|---|---|
| Main UD ChatGPT Plus | Plan, review, make decisions and coordinate work | Available on demand; no fixed time | ChatGPT for an interactive conversation |
| Codex + Remote Desktop Commander | Technical repairs, verified automation and private archive operations | Available on demand; school schedules above | Codex and reachable Mac/device; relevant authenticated app for the action |
| UD Claude Pro | Useful browser and large-context writing/research work | Retained; zero scheduled Claude jobs observed; on demand | Claude for interactive work. New paid Cowork schedules can run in cloud; local file/app work needs that Mac and Claude Desktop running ([Anthropic](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork)) |
| Deterministic Python + private drive cache | Inventory, fingerprints, reuse, checksums and receipts | Working DOE command accepted on demand; no personal schedules cut over | Authorized runtime/device and required private drive mounted; no AI chat required by code itself |
| Cheapest suitable API worker | Small changed-input summaries after deterministic checks | Proposed and disabled; no paid execution verified | Future tested runner and approved credentials; no current schedule |
| Perplexity | Focused public research with sources | On demand; no schedule verified | Perplexity for interactive research |
| Source kvond12 ChatGPT / Claude | Preserve and verify older exports while accounts are retained | Preservation incomplete; accounts not retired | Normal source-provider session on the Mac when authentication/download is needed |

The educator Job Watch’s narrow repeat rule has been saved and read back; owner, frequency, criteria and destination stay intact. The Wednesday scan serves a separate production/management candidate across PA/NJ/DE and remote US, using that project’s original resume and applications/outreach tracker. Do not merge the searches, share candidate analysis or reuse approvals. Other four jobs, gift policy, finances and school safeguards remain unchanged. Configuration readback does not prove measured savings.

App requirements describe platform behavior, not successful task execution. Older Claude Pro/Max schedules from before October 6 may remain local; none was observed active in UD Claude ([Anthropic platform guide](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)). Portable registry: private `kvond/optimized-system`.

The [DOE operator command](https://github.com/kvond/optimized-system/blob/547b301c5918e82580b7ea849f96e45c28866525/ai-ops/runbooks/doe-operator-check.md) is now implemented and accepted through Desktop Commander with encrypted receipt readback and same-request reuse. It performs zero AI calls and runs only on demand;83 tests passed at this checkpoint. It has no fixed scheduled time or candidate analysis.

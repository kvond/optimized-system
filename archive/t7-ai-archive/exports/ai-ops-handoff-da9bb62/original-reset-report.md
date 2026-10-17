# AI-system reset handoff — October 11, 2026

## Executive summary

The durable foundation is staged in the existing private answerable-skills repository under ai-ops; no new core repository, Cloud service or paid worker was created. Existing production and all scheduled jobs remain unchanged. Source inventory covered 115 accessible local Git checkouts and 12 accessible GitHub repositories (11 owned/private, one organization repository). Raw archive structure and three Git bundles were copied to T7 and all 11 files verified by Finder copy-back and SHA256. Complete AI-account history exports are not yet obtained.

The five expected personal recurring jobs are already under UD ChatGPT Plus, not kvond12 Free. UD Claude Pro is verified live and has no scheduled tasks. Personal replacements are staged as provider-neutral contracts, not enabled. Twelve synthetic runtime tests pass. The reset will finish before its fixed October 12 6:00 AM Eastern cutoff with no continuation scheduled.

## Repositories created / reused

Created: none. Reused: kvond/answerable-skills (private durable rules, compact bundles, schemas and tested local runtime). Existing kvond/Personal-Hub supplies a candidate FastAPI/Firestore pattern; no modification or deployment. School Workflow Hub untouched. Work isolated in this task’s work/core clone so existing dirty/unpushed work is not overwritten.

## Retirement and repositories needing review

Only explicitly defunct kvond/Answerable-Teaching and archived kvond/answerable-pipeline-backup are marked RETIRE / DELETE-REVIEW. Nine unique reusable legacy files preserved exactly with source commit, original paths, byte sizes and SHA256; three private manuscript JSON inventories remain in the legacy Git bundle, outside GitHub’s reusable layer. Pipeline’s nine code/config files already match answerable-skills. No deletions. Verified markers: [Answerable Teaching issue](https://github.com/kvond/Answerable-Teaching/issues/1) and [pipeline review issue](https://github.com/kvond/answerable-skills/issues/2). Archived pipeline rejected in-place description change (403); it stays unchanged.

Loaded legacy com.kvond.answerable-publish invokes missing ~/Documents/projects/Answerable-Teaching/nightly-publish.sh at 19:30 and 23:00 local time. Current readback: not running, three historical runs, last exit 127. It remains unchanged. Archived feedback-system has substantial unique code and a Render blueprint; REVIEW until live consumers verified. Other repositories remain KEEP/REVIEW; no broad retirement.

Inventory: 79 dirty checkouts, three unknown/incomplete/timed out, seven with unpushed commits by local upstream refs. Main ~/Documents/Claude/school-workflow-hub is dirty, locally 1 ahead/29 behind. ~/answerable has two unpushed commits and a verified bundle copy. Do not pull/reset/delete these checkouts. Protected Documents/Codex remains inaccessible; inventory coverage is incomplete there. Full fields/path lists in repo-inventory.json. Ahead/behind from local refs may be stale.

## Raw archive and distilled knowledge

Stable path /Volumes/T7/AI-Archive; ~829 GB free, external USB ExFAT, encryption unverified. Structure: raw platform/account folders, manifests, exports, checksums, preservation/repos. Three bundles preserve Answerable Teaching, pipeline backup and visible refs/unpushed Answerable history. Git bundle verification passed locally; all 11 prepared files matched after external copy-back. Command-line volume operations time out, so Finder supplied copy/readback. Original sources and existing drive contents unchanged. No complete ChatGPT/Claude/Perplexity exports, source date ranges or project-file completeness claims. Recommend encryption before sensitive exports.

Nine compact bundles plus retrieval/provenance manifest cover teaching, book concepts, writing/Substack voice, operational decisions, school rules, workflow preferences, account history and Wilmington source gaps. Exact Wilmington rubric/template and complete Substack template were not recovered; no invented substitutes. Older account audits are reported provenance and superseded by current user direction. No raw chats, family dates, student-identifiable records, financial/health history or full memory dumps enter GitHub.

## Cache/state/router status

Implemented/tested local stdlib Python + SQLite cache: source revision/input/contract/route/privacy keys, success-only reuse, UTC expiry, scoped invalidation. One source component per contract permits partial recomputation; missing/inaccessible coverage blocks reuse. Atomic fail-closed spend reservations, idempotent settlement, uncertain reservation retention and overrun blocking are implemented. Twelve tests cover concurrent reservations, persistence, privacy/version/expiry, failed cache results, routing and actual child/descendant stopping.

Provider-neutral router selects sufficient authorized deterministic work first, then cheapest sufficient route. Only synthetic deterministic example enabled; no API/provider adapter or automated migration acceptance. Metadata schema designs token/cost/result/receipt/retry fields; not every field is persisted by the foundational runtime. Local SQLite is not deployed to ephemeral Cloud Run.

## Google Cloud and API status

Two visible projects: school-workflow-hub-54879 and graceful-fold-341018. Hub Ready revision school-workflow-hub-00267-wrx at 100% traffic, IAP enabled, OpenAI Secret Manager key binding present. Other project has Ready personal-hub-api and personal-hub-mcp. MCP allows public Run invocation with a path-token binding; actual app authentication remains unverified. Both have Firestore. No cloud changes or secret payload reads.

Zero Run jobs returned; Cloud Scheduler inventory blocked because API disabled in both projects. This is not verified absence of every external scheduler. Reuse current authenticated/private-state patterns only after acceptance; do not build another platform or connect public MCP to school data.

OpenAI API: key binding configured in Hub, validity/account/model execution receipts and budget unverified. Anthropic: secret metadata exists; active binding/credit/worker validity unverified. No provider model calls, credits purchased or budget changes. Initial proposed API pilot: $1/day, $20/month combined cap, optionally $10 initial funding after a validated adapter; estimate assumes 2–5 changed-input summaries/day <=$0.05 each. These are spend envelopes, not price quotes or measured workload. Current official OpenAI pricing/spend-limit pages linked in cost-routing/budget.md.

## Personal scheduled-task migration

Live UD Active list: Daily News Briefing daily4:30 AM; Delaware Education Job Watch daily monitoring (exact time unexposed); Birthday Gift Workflow Monday Morning; Daily Finance Brief daily4:30 AM; Weekly Job Scan Wednesday7:00 AM. Backend timezone not exposed; client context Eastern. Exact task IDs and sanitized capability/input/destination gaps in migration-manifests/personal-tasks.json. Source prompts remain in original task, private fields omitted.

No tasks disabled or duplicate schedules created. Output delivery and replacement test receipts remain unverified. Keep UD jobs active; stage deterministic retrieval/dedupe plus cheapest authorized summaries or UD Claude background where useful. News and birthday task differ on cart staging; preserve settings and resolve intentionally before gift cutover.

## 6:30 AM owner / 7:30 AM owner

06:30: local Codex heartbeat dispatcher, ACTIVE morning-roster-check-and-submission-tidy, weekday Eastern, target thread01a0fc18-96be-7873-8386-da8a6b110384. Inputs exact Agenda/IC/source inventory; outputs filing/index/checklist/readiness for separate07:00 Chrome helper.

07:30: local Codex heartbeat dispatcher, ACTIVE morning-student-feedback-and-print-checklist, weekdays Eastern, target thread01a0f4ed-2d87-7e62-9056-46f5ac441ef3. Outputs private student/teacher reports, checklist and daily print packet; Printed/Handed-to-student preserved.

Config files locally owned by katherinevonduyke. Prior same-day audit reports Codex signed in as UD; current desktop identity inspection was denied by UI tool. TOMLs do not pin a model; configured Hub OpenAI binding is not proof of actual model used. Exact prompts/hashes preserved. Maintenance owner Katherine via source rules; proposed execution-account change intentionally deferred. Internal dispatcher wake/retry unknown; prompts enforce readback and stop on uncertain writes. Historical receipts are not fresh destination acceptance.

## Hard stop, blockers and risks

Fixed guard rejects starts at/after2026-10-12T10:00:00Z and stops only owned process groups with reserved cleanup/reap time. No reset recurring automation, cloud/background provider worker or scheduled continuation created. Guard covers child commands, not app-turn/UI enforcement; parent stops tools and checkpoints before cutoff. OS signal denial/group escape require stronger isolation and are reported, never claimed stopped. All agent work completes before handoff.

Blockers: complete account exports/project documents unavailable; protected Documents/Codex; shell access to T7; exact model/account execution receipts; provider spend/budgets; Cloud Scheduler coverage; live Render/Drive deployment dependencies; full Wilmington grading template; personal replacement destination/auth/timezone/test acceptance.

## Katherine after 6:00 AM

1. Configure the school execution account using the two unchanged heartbeat IDs/target threads; confirm model and browser/Hub source/destination receipt before any ownership cutover.
2. Keep all old accounts/repositories/schedules until unique exports/project documents and dependency checks pass. Choose encrypted archive handling for T7.
3. Use existing UD personal tasks while replacement contracts remain staged. No funding or new connector approval is needed to read the foundation.

Review [the private draft foundation PR](https://github.com/kvond/answerable-skills/pull/1) and retirement markers; do not deploy the runtime or delete legacy repositories from this report alone.

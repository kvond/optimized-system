# Cloud and legacy Render inventory gap check — 2026-10-12

This is a bounded inventory audit, not retirement clearance. No deployment, cloud setting, API enablement, authentication, source execution, database read, secret payload read or deletion occurred.

## Exact legacy deployment evidence

The accessible `kvond/feedback-system` clone at commit `c63d493ef741d6163be5edac09830c2447d65695` contains:

- `STATUS.md:17–21` (dated July 9) identifies the private repository, Render automatic deployment on pushes to main, Google Drive teaching Agenda/Teacher Dashboard consumers, and personal-account application authorization. This is historical source documentation, not current live acceptance.
- `render.yaml:2–16` defines a web service named `feedback-system`, starter plan, requirements installation, Uvicorn `app.main:app`, `/healthz`, and a persistent disk `feedback-data` mounted at `/var/data`. The plan declaration is not a current bill or measured spend.
- `webapp/app/main.py:163–243` still contains drafting, review/send and rubric routes; `:436–474` and `:603–651` contain research scanning, sheet append and follow-up send paths. Source presence does not prove these are enabled, invoked or deployed now.
- `webapp/app/usage.py:80` appends usage metadata and `webapp/app/discuss.py:152` appends discussion responses. Persistent state may therefore require preservation beyond a Git bundle. No such records were opened.
- `STATUS.md:56–64` describes demo/test/live sending and an earlier Composio Gmail verification. Current connection validity, recipient destinations, mode and provider billing remain unverified; no environment values were inspected.

The accessible `kvond/answerable-pipeline-backup` clone at commit `9f767c70c21b74f1beee423b5b5ab51111de8618` identifies the exact consumer host [feedback-system-u1br.onrender.com](https://feedback-system-u1br.onrender.com) in `docs/Render_App_Change_Spec.md:1–11`. Its August 10 specification retires the old grading/email flow but retains roster/rubric/research views. `MANIFEST.md:161–169` describes the same application and a Schoology → Drive → app roster feed, explicitly leaving the actual folder ID/connect instructions unresolved. These documents are specification/history; no verified deployment applying the retirement was found. The inspected feedback app still contains the old routes, so implementation/deployment linkage cannot be inferred from the specification.

Other accessible Answerable snapshots: `answerable-teaching-system` commit `4c6d2c8275a3651bc023f51b6f403612792385fe`; `Answerable-Teaching` commit `76acdd7c999fc25a63081164bdcbfc26cd36fa91`. `answerable-teaching-system/LIVE-WORKFLOW.md` describes September Google Sheets formula updates and explicitly does not imply a scheduled external runtime. Bounded text searches found the explicit Render hostname in pipeline documentation; they do not establish every external consumer or deployment dependency.

## Render live coverage blocker

`command -v render` returned no installed Render CLI. Computer/browser surface inventory showed Chrome PROFESSIONAL and Katherine profiles but no existing Render dashboard/application tab. No credential/config/token files were inspected, and no new login flow was initiated. Therefore authenticated Render service identity, linked Git repository/branch, deployed commit, current service status/plan, persistent disk inventory, backups, environment binding presence and request/job usage remain unverified. The known hostname was not invoked: even a public health response would not prove consumer independence or private-state preservation.

The smallest next read-only action is to open the existing authorized Render dashboard and inspect this named service's Overview/Settings/Deploys metadata: service ID, linked repository/branch, deployed commit, disk names/mounts and linked resources, without opening environment values or private logs/data. Match deployed commit to the preserved Git source before any retirement decision. Then separately map the documented Drive/Sheets/Gmail consumers and persistent-state preservation with explicit scope. An archived Git repository is not evidence that a deployment or consumer stopped.

## Google Cloud coverage and its limits

The original `ai-ops/reports/cloud-inventory.md/.json` inventories only accessible projects `school-workflow-hub-54879` and `graceful-fold-341018`. It returned zero Cloud Run jobs in both, but Cloud Scheduler was explicitly BLOCKED because its API was disabled in both; this is not a verified empty scheduler inventory. APIs were not enabled. Other projects/accounts, Render, Apps Script triggers, Codex automations, launch agents and browser integrations are outside that inventory.

The later `ai-ops/reports/cost-cutting-cloud-2026-10-12.md` records School Hub revision `school-workflow-hub-00273-fkl`, service cap1, revision min0/max20 and CPU throttling. This supersedes the older inventory's school revision for that later observed snapshot. Personal Hub revisions remain `personal-hub-api-00001-dkz` and `personal-hub-mcp-00001-q8k`, service cap20; absent minimum annotations are not measured idle cost. No current bill, utilization, actual instance counts or provider budget validity was verified.

Original metadata leaves legacy Anthropic/runtime secret consumers unresolved, inherited IAM/application authentication unverified, and private Firestore contents deliberately unread. Personal Hub build provenance matches the deployed image digest but does not identify an inspected Git commit. No named Answerable Cloud Run service/job was observed in these two projects; that does not exclude Render or external consumers. No evidence justifies disabling/deleting resources, removing secrets, discarding disks or claiming dollar savings.

## Result

Closed: exact documented legacy Render hostname, source commits, declared persistent disk, surviving code consumers and conflicting historical retirement specification are now recorded together. Still open: authenticated Render metadata, source-to-live linkage, source feed mapping and private persistent-state preservation. Google Cloud scheduler and external-platform coverage gaps remain explicit. All findings are metadata/source evidence, not retirement clearance.

## Bounded ordinary dashboard check — same-day follow-up

One normal navigation to `https://dashboard.render.com/` in the established Katherine Chrome profile redirected to `https://dashboard.render.com/login?next=%2F`. Visible page heading: **Sign In to Render**; GitHub/GitLab/Bitbucket/Google buttons and empty Email/Password fields were displayed. This establishes no authenticated dashboard session in that checked profile, not the absence of a Render account or deployment. No login button, credential field, SSO, permission or terms control was used. No application endpoint, deploy/wakeup button, Environment values, logs or private data were invoked. The agent-created intermediate tab was closed. Current live metadata therefore remains blocked by unavailable authenticated Render access; other profiles/account sessions were not probed.

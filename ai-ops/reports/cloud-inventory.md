# Read-only cloud inventory — October 11, 2026 Eastern

Evidence: current `gcloud` project, Cloud Run service/job, enabled API, Secret Manager metadata, billing association, Firestore database, Storage bucket, Artifact Registry repository, and Run IAM policy reads. Machine-readable evidence is `work/cloud-inventory.json`. No cloud configuration changed, no secret payload accessed, no model call or purchase made.

## Visible resources

| Project | Cloud Run | State |
|---|---|---|
| school-workflow-hub-54879 | school-workflow-hub, us-central1 | Ready school-workflow-hub-00267-wrx, 100% traffic; Ready timestamp Oct 11 17:18 Eastern |
| graceful-fold-341018 | personal-hub-api, us-east4 | Ready personal-hub-api-00001-dkz, 100% traffic |
| graceful-fold-341018 | personal-hub-mcp, us-east4 | Ready personal-hub-mcp-00001-q8k, 100% traffic |

Run jobs: zero returned in both projects. Cloud Scheduler inventory: BLOCKED because `cloudscheduler.googleapis.com` is disabled in both projects. The empty collection in the initial script was corrected to an explicit coverage block. No API was enabled. Codex automations, Apps Script triggers, launch agents and external projects are not covered by this cloud inventory.

Hub has IAP enabled and its Run invoker policy grants only the IAP service identity. Runtime uses the project's compute service identity. Service max-instance setting is 1; revision template retains max20 and min0. CPU request throttling is enabled. 1 CPU/512 MiB configured. Environment presence includes Agenda, roster, grading, assignment-specific Forms, IC map, student records, feedback roots, and state configuration. The OpenAI key is referenced through Secret Manager `hub-openai-api-key`, version1. This proves binding presence, not validity or usable budget. Anthropic and two earlier runtime secrets remain listed as metadata only; whether anything still uses those secrets was not established.

Personal Hub API has no bindings in the returned service-level IAM policy. Personal Hub MCP grants `allUsers` Run invocation and has a Secret Manager path-token binding. Authentication enforcement in the actual application is unverified; do not label the token-bearing endpoint secure solely from this metadata. Both use the same `personal-hub-api` service identity and have Firestore environment settings. Their service max-instance setting is20; no explicit min-instance setting was returned. These deployments were created September15 and are separate from the school project.

Firestore: Hub default native database in us-central1, deletion protection enabled, PITR disabled, one-hour version retention. Personal default native database in northamerica-northeast1, deletion protection disabled, PITR disabled. Data/document contents were not read. Both billing enabled; actual current spend, quotas, budgets and alert coverage not verified.

Storage metadata: one Hub Cloud Build bucket, one Personal Cloud Run source bucket. Artifact Registry: Hub roughly2.98 GB source deployment repository plus85 MB gcr.io repository; Personal roughly135 MB deployment repository. These are reported stored-image metadata sizes, not billed expenditure. No image or build-source deletion performed.

## Existing architecture worth preserving

Local source contract read: `/Users/katherinevonduyke/Documents/Claude/school-workflow-hub/docs/START_HERE.md` and README. This checkout may lag live code; its provider prose names older Anthropic approval while current deployment references OpenAI. Treat current authorized-session instructions and deployed evidence as primary.

The reusable patterns are one authenticated Cloud Run control center; private durable state; stable lesson/assignment/source identities; shared manual and scheduled operation entry points; deterministic Python scoring; distinct Notes and Revision denominators; source-version and history preservation; idempotency/claim/receipt gates; saved feedback that can be reopened/printed without another model call; explicit coverage holds; and destination reload/readback. Cloud hosting supplies no IC browser session. Current browser-companion grading acceptance must be independently checked before live-operation claims.

## Answerable dependency finding and minimal next steps

No named Answerable Cloud Run service or Run job appears in the two accessible projects. A bounded textual search of `/Users/katherinevonduyke/Documents/Claude/projects 2/Answerable-Teaching` across common code/config/doc extensions found no Google Cloud, personal-hub, graceful-fold, run.app, or school-workflow references. This does not prove independence: other accounts/projects, DNS, Cloudflare/GitHub Pages, browser configuration, encrypted/local settings, source in other folders and external integrations remain possible. Preserve old services, artifacts and databases until their actual users and data dependencies are mapped.

Use the existing Hub for school workflow processing rather than starting another runtime. For a new research-facing component, keep its authorization and data scope explicit and reuse verified infrastructure only after locating its storage/API contract. Do not connect a public MCP route to school data by assumption. To contain cost, retain scale-to-zero and the Hub cap; separately review Personal Hub max20, artifact retention, API usage/budget settings, and Firestore protection when authorized. No automatic cleanup, retirement, deployment or budget change is justified by this inventory.

Blockers: scheduler service disabled; no actual billing-spend/API budget evidence; no authenticated UI or worker-path acceptance; no old Answerable service dependency proof; no file contents or Firestore document contents inspected. `/Users/katherinevonduyke/Documents/Codex` read was denied; the Claude mirror was readable.

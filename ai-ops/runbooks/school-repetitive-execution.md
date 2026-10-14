# Repetitive school execution

Use the seven existing [school definitions](../workflow-contracts/definitions/)
and [school operations procedure](../workflow-contracts/school-operations-runbook.md).
This package supplies bounded invocations and private evidence checks. It is not
a second contract catalog, checklist, scheduler, grade writer or email outbox.
Actual school execution stays in the existing workflows and helper. Analysis,
code changes and implementation repairs remain with Codex.

Resolve private bindings through the current trusted configuration. Never copy
account IDs, endpoints, file IDs, browser profiles, credentials, student records
or source bodies into this repository. A school Google connection is a data
identity; it does not identify the executor or prove a school-computer runtime.

The current home Codex owner remains in place. School Claude and the school
computer require their own live bounded trial before migration. UD Claude Code
on the home Mac is independently code-capable and may already own other work;
do not start another task there or grant its pending browser permission. A
team-local browser lease does not exclude that independent session. Prefer
connector reads that do not navigate its shared browser. Do not retry or
reconnect a quota-exhausted Desktop Commander service.

## Select and invoke an existing operation

Resolve the exact workflow/action and existing owner before choosing an executor.
For actual routed execution, use the [canonical router interface](../../skills/ai-operations-router/references/interface.md):
`route_workflow` checks all required dependencies, even for one selected action.
Never mark unchecked dependencies passed to get a safe-looking substep through
the broader workflow. An independently authorized capability read can gather
evidence while a workflow remains held; label it as a trial, not that workflow's
completed action. The helper below is such an evidence comparison, not a router.

| Bounded operation | Existing governing workflow | Result required |
| --- | --- | --- |
| Read current report, dated header, source link or receipt status | `school-morning-report-resolution` | Exact account/source/date/run identity and bounded findings; unavailable fields named |
| Navigate an existing authorized page | Selected existing school workflow | Exact destination/account after navigation; global browser ownership clear first |
| Check file placement without moving it | `school-morning-preparation-and-repair` | Actual source ID, current parents and exact registered destination; no same-title substitution |
| Apply an already-authorized verified placement repair | Existing preparation workflow only | Complete current IC identity, exact source/destination, permissions, fresh version, existing preview/apply/verify and native readback |

Only the first three are appropriate capability trials here. Placement writes
require their full existing workflow and before-07:00 source mutation window;
this package does not perform them. IC remains the canonical roster, including
the complete-scan rule and preservation of former students and history. A
filing identity never establishes grade identity. The existing Chrome helper
alone enters grades. Uncertain save/send/readback stops dependent work; it is
never retried or cleared by a fallback. Feedback, delivery and their existing
outbox keep their present owners. Printed and Handed remain teacher-controlled.

## Reusable read invocation

Use this complete prompt after resolving the bracketed references privately:

> Read only [exact bounded source/range] under [existing workflow ID and action]
> using [verified current executor and school data connection]. Read the
> canonical definition and its current source procedure first. Preserve the
> current owner and resolve actual external writer conflicts. Prefer the
> connected read API; browser navigation requires its global lease. Verify the
> exact account binding, native source ID/tab/range, report date and run ID if
> present. A file modified time is not a report/run date. Read only the smallest
> necessary content; repeat the same bounded read once for comparison when safe.
> Record checked fields, unavailable fields, revision/content changes and one
> exact next step in the existing private evidence destination. Never infer
> missing work, scores or a completed morning run from a header or failed read.
> Make no source, roster, grade, feedback, email, notice, schedule or teacher-mark
> changes. Do not create a second checklist or source copy. Save and read back
> only the bounded private result. Keep source bodies and student names out of
> the public response and Git. A blocked dependency leaves the current owner in
> place; continue independent permitted reads and report the exact limitation.

For navigation, replace the first sentence with “Navigate to [exact existing
authorized page] and read only [bounded element].” Verify the browser account
before and the native URL/source after. Do not select another provider's prompt,
type into a form, toggle state, open a new task, or disturb an active writer.

For placement checks, replace the first sentence with “Read metadata for [exact
registered file] and [existing destination folder]; compare source ID, parents,
MIME type, revision and access evidence.” Missing parents/access fields stay
unavailable. A private listing or copied file alone does not prove complete
native placement or broaden the workflow's write authority.

## One exception and continuation handshake

Record one compact entry in the existing private issue record:

> [Issue reference] — [exact class/section, lesson and verified source link; name
> unverified fields]. Checked: [bounded evidence]. Held: [specific cause and
> consequence]. Next: [smallest action] — owner [current owner]. If a genuine
> teaching/access choice is required: 1. [one question with concrete choices and
> evidence-backed recommendation]. Continue independent work while pending.

Use at most three questions in the coordinator's one batch. Unchanged provider
failure is not a new question. No reply is not approval. On an answer, reread
the exact source and ownership evidence, apply the answer only to its pending
scope, and resume without another “continue.” A changed source or passed cutoff
holds only its dependent write for the existing safe window. Do not certify
other assignments from one checked panel.

For machine handoffs, use `workflow_router.build_handoff` and its existing
`handoff.schema.json`: `canonical_source_ref`, receipt-backed `completed`, exact
allowed-action `remaining`, `output_refs`, unchanged `next_owner_ref`, and one
`next_step`. A standalone read trial is not completion of the broader repair
action and must not be inserted as one. No alternative handshake schema or
ownership cutover is introduced here.

## Bounded connector-read evidence helper

`ai-ops/runtime/school_read_trial.py` compares two actual captured Sheets reads
against a frozen private binding, then creates and byte-reads a new local
private summary. It makes no network calls. It validates the existing school
definition and source reference, checks exact native source/connection/range,
freshness/order, provider errors, nonempty content and unchanged response hash.
The trial is capped at 200 cells and 50 rows. It never certifies account identity,
report date, destination capability or full workflow completion.

Keep all inputs/output outside Git. A binding has `source_id`, `link_id`, `range`
(exact native A1 range including quoted tab). Each capture has `tool` set to
`google_drive.get_spreadsheet_range`, the actual `request` arguments, actual
`source_metadata` structured response, actual complete connector `response`,
and an aware `observed_at`. These are evidence envelopes, not new workflow
contracts. The operator must capture real calls; synthetic fixtures or a
handwritten assertion cannot establish a live account/capability test. Metadata
must be freshly read with the same connection. Use native sheet metadata first
to resolve the tab and keep the exact range small.

```sh
python3 ai-ops/runtime/school_read_trial.py \
  --workflow ai-ops/workflow-contracts/definitions/school-morning-report-resolution.json \
  --source-ref private:existing-hub-tasks-checklist \
  --binding "$TRIAL_PRIVATE/binding.json" \
  --before "$TRIAL_PRIVATE/before.json" --after "$TRIAL_PRIVATE/after.json" \
  --output "$TRIAL_PRIVATE/comparison.json"
python3 -m unittest discover -s ai-ops/runtime/tests -p test_school_read_trial.py -v
```

Set `TRIAL_PRIVATE` to the existing approved private evidence location, outside
the checkout. Output is mode 0600, never overwrites an existing artifact, and
contains hashes and symbolic references without source values. Exit 0 means
bounded reads matched and the local output was read back; 2 means a saved hold;
1 means invalid input or local output failure. None means a completed school
workflow or a successful remote output write. A matching range says nothing
about uninspected rows, complete roster/source coverage or omitted revisions.
If report date, native revision, access metadata or run ID is absent, record it
as unavailable; never replace it with file modified time or the current clock.

Rollback is simply to stop using this optional invocation/helper. No service,
account, workflow owner, production record or schedule was changed. Preserve
its private evidence and the existing workflows. The coordinator alone handles
any later reviewed migration and one-owner cutover.

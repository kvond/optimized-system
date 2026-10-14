# Portable workflow definitions

`workflow.schema.json` describes sanitized reusable workflow requirements. It is
additive to the existing runtime execution-request and route schemas. Do not
replace `runtime/contracts.schema.json`, `runtime/routes.schema.json`, or the
controller's request interface with this catalog format.

Validate a definition without dispatching work:

```sh
python3 ai-ops/runtime/workflow_contract.py path/to/workflow.json
python3 -m unittest discover -s ai-ops/runtime/tests -p test_workflow_contract.py -v
```

`workflow_contract.validate_workflow(definition)` returns an independent copy or
raises `ContractError` with field paths, never the submitted values. It adds
cross-field action-conflict and distinct source/output-reference checks to the
JSON Schema shape. The CLI does not resolve accounts, create state, read a
browser, activate schedules, write outputs, or execute the workflow.

## Shared interface

| Field | Meaning |
|---|---|
| `schema_version` | Integer `1` for this interchange format. |
| `workflow_id`, `contract_version`, `title`, `domain` | Stable workflow identity and reviewed requirement revision. IDs/domains use lowercase hyphenated names. |
| `owners` | Separate `execution_owner_ref` and `maintenance_owner_ref`; a role label is not a tested capability. |
| `execution` | `executor_ref`, `account_refs`, `required_capabilities`, `privacy_partition`, `concurrency_key`. A Google data account and a coding executor are separate references. Capabilities are lowercase hyphenated registry keys. |
| `trigger` | `kind: on_demand`, or `kind: existing_schedule` with exact `schedule_ref`. Preserve the schedule registry's namespaced inventory key, such as `Local Codex::example-task`. |
| `sources` | Distinct `source_ref`, boolean `required`, `coverage: complete` or `bounded`, positive `max_age_seconds`. Freshness is a requirement, not a current observation. |
| `outputs` | Distinct `output_ref`, `kind: artifact`, `report`, or `receipt`; `verification: content_and_destination_readback`. |
| `policy` | Disjoint `allowed_actions` / `prohibited_actions`, explicit `dependency_checks`, and `uncertain_write_policy: stop_and_reconcile`. |
| `success_checks` | Nonempty concrete checks for completed work. Configured schedules and an open page are not completion checks. |
| `failure` | `max_safe_read_retries` from 0–3, boolean `continue_independent_work`, and `report_next_step: true`. Retry count applies only to safe reads, never uncertain writes. |
| `provenance` | `contract_refs` identifying governing current rules and prior decisions. Reference names do not prove the references have been read. |

Use symbolic references only for private accounts, sources and output locations.
Keep account IDs/emails, browser profile locations, source bodies, student data,
credentials, tokens and runtime state out of these committed definitions.
Arbitrary strings are not automatically sanitized by a schema: review content
before committing. Private registry resolution and live capability evidence
remain outside the portable contract.

Concurrency keys must be resolved to a shared exclusive writer lease before
work; merely declaring a key provides no locking. Multiple providers using the
same browser or source writer must resolve to the same lease. Agents can
continue independent reads without treating an unavailable source as empty.

## Acceptance boundary

These definitions have no `enabled`, `approved`, or `completed` field. Parsing
success supplies none of those claims. Before execution, the operator must
independently resolve current authorization, capabilities, private account and
source bindings, dependency evidence, and concurrency ownership. Runtime work
still needs exact source revisions, its existing request/route contracts,
deadline supervision, private receipts and actual output readback. Live
verification state belongs in receipts and the current operational checklist,
not in a stale reusable definition.

Unknown bindings remain blocked. Preserve complete prior state after partial or
failed reads. An uncertain save stops dependent writes until its exact existing
receipt and destination are reconciled; the schema never clears that block.

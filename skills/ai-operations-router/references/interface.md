# Router integration interface v1

Runtime: `ai-ops/runtime/workflow_router.py`. Standard library only; no network, provider call, state write or process launch. It reuses `workflow_contract.validate_workflow`, `foundation.Route` and `foundation.select_route`. This interface is separate from the pre-existing runner request and does not replace its cache, budget or receipt machinery.

## Entry points

- `route_workflow(workflow, request, capability_evidence, *, now, rules=None)` returns `ready` or `blocked`. `now` is an aware Python datetime, supplied by the execution host. Production callers use their actual clock; an explicit CLI clock is for reproducible offline checks.
- `resolve_intent(workflows, intent)` accepts `{workflow_id, domain, operation}`, each either an exact string or null. It returns `resolved` only for one matching workflow with explicit domain and operation, otherwise one `question`. It does not classify prose or infer an operation from a title.
- `resume_intent(workflows, pending, answer)` consumes the same three fields as a complete answer. It preserves previously supplied scope and catalog fingerprint. `answer=None` returns the same question, never permission. Resolved intent must enter `route_workflow` with fresh evidence before execution.
- `build_handoff(workflow, *, decision, canonical_source_ref, completed, remaining, output_refs, next_owner_ref, next_step)` emits the handoff schema. Completed entries are `{action, receipt_ref}`; the caller must have read those real receipts. Remaining entries are exact allowed action IDs. Next owner must be the contract's existing execution owner; a new owner needs a separately authorized contract cutover first.

Malformed inputs raise `RoutingError` (or `ContractError` for the definition). Valid but unavailable inputs return a blocked decision with one `next_step`. Input errors name fields without echoing payloads. Reference fields and decisions are still private operational data; store them privately.

## Request

Exact top-level fields:

| Field | Value |
| --- | --- |
| `schema_version` | Integer 1 |
| `request_id` | Stable private run reference |
| `workflow_id`, `domain` | Exact catalog fields |
| `operation` | One exact `policy.allowed_actions` entry |
| `execution_kind` | `deterministic`, `coding`, `browser`, or `assisted` |
| `authorization` | Stamp plus `state=authorized|unknown`, `allowed_actions` list |
| `ownership` | Stamp plus `state=clear|competing|unknown`, `owner_ref` |
| `receipt` | Stamp plus `state=clear|uncertain|unknown` |
| `sources` | Source evidence array below |
| `dependencies` | Stamp plus `check` (exact dependency text), `state=passed|held|unknown`, per dependency |

A **stamp** has `observed_at`, `expires_at`, `evidence_ref`. Dates are timezone-aware ISO strings. Authority, ownership, receipt and dependency evidence must be current, within the rule's maximum context age (300 seconds) and before explicit expiry. Expiry is exclusive; future observations fail. The resolver must inspect external writers, not merely this team's locks. `owner_ref` must match the contract's execution owner. Missing receipts are `unknown`, never `clear`.

Each source entry has exactly `source_ref`, `expected_revision`, `revision`, `coverage`, `observed_at`, `evidence_ref`. Coverage is `complete|bounded|partial|unavailable`; revisions may be null only to represent missing evidence. Required missing/partial/unavailable/stale/changed sources block. Bounded reads satisfy only bounded contracts. Optional unusable sources remain explicit in `unavailable_sources`; downstream code must not turn them into empty data or claim full coverage. Expected revisions must come from the trusted frozen source manifest, not be set to whatever a later read returned.

Every required contract capability and dependency is required conservatively even when routing a single action. This can hold a safe substep when a broader contract has unmet dependencies; define an explicitly reviewed narrower contract rather than silently dropping requirements. A dependency that says to acquire a lease must not be marked passed before acquisition. The bridge may inspect the dependency hold, acquire the known contract lease, and call the router again. Do not use preflight as a grant.

## Capability evidence

Exact container: `{schema_version: 1, routes: [...]}`. Each route has:

| Field | Meaning |
| --- | --- |
| `route_ref`, `provider_ref` | Opaque exact tool/adapter and provider references |
| `executor_ref` | The exact contract executor reference, possibly a private symbolic binding |
| `resolved_executor_ref` | Actual runtime identity resolved privately, e.g. `home-codex` |
| `account_refs` | Exact contract account reference set, with identity verified separately from executor |
| `domain`, `privacy_partition`, `operation` | Exact tested scope, never wildcard |
| `execution_kind` | Same enumeration as request |
| `capabilities` | Explicit tested capability IDs; must cover all contract requirements |
| `resource_rank` | Nonnegative integer describing relative resource size for cost ties |
| `estimated_cost` | Supplied nonnegative fixed-point dollar string, at most six decimals, or null |
| `cost_basis_ref` | Private reference to the measured/approved basis for the estimate, or null |
| `status` | `tested|unverified|blocked` |
| `identity_verified` | Actual boolean; true only after checking the exact identities in this test |
| `observed_at`, `expires_at`, `evidence_ref` | Test-observation stamp |

Unverified/blocked observations still carry the date and reference documenting the failed or unavailable check; they never route. Tested evidence expires at the earlier of its explicit expiry or the rule's maximum capability age (one day). A new source, account, operation or executor requires its own exact test. The private evidence store is trusted input, not a self-certifying claim generated by an LLM. The router cannot authenticate an evidence reference or prove a claimed live test occurred.

A request of `assisted` permits an exact sufficient deterministic route as well as an assisted route, preferring deterministic via the existing foundation. Other requested kinds are exact. Among sufficient routes of that class, the foundation chooses the cheapest supplied estimate, then the smaller resource rank, then stable route name. Unknown cost or cost provenance is ineligible. No price defaults, billing calls or savings calculations are added. A deterministic route can only execute a real installed handler verified for that operation; the string `deterministic` is not proof.

`executor_ref` matches the contract's preserved binding; `resolved_executor_ref` enforces actual executor rules. An unresolved `existing-*`/`private:*` actual runtime or conflicting actual resolutions is held. This permits Agent05's symbolic contract references without treating them as actual capable destinations. Rules are reviewed policy, not operator request data. Default rules keep coding at home Codex, limit School Claude to browser kind, and restrict IC helper capability/actions to the existing Chrome helper. Evidence and rules do not expand authority.

## Decision and execution boundary

Both decisions contain `workflow_id`, `contract_version`, `request_id`, `owner_ref`, `validated_at`, `contract_sha256`, `request_sha256`, `evidence_sha256`, `rules_sha256`, `rule_version`, `execution_attempted=false` and one `next_step`.

`blocked` adds `reason` plus an exact source ref, dependency index or ineligible route reasons when applicable. A dependency index is zero-based into the original contract array. A blocked decision contains no chosen route.

`ready` additionally names the exact route, declared/resolved executor, provider, accounts, operation, actual selected kind, partition, capabilities, concurrency key, cost input/basis, capability evidence ref, optional unavailable sources and `valid_until`. Digests bind the evaluated snapshot; they are not signatures, replay protection or authority. There is no execution success status.

The existing bridge acquires the contract's single-owner lease, freezes sources, checks adapters and calls again with fresh evidence immediately before action. It uses existing budget reservations where applicable, preserves uncertain progress, and demands native output readback. This router neither manufactures that readback nor retries. A global external writer remains a hold even if the local SQLite lease succeeds.

CLI:

```sh
python3 ai-ops/runtime/workflow_router.py WORKFLOW.json REQUEST.private.json EVIDENCE.private.json
```

Exit codes: 0 means route ready, 2 means blocked, 1 means invalid input. All three mean execution was not attempted. The CLI prints reference-only JSON and writes no files. Actual private request/evidence files and receipts must remain outside Git.

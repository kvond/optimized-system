# Offline runtime acceptance

The runtime suite covers archive preservation, private cache/receipts, deterministic execution, budget reservations, bounded local stopping, compact source-verified context and encrypted-drive storage. The [current implementation receipt](https://github.com/kvond/optimized-system/blob/d37f28ccd3a75a77698ace812d54e74c6d0ce71a/ai-ops/reports/runtime-cost-results-2026-10-12.json) records the latest full-suite count and duration; the previous checkpoint had 41 tests. These are synthetic/local acceptance checks; no cloud deployment, school workflow, paid provider, scheduled account or live connector is accepted by this suite.

## Run and inspect

From the repository root:

```sh
python3 -m unittest discover -s ai-ops/runtime/tests -v
mkdir -p ../runtime-demo
python3 ai-ops/runtime/runner.py --demo --state ../runtime-demo/private.sqlite > ../runtime-demo/first.json
python3 ai-ops/runtime/runner.py --demo --state ../runtime-demo/private.sqlite > ../runtime-demo/repeat.json
cmp ../runtime-demo/first.json ../runtime-demo/repeat.json
```

Expected demo readback: `components.sum.output.sum` is10, status `complete`, execution kind `deterministic`, `provider` and `model` are null, and `paid_dispatches` is0. The result payload, SHA256 and completion receipt commit atomically in a private SQLite row. `result_location` specifies the absolute private database, table and request key. Repeating the same demo returns the original receipt after revalidating source access, coverage, revision and content hash. A fresh state path generates a new receipt timestamp/location; output and source/result hashes remain reproducible. Keep SQLite files and private output receipts outside Git. GitHub may contain sanitized contracts and code, not raw private result content.

`Controller.execute(request)` validates bounded component requests and routes at runtime. It requires genuine booleans, nonnegative integer capabilities, fixed-point finite prices and explicit privacy strings. Missing authorization, incomplete coverage, unreadable/stale sources, wrong revisions and hash mismatch remain blocked per component; no success cache masks these conditions. A changed component revision requires a new request identity and recomputes only that component when other cache entries remain valid. Source observation age and cache expiry are checked again before the atomic commit. Conflicting inputs or route version under an existing request ID are rejected. Concurrent identical requests may compute the same trusted pure handler; atomic commits produce coherent identical receipts. Sequential retries reuse only eligible unexpired successful cache entries; expired entries recompute even when the result/receipt bytes remain identical. Adapters and handlers run outside SQLite write transactions. A stalled trusted callback does not block database writers. Handlers must be pure/read-only; external write effects require a separately designed executor. The controller does not enforce callback deadlines: run it under the external `run_bounded` supervisor for bounded local operation. Source snapshots remain point-in-time evidence; a future live adapter must supply source-specific concurrency/version guarantees.

`Controller.readback(receipt)` verifies the committed result and receipt hash/status/location. Readback proves artifact integrity. Invoke `execute` again to validate current source eligibility before reuse. A partial receipt stays partial, even if some components completed.

## Paid execution remains disabled

The runner selects only implemented, enabled, zero-cost deterministic handlers in the explicit privacy partition. AI/paid routes never dispatch. Declared provider/model configuration is not provider verification or spending permission; unknown executed provider/model fields stay null. No provider adapter or network calls are installed in this controller. Local cache partitioning is not user authentication. Adapters must independently authorize their actual caller and source scope.

`usage.UsageLedger(private_path, business_timezone="America/New_York")` provides a metadata-only reservation/receipt interface. Configure operator-approved daily and monthly caps for all three scopes before any future paid attempt:

- `configure("combined", daily=approved_daily, monthly=approved_monthly)`
- `configure("workflow:" + workflow, daily=approved_daily, monthly=approved_monthly)`
- `configure("provider:" + provider, daily=approved_daily, monthly=approved_monthly)`

`reserve(request_id=..., workflow=..., provider=..., model=..., estimated_cost=...)` fails closed on missing caps, unknown/invalid prices, exhausted scope or conflicting identity. Returned `new=False` is an existing reservation/state, never fresh dispatch authority. Pending costs remain liabilities across midnight/month rollover and restart. The estimate must be an approved bounded price, not a guessed cost.

`settle(request_id, receipt_id=..., actual_cost=..., input_tokens=None, cached_tokens=None, output_tokens=None, duration_seconds=None, status=..., retry_state=..., error_code=...)` records verified actual cost and bounded symbolic metadata. Unknown token counts remain null. Duplicate matching receipts are idempotent; conflicting/reassigned receipts are rejected. Actual overruns are retained and block future overspend. Keep uncertain calls pending until reconciled. `receipts()` and `alerts()` expose local metadata and deduplicated50/80/100% cap alerts; alerts do not send notifications. This interface alone does not authorize paid dispatch or guarantee a provider obeys estimates. The foundation's simpler partition budget primitives and this multi-scope ledger are separate interfaces; choose one authoritative accounting path in a future adapter rather than debit both.

## Required before deployment or live use

Verify caller authorization, scoped source access/revision coverage, current deployed code/image, bounded reads, private durable storage, atomic cloud reservations and receipt readback. Obtain the actual approved spend limit and historical usage before enabling a priced route. A Cloud Run replica must use a transactional durable cloud adapter; do not deploy SQLite on its ephemeral filesystem. The existing personal MCP secret-path prototype needs appropriate authentication/scopes before sensitive expansion. Preserve school job/account ownership and existing deployments.

Any new background operation needs its own authorized deadline. The expired reset guard remains an expired guard, not daytime scheduling permission. `run_bounded` reports signal/reap uncertainty honestly and reserves cleanup time; OS/container supervision is required for an enforceable absolute cutoff when children escape groups or the OS denies/delays signals. A passing local suite or demo receipt does not establish live deployment, provider, scheduler, browser or destination acceptance.

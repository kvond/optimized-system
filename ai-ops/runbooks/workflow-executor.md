# Local workflow executor and recovery

This bridge implements one bounded operation: validate an explicitly configured local workflow catalog. It connects the canonical v1 contract and evidence router to the existing `runner.Controller` and its atomic `runner_requests` result/receipt storage. It does not dispatch model requests, shell commands, browser operations, school grades, feedback, email, notices or physical printing. It installs no worker or schedule.

## Entry point and trusted configuration

Import `WorkflowExecutor` and `CatalogValidationAdapter` from `ai-ops/runtime/workflow_executor.py`. Create the adapter from an explicit trusted allowlist of one to 64 regular local JSON files, each at most 64 KiB. Files, parent paths and state may not be symlinks. The adapter uses the existing contract validator; its saved output contains only workflow IDs, contract versions, content hashes and a count. A duplicate workflow ID or malformed definition blocks execution.

The canonical definition is `ai-ops/workflow-contracts/definitions/technical-catalog-validation.json`. Select it through `resolve_intent` with domain `technical` and operation `validate-workflow-catalog`; do not substitute the synthetic test fixture for a canonical run. The exact supported contract binding is:

- Domain `technical`, execution kind `deterministic`, resolved executor `local-deterministic-runtime`, provider `local`, cost `0`, no accounts.
- Required capability list exactly `local-catalog-validation`; sole allowed operation `validate-workflow-catalog`.
- One required complete source, bound to the adapter's `source_ref`; one output bound to its `output_ref`. The default references are `source:canonical-workflow-catalog` and `output:catalog-validation`.
- An explicit concurrency key, the current execution/maintenance owners and the ordinary canonical policy, dependency, success and failure fields.

These declarations are requirements, not capability or permission evidence. The caller supplies `resolve(lease_or_none) -> (request, capability_evidence)` using the exact router interface in `skills/ai-operations-router/references/interface.md`. This is trusted, bounded read-only integration code, never a callback loaded from request JSON. It must actually reread the current authority, exact operation, native owner/receipt status, capability test, source revisions and all dependencies. An available account or installed tool is insufficient. No API accepts shell argv, arbitrary module names or remote execution endpoints.

For the local lease dependency use the exact string `Local catalog execution lease held`. Mark it unknown before the claim and passed only while the supplied lease is held. The bridge permits that single unresolved dependency during preflight; all other gates must pass when the router is evaluated again after claiming. Never use this local lease to attest school/native browser fencing.

Call:

```python
paths = resolve_storage()  # Existing storage resolver; no fallback or mount action.
adapter = CatalogValidationAdapter(reviewed_catalog_files)
executor = WorkflowExecutor(adapter, paths=paths)
result = executor.execute(workflow, fresh_private_resolver, deadline=aware_deadline)
```

The caller's resolver and allowlist are trusted application configuration outside Git when private. The library is not a generic command-line dispatcher. A ready decision is reevaluated under the lease, then again immediately before one fixed runner invocation. Expected input identity, actual file hashes, source revision and exact selected route are checked. The action deadline is the earlier of the caller deadline and the fresh router decision's validity. Reads have the contract's zero-to-three retry limit; execution, output saves and readback are never automatically retried. Count/byte limits bound the local adapter; the trusted resolver and filesystem must remain responsive. This does not claim OS isolation or preemptive interruption of arbitrary caller code.

## Storage, health and result proof

Production mode reuses `storage.resolve_storage`, the existing `cache.sqlite`, permission checks and encrypted archive mount/backing-image verification. It rechecks storage before every coordinator write. A missing mount, changed metadata, public directory/database or symlink fails closed. The bridge never mounts media, changes permissions, creates a second root or modifies configuration.

Mounted-image encryption is verified from the uniquely matched fresh `hdiutil info -plist` entry's real boolean `image-encrypted`. False or a nonboolean value fails closed. If the field is absent, the existing noninteractive `hdiutil isencrypted` metadata probe must report YES; a busy/error result remains a blocker. Exact backing image, APFS filesystem, mount and existing privacy checks remain required.

Run the read-only health check before actual work:

```sh
python3 ai-ops/runtime/storage.py
python3 -m unittest discover -s ai-ops/runtime/tests -p test_workflow_executor.py -v
python3 -m unittest discover -s ai-ops/runtime/tests -p test_storage.py -v
```

An explicit `acceptance_directory` is available only for the fixed adapter, technical domain, synthetic partition and zero accounts. It must already be mode 0700 outside Git. This test mode never claims encrypted production storage; its report says `production_storage_verified: false`. Normal operation has no automatic acceptance fallback. Synthetic tests are not live account or school acceptance.

Successful results require the existing Controller's complete receipt, exact result-location/content hash readback, a post-save source revision check, and saved coordinator-state readback. Results identify the canonical runner receipt and output reference. Repeating the same request with the same execution identity only reads the saved result again. A changed contract, adapter binding, operation or expected source revision conflicts with that ID. It cannot silently replace the previous result.

The coordinator table `workflow_execution_state` in the same Store holds only progress, stop state and pointers to existing results. It is not a second school grade/mail/feedback ledger. Do not copy live school receipts into it or add a second school writer. All runtime databases, lock files, capabilities, evidence and acceptance receipts stay outside Git. No credential value is required; account/credential references remain with the existing private resolver, and this local adapter uses no account credential.

## Ownership and recovery

A nonblocking POSIX flock serializes cooperating local invocations by the declared concurrency key in this one storage root. Lock files are retained so waiters cannot split across inodes. A held lock returns `scope_busy`, with no second execution. It does not fence another host, another database, an external Claude session, browser extension, remote UI writer or a process bypassing this bridge. Those operations are unsupported until their own native writer fence and original domain receipt protocol are integrated.

| Persisted state | Meaning | Smallest safe next action |
| --- | --- | --- |
| `prepared` | No runner dispatch marker was saved | Resume with fresh authority, ownership, source and provider evidence; the bridge rechecks everything. |
| `blocked` | A pre-action gate failed | Resolve the named source/provider/owner/deadline dependency and retry the safe preflight. No prior complete result or stop may be overwritten. |
| `running` | Dispatch may have happened; interruption left no confirmed completion | Existing owner inspects the exact `runner_result_location` and source. The entire local concurrency scope stays stopped. |
| `stopped` | Save/readback/source outcome is uncertain or a completed result was lost | Preserve the runner receipt and coordinator row; reconcile with the existing owner. Never automatically retry, clear the hold or bypass it with a new request ID. |
| `complete` | Existing result/receipt and source were read back | Reuse the same request for readback only; a genuinely new authorized input needs a new request ID. |

A new request in a held scope cannot bypass `running` or `stopped`. Independent concurrency scopes remain usable. There is deliberately no automatic stop-clearing, uncertain-write retry or manual SQL repair command in this runbook. Reconciliation and any approved future repair must preserve evidence and use the original owner's native protocol. For school grades, that remains the Chrome helper alone; for mail/feedback, it remains the original outbox and receipt system.

## Acceptance and rollback boundaries

The executor tests exercise source changes before and after execution, competing owners, unavailable capability, deadline expiry, safe read bounds, concurrent requests, same-ID conflict, duplicate replay, interruption before/after dispatch, lost readback, durable stops and independent-scope continuation. Actual catalog acceptance must additionally record the current catalog count/revision, private runner location, result hash, output readback and repeated-request receipt equality.

A passing catalog run proves this exact deterministic adapter and storage path. It does not complete a school workflow, validate a destination account, migrate a schedule, prove a future scheduled wake, or establish global browser ownership. Other workflow contracts remain valid declarations with unsupported execution adapters and explicit next steps.

Rollback is source-only: stop invoking this bridge and revert its scoped implementation after reviewing active local claims. Preserve existing SQLite results, coordinator rows and retained lock files. Do not delete uncertain state, alter school recovery, unmount shared storage or change schedules as rollback. The storage metadata correction is independently scoped and can be reverted separately if necessary; its prior behavior may again block an attached encrypted image.

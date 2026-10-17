# Cost-first working state — October 12, 2026

A usable private working cache and receipt location now exists on the mounted encrypted external archive, beyond the preserved export history:

- Root: `/Volumes/AI-Private-Archive/AI-Archive/state/ai-ops`.
- Cache/result database: `cache.sqlite`; usage metadata database: `usage.sqlite`.
- Private receipt directory: `receipts`; synthetic readback receipt: `receipts/storage-demo.json`.
- Private local path configuration: `runtime-storage.json` inside that encrypted root; databases/receipts stay outside Git.

Metadata readback verified APFS mount `/Volumes/AI-Private-Archive` belongs to `/Volumes/T7/AI-Archive/AI-Private-Archive-v2.sparsebundle`; `hdiutil isencrypted` returned YES, and the backing T7 is mounted. State/receipt directories were verified mode0700; database/config/receipt files mode0600. OwnersEnabled is not a gate. No old data was overwritten or permissions relaxed. An unlocked mounted encrypted image remains available to the current user; this is not a claim of inaccessible mounted contents.

`storage.py` checks explicit mount/image identity and encryption before making state directories and again before initializing the existing Store/UsageLedger interfaces. Missing/unverified mounts fail closed with no local fallback. It rejects symlinks, parent traversal, state paths outside the verified mount and public existing directories/files, leaving them for review. Ejection or path replacement races require OS/operator supervision; metadata checks are not an absolute filesystem isolation guarantee.

From the repository root:

```sh
python3 ai-ops/runtime/storage.py --initialize
python3 ai-ops/runtime/storage.py --root /Volumes/AI-Private-Archive/AI-Archive/state/ai-ops
python3 ai-ops/runtime/runner.py --demo --state /Volumes/AI-Private-Archive/AI-Archive/state/ai-ops/cache.sqlite
```

Flags `--root`, `--mount`, `--image` override `AI_OPS_STORAGE_ROOT`, `AI_OPS_ARCHIVE_MOUNT`, `AI_OPS_BACKING_IMAGE`. Defaults are the verified paths above; changing them still requires actual mounted-image/encryption evidence. This does not rewrite the shell/login environment or enable a recurring worker. A caller can pass resolved `paths.cache` to `foundation.Store` and `paths.usage` to `usage.UsageLedger` directly. Initialize no spending caps from guessed budgets.

Nine meaningful storage tests cover no-write failure, lost verification between phases, private permissions, cache persistence/reopen, symlinks/traversal, outside-root rejection, conflicting configuration preservation and flag/environment precedence. The actual external-drive synthetic runner completed sum10 with zero paid dispatches; SQLite receipt readback passed. The copied mode0600 synthetic receipt has SHA256 `4ad91946522c196e2e14b3305cc9a02a1f805632f33e10dc1133d369faa181a8`. This is a local deterministic storage check, not a provider, service or school-workflow acceptance claim.

## Bounded cloud cost assessment

Current metadata-only Cloud Run reads found School Hub revision `school-workflow-hub-00273-fkl` with service maxScale1, revision minScale0/maxScale20 and CPU throttling enabled. Both Personal Hub revisions remain `personal-hub-api-00001-dkz` and `personal-hub-mcp-00001-q8k`, each service maxScale20; returned revision annotations contain no explicit minimum/CPU-throttling settings. No current bill, utilization, actual instance count, provider receipts or dollar savings were inspected or claimed.

There is no evidence-backed immediate idle-cloud saving to apply from these reads: the Hub already declares zero minimum instances, while absent Personal annotations do not prove billed idle instances. Personal max20 is an expansion cap, not an idle-cost measurement. A later selected workload can justify a smaller approved cap; this task made no scale/deployment/scheduler/IAM changes. Keep existing resources until dependency/preservation evidence supports retirement.

The concrete cost-saving path implemented today is deterministic retrieval/cache/receipt work on the existing drive with paid routes disabled. Reuse eligible unchanged results and recompute only changed or expired components. No extra cloud service, paid API call, credit purchase or model-price assumption was needed. Measured monetary savings require actual usage/price receipts; none are fabricated here.

# Existing workers: compact context integration

These four appendices are supplemental inputs to the named existing workers. Preserve the complete original task prompt, criteria, account, approved sources, destination and privacy boundaries. No replacement prompt, new schedule, candidate profile or financial source body is provided here.

The saved `writing-on-demand.md` and its manifest row are historical generated artifacts.
Their writing-voice digest predates the October 17/19 guidance reconciliation, and their
Ledger-as-capture wording is superseded by [current writing-voice guidance](../../knowledge/writing-voice.md)
and the [reflection contract](../reflection-substack-bank.md). Do not append or replay this
saved context. The existing verifier must hold on changed bundles or missing private source
bytes; regenerate and deliberately revalidate the context and manifest together from the
authorized source environment before reuse. This note does not refresh hashes, waive source
verification or establish manuscript/voice acceptance.

For a local worker, generate fresh verified context before work:

```sh
python3 ai-ops/runtime/worker_context.py doe-watch --format text
python3 ai-ops/runtime/worker_context.py news --format text
python3 ai-ops/runtime/worker_context.py birthday --format text
python3 ai-ops/runtime/worker_context.py writing-on-demand --format text
```

The entrypoint pins whole reviewed paragraphs from at most two existing bundles, verifies the existing source hashes, and caps the entire emitted appendix at 400 words. A missing private source, changed bundle or missing paragraph is a hold. An older successful appendix is not a verification bypass. Local workers can use this entrypoint now; live cloud tasks cannot read the local checkout or encrypted drive merely because the helper exists.

For the root's authorized live prompt update, independently read the exact existing task, preserve its full original privately, and append the corresponding `.md` unchanged. Retain that original as an exact prefix; save and reopen for exact readback. Record the appendix's `context_sha256` and `provenance_fingerprint` from [manifest.json](manifest.json) in the operational change receipt. The prepared manifest intentionally has `ready_for_live_append=false` until that external task binding is supplied. These static cloud appendices must be regenerated and deliberately revalidated when their source policy changes; no automatic refresh is claimed.

For local metadata binding, `--binding /private/path/binding.json` accepts only the existing task ID, `original_prompt_sha256`, `source_prompt_preserved: true` and `destination_unchanged: true`. This operator-supplied metadata does not itself prove a cloud save or readback; it never contains the raw prompt. Writing remains on demand and has no scheduled-task binding.

Measured against the 2,863 words in all existing knowledge bundles, the ready appendices are DOE Watch 141 words (95.08% less), News 187 (93.47%), Birthday 146 (94.90%) and on-demand writing 274 (90.43%). These are exact whitespace-word reductions, not model tokens, bills or verified provider savings. Source metadata lives in the sidecar manifest; no private source body is emitted.

## Local writing skill append proposal

No existing skill was changed. Before a future append to `skills/writing-block/SKILL.md` or `skills/chapter-bank/SKILL.md`, preserve that original and its SHA in encrypted storage. The localized proposed addition is:

> Before a current writing run, load the verified supplemental context from `python3 ai-ops/runtime/worker_context.py writing-on-demand --format text` in the private optimized-system checkout. If verification fails, stop this context path and name the missing source; do not replay a cached appendix. Retain the exact current user task, draft, destination and editorial scope. Newer current source rules govern conflicts with older Roam-canonical or manuscript-provenance-tag instructions. The voice baseline remains provisional; this appendix does not establish preferred-voice acceptance, a formal grading rubric, or permission to publish.

This proposal is reviewable and remains unapplied. It does not retire a source skill or change its other substantive rules.

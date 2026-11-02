# Graph operations

Read `../SKILL.md` first; its mandatory boundaries still govern. Path bases do not change when detail moves here: own `scripts/` and `reference/` paths are relative to the original skill root; named sibling-skill paths such as `book-revision/scripts/` are relative to the shared `skills/` directory. Manuscript `revision/` and `book-compile/` paths belong to the designated private manuscript repository; data and derived artifacts belong only in authorized private staging. Never interpret them as paths inside this reference directory or publish private artifacts to the public skills repository. These extracted instructions preserve existing rules; they grant no new authority.

## Delegate, don't reimplement [HARD]

- **Any new page** (📇, source, QUE, concept, 🧭, bank) runs book-ops `on_create_check` first
  and is minted through the book-ops flow — chapter-bank never mints alone:
  `python3 ../book-ops/scripts/on_create_check.py --title "<proposed>" --vocab vocabulary.json --inventory inventory.json`
- **`inventory.json` does not survive between sessions.** It has now been lost twice (rebuilt
  Aug 2, gone Aug 3). Rebuild it at the top of any run that will mint, via
  `book-ops/scripts/roam_pull.py` with the token on
  `[[Local API Token: book-ops read (Katherines-MacBook-Air.local)]]` (graph `kvond`). Despite
  the page title that token is **write-capable** — Katherine's own correction, Aug 1 2026:
  "read" is a name, not a scope. The `roam-graph-local-token-` prefixed tokens are Roam Desktop
  local tokens and the cloud API rejects them.
- **The gate matches words, not meanings.** A title can return `clear` and still collide
  conceptually — an asymmetry claim landing beside a symmetry claim on the same pair of terms
  passes every layer. Run a live semantic pass on the distinctive terms of each candidate
  alongside the gate, and surface conflicts as rulings before the mint, not after.
- **Renames:** the MCP rename tool is broken (Jul 13 2026) — never use it. Two working paths:
  Roam UI rename, or backend-API `update-page` via the bulk-ops path (validated 2026-07-29 —
  repoints refs exactly like the UI). API renames must end with the verification protocol:
  old title resolves to nothing · ref count carried over · zero blocks still holding the
  literal old-title string (repair any found). Propose-then-confirm still applies.
- **Page deletion has no MCP path.** Emptying a page is possible; removing it is a UI action.
  Say so plainly rather than reporting a stray as fixed.
- **Bulk token substitution never passes through the model.** `update-block` replaces a whole
  string, so a find-and-replace through the MCP means pulling every full block text into context
  and writing it back. Use `roam_bulk_ops.py` (dry-run by default, diff report, one write per
  request, resumable — it re-queries each run and rewrites only what still matches). Roam 429s
  on large `batch-actions` payloads and stalls on long sockets; keep the per-request timeout
  short and let the backoff handle it.
- Endnotes, reference sections, master-references sync, reading render, compiled docx, citation
  checks → `manuscript-ops`. Morning time-blocking → `daily-agenda`; the ≤2h writing slice →
  `writing-block` (reads `Writing Status::`).

## Zettel sweep — new zettels are first-class distill objects

Each distill run sweeps zettels minted anywhere (content pages, article scaffolds, Author Block,
dailies):

1. **Zettelkasten FIRST.** Verify each new zettel-like note is registered: correct template,
   `Meta::` (Provenance forced), `Index:: [[🌿 Evergreen Notes]]` (that backlink IS the registry),
   selective threading on `[[🗂️ ZettleKasten]]` (spine-level entry points only — Jul 12 2026).
   Propose registration/conversion; never mint or convert silently.
1b. **Substack-spent check** (added Aug 4 2026): a zettel carrying `Published-as::` has been
   published through `[[📰 Publication Registry]]` — the sweep proposes no further Substack
   candidacy for it.
2. **THEN propose connections** where Scope matches: 📋 structure notes, hubs ([[book's
   conceptual core]], Claims Hub), matching 🧭 map(s) (pointer + role phrase, refresh
   `Current as of::`), active article pages. Propose-then-confirm; never auto-place.
3. **Strays flagged, not fixed** — stranded, pre-reconfigure-format, or duplicated zettels get a
   proposed fix, never auto-merge/move.

**Reading Katherine's ticks.** A distill run leaves `{{[[TODO]]}}` options on the daily page;
those ticks ARE the ruling and a later run reads them and does the writing. Two rules: a blanket
"execute everything" tick does not override a narrower policy tick made in the same pass — when
they collide, surface the collision and rule nothing yourself. And never un-backtick a proposed
title inside a run note: `[[...]]` mints an empty page the moment it renders.

## Topic-map hygiene — both directions

New zettels/QUEs/sources in a mapped area → propose pointer lines (maps judged by coverage +
findability, never correctness). A claim-like sentence ON a map is a 📇 trying to be born →
propose extraction through the gate, pointer left behind.

Watch the `Type::` stamp: the registry IS the backlink list, so a map stamped with a variant
title (`🧭 Topic Map` spaced, vs the canonical `🧭Topic Map`) silently falls out of the registry.
Check the stamp, not just the page.

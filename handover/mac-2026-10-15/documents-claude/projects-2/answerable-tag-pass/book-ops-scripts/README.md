# book-ops scripts

The deterministic layer the `book-ops` / `chapter-bank` SKILLs reference but that
was never bundled. These make the mint gate a **lookup**, not live LLM reasoning —
reproducible, cheap, and fork-safe.

## Files
- `build_inventory.py` — pull the Roam graph → `inventory.json` (the snapshot).
- `on_create_check.py` — the recurring guard: one proposed title → `clear` /
  `review` / `blocked`, against `inventory.json` + `vocabulary.json`.
- `vocabulary.json` — canonical names, aliases, **pending forks** (flagged, never
  auto-resolved), and the **never-merge** pins (auctor ✕ Authorial-Agency).

## Install
This cache is read-only; add the scripts to the skill via **Settings →
Capabilities → book-ops** (drop this folder in as the skill's `scripts/`, and put
`vocabulary.json` beside the SKILL). The SKILL already calls them:

```
python3 ../book-ops/scripts/on_create_check.py --title "<proposed>" \
        --vocab vocabulary.json --inventory inventory.json
```

## Build the snapshot (two paths — same schema)
1. **Direct** (needs a read token: Roam graph → Settings → Graph → API tokens):
   ```
   ROAM_API_TOKEN=xxxx ROAM_GRAPH=default python3 build_inventory.py --out inventory.json
   ```
2. **Via MCP** (no token — run the 3 datalog queries through the Roam MCP in
   Cowork, dump each result to `pulls/pages.json`, `backlinks.json`,
   `children.json`, then):
   ```
   python3 build_inventory.py --from-mcp ./pulls --out inventory.json
   python3 build_inventory.py --show-queries   # prints the exact queries
   ```
   Add `--with-edges` (and `pulls/edges.json`) to enable layer-4 backlink overlap.

## The gate
```
python3 on_create_check.py --title "student agency"          # human-readable
python3 on_create_check.py --title "auctor" --json           # machine verdict
```
Exit codes: `0` clear · `2` review (near-neighbors) · `3` blocked (never-merge pin
or unresolved fork). Layers: 1 normalized-exact · 2 fuzzy token-set · 3 alias/
acronym · 4 backlink-overlap (only with `--with-edges`) · **5 semantic is not
computed** — residual near-neighbors are emitted for you/the LLM to cluster.

Handles **both** node syntaxes (`CLM — x` and `[[CLM]] - x`) so a near-duplicate
can't fork across formats. `rapidfuzz` is used if installed; otherwise a
pure-Python fallback runs (no dependencies).

## Maintenance
- When you **rule** on a pending fork, move it from `pending_forks` to `aliases`
  (loser → canonical). When you settle a new same-word/two-level pair, add it to
  `never_merge`. The registry is the memory; keep it current and the gate stays
  honest across runs.
- Re-run `build_inventory.py` whenever the graph has changed materially; the
  pull is read-only and safe to repeat.

_Seeded 2026-07-02 from the 2nd-brain-distill session (the developmental-sequence
3-way fork, the agentive/Berlin/Equity variants, the Matusov-2011 reference fork,
and the auctor ✕ Authorial-Agency pin)._

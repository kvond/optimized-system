# book-ops dedup snapshot — 2026-07-05 (evening)

Restore point before removing exact-duplicate top-level concept blocks created by a
double-import tonight. Each page below had its concept note pasted **twice**; the two copies were
byte-identical. Kept the first copy, deleted the second. **No block in the graph referenced any of
these UIDs** (verified via :block/refs query → 0 results), so nothing was repointed.

Roam is canonical; these concept pages are outside the git `source/` backup namespace, so this
file is their only pre-change snapshot.

## Removed (second copy) / Kept (first copy)

| Page | Kept UID | Deleted UID | Content (identical in both) |
|---|---|---|---|
| Agency Definition | `aW5UrmuZ8` | `daeER42QA` | "Agency is ecological" concept note |
| The three-legged stool — student agency, teacher perception, classroom ecology | `aDXGxuuo0` | `v6NyKyUg9` | self-titled concept note |
| The genres of agency are plural patterns, not traits | `36qN2KPJH` | `-I955Mz9H` | self-titled concept note |
| Agency is both given and developed | `rhiQ2rFCO` | `S0CQ-lK6s` | self-titled concept note |

Each concept note carried the standard template: __Type: concept__ · Core idea · Why it matters ·
Connections · Questions · Source trail. The "Agency Definition" page also retains its canonical
definition quote block (`TkljfnYp1`, order 0), which was not a duplicate and was left in place.

Verbatim Core-idea text of each kept note is preserved in the nightly Writing Log context and in
the graph itself (the kept copy). If a restore is ever needed, re-create the deleted block as an
exact copy of the kept sibling on the same page.

## Not touched
- "Real (2022), Us — the relational critique of individualism" — single copy, not doubled.
- "book's conceptual core" — hub; top-level blocks are distinct (no top-level doubling detected).
- All `[[Engaged-Agency]]` / `[[Epistemic-Agency]]` / etc. concept pages — not in tonight's
  modified set; left for a future full sweep if wanted.

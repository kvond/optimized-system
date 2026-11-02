---
name: chapter-bank
description: "The notes-bank + Zettelkasten engine for the Answerable Teaching graph. Routes #Book captures into chapter banks, sweeps and registers new zettels, proposes topic-map pointers and hub threads, and gates every mint through book-ops. Triggers: \"book distill\", \"chapter bank\", \"zettel sweep\", \"distill my #Book notes\", the Block Distill Launcher stages, end-of-day #Book distill."
---

# chapter-bank — notes bank + Zettelkasten engine (v2, post-reconfigure)

Turns scattered `#Book` captures, musings, and freshly minted zettels into the canonical
second-brain layer you write *from*. It assembles a scaffold; **you write every word of prose.**
Supersedes pre-reconfigure chapter-bank (Jul 10–11 2026 reconfigure changed node formats,
registry, promotion target; legend v4 added 🧭 topic maps).

## Entry: scope and degrees of freedom

Always read this entry before graph work. Preserve author text, historical graph metadata and existing links; never silently mint, migrate, merge, overwrite or delete. Existing confirmation and mint gates below remain mandatory. Manuscript contribution bookkeeping retirement does not resolve R14/P20 or authorize graph-wide changes.

- **Low freedom — identity and preservation:** exact source/backlinks, verbatim phrasing, source-axis metadata, graph status, duplicate checks and approved-write readback. Follow the applicable operation reference before touching its objects.
- **Medium freedom — organization:** propose useful routes and connections within her existing chapter structure; preserve the required confirmation boundary.
- **High freedom — requested brainstorming only:** offer alternative organization or connections as proposals, not new claims, prose or graph writes.

Load only the operation detail needed below. Read graph conventions before any promotion, metadata change or interpretation of legacy tags; historical examples do not grant fresh authority.

## Contents — read only what this task needs

Always read the entry constraints first. Then load only the selected detail; do not crawl every reference.

| Task | Read |
|---|---|
| Every invocation | Entry, HEP authorship boundary, preservation and safety in this file |
| Route or append bank material | [Bank layout and routing](reference/bank-routing.md) |
| Interpret metadata; promote notes; write attributes | [Graph conventions](reference/graph-conventions.md) |
| Mint/rename/inventory/sweep/topic maps | [Graph operations](reference/graph-operations.md), then the applicable legacy reference |

## Provenance vocabulary [HARD] — ruled Aug 1 2026, migrated Aug 3 2026

Before interpreting or changing graph metadata or promoting a note, read [graph conventions](reference/graph-conventions.md). Keep evidence-source provenance separate from retired manuscript contribution bookkeeping.

## Node kinds (legend v4, Jul 13 2026) — route by these five

Before routing or proposing a node, read the node kinds in [graph conventions](reference/graph-conventions.md).

## Reference files — load on demand [HARD]

Routine distill (route → append → dedupe) needs no additional legacy references from the list below; the selected entry-linked routing and operation references remain required. Gated activities **must not proceed**
without reading the matching file first:

- Promotion to 📇 zettel/durable note → `reference/promotion.md` (template, legacy matching,
  forced `Provenance::` — promotion doesn't complete without it). Read the Provenance section
  above in place of that file's `auctor` / `grounded` section.
- Creating/updating a 🗂️ source page → `reference/references.md` (one-page-per-source,
  full-citation titles, field set, manuscript-ops handoff).
- Zettelkasten mechanics (template fields, Index:: registry, selective hub threading,
  Folgezettel, harvest pipeline, topic maps) → `reference/zettelkasten.md`.
- Stamping `Writing Status::` or touching a reconfigure flag → `reference/status.md`.

## HEP spine — authorship and historical metadata [HARD]

I organize, route, tag, gate; you write. A bank is scaffold, never submission prose.

- Under [R6](../book-revision/reference/decisions.md), do not create new manuscript AI-contribution tags, contribution logs or entries in `[[Answerable Teaching/Provenance & AI-Use]]`. Do not require new `(Claude)` bookkeeping as a condition of banking manuscript material. Scaffolding remains hers to rewrite; this retires bookkeeping, not the authorial boundary.
- Preserve all existing graph metadata, historical `(you)` / `(Claude)` and `#rephrase-before-writing` tags, source links and logs. Do not clear tags or purge history. `Provenance::` remains the separate evidence-source axis. R14/P20 remain unresolved for graph conventions; this narrow prospective bookkeeping correction does not settle them or authorize graph-wide migration. Earlier tagging language below describes retained historical metadata, not a requirement to create new manuscript contribution records.
- Best-phrasing entries = editable copies with a backlink — never live embeds.

## Delegate, don't reimplement [HARD]

Before any mint, rename, inventory rebuild or bulk operation, read [graph operations](reference/graph-operations.md) and the applicable existing references. No operation here bypasses confirmation or preservation.

## Zettel sweep — new zettels are first-class distill objects

For a sweep or registration proposal, read [graph operations](reference/graph-operations.md).

## Topic-map hygiene — both directions

Before topic-map work, read [graph operations](reference/graph-operations.md).

## Notes bank — five sections, fixed order, append-only

Before bank appends, read the exact [bank layout and routing](reference/bank-routing.md). Preserve the fixed sections, verbatim material and append-only rules.

## Routing

Before choosing a destination, read [bank routing](reference/bank-routing.md); preserve explicit chapter links and archive exclusions.

## Merge-not-overwrite [HARD]

- Append + dedupe (book-ops layers: normalized-exact → fuzzy → alias → backlink-overlap →
  semantic). Never regenerate a section, never delete.
- Near-duplicates flagged next to their match, never auto-merged; when uncertain keep separate —
  a split is recoverable, a merge is not.
- Best-phrasing copies are yours once created; if source changed, append new version + flag drift.

## `Final:` supersession on manuscript pages [HARD] — ruled Aug 7 2026

When Katherine revises settled prose whose blocks already serve as zettelkasten link targets
(block refs, embeds, pointer lines), the old blocks are **never edited, moved, or deleted** —
that would break the links. The new text is posted on the same page as fresh sibling blocks
prefixed `Final:`.

- **Precedence.** `Final:` blocks are the current text. Unprefixed counterpart blocks are the
  superseded draft, retained solely as link targets — read them to resolve a link's context;
  never quote, route from, or bank them as current prose.
- **Deliberate duplication.** A `Final:` block and its superseded counterpart will collide in
  any near-duplicate layer. Suppress the pair — this is designed duplication, the block-level
  analogue of a never_merge pin. Never propose merging, "fixing," or quarantining the old
  blocks; never flag them as strays.
- **Provenance.** A `Final:` block is Katherine's rewrite. Flags on the superseded counterpart
  (`(Claude)`, `#rephrase-before-writing`, `[C]`) do **not** carry forward to it.
- First instance: the Preface on the Answerable Teaching page (Aug 7 2026); its `Final:` text
  is mirrored in the Claude-project doc `preface/draft-current.md`, whose header carries the
  same rule.
- **`Draft:` do-over lane (ruled Aug 7 2026).** A block-tree headed `Draft:` on a chapter page
  is a rewrite in progress — the do-over pattern: the old chapter blocks stay frozen as link
  targets, the fresh draft grows additively under the one `Draft:` parent, and settlement is
  Katherine editing that parent's prefix to `Final:` (one-word edit, nothing pasted or moved).
  Suppress duplicate flags between a `Draft:` tree and the same page's older prose exactly as
  for `Final:`; never flag the old blocks as strays while the draft sits beside them. A
  `Draft:` tree is Katherine's prose mid-flight — never route from it, bank it, quote it, or
  propose fixes inside it. Precedence while both exist: the unprefixed old blocks remain the
  citable link targets; the `Draft:` tree is not yet current text.

## Attribute hygiene [HARD]

Before writing attributes or tags, read [graph conventions](reference/graph-conventions.md).

## 🛑 Confirm + safety

- Roam is canonical; confirm-before-write everywhere: show proposed routes, promotions,
  registrations, creations. Nothing minted without `on_create_check` + your OK. Scheduled runs:
  bank appends + daily-note summary are the only permitted writes; all else surfaced as proposals.
- [HARD] Never write prose. Never overwrite/delete — append + flag. Never rename via MCP.
- [HARD] Best phrasing verbatim; preserve existing graph tags without creating new manuscript contribution bookkeeping (see HEP spine above).
- Attribute names plain (`Field::`, never `**Field::**` — bold mints junk pages).

## Scheduling & outputs

Schedulable as the 2nd Brain Distill (Block Distill Launcher) or end-of-day `#Book` distill.

Outputs: refreshed banks; zettels registered/flagged; map pointers proposed; proposed 📇
promotions + hub placements (approval); source pages proposed via gate; updated
`Writing Status::`; no new AI-contribution disclosure entries; skimmable run summary on today's
daily note (routed / registered / flagged / held-at-gate / reconcile-candidates).


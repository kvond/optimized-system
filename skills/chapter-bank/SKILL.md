---
name: chapter-bank
description: "The notes-bank + Zettelkasten engine for the Answerable Teaching graph. Routes #Book captures into chapter banks, sweeps and registers new zettels, proposes topic-map pointers and hub threads, and gates every mint through book-ops. Triggers: \"book distill\", \"chapter bank\", \"zettel sweep\", \"distill my #Book notes\", the Block Distill Launcher stages, end-of-day #Book distill."
---

# chapter-bank — notes bank + Zettelkasten engine (v2, post-reconfigure)

Turns scattered `#Book` captures, musings, and freshly minted zettels into the canonical
second-brain layer you write *from*. It assembles a scaffold; **you write every word of prose.**
Supersedes pre-reconfigure chapter-bank (Jul 10–11 2026 reconfigure changed node formats,
registry, promotion target; legend v4 added 🧭 topic maps).

## Provenance vocabulary [HARD] — ruled Aug 1 2026, migrated Aug 3 2026

`Provenance::` takes exactly two values:

- **`[K]`** — the claim originates with Katherine. Her own theoretical move: the taxonomy, the
  origination criterion, the perceptual seams. Not a gap to fix; these are the contribution.
- **`literature link`** — the claim stands on cited literature or EVD. *Literature link* names
  the thing a reader goes and checks, which is why it replaced *grounded*.

**`auctor` and `grounded` are retired.** The 172 live `Provenance::` attributes carrying them
were migrated Aug 3 2026 by `roam_bulk_ops.py --job provenance`; verification returned zero
residue. Historical prose that *mentions* the old values inside run logs was deliberately left
alone — those are records, not live attributes.

⚠ **`reference/promotion.md` and `reference/zettelkasten.md` still print the retired
`auctor | grounded` pair.** This section supersedes both on that point and only that point;
everything else in those files stands. They are read-only from a session and need regenerating
at the file level.

**Distinct from the `(you)` / `(Claude)` tags [HARD].** Those track *who phrased it*; Provenance
tracks *where the claim comes from*. A `(Claude)`-phrased block is normally `Provenance:: [K]` —
Claude scaffolding Katherine's ruling. A `(you)`-phrased claim can be `literature link` — her
words, Lareau's idea. Never collapse the two axes. `[K]` is **not** the counterpart of `[C]`:
`[C]` says Claude typed this, `[K]` says the idea is Katherine's.

⚑ **Known gap in the vocabulary.** There is no value for a claim that originates with Claude and
is adopted by Katherine on a tick. `[K]` is the closest fit and it is not exact. Flag such mints
rather than filing them silently.

## Node kinds (legend v4, Jul 13 2026) — route by these five

- **📇 zettel** — ONE claim; page `📇 {bare-sentence claim}`, body [[Template - Zettel Claim]].
  Concept notes use the concept-note form (plain title OK).
- **🗂️ source page** — someone else's work; full-citation title, ONE page per source.
- **📋 structure note** — sequences claims into an argument ([[Template - Structured Notes]],
  layer 4). Claims Hub is one.
- **QUE —** — one question.
- **🧭 topic map** — curates a topic area's atoms; **points, never claims.**

## Reference files — load on demand [HARD]

Routine distill (route → append → dedupe) needs none. Gated activities **must not proceed**
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

## Notes bank — five sections, fixed order, append-only

Per `Answerable Teaching/Chapter N — Notes Bank`:

1. **Claims** — candidate assertions, `(you)`/`(Claude)` tagged; a stabilized `#clm-candidate`
   is what gets promoted to 📇.
2. **Examples** — classroom anchors/vignettes (Abraham, Aliyah, Maya, Noelle…), each backlinked
   to source block.
3. **Possible subsections** — structure options, not prose.
4. **Research anchors** — your manual paste lane (Perplexity/Scite); I file + backlink, never fetch.
5. **Best phrasing** — **verbatim, never bulletized [HARD]**; `(you)`/`(Claude)` tagged; each an
   editable copy with a `((backlink))`.

`Scope::` = page-level attribute per bank, drafted from Tag Hub concepts + book-ops vocabulary,
**confirmed by you**. Scope is the routing key; explicit chapter link overrides.

## Routing

1. [HARD] Explicit link to the chapter page (or `[[chN]]`) → that bank, period.
2. Scope match on concepts/links; multi-scope blocks surfaced for you, never auto-split.
3. No match → `#Book / unrouted` lane. Never force-fit.

Canonical chapters = **`[[📋 Answerable Teaching — Master Outline]]`** (weave arc, adopted
2026-07-29) — the authoritative list and numbering. Cross-check `📋 Projects → [[**Book**]]` and
`[[Answerable Teaching/Tag Hub]]`, but the Master Outline wins every conflict. Duplicate/
non-namespaced pages = reconcile-candidates, surfaced, never silently routed into.
[HARD] Never route into, draw from, or propose merges with `🗄 Archive/` pages or pages stamped
`Status:: archived` — archives are provenance, not sources.

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

Attribute names stay plain: `Field::`, never `**Field::**`. Bold or trailing punctuation inside
an attribute or tag mints a junk page — `rephrase-before-writing:**` and `VERIFY.` are both live
examples. Write `#VERIFY` with the punctuation outside the tag.

Note the cost of attribute syntax in dialogue captures: `Field::` for speaker turns buys a
queryable transcript and spends one page per turn. A single Aug 3 capture minted about ninety
one-backlink pages that way. Flag it; don't silently convert it.

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


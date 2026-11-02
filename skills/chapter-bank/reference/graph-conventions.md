# Graph conventions

Read `../SKILL.md` first; its mandatory boundaries still govern. Path bases do not change when detail moves here: own `scripts/` and `reference/` paths are relative to the original skill root; named sibling-skill paths such as `book-revision/scripts/` are relative to the shared `skills/` directory. Manuscript `revision/` and `book-compile/` paths belong to the designated private manuscript repository; data and derived artifacts belong only in authorized private staging. Never interpret them as paths inside this reference directory or publish private artifacts to the public skills repository. These extracted instructions preserve existing rules; they grant no new authority.

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

## Attribute hygiene [HARD]

Attribute names stay plain: `Field::`, never `**Field::**`. Bold or trailing punctuation inside
an attribute or tag mints a junk page — `rephrase-before-writing:**` and `VERIFY.` are both live
examples. Write `#VERIFY` with the punctuation outside the tag.

Note the cost of attribute syntax in dialogue captures: `Field::` for speaker turns buys a
queryable transcript and spends one page per turn. A single Aug 3 capture minted about ninety
one-backlink pages that way. Flag it; don't silently convert it.

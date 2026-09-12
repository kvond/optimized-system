---
name: manuscript-ops
description: "Operations over the manuscript files: stage/export chapters from Roam, render reading copies, run continuity + citation checks against the sources manifest, compile deliverable docx. Never generates or edits prose. Triggers: staging/exporting the manuscript, consistency or citation pass, \"compile for editor/committee\"."
---

# Manuscript-Ops — operations over the manuscript files

The mechanical, structural work around the manuscript, kept strictly separate from the
thinking. This skill never writes prose and never edits a chapter — argument generation and
revision stay in the Book Project. Here Cowork only renders, checks, compiles, and flags.

Roam is canonical. `source/` is the faithful export (links intact, the backup); `writing/`
is the tag-stripped reading copy. Neither is ever hand-edited — edits happen in Roam, and
these are regenerated downstream, the same discipline as RAW_ORIGINALS.

Standing caveat (2026-09-12): the last nightly publish from Roam ran 2026-07-02, and the
drafting since then has happened in the Working Copy Google Doc and in `book-compile/`.
Until decision P18 in the revision ledger (`skills/book-revision/reference/decisions.md`)
is ruled, treat the Doc as the current draft and this skill's Roam jobs as the
reconciliation route, not the source of the latest text.

## Authorship (ruled Sept 11, 2026)

The provenance record keeping is retired. No [Y] / [CO] / [C] tags, no contribution ledger,
no entries to the Roam "Provenance & AI-Use" page, and no provenance note prepended to a
compiled deliverable. The book is Katherine's intellectual work, produced through her own
drafting, conversation with AI, and her redrafting. The voice file
(`book-compile/voice-guide.md` in `kvond/Answerable-Teaching`) carries the same ruling.

## Bundled scripts

Run the scripts for the deterministic work; let Claude judgment enter only where noted.

- `scripts/render_reading.py` — built. Roam export → clean reading prose: brackets removed,
  workflow tags stripped, components/block-refs/attributes/highlight gone, bullets flattened
  to paragraphs; headings/bold/italics kept. Inline content tags keep their words; workflow
  tags (`#next #near #book #[[parking lot]]`…) are removed whole.
- `scripts/check_consistency.py` — built. Extracts chapter cross-references (and whether the
  target chapter exists), vague back-references with no number, and every tracked-term
  occurrence with context, into one report. Extraction only — Claude adjudicates. The
  fuller checker for a whole-manuscript snapshot (dashes, bans, residue, pseudonyms,
  duplicates, note markers) is `book-revision/scripts/manuscript_check.py`; use it for
  revision passes and keep this one for the Roam-export layout.
- `scripts/check_citations.py` — planned. Extract in-text citations, set-difference against
  the sources manifest, flag orphans and unused entries. Author-name variants normalized by
  the same dedup logic as book-ops.
- Deliverables use the built-in **docx skill**, not a bundled script.

## Defaults for this manuscript

- **Source** — the chapter pages in Roam, pulled via the Roam MCP (scoped to chapters, not
  the whole graph).
- **Layout** — `source/` faithful export, `writing/` tag-stripped reading copy, both under git.
- **Tracked terms** for the consistency pass (refreshed 2026-09-12 to the public pseudonym
  set): Angie, Nancy, John, Toma, Heidi, Marcus, Priya, Malik, Ben, Brian, Peter (son), Eli,
  Zara, Noelle, Gustov, Lezir, Karen, Dana, Cindy, Mike; and the terms legibility,
  sense-making, meaning-making, time-world, chronotope, adjacent agency, intellectual
  authorship, intellectual apprenticeship, critical aspect, shared object, reframing
  epistemic agency, standing as a knower. Add to this list as coined concepts stabilize;
  the same list lives in `manuscript_check.py` and the two must agree.
- **Sources manifest** — `revision/sources.json` in the book repo once the notes lane has
  built it (`sources.json` or `.bib` before then): Bakhtin, Scott, Lareau, Ito, Variation Theory…
- No external Python dependencies; the scripts are standard library only.

## Version retention (Drive working copies)

Roam stays canonical; the compiled Google Doc is a downstream reading/deliverable copy, not
a second source of truth. One rule keeps the Drive side from fragmenting into the kind of
`(final) + X` swarm that accumulated during the June apparatus passes:

- **One LIVE doc.** Exactly one Google Doc is the current manuscript, named
  `Answerable Teaching — LIVE`. Apparatus, formatting, APA-7, and HEP-flag passes happen
  *in place* in that doc, versioned through File → Version history (name each version per
  pass: "Ch2 notes renumbered", "APA-7", "mechanical + HEP flags"). Never clone-and-suffix
  into a new copy — that habit is what produced the swarm.
- **Archive, don't delete.** A genuinely superseded doc moves to `HOME/book/archive/`
  (dated) and stays there as version history. Deletion is reserved for confirmed
  byte-duplicates (the same pass copied into two accounts) and only after verifying identity.
- **One account owns it.** LIVE doc and archive live in a single canonical account (udel),
  so ownership and version history don't split across kvond@udel / kvond12@gmail.
- **Reconcile back to Roam.** If a pass happens in the Doc rather than Roam (as the June
  passes did), flow it back so `source/`/`writing/` stay faithful — the Doc is never allowed
  to become a silent parallel master.

Retention convention only — never touches argument or wording.

## Invoking

One-line requests trigger the matching job with these defaults; nothing writes to Roam or
to the manuscript without showing you the result first:
- "stage the manuscript" / "sync the chapters" → job 2
- "run a consistency pass" / "check cross-references" → job 1
- "check the citations" → job 3
- "compile the manuscript" / "make a docx for the editor" → job 4

## Job 2 — staging / export (the foundation)

1. Pull the chapter pages via the Roam MCP (the `roam_pull.py` query shapes from book-ops,
   scoped to chapter pages) and write each to `source/`.
2. `python3 scripts/render_reading.py --in source/ --out writing/`
3. Commit `source/` and `writing/` to git, then push to the private remote so the reading
   copy is browsable on GitHub.

The weekly `#book` distill is a separate scheduled local task (same machinery as
daily-agenda): pull the week's `#book` captures, organize them, drop them where the writing
session expects. The MCP pull + git wrapping is the piece to wire on first run.

## Job 1 — consistency pass (on-demand, e.g. pre-submission)

`python3 scripts/check_consistency.py --in writing/ --out consistency_report.md`

Then read the report and flag the judgment calls: does each cross-reference's claim actually
live where it points; is "double booking" used consistently with its definition; are the
anchor students characterized consistently. Surface findings for the user; never edit the
manuscript — propose changes for Roam. For a full pass over the current draft, use the
revision skills instead: `book-revision` and its lanes.

## Job 3 — citation integrity (on-demand)

Maintain the sources manifest. `check_citations.py` extracts every in-text citation and
diffs against it, flagging cited-but-missing and present-but-unused. Normalize author-name
variants (Scott / J.C. Scott / Scott 1998) before diffing.

## Job 4 — deliverables (on-demand)

Use the docx skill to compile `writing/` into a formatted .docx — full manuscript or
per-chapter — with table of contents and front matter, in the editor's required manuscript
format. The format is set once; this is a transform, not a judgment. Compile with
`SKIP_PROVENANCE=1` (or leave `provenance.md` out): no provenance note goes in front of the
manuscript.

## Safety

- Never edit the manuscript. `writing/` and every report are derived and advisory; fixes go
  into Roam, by the user.
- `source/` is the faithful backup; before any git operation confirm it reflects the current
  Roam state.
- The reading render is a convenience copy, not a typeset proof — an inline editorial aside
  left next to a stripped `{{TODO}}` may survive into `writing/`. Don't treat it as final.

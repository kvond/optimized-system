---
name: manuscript-ops
description: Operations layer over the Beyond Motivation manuscript files — renders Roam chapter exports into clean reading prose, runs continuity and citation checks across the whole manuscript, and compiles formatted deliverables. Use this skill whenever staging or exporting the manuscript from Roam, rendering a reading copy, running a consistency or cross-reference pass, checking citations against the sources manifest, or producing a compiled docx for an editor or committee — even if the user does not say "manuscript-ops". It never generates prose and never edits the manuscript; it extracts, checks, compiles, and flags for review.
---

# Manuscript-Ops — operations over the manuscript files

The mechanical, structural work around the manuscript, kept strictly separate from the
thinking. This skill never writes prose and never edits a chapter — argument generation and
revision stay in the Book Project. Here Cowork only renders, checks, compiles, and flags.

Roam is canonical. `source/` is the faithful export (links intact, the backup); `writing/`
is the tag-stripped reading copy. Neither is ever hand-edited — edits happen in Roam, and
these are regenerated downstream, the same discipline as RAW_ORIGINALS.

## Bundled scripts

Run the scripts for the deterministic work; let Claude judgment enter only where noted.

- `scripts/render_reading.py` — built. Roam export → clean reading prose: brackets removed,
  workflow tags stripped, components/block-refs/attributes/highlight gone, bullets flattened
  to paragraphs; headings/bold/italics kept. Inline content tags keep their words; workflow
  tags (`#next #near #book #[[parking lot]]`…) are removed whole.
- `scripts/check_consistency.py` — built. Extracts chapter cross-references (and whether the
  target chapter exists), vague back-references with no number, and every tracked-term
  occurrence with context, into one report. Extraction only — Claude adjudicates.
- `scripts/check_citations.py` — planned. Extract in-text citations, set-difference against
  the sources manifest, flag orphans and unused entries. Author-name variants normalized by
  the same dedup logic as book-ops.
- Deliverables use the built-in **docx skill**, not a bundled script.

## Defaults for this manuscript

- **Source** — the chapter pages in Roam, pulled via the Roam MCP (scoped to chapters, not
  the whole graph).
- **Layout** — `source/` faithful export, `writing/` tag-stripped reading copy, both under git.
- **Tracked terms** for the consistency pass — Abraham, Aliyah, double booking, agency,
  perception, ecology. Add to this list as coined concepts stabilize.
- **Sources manifest** — `sources.json` (or `.bib`): Bakhtin, Scott, Lareau, Ito, Variation Theory…
- No external Python dependencies; the scripts are standard library only.

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
live where it points; is "double booking" used consistently with its Ch. 5 definition; are
Abraham and Aliyah characterized consistently. Surface findings for the user; never edit the
manuscript — propose changes for Roam.

## Job 3 — citation integrity (on-demand)

Maintain the sources manifest. `check_citations.py` extracts every in-text citation and
diffs against it, flagging cited-but-missing and present-but-unused. Normalize author-name
variants (Scott / J.C. Scott / Scott 1998) before diffing.

## Job 4 — deliverables (on-demand)

Use the docx skill to compile `writing/` into a formatted .docx — full manuscript or
per-chapter — with table of contents and front matter, in the editor's required manuscript
format. The format is set once; this is a transform, not a judgment.

## Safety

- Never edit the manuscript. `writing/` and every report are derived and advisory; fixes go
  into Roam, by the user.
- `source/` is the faithful backup; before any git operation confirm it reflects the current
  Roam state.
- The reading render is a convenience copy, not a typeset proof — an inline editorial aside
  left next to a stripped `{{TODO}}` may survive into `writing/`. Don't treat it as final.

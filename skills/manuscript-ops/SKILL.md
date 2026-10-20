---
name: manuscript-ops
description: "Operations over the current manuscript: stage verified read-only inputs, render reading copies, run continuity checks, report citation gaps, and compile derived deliverable docx. Roam exports are historical reconciliation inputs. Never generates or edits prose. Triggers: staging/exporting the manuscript, consistency or citation pass, \"compile for editor/committee\"."
---

# Manuscript-Ops — operations over the manuscript files

The mechanical, structural work around the manuscript, kept strictly separate from the
thinking. This skill never writes prose and never edits a chapter — argument generation and
revision stay in the Book Project. Here Cowork only renders, checks, compiles, and flags.

Read [current writing-voice guidance](../../ai-ops/knowledge/writing-voice.md), the
[book-revision source table](../book-revision/SKILL.md) and the
[manuscript operations contract](../../ai-ops/workflow-contracts/definitions/book-manuscript-operations.json).
The single live manuscript is **Answerable Teaching — Full added notes**, at the existing
Google Doc bound in that source table. Katherine's latest draft controls. Roam, older
Working Copy documents and `source/`/`writing/` exports are historical reconciliation
sources, never a replacement for current text. The September P18 observation is history,
not an instruction to reopen the source decision.

GitHub backup/version history belongs in the designated private manuscript repository under
its [delivery rule](https://github.com/kvond/Answerable-Teaching/blob/main/revision/MANUSCRIPT-DELIVERY-RULE.md).
This skill produces derived checks/artifacts only; it does not perform canonical writeback,
backup commits or publishing. Keep private prose and identifying cases out of this repo.

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

- **Source** — a complete, fresh, read-only snapshot of the bound current manuscript,
  with revision and exact chapter/section recorded. An unavailable source blocks dependent
  work; never substitute an old export. Consult Roam only for explicitly scoped reconciliation.
- **Layout** — preserve the snapshot and derived artifacts in the authorized private working
  location. Existing `source/` and `writing/` paths describe the legacy Roam-export layout,
  not a reason to export prose into this repository or overwrite the manuscript backup.
- **Tracked terms** for the consistency pass (refreshed 2026-09-12 to the public pseudonym
  set, corrected 2026-09-12 to the Aug 23 ruling): Angie, Nancy, John, Toma, Heidi, Marcus,
  Priya, Malik, Ben, Brian, Peter (the greenhouse student), Paul (son), Eli (retired name for
  Peter; find and rename), Zara, Noelle, Gustov, Lezir, Karen, Dana, Cindy, Mike; and the terms legibility,
  sense-making, meaning-making, time-world, chronotope, adjacent agency, intellectual
  authorship, intellectual apprenticeship, critical aspect, shared object, reframing
  epistemic agency, standing as a knower. Add to this list as coined concepts stabilize;
  the same list lives in `manuscript_check.py` and the two must agree.
- **Sources manifest** — `revision/sources.json` in the book repo once the notes lane has
  built it (`sources.json` or `.bib` before then): Bakhtin, Scott, Lareau, Ito, Variation Theory…
- No external Python dependencies; the scripts are standard library only.

## Version retention (Drive working copies)

The existing Full added notes Doc remains the single live manuscript. Preserve its identity,
history and current author text; derived deliverables do not become additional live copies.

- **One live doc.** Use the existing **Answerable Teaching — Full added notes** binding;
  do not rename it to the historical `Answerable Teaching — LIVE` title. Authorized
  apparatus, formatting, APA-7, and HEP-flag passes happen
  *in place* in that doc, versioned through File → Version history (name each version per
  pass: "Ch2 notes renumbered", "APA-7", "mechanical + HEP flags"). Never clone-and-suffix
  into a new copy — that habit is what produced the swarm.
- **Preserve history.** This invocation does not move, delete, rename or change access to
  existing documents. Any separate archive action follows its own authorization.
- **Preserve the binding.** Verify the account/source specified by the source table rather
  than creating another copy or changing ownership.
- **No Roam paste-back.** Roam remains archive/source. Current manuscript delivery follows
  the designated repository's GitHub-first rule, with exact commit and Doc readback; this
  derived-check invocation does not execute that write sequence.

Retention convention only — never touches argument or wording.

## Invoking

One-line requests trigger the matching job with these defaults; nothing writes to Roam or
to the manuscript without showing you the result first:
- "stage the manuscript" / "sync the chapters" → job 2
- "run a consistency pass" / "check cross-references" → job 1
- "check the citations" → job 3
- "compile the manuscript" / "make a docx for the editor" → job 4

## Job 2 — staging / export (the foundation)

1. Resolve the current source/account and shared writer lease under the operations contract.
   Read the exact current revision completely and preserve a read-only private snapshot.
2. Select the checker for the actual supported input: `book-revision`'s manuscript checker
   for a current manuscript snapshot; the bundled reading renderer/consistency checker only
   for the explicitly requested legacy Roam-export layout. Do not treat a rendered export
   as current manuscript or editorial acceptance.
3. Read back the derived artifact, source revision and private destination; report coverage
   gaps. Do not commit source prose or derived private content into optimized-system.

No weekly distill, publish job or schedule is created, resumed or verified by this skill.

## Job 1 — consistency pass (on-demand, e.g. pre-submission)

`python3 scripts/check_consistency.py --in writing/ --out consistency_report.md`

Then read the report and flag the judgment calls: does each cross-reference's claim actually
live where it points; is "double booking" used consistently with its definition; are the
anchor students characterized consistently. Surface findings for the user; never edit the
manuscript — propose changes against the current Doc with exact locations. For a full pass
over the current draft, use the revision skills instead: `book-revision` and its lanes.

## Job 3 — citation integrity (on-demand)

`check_citations.py` is planned, not implemented. Report that limit rather than claiming
the command ran. Use an authorized current source manifest to identify actual citation gaps;
do not invent references or silently normalize uncertain author/year matches.

## Job 4 — deliverables (on-demand)

Use the docx skill to compile `writing/` into a formatted .docx — full manuscript or
per-chapter — with table of contents and front matter, in the editor's required manuscript
format. The format is set once; this is a transform, not a judgment. Compile with
`SKIP_PROVENANCE=1` (or leave `provenance.md` out): no provenance note goes in front of the
manuscript.

## Safety

- Never edit the manuscript. Reading copies and reports are derived and advisory; canonical
  changes require their own accepted change list and authorized writeback/readback.
- Verify the current Doc revision and completeness before checks; historical `source/`
  exports do not establish current state or authorize a backup commit.
- The reading render is a convenience copy, not a typeset proof — an inline editorial aside
  left next to a stripped `{{TODO}}` may survive into `writing/`. Don't treat it as final.

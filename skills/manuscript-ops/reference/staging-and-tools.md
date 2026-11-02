# Staging and tools

Read `../SKILL.md` first; its mandatory boundaries still govern. Path bases do not change when detail moves here: own `scripts/` and `reference/` paths are relative to the original skill root; named sibling-skill paths such as `book-revision/scripts/` are relative to the shared `skills/` directory. Manuscript `revision/` and `book-compile/` paths belong to the designated private manuscript repository; data and derived artifacts belong only in authorized private staging. Never interpret them as paths inside this reference directory or publish private artifacts to the public skills repository. These extracted instructions preserve existing rules; they grant no new authority.

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

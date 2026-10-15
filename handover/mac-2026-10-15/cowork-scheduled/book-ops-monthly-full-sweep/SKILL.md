---
name: book-ops-monthly-full-sweep
description: Monthly book-ops FULL sweep — the O(all-pairs) safety-net dedup that catches drift the nightly delta model can't see. Propose-only; never auto-applies. Surfaces candidates to [[book-ops review]] for Katherine's ruling.
---

Run the MONTHLY book-ops FULL sweep — the ~monthly safety net for the book graph, complementary to the nightly delta run (tags-pages-sweep). The nightly delta only sees new/edited pages; this full sweep re-scans the whole graph to catch drift the delta model structurally cannot see. Today's date is the run date.

Invoke and follow the **book-ops** skill in FULL-SWEEP mode (scripts/dedup_sweep.py, O(all pairs)). Its bundled scripts do the deterministic matching — run them; do not re-derive matching by reasoning.

Contract for this run:
- This is the FULL sweep, NOT the delta. Run scripts/dedup_sweep.py over the whole inventory (ranked candidates + quarantine list). Rebuild vocabulary.json first from [[🏷️ TAGS]] + [[book-ops state]] alias:: blocks + [[never_merge registry]].
- INVENTORY PULL — token first (off-context): fetch the book-ops read token page; if present, run the bundled roam_pull.py in the sandbox with ROAM_GRAPH and ROAM_API_TOKEN set inline on the same bash command (never echo/print/log the token). If unavailable, fall back to the Roam MCP path noted in the skill; say which path was used.
- PROPOSE-ONLY — this run NEVER auto-applies anything. No merges, no repoints, no tag rewrites are written by this task. Full-sweep is tuned for recall and re-surfaces already-adjudicated items, so everything is surfaced for Katherine's review, not acted on. Respect [[never_merge registry]] and the [[book-ops state]] flagged:: list to suppress known pairs where possible, but when in doubt, surface.
- This is an AUDIT, not a purge. NEVER delete or merge a page. Quarantine adds only.
- Respect the book-ops on_create_check before any page would ever be created (none should be, in this run).

OUTPUT:
- Write findings as a new dated section at the top of [[book-ops review]] under a clear "🗓 MONTHLY FULL SWEEP — <date>" header: ranked merge candidates (both titles, layer+score, backlink counts, recommended action), proposed QUE pages, and the quarantine list. Keep it reviewable — if there are many candidates, lead with the highest-confidence and link the rest.
- Post ONE short pointer line on today's Roam daily note (counts from the sweep, not the block list), matching the book-ops one-line convention.
- End with a short chat summary: total pages scanned, candidate count by confidence tier, quarantine count, and the pull path used. Remind Katherine this is the safety-net sweep and that acting on any candidate is her call via the review page.

Do NOT run git. Do NOT write to any RAW_ORIGINALS / frozen directory. Roam is canonical.
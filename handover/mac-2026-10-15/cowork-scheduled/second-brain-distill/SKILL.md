---
name: second-brain-distill
description: On-demand 2nd Brain Distill → routes #Book + literature captures into the zettelkasten notes bank + claims, AND sweeps new zettels (from writing sessions or daily pages) into the Zettelkasten first, then structure notes/articles. Manual trigger only (via launcher).
---

Run Katherine's "2nd Brain Distill" — the on-demand distill of her second brain (zettelkasten + claim/evidence graph), not just the manuscript. It routes recent #Book and literature/reading captures from her Roam daily pages into the per-chapter notes bank and the parallel claim/evidence discourse graph, and sweeps newly created zettels into the Zettelkasten layer.

Today's date is the run date.

NODE-KIND LEGEND (v4, ruled Jul 13 2026 — route by these five kinds):
📇 zettel = one claim (Template - Zettel Claim, 📇 sentence title) · 🗂️ literature/source page = someone else's work (full-citation title, five-field schema; ONE source page per source) · 📋 structure note = sequences claims into an argument (Template - Structured Notes) · QUE — = one question · 🧭 topic map = curates a topic area's atoms, POINTS NEVER CLAIMS (Template - Topic Map; registry = the Type:: [[Topic Map]] backlink list; new maps titled 🧭 {Topic} via the gate; Democratic Pedagogy + Dialogic Pedagogy grandfathered under old titles).

Invoke and follow the **chapter-bank** skill (it owns this work). Operate in capture/distill mode:

1. Scan recent Roam daily-page captures tagged #Book and any reading/literature notes since the last distill. Treat musings, claims, examples, possible subsections, research anchors, and best-phrasing fragments as routable.
2. ZETTEL SWEEP: new zettels are first-class distill objects — whether minted during live writing/working sessions (on content pages, CLM nodes, Author Block, article pages) or drafted on daily pages. For each new zettel-like note since the last run:
   a. Route it to the Zettelkasten FIRST: verify it is registered in the canonical layer — correct template ([[Template - Zettel Claim]] for claims with 📇 sentence title; concept-note form for concepts), Meta/Provenance fields, Index:: [[🌿 Evergreen Notes]], and selective threading on [[🗂️ ZettleKasten]] (entry points for spine-level notes only, per the Jul 12 ruling; the Index:: backlink is the complete registry).
   b. THEN propose connections outward where Scope matches: 📋 structure notes, hubs like [[book's conceptual core]], Claims Hub, the matching 🧭 topic map(s) (add a pointer + role phrase; refresh the map's Current as of::), and active article pages (e.g. Article #1). Propose-then-confirm — never auto-place into articles or chapters.
   c. Zettels stranded as sections on other pages, left in pre-reconfigure format, or duplicated get flagged with a proposed fix, never auto-merged or auto-moved.
3. TOPIC-MAP HYGIENE (both directions): (a) new zettels/QUEs/sources that belong to a mapped topic area → propose pointer lines on that 🧭 map; (b) any claim-like sentence found ON a topic map is a 📇 zettel trying to be born — propose extraction through the book-ops gate, leaving a pointer behind. Topic maps are judged by coverage and findability, never correctness.
4. Route each remaining capture into the matching chapter's notes bank by Scope match — append-and-dedupe, NEVER overwrite.
5. Where a claim is stable and reusable, propose promoting it to an atomic CLM/📇 node and attach EVD evidence via DG relations. Sources: ONE page per source, full-citation title (check the gate for an existing source page before proposing a new one — near-duplicate citations are a known trap).
6. GATING: every new page (📇, QUE, concept, 🧭 topic map, reference) must pass the book-ops on_create_check first. Never mint pages unprompted — surface proposed new pages for Katherine's approval rather than creating them silently.
7. TOOLING CONSTRAINT: the MCP page-rename tool is broken (book-ops state, Jul 13 note). Never rename pages — propose renames for Katherine to do in the Roam UI (UI rename repoints all refs).
8. Never write prose. This skill organizes, routes, tags, and gates only.

Output: post a short, skimmable summary to today's Roam daily note — what was routed and where, zettels registered/flagged, topic-map pointers proposed, any claims proposed for promotion, and anything flagged for approval (new pages held at the on-create gate). Manual trigger only (via the Block Distill Launcher).
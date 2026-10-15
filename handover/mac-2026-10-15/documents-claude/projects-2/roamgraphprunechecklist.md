# Roam Graph — Prune Checklist

Audit run Jul 10, 2026 · read-only, nothing deleted.

## The headline (read before you prune)

**Agent output is not the problem.** Machine-written blocks are ~3.5% of blocks, ~4% of text.
The graph is big because *your corpus* is big.

| Metric | Value |
|---|---|
| Pages | 2,320 |
| Blocks | 50,813 |
| Block text | 6,511,824 chars (~6.5 MB) |
| Daily pages | 1,236 pages · 32,163 blocks (63%) · 3.22M chars (49%) |
| Long blocks (>300 ch) | 5,431 blocks (10.7%) holding **53.8% of all text** |
| Exact-duplicate long blocks | ~224,500 wasted chars (3.4%) |

Ten percent of your blocks carry over half the text. **Character mass, not block count, is what's warning you.**

**Realistic prune ceiling: ~2,000–2,600 blocks / ~250–350k chars — about 4–5% of the graph.**
That alone will not clear a size warning. The two structural decisions at the bottom are the only things that will.

---

## 🛑 GATE — do this first, no exceptions

- [ ] **Export the full graph — BOTH formats.** Roam → Export All → **JSON** *and* **EDN**.
- [ ] Verify the export file actually opens and is non-trivial in size.
- [ ] Park a copy on the T7 (you already have an "export Roam to T7 monthly" TODO — this closes it).

Roam's block-level undo does **not** survive a session, and the page-delete confirm does **not** stage a backup. No deletions until the export lands.

---

## Tier 1 — safe, do these

- [ ] **`Final - Answerable Teaching - to ch 2`** — 154 blocks / 67,181 chars.
      **0 backlinks; 130 of its substantive blocks are exact duplicates of content on other pages.**
      Functionally redundant. Not regenerable, but recoverable from export. *Best single candidate.*
- [ ] **`book-ops review archive · through Jul 9 2026`** — 145 blocks / 26,471 chars.
      Resolved history, already superseded by `book-ops state`. 1 backlink.
- [ ] **Daily Brief blocks on date pages** (17 briefs) — 643 blocks / 56,738 chars.
      Fully regenerable. **Collapse or archive rather than hard-delete.**
- [ ] **Sweep-log blocks on daily pages** (12 sweeps) — 147 blocks / ~10,000 chars. Regenerable, trivial.

## Tier 2 — check before you cut

- [ ] **Perplexity / ChatGPT scratch pages** — 457 blocks / ~80,700 chars.
      (`Perplexity draft` **0 backlinks**, `Perplexity 2nd draft` **0 backlinks**, `Perplexity Notes for ch 11`,
      `Notes from perplexity`, `ChatGPT Chat Export`.)
      AI scratch drafts — **not regenerable.** Skim for unharvested content first.
- [ ] **`roam/js/pdf/data/*`** (23 pages) — ~324 blocks / ~83,800 chars (one page holds 44,778).
      PDF highlight data. **Deleting breaks annotations on those PDFs.** Only prune where the source PDF is gone.
- [ ] **`zettel-harvest review`** — 288 blocks / 47,475 chars.
      Disposable *after* you work its open flags (**F2, F4 still live**). Don't touch yet.
- [ ] **Duplicated trees on Noelle / Maya / Sense-making** — ~45–90 blocks / ~9,500 chars.
      Import artifact, already flagged F4. This is a correctness fix, not a size fix.

## Skip — costs nothing

- **Empty pages** — 536 pages have no substantive block, but only **20** have zero blocks *and* zero backlinks.
  The other 516 are live tag/stub targets. Deleting them breaks refs for zero gain.
- **`book-ops state`** — 158 blocks / 22,192 chars. Regenerable in principle, but it *is* the durable memory. Leave it.

---

## ⛔ DO NOT TOUCH

- **Daily-page captures** — 32,163 blocks / 3.22M chars. Half the graph, and it's your thinking.
- **`Answerable Teaching/` namespace** — 32 pages / 2,199 blocks / 803,624 chars.
- **`Book Draft 2 (sourced notes)`** — 542 blocks / 150,190 chars (only 30 duplicated — mostly unique).
- **Discourse nodes** (CLM / EVD / QUE / 📇) — 109 pages / 1,291 blocks / 105,316 chars.
- **Zettles + ZettleKasten + Evergreen Notes** — 527 blocks / ~79,600 chars.
- **Spanish practice log** — 387 blocks / 41,458 chars.
- **Projects · Status of the Blocks.**

---

## The two that actually move the needle

Both are **decisions, not cleanups.** Flagged, not recommended.

### 1. `Book Draft 1` — the single largest object in the graph
**1,909 blocks / 509,573 chars / 7.8% of all graph text.** 28 backlinks.
Only 100 of its blocks have exact twins elsewhere, so it is **genuinely unique prose** — this is not dead weight.

- [ ] Verify whether Book Draft 1 also lives in your manuscript files (check `manuscript-ops` staging).
- [ ] If it does: the Roam copy is a snapshot you're paying full freight for → archive it out.
- [ ] If it doesn't: **keep it.** Do not delete unique prose that exists nowhere else.

### 2. Pre-2024 daily pages (2020–2023)
**13,386 blocks / 1,232,755 chars — 26% of blocks, 19% of text.**
The only bloc large enough to meaningfully shrink the graph.

- [ ] Decide: split to a **second/archive graph** rather than delete.
- [ ] This is an era-archive decision — old dailies are still your thinking, just cold.

---

## Bottom line

Pruning the machine output is good hygiene but won't fix the size warning. If the graph genuinely
has to get smaller, it's the **pre-2024 daily archive split** that does it — and that's a
preservation move (second graph), not a deletion.

# book-ops change log

## 2026-06-15 — Phase 1 (read-and-propose; NO Roam writes)
- Convention decision: questions standardize on the `QUE —` prefix (depot program with
  evidence-link writing section). `Q:` reserved for a future from-scratch graph.
- Script fix (local, reversible): `is_q` detection in `dedup_sweep.py` and
  `on_create_check.py` now recognizes `QUE —` (and `Q:`) as question-type, so the
  permanent on-create guard and the sweep no longer treat your QUE pages as concepts.
  One-line change in each file; revert by restoring `startswith("q:")`.
- Dropped from scope per user: Health / tracker / system "noise" pages (no merges proposed).

## 2026-06-15 — re-sweep (current graph, before apply)
- Re-pulled inventory after your dedup pass: 485 pages (was 467). Artifacts: inventory2.json,
  dedup_review2.md, dedup_candidates2.json, semantic_candidates2.json. (No Roam writes.)
- GRAPH CHANGE: `Beyond Motivation` renamed to `Answerable Teaching` (the book hub). Old
  links auto-repointed by Roam. Question-page source tags updated to cite `Answerable Teaching`.
- Health-log import added ~16 noise pages, incl. 13 `- `-prefixed duplicates of existing
  trackers (`- Calories`/`Calories`, etc.). OUT OF SCOPE for book-ops — fix in the health-log
  template (it is prepending "- " to page titles), not here.
- Added to apply batch: A4 chapter tag — `Ch5` ⇐ `CH5`.
- A1 reduced to JUST `Book` ⇐ `Book.` per your call; rest of punctuation batch deferred.

## 2026-06-15 — APPLIED to Roam (snapshot confirmed by user)
Created 18 QUE — question pages (Type:: #q-book-resolves / #q-about-book, Source:: attribute).
Applied merges (repoint refs -> canonical, move content, tombstone loser):
- B1#3 [[Individualism is a theory of society, not its opposite]] -> [[...not of the lone individual (Hayek)]] (content moved, 7 refs repointed)
- B1#4 [[Dialogism dissovles the internal/external divide]] -> [[Dialogism dissolves the intrinsic/extrinsic motivation dualism]] (content moved, 1 ref)
- B1#1 [[Burgh — democracy is a process, not a destination]] -> [[...not something to educate toward]] (1 ref)
- B1#2 [[Real (2022), Us…]] -> [[Real (2022), Us — the relational critique of individualism]] (1 daily-note ref)
- A1  [[Book.]] -> [[Book]] (2 daily-note refs; phantom page from sentence-ending #Book.)
- A3  [[Finance]] -> [[FINANCE]] (2 refs) ; [[calls]] -> [[CALLS]] (2 refs) ; [[errands]] -> [[ERRANDS]] (3 refs)
All 8 losers verified 0 inbound refs post-merge; each left with a "Merged into [[canonical]]" tombstone.
DEFERRED (not applied): entire A2 agency family (both layers kept); A4 Ch5<-CH5 (awaiting confirm);
rest of A1 punctuation batch; self-duplicated [[Authorial agency]] page (user handling separately).

## 2026-06-15 — A4 applied (after content check)
- Checked CH5: no page content of its own (pure casing-variant tag) -> eligible per rule.
- A4 [[CH5]] -> [[Ch5]] : repointed 6 #CH5 refs to #Ch5, tombstoned CH5. Verified 0 inbound refs to CH5.
  Ch5 now carries all references (6 repointed + 1 pre-existing #Ch5 + tombstone).

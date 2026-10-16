---
name: answerable-nightly-distill
description: >
  Nightly distill for the Answerable Teaching manuscript. After a writing day, captures what
  changed, flags what needs attention, keeps the connection layer current, logs the day, and
  refreshes the GitHub backup. Incremental — only the chapters edited today, PLUS any page whose
  Roam edit-time is newer than its backup (freshness check). Replaces the book side of the old
  weekly Sunday distill. Trigger nightly (scheduled) or on "distill my writing".
---

# answerable-nightly-distill

Runs after a writing session so the graph never drifts: capture → flag → (optionally) tag → log → back up.

## MODE (set at top of the run)
- **capture** = read-only: log + flag only, edit nothing. (Safest for unattended runs.)
- **capture+tag** = also run the inline tag/citation pass on today's chapters (edits prose; uses the
  fidelity self-check). Default to **capture** unless you've told it **capture+tag**.

## Source of truth (read first, every run)
- ~/Documents/Claude/manuscript-ops/LINKING_SPEC.md — term→page vocabulary, aliased-link rule, criticism map.
- **[[🌿 Evergreen Notes]] — the index of the current link vocabulary.** This replaced the retired
  `[[Answerable Teaching/Tag Hub]]` (Jul 2026); the Tag Hub page no longer exists — do not read or write it.
  Evergreen Notes **is the index**: every evergreen note lands there automatically via its
  `Index:: [[🌿 Evergreen Notes]]` backlink, so "absent from Evergreen Notes" = "not yet a note."
  - **Note pages carry the `📇` title prefix** (e.g. `[[📇 Dialogism is not discussion]]`). The 📇 page is the
    canonical note. An **unprefixed twin** of the same title is a merged/superseded stub awaiting deletion —
    never link a chapter to one. See the link-target guard in STEP 2.
  - `[[🗂️ ZettleKasten]]` is now a 2-block pointer, and `[[🗂️ ZettleKasten — pre-index archive · Jul 12 2026]]`
    is a frozen snapshot. Neither is authoritative; both are historical.
- [[Answerable Teaching/References]] — this manuscript's reference list (`[[REFERENCES]]` = the other book).
- ~/Documents/Claude/answerable-nightly-distill/ … and the tag pass at ~/Documents/Claude/answerable-tag-pass/SKILL.md.

## Repo coordinates (the backup target — everything needed to push)
- **Local repo:** `~/Documents/projects/Answerable-Teaching`
- **Remote:** `git@github.com:kvond/Answerable-Teaching.git` (SSH) · **branch:** `main`
- **Layout:** `source/` = faithful Roam export · `writing/` = rendered reading copy · `scripts/render_reading.py` = the renderer · `scripts/export_pages.py` = freshness check + faithful export straight from the Roam backend API (auth: gitignored `.roam-token` in the repo root) · `SYNC.md` = the page→file manifest (authoritative; filename map table + machine-readable ```exclude``` block, both parsed by export_pages.py).
- **Push only authenticates on Katherine's Mac (Keychain/SSH).** A scheduled/sandbox run cannot push — it commits and hands off the command (see STEP 5/6).
- **The exact push command (always give this when not pushed):**
  `cd ~/Documents/projects/Answerable-Teaching && git push origin main`
  (or `./sync.sh`, which renders + commits + pushes in one step.)

## STEP 1 — Scope (manifest-integrity guard, then edited-today UNION freshness check)
**Preferred path (fast): run the script.** From the repo root:
`python3 scripts/export_pages.py --check`
It performs everything below in one call — resolves every SYNC.md entry against the live graph
(⚠ on zero/multiple matches), flags unmapped pages not covered by the SYNC.md ```exclude``` block
(surface these; exclusion is the author's call), and prints the export set = edited-today ∪ stale
(Roam max `:edit/time` vs `git log -1 --format=%ct` per file). Treat its ⚠ lines exactly as the
manual ⚠ rules below. Fall back to the manual MCP procedure only if the script/API fails.
**Known blind spot (both paths): pure block DELETIONS don't bump a page's max edit-time, so a
page that only lost blocks won't show stale.** Mitigation: about once a week (or when asked),
run `python3 scripts/export_pages.py --export all --verify` and report any file whose diff isn't
explained by known edits.
**0. Manifest integrity check (run FIRST, before scoping).** The map resolves each entry to a page by title, so
a rename or a new parallel draft silently drops a chapter from the backup with no error. (Map entries may be
abbreviated — e.g. "Three School Models…" — so resolve by best-match, not byte-equality.) Reconcile `SYNC.md`
against the live graph before anything else:
   - (a) For every entry in the SYNC.md filename map, confirm it resolves to exactly ONE live `Answerable
     Teaching/` page. If an entry resolves to **zero** pages (the page was renamed/deleted) or to **two or more**
     plausible pages (a parallel draft appeared), do **not** silently skip or guess — record a ⚠ in the
     completion note and the Writing Log naming the entry, its `source/` file, and the candidate page(s). A
     backup file whose live page is gone is frozen and will silently rot.
   - (b) For every `Answerable Teaching/` page in the graph, confirm it is either mapped in SYNC.md or covered
     by the SYNC.md "Excluded" set (`… — Notes Bank`, Writing Log, parallel/superseded drafts, etc. — the
     `Tag Hub` / `Discourse Graph` / `Claims Hub` patterns are retired and now match nothing; harmless, left
     inert). Any page that is neither — an unmapped, non-excluded namespace page —
     is a candidate canonical page falling out of backup: flag it ⚠. Do **not** auto-add or repoint the
     manifest; which page is canonical is the author's call.
   - This is what catches splits like Chapter 9 "the whole school" vs "… V notes," and the mis-namespaced
     Chapter 5 page. Surface drift; never resolve it silently.
Build the export set from BOTH checks — never trust "modified today" alone, because edits made *after* an
earlier export in the same session get silently missed:
1. **Edited today** — `Answerable Teaching/` pages with block `:edit/time` since local midnight
   (roam_find_pages_modified_today filtered to the namespace, or a datomic max-edit query).
2. **Stale vs backup (the real safety net)** — for EVERY `Answerable Teaching/` page, compare its max block
   `:edit/time` (ms) against the last commit time of its mapped `source/` file:
   `git log -1 --format=%ct -- source/<file>` (seconds → ×1000 for ms). If Roam edit-time > file commit-time,
   the page is **stale** → add it to the export set. This catches anything that drifted, not just today's work.
   Map pages→files via `~/Documents/projects/Answerable-Teaching/SYNC.md`.
The export set = (edited today) ∪ (stale). If it is empty, write a one-line "nothing to back up" log entry and stop.
- For each page in the set, note a rough **word-count delta** (momentum).

## STEP 2 — Capture & flag (read-only)
For the changed chapters, collect:
- **Editorial markers** — new `【NOTE/GAP/FIX/VERIFY】` and `[draft …]` added today, AND any resolved since
  yesterday. This is the live to-do/done list.
- **Filled vignettes** — `[GAP — your vignette]`/`[draft]` placeholders that became real prose.
- **New concepts** not yet indexed on [[🌿 Evergreen Notes]] → flag "needs a note." Evergreen Notes is the
  complete index (every note backlinks there via `Index::`), so absence from it is real evidence the concept
  has no note yet — not just that it wasn't picked as an entry point.
- **Link-target guard (dead-stub check) — run over every chapter link changed today.** For each `[[…]]` target
  in the changed chapters, confirm the target page is not a superseded stub: a page whose first block starts
  with `⛔ Merged` / says "canonical is …" / "flagged for … deletion". If a chapter link lands on one, flag it
  ⚠ with the canonical `📇` title to repoint to. **Why this exists:** on Jul 12 2026 a rename of
  `Dialogism-Is-Not-Discussion` → `Dialogism is not discussion` silently dragged the Chapter 4 and Chapter 5
  links onto the merged stub of that name, while the real 37-block note sat at `📇 Dialogism is not discussion`.
  Roam rename-ripple moves links without touching prose, so nothing else in this distill would have caught it.
- **New in-text citations** → check each against [[Answerable Teaching/References]]; append any with no entry
  to ~/Documents/Claude/manuscript-ops/orphan-citations.md (do not invent reference details).
- **New open questions** in the prose → candidate `QUE —` pages (run book-ops on_create_check before suggesting; do not mint unprompted).

## STEP 3 — Tag/citation pass (ONLY if MODE = capture+tag)
- Invoke the answerable-tag-pass over today's changed chapters: inline ALIASED concept/QUE links +
  citation links. The index refreshes itself — a note appears on [[🌿 Evergreen Notes]] by carrying
  `Index:: [[🌿 Evergreen Notes]]`; there is no hub list to hand-maintain (that was the old Tag Hub).
- When linking a chapter to an evergreen note, **the target must be the `📇`-prefixed page.** Never point
  chapter prose at an unprefixed twin — those are merged stubs pending deletion.
- HARD RULES (non-negotiable, this edits the book): aliased links only — wrap existing words, change
  nothing; never link inside `【NOTE…】`; never create a target page by linking (verify it exists);
  self-verify each edited block (strip wrappers → must equal the original verbatim) and REVERT any block
  that fails. Report PASS/FAIL per block.

## STEP 4 — Log the day
- Append a dated entry to [[Answerable Teaching/Writing Log]] (create the page if missing) under a
  `[[<today, ordinal>]]` bullet: chapters touched + word deltas, markers added/resolved, vignettes filled,
  new concepts/citations/questions flagged, and (if tagged) what was linked. Keep it terse and specific —
  quote her actual new phrasing where it helps. This log is the daily capture; nothing else compounds it.

## STEP 5 — GitHub backup (the STEP 1 export set)
- **Preferred path: `python3 scripts/export_pages.py --export stale`** — pulls each scoped page over
  the Roam API and writes the faithful `source/<file>` byte-exactly (2-space indents, `- ` bullets,
  `#`×heading-level, NBSP→space, single trailing newline). No page content should transit the LLM.
  Then regenerate the reading copy: `python3 scripts/render_reading.py --in source/ --out writing/`.
  For the capture step, read the *diffs* of the exported files (plain `diff` vs a pre-export copy, or
  `git diff` — read-only), not the whole chapters.
- Fallback (script/API down): manuscript-ops Job 2 logic — MCP markdown fetch, drop the
  `# Answerable Teaching/<title>` first line + one blank line, write byte-for-byte, then render.
- `git add -A`; review `git diff --cached --stat` before committing.
- Commit (`nightly: <pages>`), then push. **Push only works on the Mac.** If running locally/attended, run
  `./sync.sh` (renders + commits + pushes). If unattended/sandboxed, commit and ALWAYS end by printing the
  literal command for Katherine to paste:
  `cd ~/Documents/projects/Answerable-Teaching && git push origin main`

## STEP 6 — Completion note
- One short summary: pages exported (today + any stale ones caught), deltas, top markers added/resolved, any
  new orphan citations, whether a tag pass ran (and any FAIL/revert), and the git status.
- ALWAYS state whether the work is pushed or pending; if pending, print the exact push command above so it is
  ready to paste. Never end a run that left unpushed commits without surfacing that command.

## Safety
- Roam is canonical; `source/`+`writing/` are derived. Never edit `source/`/`writing/` by hand.
- In **capture** mode, change nothing in the manuscript — only the Writing Log, the orphan list, and the
  GitHub backup are written.
- Never mint Roam pages (QUE or otherwise) without flagging for approval.

## Notes
- This replaces the **book** side of the retired Sunday distill. If you still want the other domains
  (Health, Teaching, Personal/Intuition) compounded, they now have no scheduled home — decide separately.
- Pairs with: answerable-tag-pass (the editing pass) and manuscript-ops (extract/check/compile).

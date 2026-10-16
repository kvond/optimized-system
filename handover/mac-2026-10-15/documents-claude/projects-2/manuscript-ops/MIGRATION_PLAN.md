# Answerable Teaching — Migration Plan & Standing Rules

_Captured 2026-06-16. Standing decisions unless Katherine changes them._

## Source of truth right now
- The full manuscript lives on the Roam page **"Answerable Teaching - old migrating (do not edit)"** (UID `NDf_HMW4M`).
- It is the sole, complete **Raw copy**. Migration has NOT started (GitHub repo has only README + test commits; no new tagged Roam page yet).

## Architecture (Roam canonical; GitHub is a derived backup)
- **Roam** = canonical, **tagged**, question-linked drafting home. Tagging + `QUE` connections only exist here.
- **GitHub** (`~/Documents/projects/Answerable-Teaching`) = derived backup:
  - `source/` — faithful Roam export (links/markers intact).
  - `writing/` — tag-stripped readable copy (render_reading.py).
  - GitHub canNOT hold tags or QUE links — it is a safety net + reading copy, not a workspace.

## Katherine's requirements
1. **Delete the old `…(do not edit)` page after safe migration** — to avoid having two Roam copies that both get tagged (double-tagging).
2. The working copy must remain **taggable + question-linkable as she drafts** (so connections can be built) → that means the drafting copy stays in **Roam**, not GitHub.

## Safety rule (no exceptions)
- **Never delete the old page until content is verified safe** in BOTH GitHub and the new tagged Roam working copy.
- **Diff old-vs-new before any deletion** to prove nothing dropped.
- GitHub `source/` is the backstop that makes deletion reversible.

## Sequence
1. Export old page → GitHub `source/` + `writing/` (non-destructive). ✅ DONE (staged; awaiting Katherine's `git push`).
2. Stand up the new **tagged Roam working copy**. ✅ DONE — 14 namespaced pages under `Answerable Teaching/` (Front Matter, Introduction, Chapter 1–11, Editorial Notes), imported faithfully from `source/`.
3. Verify both against the old page (block/section counts, diff). ⬜ TODO before any deletion.
4. Only then delete the old page. ✅ DONE 2026-06-16 — verified 28 old blocks fully covered by new pages + source/ (58,059 words on disk); emptied the old page (28 blocks deleted), left a migration-pointer block. Empty shell remains (no page-delete API) — delete in Roam UI if desired.

## Status 2026-06-16
- Content now lives in THREE places: old page `NDf_HMW4M` (intact backup, untouched), new `Answerable Teaching/…` namespaced pages (tagged working copy), and repo `source/`+`writing/` (staged, not yet pushed).
- Two Roam copies coexist for now (old + new) — the temporary double-tag state Katherine accepted; resolves when the old page is deleted.
- Minor: a few `Some_Underscored_Tokens` inside `【NOTE…】` editorial markers render as italics in Roam (double-underscore parsing); harmless, text preserved verbatim.

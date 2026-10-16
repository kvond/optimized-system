---
name: answerable-tag-pass
description: >
  Post-writing-session connection pass for the Answerable Teaching manuscript. After a
  drafting session, re-applies the controlled-vocabulary inline links (zettelkasten notes,
  QUE questions, source citations), refreshes the criticism block, and updates the Tag Hub —
  only for the chapter(s) just edited. Use when the user says "update the tags", "tag pass",
  "I finished writing Chapter X", or after any Answerable Teaching writing session. It EDITS
  manuscript prose deliberately (the working copy), so it is separate from manuscript-ops
  (which never edits).
---

# answerable-tag-pass

Keeps the manuscript's connective tissue current as it's drafted. New prose arrives untagged;
this pass wires it into the zettelkasten so cross-book linked-references stay complete.

## When to run
- After a writing session on any `Answerable Teaching/` chapter page.
- Default scope: namespace pages modified today (`roam_find_pages_modified_today` filtered to
  `Answerable Teaching/Chapter`), or a chapter the user names.

## Inputs (the durable spine — read these first)
- `~/Documents/Claude/manuscript-ops/LINKING_SPEC.md` — the controlled vocabulary (term → target
  page), the aliased-link rule, and the criticism→chapter map. Source of truth for what links to what.
- `[[Answerable Teaching/Tag Hub]]` — the current alphabetical index; this pass appends to it.
- `[[REFERENCES]]` in Roam — its child blocks each link a source's citation page; the match
  list for in-text citations. Build the citation-match set by reading this page (don't hardcode).

## Procedure (per target chapter)
1. **Fetch** the page (`format: structure`) for block uids; then pull the EXACT verbatim
   `:block/string` (datomic) for every block you intend to edit. Never edit from a preview.
2. **Concept / question links** — per `LINKING_SPEC` dictionary, wrap the first (and one more if
   natural) occurrence of each term in an **aliased** link: `[exact words]([[Target]])`. Add QUE
   links where the prose raises a question on the list.
3. **Citation links** — for each in-text citation `(Author, Year)`, if a matching citation page
   exists on `[[REFERENCES]]`, wrap the in-text cite in an aliased link to that page. Skip cites
   with no page. Do NOT link inside `[1]`/superscript footnote markers unless there's a real block.
4. **Criticism block** — ensure the top `**⚠ Criticisms to address — review before writing**`
   block exists with the chapter's mapped QUE(s) + `[[Addressing Criticisms]]`. (Leave any the
   author repositioned alone.)
5. **Apply** all edits in ONE `roam_process_batch_actions`.
6. **Tag Hub** — add any NEW target pages to `[[Answerable Teaching/Tag Hub]]`, keeping each
   section alphabetical (full-rewrite via `roam_update_page_markdown` is simplest).

## Hard rules (fidelity — this edits the book)
- Only ever wrap text that is **already there** in `[..]([[..]])`. Never change a word, mark,
  space, or curly/straight quote. Preserve `—`, `’ “ ”`, `**bold**`, `__italics__`, and
  `【NOTE…】` markers exactly. Never link inside `【NOTE…】` editorial markers.
- **Never create a target page by linking** — verify every target exists (datomic) first.
- **Self-verify each edited block**: re-fetch its `:block/string`, strip the `[..]([[..]])`
  wrappers, and confirm the remainder equals the original verbatim. Report PASS/FAIL per block;
  on any FAIL, revert that block.
- Roam is canonical. The GitHub `source/`+`writing/` export is regenerated downstream (run
  manuscript-ops Job 2 after a tagging pass if you want the backup current).

## Output
- Per chapter: blocks edited → targets, new vocabulary added, criticism status, fidelity PASS/FAIL.
- Updated `[[Answerable Teaching/Tag Hub]]`.

## Notes
- Incremental by design — touch only the session's chapter(s), not the whole book.
- Pairs with the weekly `#book` distill and with manuscript-ops (extract/check/compile, never edits).
- Can be wired to a scheduled task, but prefer manual/after-session triggering since it edits prose.

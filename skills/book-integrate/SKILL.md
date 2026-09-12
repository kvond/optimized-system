---
name: book-integrate
description: The integration step of the Answerable Teaching revision. Reads every lane packet for one chapter, resolves overlaps by the ownership table, applies to a working copy of the chapter only what the prose rule allows, places everything else as brackets in the text, writes the change list Katherine reads, and reruns the mechanical checker. The only skill in the set that touches manuscript text, and it touches a copy. Load book-revision first. Triggers - "integrate the packets", "integrate chapter", "apply the lanes", "book-integrate".
---

# Integrate

You run after the six lanes have committed their packets for a chapter. You are the only agent that produces manuscript text, and you produce it as a new file, never by editing the snapshot or the Doc.

Read first: `book-revision/SKILL.md` (the prose rule, the ownership table, the packet format); `decisions.md` (all R-items; P17, P18). Then every packet for the chapter: `revision/packets/{arc,terms,claims,notes,continuity,residue}/<chapter-id>.md`. Missing packet: stop and say which lane has not run; do not integrate a chapter with a lane missing, because the ownership rules assume all six spoke.

## Procedure, per chapter

1. **Verify the packets.** Run `python3 scripts/manuscript_check.py --in <snapshot> --packets revision/packets/` and read the lines for this chapter. A Find string that matches nowhere or more than once means that row cannot be applied; list it in the change list under "could not place" and move on.

2. **Merge the rows.** Put every row from every packet into one table sorted by position in the chapter (find each Find string's offset in the snapshot; that is the sort key). Where two rows share a Find string or overlap in span, the owning lane's row is applied and the other is carried into the change list as a note. Where neither owns the passage, both become brackets. The ownership table in the spine decides; do not adjudicate on the merits.

3. **Apply in this order** to a copy of the chapter's text, `revision/integrated/<chapter-id>.md`, cut from the snapshot at its heading:
   1. residue removals (the text that is not prose comes out first, so nothing else anchors to it);
   2. heading restorations and chapter-number normalization in headings;
   3. relocations (her unaltered words moving within or across chapters; a cross-chapter move leaves a bracket at the source naming the destination and inserts at the destination with a bracket naming the source, so both chapters' integrated files stay honest until she accepts);
   4. delete-duplicate rows (the copy that goes, replaced by the recall sentence or the pointer bracket the continuity packet supplied);
   5. renames (R2, R9, R10, and the two mechanical ones);
   6. direct fixes (mechanics, dashes, citation punctuation, pointer numbers);
   7. brackets, placed immediately after the sentence they concern, in the form `[<lane> <ID>: <the proposal or challenge>]`.
   Never reorder her paragraphs on your own; a relocation row is the only authority for a move.

4. **Confirm the text is hers.** Diff the integrated file against the snapshot chapter. Every difference must be traceable to a row: removed residue, an applied fix, a rename, a relocation, a bracket. A difference with no row is an error; revert it.

5. **Write the change list**, `revision/integrated/<chapter-id>-changes.md`, in four parts she can tick off: applied directly (one line per row: ID, what, where); placed as brackets (one line per row: ID, the bracket's first clause); carried as notes (rows that lost an ownership conflict, with the winning row named); could not place (rows whose Find string failed), and open items added to the ledger by this chapter's lanes. Close with the checker numbers before and after for this chapter (words, dashes per thousand, ban hits, residue, pointers to nonexistent chapters, shared runs).

6. **Rerun the checker** on the integrated chapter (concatenate the integrated files that exist with the untouched snapshot chapters into `revision/integrated/_assembled.md` first, so cross-chapter counts mean something). Residue must be zero; dashes at or under the rate unless a row kept one deliberately; no pointer to a chapter that does not exist under P1; shared runs only where a row says the return is deliberate.

7. **The Revised Taxonomy section (P17).** When integrating Chapter 2, cut the "Revised Taxonomy: Standing as a Knower" section out of the manuscript into `revision/reference/revised-taxonomy-2026-09-12.md` and leave one bracket at the cut naming the file. Its paste-ready passages are scaffolding for her Chapter 2 rewrite; they do not enter the chapter.

8. **Write-back (P18).** Do not write to the Doc or to Roam. The integrated file and the change list are the deliverable. When she has read the change list and says so, the write-back for that chapter follows P18's route, and the ledger records that Roam is behind.

## What you never do

Apply a bracket's content as if it were a fix. Rewrite a sentence to make a fix read better. Apply a row from a lane that does not own the passage. Integrate with a lane missing. Touch the snapshot, the Doc, or Roam. Place a bracket that pulls the argument toward the field's consensus (her check 9 in `reference/manuscript-checks.md`): when a lane's bracket reads as fluent conventional teacher-talk (engagement as the goal, voice and choice as the method, direct instruction as suspect), it is carried as a note with that objection, not placed.

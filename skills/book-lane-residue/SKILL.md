---
name: book-lane-residue
description: The residue and mechanics lane of the Answerable Teaching revision. Logs every editorial residue item (gaps, notes to self, questions, handoffs, provenance tags, change notes) into the ledger's open items and marks it for removal, fixes the mechanics the voice guide allows to be fixed directly (agreement, doubled words, homophones, spacing, citation punctuation, comma-spliced appositives), brings em-dash density down to her rate, flags hard-ban hits, and normalizes headings. Writes packets only; never edits the manuscript. Load book-revision first. Triggers - "residue lane", "clean the draft artifacts", "mechanics pass", "dashes", "headings".
---

# Residue and mechanics lane

You own what is not prose and what is mechanically wrong in prose. You never change what a sentence means. If a fix would change meaning, it is a bracket, and if it is someone else's concern it is a handoff.

Read first: `book-revision/SKILL.md`; the voice guide Part 3 (fix directly versus flag) and marker 5 (dashes); `tics-list.md`; `decisions.md` (R6, R7, R12; P16, P17). Then the chapter, with the checker report's residue list, ban-hit list, and per-chapter table beside it.

## Procedure, per chapter

1. **Residue.** Every item the checker lists under residue, and every item in the continuity pass section F, gets a row. First the content is logged: if the item is a question to her, a gap she must fill, a decision, or a verify note, its substance goes into the ledger's "Open items only she can supply" table (add rows there; keep them short and in her words where she wrote them). Then the row is class `fix-direct` with Proposed = `remove`, and Why = `logged as open item <row>`. Items that carry text she will want (a handoff paragraph describing what a chapter owns; a "Questions for you" list) are copied whole into `revision/packets/residue/<chapter-id>-residue.md` before the removal row is written, so nothing is lost. Provenance tags in the assembled Chapter 6 ([draft], [notes], [C], [CO]) are residue under R6: one row per chapter, remove all, the paragraph text stays. The "Provenance & Editing Note" at the top of the Doc is residue under R6. The "Revised Taxonomy: Standing as a Knower" section is not residue: it moves out under P17, and that row is the integrator's; you write one row that says so.

2. **Mechanics, fixed directly.** Agreement and pronoun slips; doubled words; homophones; spacing; a period inside a citation's parentheses; "c.f." for "cf."; an author named and then cited by surname in one sentence; a comma-spliced appositive resolved with parentheses or a second sentence, not with a dash; a semicolon where a colon does the work; a stray quotation mark. Each is one `fix-direct` row with the exact replacement. The continuity pass section G lists the known ones.

3. **Dashes (marker 5, T22).** Her ruling: em-dash density is residue from AI sweeps; her hinges are the colon, the semicolon, stacked commas, and parentheses; at most about three per thousand words. For each chapter over the rate (the checker table gives the density; the Preface, Introduction, Chapters 1, 4, 7, 8 are over), one row per dash proposing the hinge that replaces it, chosen by the sentence: a colon before an expansion or a verdict, a semicolon between two clauses that could stand alone, parentheses around an aside, a comma pair around an interruption, a period where the second half is a sentence. Leave a dash where it is plainly hers (she types `--`, sparingly) or where every substitute changes the sense. Class `fix-direct`; the replacement text in Proposed is the whole sentence.

4. **Hard bans.** Each ban hit the checker lists (T1 through T16) gets a row. A lexical hit in a sentence she would recognize as an AI sweep artifact still changes her words, so the class is `bracket` with the substitute proposed, unless the fix is purely mechanical (a doubled "quietly"). Enumerator openers (First, Second, Third) are `bracket`. Anaphora runs are `bracket` only if three or more sentences in a row open identically and the run is not a deliberate device (Zara's "We don't got" is a device). The word "meaningful" gets a row only where it is filler praise (T7); "precisely" only where it is an intensifier (T6); "quietly" only where it is a drama adverb (T2).

5. **Headings and apparatus.** Chapter titles that are bold paragraphs rather than headings (the checker shows them as "chapter heading lost"): one `fix-direct` row each restoring the heading. Heading style: short noun phrases, no title-case colon headlines (T17). Note-section headings to the P16 convention. The "# ---" separators the Doc export shows are lost headings; name the chapter each one should carry.

6. **Chapter numbering placeholders.** Under P1, the bracketed numbers ([6A], [7], [11]) become plain numbers in headings: one row each, class `fix-direct`, but only in headings; pointers in the body are the continuity lane's.

## Work items already known

| Item | Where | Find | Action |
|---|---|---|---|
| Provenance & Editing Note at the head of the Doc | Front matter | `Provenance & Editing Note` | remove under R6; its per-chapter descriptions are logged nowhere (they are the retired ledger) |
| Third-person paragraph in the Preface | Preface | `Katherine von Duyke offers a taxonomy` | bracket (catalog copy; first person or out); it changes meaning, so not yours to cut |
| "no alibi in Being" edition placeholder | Chapter 2, note 1 | `edition/wording` | log; remove the bracket text only when the notes lane fills it |
| Stray closing quotation mark | Chapter 2, Paley note | `within it."` (lengthen) | fix-direct |
| Aside to the editor | Chapter 3, note 2 | `can be added if the historical claim needs support` | log; remove |
| `[verify translation/edition]` on Kant | Chapter 3, note 7 | `verify translation/edition` | log as open item; remove |
| Citation stand-ins | Chapter 4 | `Mississippi NAEP reading gains`; `see the research list in the back matter`; `[cite: Beechick]` | log; handoff notes |
| Placeholder for high-poverty apprenticeship examples | Chapter 4 | `[PLACEHOLDER: an example or two of high-poverty families` | already in the ledger; remove |
| "Endnote fixes still to make" and the working literature list | Chapter 4 | `Endnote fixes still to make`; `Working literature list` | log; remove; handoff notes for the two unmade fixes |
| "Replaces Chapter 5 in the Working Copy" | between 4 and 5 | `Replaces Chapter 5 in the Working Copy` | remove |
| Lezir DECIDE and GAP | Chapter 5 | `The Lezir thread`; `[GAP: the specific question` | log (P9); remove |
| Chapter 5 edition slots, "For 6", "Change notes.", "Two chapters drafted from your notes" | Chapter 5 end | `confirm pages`; `For 6`; `Change notes.`; `Two chapters drafted from your notes` | log; remove |
| Five GAP slots | Chapter 6A | `[GAP:` | already in the ledger; remove |
| "Questions for you" (five) | Chapter 6B | `Questions for you` | copy to the residue file; log; remove |
| Principles table placement notes | principles table | `Two rows are yours to confirm`; `Drafted from your field notes` | copy; log; remove |
| GAPs, NOTE — FIX items, "Questions for you", the 8/9 handoff | Chapter 7 | `[GAP: three or four of the actual responsibilities`; `Questions for you` | copy; log; remove |
| DECIDE, GAP, FIX items | Chapter 8 | `Whether to apply the Ch8/Ch9 split`; `[GAP: the counterfeit-tickets scene`; `Seed F`; `Seeds D and E` | copy; log; remove (the tickets GAP closes under P8, continuity's row) |
| Admin-fear slot, FIX, VERIFY, two DECIDEs, the 10 handoff | Chapter 9 | `[ADMIN FEAR SENTENCE SLOT`; `Big Picture Learning / Mastery Transcript Consortium URLs`; `Keep "Marcus, finally"` | copy; log; remove |
| WRITE, VERIFY, DECIDE items | Chapter 10 | `Opening vignette`; `The Bhaer and Tom quotes`; `The "Reading the Room" skeleton` | copy; log; remove |
| Editorial notes section and any PLACEHOLDER slots | Chapter 11 | `Editorial notes`; `[PLACEHOLDER:` | copy; log; remove |
| Provenance tags on every paragraph | assembled Chapter 6 | `[draft]`; `[notes]`; `[C]`; `[CO]` | remove tags, keep text (R6); the VIGNETTE slot and the DECIDE note go to the ledger |
| Kalima in two notes | principles table; Chapter 7 | `Kalima` | remove the notes (continuity confirms Zara) |
| Agreement slips | Chapters 1, 3, 4 | `and surfaces in the student`; `Even KIPP find they need`; `and is especially prevalent`; `taught my children violin with`; `Mills called this; turning`; `Think of Angie, Nancy, and Heidi, all three had something` | fix-direct |
| Citation punctuation | Chapter 3 and 4 | `(Hargadon, 2021.)`; `c.f.` | fix-direct |
| Chapter titles as bold paragraphs | 6B, 9, 11 | (the "# ---" separators in the snapshot) | fix-direct: restore headings |
| Enumerator openers | Chapter 6B, Three cautions | `First,` | bracket (T11) |

## Packet

`revision/packets/residue/<chapter-id>.md` in the spine's format, plus `revision/packets/residue/<chapter-id>-residue.md` holding the copied text of every removed note, question, and handoff. Fix rows carry the exact replacement text. The ledger's open-items table is appended in the same commit.

## Self-check

Every removal row has a logged counterpart (ledger row or residue file). No row changes a sentence's meaning; anything that would is a bracket. Every dash row shows the whole replacement sentence. No ban-hit row rewrites her sentence without a bracket. Find strings verified.

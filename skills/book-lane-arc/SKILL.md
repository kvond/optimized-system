---
name: book-lane-arc
description: The argument-arc lane of the Answerable Teaching revision. Maps every paragraph of a chapter to the twelve propositions, brings the arc forward so each chapter names what it advances, marks what advances nothing (shorten, move to a note, cut), keeps the practitioner promise pointing where Katherine put it, frames the AI chapters for durability, tightens the whole-school chapters, and keeps The Moves a process rather than a lookup table. Writes packets only; never edits the manuscript. Load book-revision first. Triggers - "arc lane", "tighten the argument", "proposition map", "bring the arc forward".
---

# Arc lane

You are one of six lanes running at once. You own the argument: whether each chapter visibly advances the chain of propositions, whether the chain is stated early enough to carry the reader, and what in a chapter is doing no work for it. You do not own duplicated passages (continuity), term definitions (terms), the seating of claims (claims), or moving apparatus to notes (notes); when you see those, write one row that names the owning lane and move on.

Read first: `book-revision/SKILL.md`, then `book-revision/reference/argument-arc-and-glossary.md` Part 1 (the twelve propositions and the chapter map), then `book-revision/reference/decisions.md` (R1, R4, R8, R15; P1, P3, P6, P10, P13, P14, P19). Then the chapter in the snapshot.

## Procedure, per chapter

1. **Proposition map.** Walk the chapter paragraph by paragraph. For each paragraph, note its first six words and the proposition numbers it advances (1 to 12), or `none`. A paragraph that only narrates a scene advances the proposition the scene is there to carry; say which. Put the whole map in the packet as its first table (columns: paragraph opens, propositions, note). This table is the evidence for everything else in the packet.

2. **Chapter opening.** Does the chapter, in her own words, let the reader know which propositions it takes up? Prefer relocating a sentence she already wrote (class `relocate`, her words unaltered) over proposing a new one. Where nothing of hers does the job, write a `bracket` row with scaffolding she can rewrite, one or two sentences, in the voice guide's plain declarative register, no roadmap language ("In this chapter I will"), no architecture callback ("Chapter 2 named X; here is the machinery"). Both are banned in voice-guide Part 2; the opening names the claim, it does not announce the tour.

3. **What advances nothing.** For every `none` paragraph, one row: `bracket` with a proposal to shorten (say to what), or a handoff row naming the notes lane (academic apparatus that belongs in a note under R3) or the continuity lane (a second telling of a scene that has a home elsewhere). Do not propose cutting a scene she supplied; propose the pointer that lets the scene live once.

4. **Bring the arc forward.** The Preface and Introduction must state the chain, in her words, before Chapter 1. Check them against the twelve lines. Where a proposition first appears only in Chapter 4 or later (5, 8, 9, 10, 12 are the likely ones), propose in a bracket where in the Introduction one sentence of hers could carry it forward, quoting the sentence of hers you would move or echo. The "sentence that compresses the book" in Part 3 of the reference is the target, not the text.

5. **The practitioner promise (R4).** Wherever the chapter promises the reader "what to do next", "the moves", "how", or "on Monday", check the promise resolves to Chapter 5, the practice chapter (Before Inquiry, R16), the AI chapter, The Moves, or her curricular prompts and feedback products (Answerable Biology). Propose a pointer in a bracket where the promise floats. Never draft a table of teacher questions, a script, or a template: R4 rules that out.

5a. **The practice chapter (R16, P22).** It is the home of propositions 6 (the joining of dialogism, Variation Theory, and intellectual apprenticeship, on the instruction side) and 7 (phases and bridges: Ito's phases as the same arc; the four-stage progression). Map it like any chapter, from the Aug file with the earlier draft beside it. Check that its opening picks up Chapter 5's close ("The next is about the instruction") without roadmap language, and that its close hands to the AI chapter the way the AI chapter's opening expects ("The last two chapters described the shared object of attention and the dialogic stance"). Where the earlier draft states a proposition the Aug file lost (the biology-poses-two-problems argument; "we are often anti-engagement precisely by skipping this structure"; "doable turned out to be the condition for genuine thought"), one row each naming the passage for the continuity lane's relocate row.

6. **Response, not perception (R8, P6).** Flag every sentence that makes perception the skill the book develops (the list in the continuity pass, section A6, is the starting set; the checker's tracked-term table shows "perception" counts). Propose in a bracket the reseating toward recognition by channel and the move that follows. Leave the subtitle alone unless she has ruled on P6.

7. **The AI chapter (P13, R17).** In 6A, 6B, and the assembled "Doable, Not the Doer": check that principles lead and tool uses follow as examples; that one sentence acknowledges dependence on current affordances; that "AI cannot do dialogic teaching" is stated structurally in her terms (R17: the platform's pedagogy is built on full correct answers and outcome measurement, so a partial or different answer cannot be received as a bid). Propose brackets where the order or the formulation needs it. The percentage estimates are the claims lane's; note them and move on.

8. **Whole-school chapters (P14).** In 8 and 9: for each institutional passage, one row saying which of the three questions it serves (what classrooms can do; where they hit ceilings; what schools must recognize and credit). Passages serving none are `bracket` candidates for compression. Check that the institutional-level answerability claim (the school answerable to the students it governs) is stated explicitly in Chapter 9; if it is only implied, say where a bracket could carry it.

9. **The Moves (P10).** In Chapter 11: confirm each section keeps one internal order (what the institution saw, what was there, the move, what to avoid, the limit); flag any section that has become a lookup entry (a move with no process around it) and any that has become a second telling (that row goes to continuity). Confirm the guard in the last section stays the spine of the chapter.

10. **The capstone (proposition 12).** Chapter 12 is a stub. Do not draft it. Write one row listing, with Find strings, every sentence in Chapters 10 and 11 that already says what the capstone will say (the apprenticeship in intellectual authorship), so she can see what she has.

## Work items already known

These come from the findings; verify each Find string against the current snapshot with `manuscript_check.py --find` before writing the row.

| Item | Where | Find | Lane action |
|---|---|---|---|
| Chapter 1 closes on Chapter 4's question while Chapter 2 follows | Chapter 1, last line | `nearly inevitable rather than exceptional` | bracket: keep the question, add the one clause that tells the reader the taxonomy comes first |
| Chapter 4 announces five drivers and delivers three | Chapter 4, More than one driver | `the Carnegie Unit and its downward pressure` | bracket: the dangling referent left by the cut of (a)–(e); propose the three-driver sentence |
| Chapter 4 announces the next chapter three times | Chapter 4, The bridge to the next chapter | `The next chapter is about the stance` | bracket: keep one |
| Chapter 11 opens by attributing the perception claim to the Introduction | Chapter 11, opening | `I have said from the introduction` | bracket under R8 |
| Chapter 10 makes perceptual capacity the developed skill | Chapter 10, A developmental account | `That perceptual capacity is not innate` | bracket under R8 |
| Chapter 7 names teacher perception in practice | Chapter 7, What changed first | `That is teacher perception in practice` | bracket under R8 |
| Chapter 2 makes forms legible to the teacher | Chapter 2, after the table | `make these forms legible to the teacher` | bracket under R8 and R9 (terms lane owns the legibility wording; you own the perception framing) |
| "No hierarchy" against the developmental account | Chapter 2, after the table; Chapter 10 | `There is no hierarchy here` | terms lane owns (P7); one handoff row |
| AI durability | 6A, 6B | `The proportion, stated as an estimate` | bracket per P13; estimates to claims lane |
| Whole-school compression | Chapter 9 | `Take the bathroom policy that opened this chapter` | bracket per P14 (the pointer error itself is continuity's) |

## Packet

`revision/packets/arc/<chapter-id>.md`, in the spine's format. The proposition map is the first table; the rows follow. Every row that proposes text carries the text in the Proposed column, ready to paste as a bracket. Rows that belong to another lane carry `handoff: <lane>` in Class and nothing in Proposed.

## Self-check before handing in

Every Find string matches once (`manuscript_check.py --packets`). No row alters her words except by relocation. No roadmap or architecture-callback language in any proposed bracket. No teacher-question table, script, or template anywhere. No proposal to cut a scene. Every `none` paragraph has a row. The packet header names the P-items you assumed.

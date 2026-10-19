<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

## 2. Slide order

Day 1 and Day 2 keep the order in which you built them. Two parts of the deck have
a fixed order: the block for each critical aspect, and the end of the deck.

### 2.0 The front of the deck (added 2026-08-17)

- **Slide 1** is the teacher reference slide.
- **Slide 2** is **"Additional Resources — Teacher Prep"**: three sections — BUY
  AHEAD, PREPARE, PUT OUT FOR STUDENTS — built from the deck's own activities.
  Kicker `TEACHER REFERENCE` 11pt bold `666666`, heading 16pt bold `111111`,
  section labels 10pt bold `028090`, items 12pt with space after each. If a lab
  has a materials list on its activity slide, the complete list is repeated here —
  slide 2 alone must be sufficient to prep the cycle. Purchasable items carry live
  product links (label + small gray URL).
- **The Bellringer slide** carries two labeled resource lines, 12pt, bold labels,
  live links: `FOR READERS:` — the companion section from the CK-12 Biology
  FlexBook 2.0 (deep link to the section, not the book), and `FOR TESTERS:` — the
  matching Khan Academy lesson set (deep link to the unit). Both also appear on
  the links slide per §8.

### 2.0a The teacher note slide (added 2026-08-29)

**One slide. Not speaker notes.** Speaker notes are invisible to the person this
is written for, and scattered notes cannot be removed as a unit. One slide can be
deleted in a single action and the deck still runs. It sits in the front
teacher-facing block, immediately after the Teacher Prep slide.

It carries a marker string in its title, so `deck_lint.py` can require it and a
teacher can find every instance. **Its absence is a hard failure. The deck does
not ship without it.**

**Seven declarations. A note carrying six is missing one.**

1. The **critical aspect** this cycle teaches, in plain words.
2. What is held **invariant** across the examples, and the sentence saying the
   examples differ in one dimension on purpose.
3. **What breaks if you substitute an example.**
4. **Position in the sequence** — what this cycle assumes has already been
   discerned, and what later cycle depends on it.
5. **The slide-type map** — which slide types appear here, and which conditional
   ones were deliberately left out, and why.
6. **Which simultaneity this cycle works on** — synchronic (two aspects in the
   same case in the same moment, which is fusion in the strict sense) or
   diachronic (things met at different times brought together, which is what the
   Concept Bank does), or both.
7. **The visibility rung** — what this cycle asks students to expose, and to
   whom, written as a decision: *"visibility: written and private, building toward
   unattributed read-aloud."* The rungs are: 1 written and seen only by the
   teacher; 2 written and shown to one assigned partner; 3 the teacher reads a
   wrong but productive answer aloud, unattributed, and uses it; 4 a student owns
   an answer aloud by private invitation; 5 public simultaneous commitment, the
   vote.

Both simultaneity terms appear here with a one-line gloss because this slide is
teacher-facing. **Neither appears on any slide a student reads.** The standing rule
against coding vocabulary to students holds.

[Why the rung is declared and not merely chosen. A room at rung 1 or 2 shows quiet
students writing, which reads as low engagement against every walkthrough rubric in
use, and is the correct instruction for that room at that time. Declared, the
absence becomes a stated design decision, and an observer can argue with a
decision. She cannot argue with an absence, because an absence looks like a
failure. One line, and it is what makes the ladder survivable in a building.]

[The marker string: the recommendation, when Katherine sets it, is a fixed kicker
`TEACHER NOTE` on the model of `CONCEPT BANK` in §3b, registered in the §7 table
and added to the §7.1 diagnostic-count exclusion list in both scripts in one pass —
the slide asks the student nothing and must not be counted. Not built until she
says the token.]

### 2.0b The visibility-ladder slide (added 2026-08-29)

**One slide, and it sits immediately after the teacher note.** The note declares
this cycle's rung. This slide says what the rungs are. Read the other way round it
is a glossary standing in front of a term nobody has met yet.

[Katherine asked for slide 2, and it is one line to move — move it if you want it
there. Two things argue for the position after the note. §2.0 fixes slide 2 as
Teacher Prep, which is the slide you open the night before to buy things, and a
theory slide in front of it delays the only actionable slide in the front block.
And Teacher Prep already points at "slide 3" for the rung: put the ladder at 2 and
that reference is wrong the moment it is inserted. Placed after the note, the
declaration is read first and this slide answers it.]

**It is teacher-facing and it is never projected.** Its kicker carries the string
`do not project`, which is in `NON_DIAGNOSTIC` in `deck_lint.py` and in
`NON_DIAGNOSTIC_MARKERS` in the grader — §7.1. Both tuples are tested *before* the
four diagnostic classifiers, so the slide cannot inflate a diagnostic count.
Confirm that on every build: the diagnostic count must not move when this slide
goes in.

**What it carries.** All five rungs, each with what you actually do and the
observable thing that opens the next one. Rung 3 gets the longest block on the
slide, because it is the rung that does the work and the one no PD teaches. Then
descent — drop a rung and do not announce that you have — and the fact that group
work is a visibility *reducer* and not a rung at all, which is why the What if is
written individually. Last, the per-move ceilings, so you know where cold call is
safe.

**The marker-string precaution, and it is not theoretical.** The slide has to name
the moves, and two of those names are unique slide-type markers (§7). `deck_lint.py`,
`extract_and_grade.py` and the teacher prompts match those strings anywhere in the
deck, case-insensitively. Writing "Pattern Break" plainly makes this deck count two
Pattern Breaks where it has one. The §7.1 exclusion tuple saves the linter's own
count and does **not** save the raw string count that §11 check 3 runs. So every
move name on this slide is written in a form with no marker in it —
`Pattern-Break`, `Build-a-Rule`, `What-if`, `3-Tier Question`, and
`Critical Aspect question` with no colon after "aspect". A hyphen reads identically
to a person and is invisible to the matchers. Count the markers before and after
you add the slide. Every count must be unchanged.

**Building it.** `scripts/deck_apply_changes.py` holds the copy in `VL_BLOCKS` and
builds it in `build_visibility_ladder()`. Import that; do not retype the wording
into a deck build script. Two copies of the same paragraph that have to stay in
sync is the failure §7.1a is about, one level down. The insert is idempotent and
will not double-insert.

**Format.** Arial, 11pt body, one column at x 548640, y 1554480, w 8046720,
h 5120640 — both y and h are §13.3 tokens. Bold teal `028090` labels running into
body black `111111` in the same paragraph, 3pt after each block. 11pt and not 12:
the copy is 27 lines of Arial 11 in that box, which is 377.4pt of the 396.0pt the
box holds. At 12pt it is 31 lines and runs off the bottom of the slide. Measure it
against the box. Do not guess, and do not trust the crude estimator in
`deck_apply_changes.py` — it reads two lines high and is there to catch an edit,
not to certify a fit.

**Renumbering.** Inserting a slide in the front block moves every slide below it by
one, and the decks in this arc carry slide numbers in prose: the teacher note points
at its own coordination structure, the image credits point at the slides that need
images, and a speaker note points at the What if. `build_12b.py` renumbers all of
them in the same pass. `deck_apply_changes.py` does not — it emits a warning
instead, because rewriting a teacher's prose mechanically is how you destroy a
sentence nobody read. Fix them by hand, then check them against the render.

**Its absence is an ADVISORY, never a hard failure.** `deck_lint.py` reports
`A-VIS-LADDER`. The slide was invented on 2026-08-29 and no shipped deck in the arc
carries one, so a hard rule here would fail every deck on its first run — which is
the whole reason the linter has two tiers.

[One thing that is Katherine's call and is not settled here: whether a teacher who
already knows the ladder should get the slide at all. It is deletable in one action
like the note, and the speaker note says so. The argument for shipping it to
everyone is the same as the argument for the note — the person who needs it is the
person who does not know she needs it.]

---

### 2.1 The block for each critical aspect

1. Critical Aspect question
2. Stock-and-flow model (conditional)
3. Contrast Set
4. Explanation (optional). Put it after the Contrast Set. Never put it before.
5. Build a Rule
6. Pattern Break
7. Continuity question (conditional)
8. 3-Tier Question
9. **Response slide** for that aspect. See section 3.
10. Activity for that aspect

[Moves 8 and 9 — the compensatory pair and the conflict case — are not in this
block. They coordinate two aspects, so they cannot sit inside the block for one of
them. They belong at the end of the deck, immediately above the What if that reads
them, in the §2.2 order.]

### 2.2 The end of the deck

1. Compensatory pair, or conflict case (conditional — moves 8 and 9, §1). Only
   where the content already holds one. It may run as group work.
2. What if. This is a response slide. It has boxes and a prompt. **Individual and
   written, with no exception.** Moves 8 and 9 may be group work; a group product
   says nothing about who coordinated, so a group What if is an empty diagnosis.
   Where the deck carries a coordination structure above it, this slide reads it —
   the structure is the occasion and the What if is the evidence. The slide is
   required in every Biology deck either way (§3).
3. Optional challenge. It is harder and not required. It needs a writing box.
4. Relates to me. The student writes the relevance. It needs a writing box.
5. **Concept Bank.** One slide, or two where the cycle carries more than fourteen
   terms. The printed terms of the cycle, with an empty writing box for each
   definition. The student fills it across Day 1 and Day 2 and reads it on revision
   day before rewriting. See section 3b.
6. **Day 3 divider. This is the rewrite slide.**
7. Closing checklist — **only when no earlier slide already carries the
   Think → Write → Submit information.** If the Day 3 divider (or any other slide)
   already states it, do not ship a second slide repeating it; delete the
   duplicate, never the divider. (Rule added 2026-08-17.)
8. Activity and resource links
9. Image credits

**Two constraints on the What if question itself.** Name what changes and what is
held, or the student does not know how far to go or at what scale — an
unconstrained counterfactual is the polar bear question in another costume. And in
Biology, hold the mechanism fixed and vary the condition. "What if snakes had kept
their legs?" hands a student reaching for purpose an easy answer; "what if the
ancestral population had lived in open ground rather than in burrows" makes the
same coordination demand with no invitation to teleology.

### 2.3 The rule for Day 3

Day 3 is for revisions only. No slide that asks the student a question can come
after the Day 3 divider. Only three slide types can follow it: the closing
checklist, the links slide, and the image credits.

The Concept Bank is the last slide above the divider. It belongs above the divider
because the student fills it on Day 1 and Day 2, and it belongs immediately above
because the student reads it on revision day as the last thing before the rewrite.
Do not move it below the divider to sit nearer the rewrite slide. A cell the
student has not filled is a question the student still owes, and section 2.3
forbids a question below the divider.

This rule covers more than the What if slide. Continuity questions, "How does this
connect to you?", optional challenges, and response slides were all below the
rewrite slide in real decks. Move each one above the divider. Keep the order they
were in.

### 2.4 Slide types removed on 2026-08-12

Do not build these. Do not restore them.

- **Then and Now.** The self-rating slide.
- **Turn your answer into a draft.** The revision prompt moved into the speaker
  notes, so this slide is no longer necessary.
- **Slide type list for the teacher.** Section 7 gives the rule that replaced it.
- **Slide numbers in the corner.** Removed on 2026-08-06. The numbers went out of
  sequence each time somebody moved a slide, and a number alone tells a student
  nothing.

### 2.5 Never delete a day divider

A Day 3 divider can have the title "Day 3 of 3 — turn your best answer into a
draft". That slide is a divider. It is not the removed draft slide. If a rule
deletes removed slides, the rule must skip every slide that matches `Day N of N`.
This error already destroyed the rewrite slide in one deck.

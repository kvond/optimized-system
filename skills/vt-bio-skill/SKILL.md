---
name: vt-bio-skill
description: Finish an Answerable VT cycle deck to the shipping standard (Biology; §16 also covers Forensics and A&P until their forks exist). Covers the 5 core questions, the four conditional slide types, the teacher note, response slides and revision prompt, What if, Concept Bank, images, icons, marker strings, links slide, /copy distribution, restoring original lessons into VT decks without losing pictures or material (/restore-vt-slides), the enhance pass (/vt-gemini-enhance), embedded codes for new student textboxes ([[BANK:CYCLE:TERM]]), adding deck and activity links to the Master Agenda, and the checks before delivery. Use it to build, repair, merge, enhance, code or complete a cycle deck, or to ask whether a deck is ready. Triggers - "VT deck", "finish the deck", "restore VT slides", "merge original and VT", "gemini enhance", "embed codes", "add agenda links", "is this deck ready".
---

# vt-bio-skill — VT Deck Finishing, Biology

Run this skill after the text of a cycle is final. Run it before you give the
deck to Katherine. It covers slide order, response slides, images, icons,
appendix slides, and link tests. It sits above `deck_lint.py`. `deck_lint.py`
stays the last gate.

Katherine established this skill on 2026-08-06, on Cycle 2.

Revised 2026-08-12. The revision changed the reference build, removed three slide
types, removed the slide numbers in the corner, moved the revision prompt into the
speaker notes, and replaced the batch pipeline with three prompts.

Revised 2026-08-17, by Katherine's direction. This revision changed the type scale
(student body text is now 18pt, bulleted, with space after each item — see §13.4),
permitted Claude to draft NGSS codes (see §5), retired standalone activity guides
(see §4b), added the Teacher Prep slide as standard slide 2 (see §2.0), added the
Bellringer FOR READERS / FOR TESTERS lines (see §2.0), made the closing checklist
conditional on non-duplication (see §2.2), and corrected the stale script IDs in
§11. All 26 decks were brought to this standard on 2026-08-17.

Revised 2026-08-18, by Katherine's direction. This revision added the **Concept
Bank slide** as a required slide immediately before the Day 3 divider (see §3b and
§2.2), and **scoped this file to Biology**, because Katherine now labels the
deck-finishing skills by course (see §15). The file was renamed
`vt-bio-skill` on Katherine's instruction. She asked for `VT_Bio_skill`; skill
`name` values take lowercase letters, digits and hyphens only, and the save
normalises anything else, so the file now carries the normalised form directly
rather than relying on the save to fix it. All 26 Biology decks need the Concept Bank retrofit;
the reference build takes it first (see §14.2). It added **§9.1**, which records
that a locally built deck cannot be uploaded through Composio. It recorded the
measured finding that the exclusion list matches nothing in Cycle 02 (see §7.1). The revision also wrote down the
**diagnostic-count exclusion list** and the rule that it is edited in two files in
one pass, and recorded the Continuation / Continuity name mismatch as an open
defect (see §7.1). It also permitted a
second Concept Bank slide where a cycle carries more than fourteen terms (see §3b).
It recorded that a
second `.pptx` in a cycle folder is an EXTEND deck (§0), and that the agenda
carrying fewer cycles than the product is deliberate (§9.3a). It added **§3c**,
which documents the marker fault the
Concept Bank build surfaced — an ellipsis broke the linter while the grader kept
working — and makes reading the `markers present:` line a standing check.

Revised 2026-08-29, by Katherine's direction. The conditional slide types are now
**four**, not two — the compensatory pair and the conflict case join the Continuity
question and the Stock-and-flow model as moves 8 and 9 (see §1). This revision
added **§2.0a, the teacher note slide**, one slide rather than speaker notes,
carrying seven declarations, its absence a hard failure. It made the **What if
individual and written** without exception and gave it its two constraints (§2.2).
It made the Concept Bank ask the student **how two terms connect**, because
co-presence is the precondition and not the achievement (§3b). It added the
delivery checks that follow, and marked which of them are advisory rather than
hard (§11). The word forbidden by §1 was removed from §1 itself, which had been
the last place in this file it appeared.

Revised 2026-09-03, by Katherine's direction. §0 and §11 now name the repository as the
only place a script is fetched from, and the Drive IDs are retired. Cause: a Cycle 01
check that morning ran the stale Drive `deck_lint.py` and under-reported by nine hard
failures. Also recorded in §7.1a: the exclusion-list sync rule is now a repository edit,
not a four-copy edit.

Revised 2026-10-15, by Katherine's direction (Slack #vt-decks). Added **§16**, which brings
the restore, enhance, code and agenda-link passes into this skill, so a deck comes out
finished and doesn't need repairing later. §16 is course-neutral. Until the Forensics and
A&P forks exist (§15), it is the rule for those courses' decks too.

This skill stands for every cycle until Katherine changes it.

Reference build: **`Cycle 02 — Ecosystems & Feeding Relationships (VT deck)`**,
33 slides. If this file and the reference build disagree, the reference build wins.

---

## 0. Prerequisites

- Work on a real `.pptx` file. Do not work on a native Google Slides file. A
  native Slides file exports as a PDF, so there are no bytes to edit.
- **Find the live deck by its `.pptx` twin** (rule added 2026-08-18). Drive holds
  65 live Google Slides files with `VT` in the name across about twenty cycles —
  two to four near-duplicates per cycle, some with identical names in different
  folders. The name alone does not tell you which one ships. The test that does:
  **the live deck is the Slides file that has a `.pptx` of the same name in the
  same folder.** `Cycle 05 — Photosynthesis (VT deck)` beside
  `Cycle 05 — Photosynthesis.pptx` is live; the other file of that same name,
  in a folder with no `.pptx`, is not. That test yields 24 decks in 19 folders,
  and it is also where you get the bytes to work on. Do not touch the other 41.
  - Match the *name*, not just the folder, or a folder holding two decks pairs
    wrongly.
  - **A second `.pptx` in a cycle folder is usually an EXTEND deck, not an
    orphan** (corrected 2026-08-18). §2 of the Teacher Manual says every cycle
    ships a **CORE** deck and that cycles **07, 12, 15 and 16** add an **EXTEND**
    deck for a faster class. So `Cycle 12 — The Process of Meiosis (VT deck,
    rebuilt).pptx` is Cycle 12's EXTEND deck and is a build target like any other.
    It currently has no Slides counterpart in the live folder, so it needs one
    made. Never write off a second deck as a duplicate without checking the
    CORE/EXTEND list.
  - Two cycles have no `.pptx` anywhere: **Cycle 01 (Lab Safety)**, which also has
    several competing variants and needs Katherine's eye before anything is built,
    and **`Cycle 13 — Genetics Continued _ Punnett (VT deck)`**. Export those two
    from Slides so every cycle ends with a `.pptx` source of truth.
- **Build a new deck from the reference build. Do not restyle the old deck.**
  See section 14. The old deck is a content source only.
- Get the scripts from the repository at run time: `kvond/answerable-skills`, folder
  `scripts/`, read on every machine through the `~/.claude/skills` symlink. That is the
  only copy. Do not fetch a script from Drive: the two Drive folders named
  `scripts (Do NOT Delete)` hold stale copies (their `deck_lint.py` is the 7 KB
  pre-2026-08-29 version; the repository holds the 57 KB two-tier rewrite), and a run
  that picked one up on 2026-09-03 reported one hard failure where the current linter
  reports ten. Do not write a script again from memory. (Decided 2026-08-29; the
  Drive IDs that this file carried before that date are stale and are being removed.)
- Check the deck before and after every pass. Compare the slide count, the slide
  order, the slide size, and the text of each shape. You must be able to name the
  reason for each difference.
- Match the design tokens in section 13. Do not invent a color, a size, or a
  position. Every deck must look like the reference build.

---

## 1. Words to use

The term is **5 core questions**. A slide has a **slide type**. Use no other
vocabulary for either — not in a deck, not in the manual, not in sales copy, not
in this file.

### The 5 core questions

Use this order, one time for each critical aspect.

1. **Critical Aspect question.** The question that opens the aspect.
2. **Contrast Set.** Case A against Case B. All conditions stay the same except one.
3. **Build a Rule.** The student completes a sentence that states a general rule.
4. **Pattern Break.** The case that strains the rule the student just made.
5. **3-Tier Question.** Getting Started, Working On It, and Mastery. Add a word
   bank. Offer the word bank as "use any, modify any, or use none".

### The 4 conditional slide types

Use these four slide types only when the content needs them. They are moves 6
through 9; the 5 core questions are moves 1 through 5.

- **6. Continuity question.** The question that has no answer to look up.
- **7. Stock-and-flow model.** Use it only when the aspect turns on a quantity
  that fills and drains.
- **8. Compensatory pair.** Two aspects vary inversely while the outcome is held
  invariant, so neither aspect alone predicts it. *Sea turtle and elephant: a
  hundred eggs with almost no survival, one calf with high survival, both
  populations steady.*
- **9. Conflict case.** One case in which one aspect points one way and a second
  points the other, so the case cannot be resolved from either alone. *Legless
  snakes.*

Cycle 02 has the Continuity question and the Stock-and-flow model on Critical
Aspect 1 and neither type on Critical Aspect 2. That is correct. Do not force a
conditional slide type onto an aspect that does not need it.

**Moves 7, 8 and 9 are the coordination structures, and they are not the same kind
of object.** Stock-and-flow is a representation and can be *added* to any cycle
whose content accumulates. A compensatory pair is a case set and a conflict case is
a single case, and both have to be *found* in the content. Neither can be
manufactured, and a manufactured one teaches a relationship that is not there.
Diagnosing whether a cycle can carry one is `vt-fusion-retrofit`, not this file.

**Every coordination structure is read by a What if.** The What if does not create
coordination; it tests whether coordination happened, which makes it evidence
rather than an occasion. Moves 8 and 9 may run as group work; the What if may not.
In Biology this costs nothing to enforce, because §3 already puts a What if in
every deck — a cycle that gains a coordination structure gains the occasion for a
slide it already had. See §2.2 and §3.

[Left open, and not resolved here: whether the What if is a tenth move or a
required companion to whichever coordination structure a cycle carries. This file
treats it as a companion, which is why it sits in the end-of-deck order in §2.2
rather than in the list above.]

---

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

---

## 3. Response slides

A response slide has a first-answer box and a revised-answer box. A response slide
always has a prompt in the speaker notes. There is no exception.

Each deck has one response slide for each critical aspect, and one more for the
What if slide.

**Title.** Use `Your answer — Critical Aspect N · <aspect name>`. For the What if
slide, use `What if? · <the aspect it extends>`.

**Instruction line.** Use these words:

```
Write your first answer now. On revision day, open this slide's Notes, run the prompt, and write your revised answer below — leave both showing. Seeing your thinking change is the point.
```

Use "On revision day". Do not use "On Day 3". A cycle can run for 2 or 4 class
meetings, and "On revision day" stays correct.

**Box labels.** Use `Your first answer` and `Your revised answer`. Use the same
two labels in every deck. Do not add text in parentheses. The instruction line
already gives the time.

**The writing box.** Fill color `#F2F6F9`. Border color `#CCCCCC`. Copy the box
from a slide that already has one. Do not build a new box. A new box lets the
style drift. One build made boxes at `#EFF3F6` and `#BFCBD4` because the operator
built them instead of copying them.

Every slide that asks the student to think needs a box to write in. A question
with no box is a defect. The optional challenge and the Relates to me slide both
shipped with no box before this rule existed.

**Speaker notes.** Use this text. Replace only the question in brackets.

```
REVISION PROMPT — copy everything between the lines into your AI, and paste your first answer where it says [YOUR FIRST ANSWER]. The AI will NOT give you the answer — it helps you see your own thinking so you improve it yourself.
-----
I am a high school student. Below is a science question and my first answer. Do NOT rewrite my answer and do NOT give me the answer. Instead:
1. Tell me one thing I got right, and quote my own words back to me.
2. Ask me two questions that make me look again at one idea I might have wrong or left out.
3. Name one distinction or example worth thinking about.
Keep it short and in plain language, then stop so I can write my own revised answer.

QUESTION: [this slide's question, word for word]
[YOUR FIRST ANSWER]:
-----
Now write your revised answer in "Your revised answer" on the slide — in your own words.

TEACHER: the finished deck (first + revised answers) is the single artifact the two teacher prompts read. Completion = both boxes filled on every response slide.
```

For a critical-aspect response slide, use the Mastery question of that aspect, word
for word. For the What if slide, use the What if question.

Keep the prompt in the speaker notes only. Never print it on the slide.

---

## 3b. The Concept Bank slide (added 2026-08-18)

Katherine specified this slide on 2026-08-18. It is required. Every deck has
exactly one.

**Where it goes.** Immediately before the Day 3 divider. It is the last slide the
student sees before the rewrite slide, and it is the slide the student reads on
revision day before rewriting anything.

**What it asks, decided by Katherine 2026-08-30.** Fill in the blanks. Nothing
more. "We're not asking students to put those two ideas together for any of that
vocabulary. They're not ready for that at that step." The bank supplies
co-presence; it does not ask the student to relate two terms, and a builder who
adds a relating prompt to it is working against the sequence rather than for it.

**What follows it, same decision.** The conflict case is the next slide. The
relating the bank deliberately does not ask for is what that slide asks for, on
content rather than on vocabulary, once the terms are in front of the student.

[Two things this changes and one it strains. It supersedes the sentence above
that the Concept Bank is the last slide above the divider - the conflict case now
sits between them. It retires `A-BANK-NO-RELATE` in `deck_lint.py`, which is
recorded there. And it strains
`coordination_judgment_and_the_package.md` section 7, which says in as many words
that a page which only lists "has left the relating to chance". That document and
this section now say different things about the same slide; the version that
survives should be written down, because the next person to read section 7 as a
spec will put the relating prompt back.]

**What it is.** A grid of the terms the cycle depends on. The terms are printed on
the slide. Each definition cell beside a term is an empty writing box. The student
fills the cells across Day 1 and Day 2, as each term is met.

Printing the terms is the job of the slide. A student asked to list the terms of a
cycle misses the terms they did not notice. A student given the terms can see which
cells are still empty, and an empty cell is itself the instruction to go back.

**The slide must also ask the student to state how two of the terms connect
(added 2026-08-29).** This is a requirement, not an enhancement. The Concept Bank
is diachronic simultaneity as a built artifact, and *co-presence is the
precondition, not the achievement*: a page that only lists the terms has achieved
co-presence and left the relating to chance. A page that asks for a relation does
the work. Same absence of testing pressure either way — the whole difference is in
the demand.

[This is also why review sheets and cumulative tests do not do this job. They
attempt diachronic simultaneity and reach only co-presence, because filling a blank
exercises retrieval, and retrieval leaves a sequence a sequence. A Concept Bank
that only lists is a review sheet with a teal kicker.]

The relating demand rides in the instruction line below, so the grid is untouched
and §13.3's two columns and seven rows stand.

[Open, and it needs Katherine, because two standing rules collide here. §3 says
every slide that asks the student to think needs a box to write in, and a question
with no box is a defect. §13.3 fixes this slide's geometry, and a full grid is
already the densest slide in the deck. So the relating sentence has no box of its
own. Two ways out. **Recommended:** the student writes the relating sentence at the
top of the Day 3 rewrite, where a box already exists and where she is already
reading this slide — the Concept Bank asks, the rewrite slide holds the answer, and
nothing moves below the divider that was not already there. **The alternative:**
one short writing box under the grid, which costs the two source links their
position and makes the densest slide denser. Built as recommended until she says
otherwise.]

**Where the terms come from.** Take every term in the 3-Tier word banks of every
critical aspect in the deck. Add any term that a Contrast Set, a Build a Rule
sentence, or a Pattern Break requires the student to hold. Remove duplicates. Take
no term from outside the deck.

**Order.** Order of first appearance in the deck. Fill column 1 from the top, then
column 2 from the top. Reading order down the grid then matches the order in which
the student met the terms, so a student filling the grid on Day 1 works the top of
column 1 and can see the distance covered.

**Size.** Two columns, seven rows, fourteen terms per slide. **A deck may carry one
or two Concept Bank slides** (rule changed by Katherine, 2026-08-18; the first
version required her approval for a second slide).

- **Fourteen terms or fewer: one slide.** This is the normal case. Cycle 02 came to
  exactly fourteen.
- **More than fourteen: two slides, split by critical aspect.** Slide one carries
  Critical Aspect 1, slide two carries Critical Aspect 2. Both sit together,
  immediately before the Day 3 divider, in aspect order. Title the second one
  `Define these in your own words (continued)`.
- **Never three.** Twenty-eight terms is the hard ceiling for a 3-class cycle. A
  deck that produces more than twenty-eight is carrying vocabulary its critical
  aspects never use, and the content needs the cut, not the slide.

Do not shrink the type to avoid a second slide, and do not run the grid past seven
rows. The geometry in §13.3 is fixed.

[Note on the split: where a deck needs two slides, group by aspect rather than
continuing the first-appearance order across both. The first-appearance rule in the
next paragraph orders the terms *within* a slide. Across two slides, aspect order
wins, because the point of the second slide is that the student can find the
Critical Aspect 2 terms without reading past the Critical Aspect 1 ones.]

**Header.** Kicker `CONCEPT BANK`, 11pt bold `028090`. Heading
`Define these in your own words`.

**Instruction line.** Use these words, 12pt plain `111111`:

```
Fill each box as you meet the term on Day 1 and Day 2. Use your own words, not a copied definition. On revision day, read this slide before you rewrite anything, then start your rewrite with one sentence saying how two of these terms connect.
```

(The last clause was added 2026-08-29 and is required. A Concept Bank whose
instruction line stops at "read this slide" only lists.)

**The definition cell.** Fill `F2F6F9`, border `CCCCCC` — the same writing box as
section 3. Copy the box from a slide that already has one. Do not build a new box.
Ship every cell empty. Do not put a placeholder, a sentence starter, or a light gray
example inside a cell.

**How to build the term box.** Clone the small label text box from a response
slide (the one that reads `Your first answer`). After cloning, remove its
`<a:spAutoFit/>` and set `wrap="square"`, set the paragraph alignment to left, and
set the vertical anchor to middle. A cloned label arrives with `spAutoFit` and
`wrap="none"`, and in that state the renderer sizes the box to the text and hangs
it from the right, so the terms come out right-aligned in a ragged column even
though the XML says `algn="l"`.

**The term.** 12pt bold `028090`, in its own box to the left of its cell. The
Concept Bank is a dense slide role, so it sits below the 18pt of section 13.4, in
the same way the CASE A and CASE B labels do.

**The two source links.** Under the grid, two lines, 11pt, bold labels, live
hyperlinks. Use the same two labels the Bellringer uses in section 2.0:

- `FOR READERS:` — the same CK-12 Biology FlexBook 2.0 section the Bellringer
  names, deep-linked to the section, not to the book.
- `FOR TESTERS:` — the same Khan Academy lesson set the Bellringer names,
  deep-linked to the unit.

**Build the links block by cloning the Bellringer's own two paragraphs**, not by
typing the labels and re-adding the hyperlinks. Two things are carried in that XML
and are lost if you rebuild it. The label is 12pt bold `028090` and the linked text
is 12pt `111111` underlined — the link text is *not* teal, and it is not the theme
hyperlink blue. And each `<a:hlinkClick>` carries an
`<ahyp:hlinkClr val="tx"/>` extension, which is the instruction to draw the link in
the run's own colour rather than the theme hyperlink colour. Drop that extension
and the link renders blue, against a Bellringer whose identical link renders black.

A cloned paragraph carries the *source slide's* relationship id, which does not
exist on the new slide, so the hyperlink is dead on arrival. Rebind it: keep the
cloned `hlinkClick`'s `extLst`, set the address through the API so a valid
relationship is created, then put the `extLst` back on the new `hlinkClick`.

They are the same two links in a second place, on purpose. The student checks their
own wording against a published source at the moment they are about to rewrite,
rather than against what they remember the teacher saying. Do not substitute a
different source here. When a Bellringer link changes, change this one in the same
pass.

**What this slide is not.** It is not a response slide. It has no first-answer box,
no revised-answer box, and no revision prompt in the speaker notes. It does not
count toward completion, which stays defined in section 9 as both answers present
on every response slide.

[Challenge: the alternative is to count the Concept Bank as a completion item, so
an unfilled grid costs the student credit. I have not written it that way, because
section 10 puts proficiency in the Growth Report and leaves the gradebook holding
completion of the response slides only, and adding a fourteen-cell grid to that
definition changes what a completion score means. Say so if you want it counted.]

The Concept Bank carries no `Critical aspect:` group label, because it spans every
aspect. It carries no slide-type marker from section 7.

**It goes on the diagnostic-count exclusion list.** Add `"concept bank"` to
`STANDING_REFLECTION_MARKERS` in `extract_and_grade.py` and to `STANDING_REFLECTION`
in `deck_lint.py`, in the same pass. As specified above the slide trips none of the
diagnostic tests, so the exclusion is defensive rather than a repair — its job is to
catch a Concept Bank cloned from a 3-Tier slide with a tier label left on it, and to
make the exclusion a stated decision. The exclusion is an edit to two scripts and is
not part of a deck build. See section 7.1.


---

## 3c. The marker fault, and the `markers present:` line (added 2026-08-18)

Katherine hit this while the Concept Bank was being built. An ellipsis broke the
linter while the grader kept working. Nothing looked wrong. That is the version of
this bug that survives longest, so the rule below is now a standing check.

**The rule. Read the `markers present:` line on every build. Do not trust a
clean-looking deck.**

### Why the two scripts disagree

They match markers by different mechanisms, and the mechanisms fail on different
characters.

| | `extract_and_grade.py` | `deck_lint.py` |
|---|---|---|
| How | Plain substring, lowercased | Compiled regex, `re.I` |
| What if | `"what if?" in text` **or** `^\s*what[- ]if\b` at line start | `what if\?` only |
| Critical aspect | `Critical aspect:\s*(...)` | `critical aspect\s*:` |

The grader carries a second, looser test for the What if slide that matches
`what if` or `what-if` at the start of a line with no question mark. The linter has
no such fallback. A slide that reads `What if…` with an ellipsis in place of the
question mark therefore still classifies as `what_if` in the grader and vanishes
from the linter's marker set. The two counts then differ by one, and nothing on the
slide looks wrong, because an ellipsis is a plausible thing to type.

### Why a clean report hides it

`deck_lint.py` sorts its output into `errors`, `warnings`, and `notes`, and then
prints `clean — no tier/marker/color problems found` when there are no errors and
no warnings. A missing marker goes into **`notes`**, with the text
`diagnostic markers not found in deck: [...] (fine if this arc doesn't use them;
flagged for eyeball)`. So the deck prints `clean` on the last line while a note two
lines above says a marker is gone. The word `clean` is not a verdict on the markers.

### What to do on every build

1. Read the `markers present:` line. It must list every marker the deck actually
   uses: `Critical aspect`, `Pattern break`, `Build-a-rule`, and `What-if` for a
   normal two-aspect cycle.
2. Read the `notes` block even when the last line says `clean`.
3. Compare `diagnostic slides:` from the linter against the diagnostic count from
   the grader. See §7.1. A difference of one is this fault or the exclusion-list
   fault, not noise.
4. Where a marker is missing, find the slide and look at the punctuation before you
   change anything. The usual cause is a typographic character standing in for an
   ASCII one: `…` for `?`, a curly apostrophe, a non-breaking space, an en dash for
   a hyphen in `what-if`.

### The general rule

A marker string is matched by machine, not read by a person. Type it in ASCII,
verbatim, exactly as §7 gives it. Do not let a smart-punctuation pass, a paste from
a word processor, or a well-meant tidy of the wording touch a marker string. If a
marker has to change, it changes in §7, in both scripts, and in every deck, in one
pass — the same discipline as the exclusion list in §7.1.

[Challenge: the deeper fault is that two scripts implement the same concept twice,
by different means, and the only thing keeping them aligned is a comment and a
habit. One shared module holding the marker definitions, imported by both, removes
this whole class of bug. That is a change to the scripts, not to a deck, and §11
says not to rewrite them casually — but it is worth doing once, deliberately, and
it would retire both §3c and half of §7.1.]

---

## 4. Organization and clarity

A deck is not finished when it has the correct slide types in the correct order. A
deck is finished when each slide does one job, and when the title of the slide
names that job.

Read your deck against Cycle 02. Its content slides have the titles "Makers and
eaters", "Zoom out from your plate", and "Where does the other 90% go?". Each title
tells the student what the slide is for.

A deck with five slides in a row titled "Gene Mutations" is not organized. The
slide types around them do not change this. A new title is not decoration. A
student who looks back through the deck navigates by the titles.

Do this when you finish an old lecture deck:

1. Give each content slide a title that names what the slide does. Use plain words.
2. Combine slides that make the same point. Divide a slide that carries two ideas.
3. Order the content so that each slide earns the next slide. The student must be
   able to answer the Contrast Set from the slides before it. The Pattern Break
   must strain the rule the student just made.
4. Remove content that the critical aspect does not need. An old lecture deck holds
   material that no slide type uses.

Do not keep the order of the source deck to stay safe. To keep it is the failure.

## 4b. Activity guides are retired (2026-08-17)

There are no standalone activity guides. Either set the activity up with a slide
(concise student steps ON the slide, longer teacher directions in that slide's
speaker notes, prep on slide 2) or do not use it.

The one exception is a **printable students physically use** — card sets, sorting
sets, student data pages. Those live in the cycle folder (or "My Class only
(print)"), and the activity slide links to them. Where an activity works as
movable pieces, prefer building the pieces as draggable shapes on a slide —
the deck is the manipulative — over printing anything.

Old guides whose content has been folded into slides go to a
`_retired guides (folded into slides)` subfolder in the cycle folder. Nothing is
hard-deleted.

---

## 5. How to complete a deck that has slide types missing

You cannot repair a deck by a change of order when it has no Critical Aspect
questions, no Build a Rule slides, or no response slides. Write the missing slides.
Complete the deck.

**Build these without approval.** Response slides, day dividers, the teacher
reference slide, the closing checklist, the links slide, and the image credits. A
response slide uses the Mastery question that already exists, so you write nothing
new.

**Write these, and mark them.** Critical Aspect questions, Build a Rule sentences,
activities, Relates to me, optional challenges, and **the teacher note slide**
(§2.0a). The note is bracketed like everything else in this list, and for a
sharper reason: five of its seven declarations are design intent, and design
intent is Katherine's. Draft what the deck itself shows — the critical aspect, the
invariant, the slide-type map — and mark the rest for her. A guessed visibility
rung is worse than a missing one, because it reads as a decision that was made.

Write them from the content of the deck. Do not use knowledge from outside the
deck. The rule in a Build a Rule slide must be the rule that the Contrast Set of
that deck supports.

Put brackets around every word you write. Katherine can then see which words are
hers and which words are yours. She approves each one or writes it again. When she
approves a line, remove the brackets. The text is then hers.

**NGSS codes may be drafted** (rule changed by Katherine, 2026-08-17): verify the
performance-expectation wording verbatim against nextgenscience.org before writing,
and bracket the codes for her check. The essential claim and the objectives may be
drafted only when Katherine explicitly authorizes it for that deck; otherwise mark
them `⚠ NEEDS KATHERINE`.

---

## 6. Images

A deck is not austere text. Put graphics through the deck where they teach. A slide
that has text only is not finished.

**Where to put an image**

- Contrast slides and case-pair slides. Use one image for each case. Use the same
  size and the same vertical position for both.
- Definition slides and category slides. Use one image for each category. Put the
  images in the same left-to-right order as the definitions above them.
- Pattern Break slides where the student cannot imagine the organism. Examples are
  the bee orchid, the dodder, and the anglerfish. This is the most valuable
  position in the deck. The slide does not work if the student cannot see the
  unusual case.
- Teaching slides that have an empty band below the text.

**Where not to put an image**

- Question slides and writing slides stay white. The plain look is deliberate and
  distracts the student less.
- Never put a decorative photograph on an information slide. If the image does not
  make the idea clear, leave the space empty.

**Where to get an image**

- Use Wikimedia Commons only. Public domain and CC0 are best. CC BY and CC BY-SA
  are acceptable if you record the attribution.
- Never use a photograph from a news site.
- Never use an image from a generative model. These models corrupt biological
  labels. An incorrect label is worse than no image.
- Prefer an image with no label. A caption that names the category gives the
  student the discrimination that the slide asks the student to make.

**Checks you must do**

1. Make a contact sheet of every candidate image. Look at the sheet before you
   insert an image. A relevant search result is not always a clear depiction. The
   search "red-tailed hawk perched" returned a hawk 200 metres away on a rock. The
   image was useless at a width of 1.9 inches.
2. Crop each image from the center to the target ratio. The image then keeps its
   proportions.
3. Render the slides you changed. Look at them. No image can touch a writing box.

**What to record.** Record `LicenseShortName`, `Artist`, `LicenseUrl`, and the URL
of the Commons page for each image. Record them when you get the image. Make two
outputs: an `.md` table of the licenses, and an **Image credits** slide at the end
of the deck.

---

## 7. Icons, and the marker strings

**Icons.** Use Twemoji (`jdecked/twemoji`), CC BY 4.0. Rasterize the SVG file at
320 px. Flatten it onto white. A transparent PNG file can show as a gray box in
PowerPoint.

Put the icon in the top right corner. Use 0.55 inches at about (8.95, 0.55). A day
divider takes 0.80 inches at (8.60, 0.55).

Select an icon that names the content of the slide, not a mood. Use a mushroom on
the decomposer Pattern Break, a flame where energy leaves as heat, a crystal ball
on the What if slide, and a pencil on Build a Rule.

Skip any slide where the icon touches a photograph or text. Render the slide and
look at it. Do not trust the coordinates.

Credit Twemoji on the Image credits slide.

**The marker strings.** The teacher prompts find the diagnostic slides by an exact
text match. Two different kinds of string do two different jobs. Do not confuse
them.

**`Critical aspect: <name>` is a group label, not a slide-type marker.** Put it on
every slide that belongs to that aspect. Cycle 02 carries it on 13 of 33 slides,
including its Build a Rule slides and its Pattern Break slides. The label tells the
student and the teacher which aspect the slide serves.

**The slide-type markers are unique.** Each one appears one time for each slide of
that type, and nowhere else.

| Marker string | Slide type | Count in Cycle 02 |
|---|---|---|
| `Pattern break` | Pattern Break | 2, one for each aspect |
| `Finish this sentence as a rule` | Build a Rule | 2, one for each aspect |
| `What if?` | What if | 1 |
| `Getting Started` | 3-Tier Question | 2, one for each aspect |

Do not put a slide-type marker on a slide of a different type. That fault makes
the prompt count the slide two times. It is the same fault as the extra
navigation-slide count that `extract_and_grade.py` fixed on 2026-07-06.

**The Concept Bank slide.** Its heading, `Define these in your own words`, is
unique and appears one time in the deck. Use that string where a prompt has to find
the slide or skip it. Put none of `Pattern break`, `Finish this sentence as a rule`,
`What if?`, `Getting Started`, or `Critical aspect:` on it. A Concept Bank that
carries a tier label copied from a 3-Tier slide will be counted by the teacher
prompt as a second 3-Tier slide.

The word `Mastery` alone is not a reliable marker. Activity slides say "Attempt the
Mastery response", so the word appears 6 times in Cycle 02. Count `Getting Started`
to count the 3-Tier slides.

Check the counts after each build. The count of each slide-type marker must equal
the number of slides of that type. The count of `Critical aspect:` must equal the
number of slides in all the aspect blocks together.


### 7.1 The diagnostic-count exclusion list

Written 2026-08-18 against the copy of `extract_and_grade.py` Katherine supplied
that day, whose `STANDING_REFLECTION_MARKERS` tuple is dated 2026-08-06. Section 0
says to get the scripts from Drive at run time. Read the live copy before you edit
it, and confirm these tuple names still hold.

`extract_and_grade.py` classifies every slide of the teacher deck. Every slide it
does not classify as `other` is diagnostic, and diagnostic slides are the only
slides scored for completion. `classify_slide()` returns a diagnostic type when the
slide text contains, case-insensitively:

- all three of `Getting Started`, `Working On It`, and `Mastery` — `critical_aspect_concept_question`
- `Pattern break` — `pattern_break`
- `Build a rule from`, `Finish this rule`, or `Finish this sentence as a rule` — `build_a_rule`
- `what if?`, or `what if` / `what-if` at the start of a line — `what_if`

Two exclusion tuples are tested **before** any of those four.

| Tuple in `extract_and_grade.py` | Contents | What it covers |
|---|---|---|
| `NON_DIAGNOSTIC_MARKERS` | `"do not project"`, `"teacher navigation"` | Teacher slides that are never projected |
| `STANDING_REFLECTION_MARKERS` | `"continuation question:"`, `"relates to me:"` | Real, projected, student-facing slides that are never scored |

The two tuples are separate on purpose, so the reason a slide was excluded stays
auditable. The comment above `STANDING_REFLECTION_MARKERS` states that it **must
stay in sync with the `STANDING_REFLECTION` tuple in `deck_lint.py`**. The tuple
has a different name in each of the two files. Do not assume the name carries
across.

The tuple names differ across the two files in both cases:

| File | Role | Unscored-reflection tuple | Never-projected tuple |
|---|---|---|---|
| `extract_and_grade.py` | The grader | `STANDING_REFLECTION_MARKERS` | `NON_DIAGNOSTIC_MARKERS` |
| `deck_lint.py` | The linter | `STANDING_REFLECTION` | `NON_DIAGNOSTIC` |

### 7.1a Each script exists twice in Drive (found 2026-08-18)

[Superseded 2026-09-03: the four Drive copies are stale and no longer edited. The exclusion list is edited once, in `scripts/extract_and_grade.py` and `scripts/deck_lint.py` in the repository. The paragraphs below are kept as history.]

[Correction, 2026-08-29. Every claim in this section was tested against Drive today
and most of it no longer holds. What is actually there:

- `1SEe_chKL1lQ2anjoj0QoDNGkfKXBzvDS` resolves, and is `scripts (Do NOT Delete)` — but
  it is owned by **kvond12@gmail.com** and sits at that account's My Drive root, not
  Red Clay's. That is why it is invisible to any session authenticated as the school
  account.
- The entire second row is gone. `1AbfjWXx8zBVq8EgEDeIG2Mgvx41CyE1h`,
  `165XV8l9Wj6A8agYVJn30UzUYaUDH6f0L` and `1-TenYZr2BDsASCKu7hXC_0dID3VZqu6Z` all
  return "not found". No folder named `19_Bio_Pipeline v2 (do not delete)` exists at
  My Drive root. One with that name exists inside
  `06 TPT/TEACHERS PAY TEACHERS (Shared)/CLAUDE SKILL FILES/`, and it holds no `.py`
  files at all.
- So there were not four copies of the exclusion list. There was one. The MD5
  verification recorded above is describing files that no longer both exist.
- `deck_link_check.py` was in neither scripts folder. It was at
  `06 TPT/TEACHERS PAY TEACHERS (Shared)/CLAUDE SKILL FILES/deck_link_check.py` — a
  third location this file never names. It is now in the repo at `scripts/`.

The sync discipline this section is built on therefore has nothing left to
synchronise, and the "four places, verify four MD5s" instruction should not be
followed. Git replaces it: an edit to the exclusion list is one commit touching both
`extract_and_grade.py` and `deck_lint.py`, and the diff shows whether the second file
was actually changed. That is the durable fix the challenge note below asked for.]


There are two folders named `scripts (Do NOT Delete)`, and each holds a copy of
both scripts. That makes the exclusion list live in **four** places, not two.

| Folder | Where it sits | `extract_and_grade.py` | `deck_lint.py` |
|---|---|---|---|
| `1SEe_chKL1lQ2anjoj0QoDNGkfKXBzvDS` | My Drive root. Also holds every `.bak` | `1Qwb6KxfjEOAZhSBmRVcxhXCtaFJgUEmM` | `1eh8cG3J1obRsDcaMhBFOhcCwS-d53m58` |
| `1AbfjWXx8zBVq8EgEDeIG2Mgvx41CyE1h` | Inside `19_Bio_Pipeline v2 (do not delete)` | `165XV8l9Wj6A8agYVJn30UzUYaUDH6f0L` | `1-TenYZr2BDsASCKu7hXC_0dID3VZqu6Z` |

Verified 2026-08-18: the two copies of each script are byte-identical. MD5 of
`deck_lint.py` is `f3e7b43a64288711cde142fa986a9efd` in both folders, and MD5 of
`extract_and_grade.py` is `0b647764ee967200341fe5beff01aa11` in both. The copy in
the v2 folder was made on 2026-08-09 from the root copy. They agree today.

**Section 11 is wrong about the dead ID, and this file corrects it.** Section 11
says the `1eh8cG3J…` ID for `deck_lint.py` is dead. It is not. That file exists,
is not trashed, and was last modified 2026-08-10, which is one day *later* than
the copy section 11 calls current. Neither ID is dead. The two are duplicates.

**The consequence for this section.** An edit to the exclusion list has to land in
four files, not two, or the two folders diverge and which answer you get depends on
which folder a run picked its scripts up from. Verify the four MD5s match after the
edit, in the same pass.

[Challenge: four copies of a script that must stay in sync is the same class of
failure the sync comment was written to prevent, one level up. The durable fix is
one copy and a link, not four copies and a discipline. Before making the exclusion
edit, decide which folder is authoritative and make the other a shortcut. Ask
Katherine, and do not delete anything — both folders are marked "do not delete".]


**Matching is case-insensitive substring matching.** An entry must be lowercase,
and it must be a string that actually appears on the slide.

**Two slides now ride on the `do not project` entry** (2026-08-29): the teacher
note, §2.0a, and the visibility-ladder slide, §2.0b. Neither is scored and neither
may be counted. That entry is the only thing keeping them out of the diagnostic
count, so a build that drops the kicker, or paraphrases it to "not for projection",
silently adds two diagnostic slides to the deck. `deck_lint.py` checks for that on
the ladder slide and reports `A-VIS-LADDER` if the string has gone.

**The Concept Bank goes on that list.** Add the entry `"concept bank"` — lowercase,
no colon. One entry covers both slides where a deck carries two, because the kicker
is the same on each. The two existing entries carry a colon because those slide titles are
followed by one. The Concept Bank kicker is `CONCEPT BANK` and carries none. Add
the same string to `STANDING_REFLECTION` in `deck_lint.py` in the same pass.

**What the exclusion actually protects against.** Read against the current
`classify_slide()`, a Concept Bank built to section 3b trips none of the four
diagnostic tests, so it already falls through to `other`. The exclusion still earns
its place, for two reasons.

1. Section 14.2 says to build a slide by cloning one that already exists. The
   obvious clone source for a fourteen-row grid is a 3-Tier slide, and one leftover
   `Getting Started`, `Working On It`, or `Mastery` label anywhere on the cloned
   slide makes it a scored `critical_aspect_concept_question`. The exclusion tuples
   are tested before the tier test, so the exclusion catches that build error
   instead of letting it reach the gradebook.
2. It makes the exclusion a stated decision rather than an accident of which words
   the slide happens to avoid. That is why the two tuples were split apart.

[Correction to what I told Katherine before I had the file: I wrote that the
Concept Bank heading `Define these in your own words` is a marker string that
inflates the diagnostic count today. That was wrong. It appears in no marker tuple,
and the slide classifies as `other` as specified. The exclusion is worth making,
but it is defensive. A deck that ships a Concept Bank before the edit lands is not
mis-scored on this account.]

**Open defect, found 2026-08-18. The exclusion list matches nothing in Cycle 02.**

Every entry in `STANDING_REFLECTION_MARKERS` was tested, as a lowercased substring,
against all 35 slides of the finished Cycle 02 deck. Neither entry fires.

| String tested | Slides matched |
|---|---|
| `"continuation question:"` | none |
| `"continuation question"` (colon dropped) | none |
| `"continuity question"` (§1's own term) | none |
| `"relates to me:"` | none |
| `"relates to me"` (colon dropped) | 31 |
| `"concept bank"` | 32 |

Two separate faults, and they need different fixes.

**The colon.** `"relates to me:"` misses because the slide is titled `Relates to me`
with no colon after it. Dropping the colon from the entry fixes that one.

**The words.** The continuity-question entry cannot be fixed by punctuation. §1
calls the slide type a **Continuity question**, the grader looks for
`continuation question`, and the slide in Cycle 02 is actually titled **`Keep
going`**. Three names, no two of which agree, and none of the three appears in the
tuple in a form that matches the deck.

Nothing is mis-scored today, because both slides fall through to `other` anyway —
neither carries a tier label, a Pattern break, a Build-a-rule sentence, or a What
if. The exclusion list is inert, not wrong. It stops being inert the moment one of
those slides gains a phrase that trips a diagnostic test, and then the fault
appears in a deck nobody was editing.

**The fix, and why the Concept Bank is the model.** The Concept Bank matches
because §3b gave it a fixed kicker, `CONCEPT BANK`, and §7 records that string. Do
the same for the other two: give each unscored student-facing slide type one
stable marker string, record it in §7, put it in both tuples, and title the slides
with it. Reconciling Continuity / Continuation / Keep going into one word is
Katherine's call, since it changes §1's vocabulary and the titles in 26 shipped
decks.

[Recommended, when she decides: keep §1's `Continuity question` as the term, add a
fixed kicker `CONTINUITY QUESTION` to that slide type the way `CONCEPT BANK` works,
and set both tuples to `("continuity question", "relates to me", "concept bank")` —
lowercase, no colons. Retitling is then the only per-deck work, and the exclusion
list starts doing the job it was written for. I have changed nothing.]

**This is a deliberate edit to two scripts, not a step in a deck build.** Section
11 says never to write the linter again, and that rule stands. Adding a slide type
to an exclusion list is a named change to one named tuple in each of the two files,
made once, on purpose, and checked by running both against a deck that carries the
new slide type. Do not make this edit as a side effect of finishing a deck, and
never regenerate either script in order to make it.

**Status on 2026-08-18: not done.**

**When you add any future slide type,** ask first whether it is scored. A
student-facing, unscored slide type goes on this list in both files, in the same
pass, before the type ships in any deck.

[Answered 2026-08-29, by Katherine's direction. Student feedback now runs through
a **prompt, not a script**. `extract_and_grade.py` is no longer the live grader, so
the sync rule this section is built on has **no second half**. The tuple that
matters is the one in `deck_lint.py` alone, and the edit below is a one-file edit,
not a two-file one. `"concept bank"` was added to `STANDING_REFLECTION` in
`deck_lint.py` that day; the diagnostic count did not move, which is what this
section predicted — the exclusion is defensive, not a repair.

Treat the two-script language remaining in this section as history. Do not go
editing `extract_and_grade.py` to satisfy it.]

---

## 8. The links slide

- List every hyperlink in the deck, in the order of the deck. Make the label a live
  hyperlink. Print the plain URL below it in small gray text. The URL then survives
  a print.
- Link to the page of the resource. Do not link to the home page. A home page makes
  the student search.
- Prefer the original source to a copy. Scribd, Studocu, and CourseSidekick are not
  sources. If you can find only these, use the credit line on Katherine's own copy.
- Every document that the product names must have a link that works.
- The Concept Bank repeats the two Bellringer source links (section 3b). List each
  of those two links one time on the links slide, not two times.
  `deck_link_check.py` reports both occurrences. That is not a defect.

**Link test.** Run `deck_link_check.py` on the finished deck for every build. The
script walks each hyperlink and reports the HTTP status.

```bash
python3 deck_link_check.py deck.pptx
```

Read the output with judgment. A `429` from YouTube is a rate limit, not a dead
link. A `URLError` on a bare domain is usually a typographical error. One example
is `biomanbiology.com`, which must be `biomanbio.com`. Correct the errors. Run the
script again until each line is clean or explained.

---

## 9. Distribution, and the closing checklist

A teacher does not get a copy of the Slides file. A teacher gets a link to the
master deck with `/copy` at the end. Google then asks the teacher to make a copy
in the Drive of the teacher.

```
https://docs.google.com/presentation/d/<DECK_ID>/copy
```

Change every `/edit`, `/edit?usp=sharing`, and `/view` link to `/copy`. Do this on
each form and each template. Keep the master decks viewable by link. No teacher
gets edit access to a master deck. Each product section holds its part of the
course. Each section links only to the master decks for that part.

**A customer deck names no LMS.** Katherine uses Infinite Campus. A customer uses
neither Infinite Campus nor Schoology. Use this closing checklist:

```
Think → Write → Submit
☐  Finish your notes on every slide.
☐  On each response slide, open the Notes, run the revision prompt in your own AI, and write your revised answer under your first one. Leave both showing.
☐  Turn in your finished deck to the assignment.
Do not name your file. Your name is already attached where you turn it in.
Completion = both answers present on every response slide. Your growth shows in your printed Growth Report, not the grade.
```

A student does not name the file. The name of the student is already attached at
the place where the student turns the file in.

### 9.1 A built deck cannot be uploaded through Composio (found 2026-08-18)

`GOOGLEDRIVE_UPLOAD_FILE` does not take a file. It takes an `s3key` — a reference
to content **already inside Composio's own storage**, put there by an earlier
Composio download. A `.pptx` built anywhere else has no such reference, so the
upload fails with "Failed to retrieve uploaded file content. The file does not
exist in storage." Tested on 2026-08-18 four ways, all of which failed the same
way:

1. Local path passed as `file_to_upload` — rejected as not a dictionary.
2. Local path passed as `s3key` — file not in storage.
3. Deck rebuilt inside `COMPOSIO_REMOTE_BASH_TOOL` (Python 3.13 and python-pptx
   1.0.2 are both present there, and the rebuild succeeded), then uploaded by its
   sandbox path — file not in storage.
4. Same file copied to the sandbox's cloud-backed `/mnt/files/` mount and uploaded
   through `run_composio_tool` — the workbench crashed.

Nothing partial was written to Drive by any of the four. Verify the destination
folder afterwards regardless.

`GOOGLEDRIVE_EDIT_FILE` is not a way round it either, and it is the one that looks
like it should be. It preserves the file ID, so it would remove the relink problem
completely — but its `content` parameter is **a string, UTF-8 encoded on upload**.
A `.pptx` is binary. Pushing one through that parameter corrupts it. That is the
same failure Katherine's notes record as "base64 corruption on programmatic
upload", and it is visible in the tool schema rather than only in experience. The
schema also says the action does not work on Google Workspace native files at all,
so the Slides master is out of reach by that route regardless.

**There is therefore no write path for a deck through Composio.** Reading is free:
every live deck has a `.pptx` in Drive (see §0), so a build never needs a Slides
export. Writing back is manual, per deck.

**So the last step is Katherine's, and there is no way around it.** Hand her the
`.pptx`. She places it in Drive. Then take the new file ID and do the §9 relink.

### 9.2 What to do after she places a deck (proved on Cycle 02, 2026-08-18)

1. **Verify the placed file before anything else.** Export it back to `.pptx` and
   compare against the deck you built: slide count, slide size, and the text of
   every slide. Cycle 02 came back 35 slides, 9144000 x 6858000, zero slides
   differing, Concept Bank cells still `F2F6F9`, all 14 empty, both source links
   live. Do not assume the conversion was clean — check it.
2. **Rename it. Drive mangles the name on conversion.** `Cycle 02 — Ecosystems &
   Feeding Relationships (VT deck) — with Concept Bank.pptx` arrived as
   `Cycle_02___Ecosystems__Feeding_Relationships_VT_deck___with_Concept_Bank` —
   em dashes, the ampersand, the parentheses and the spaces all became
   underscores. That breaks the §0 live-deck test, which needs the Slides name to
   match the `.pptx` name. Rename with `GOOGLEDRIVE_UPDATE_FILE_PUT` to the
   canonical `Cycle NN — <title> (VT deck)`.
3. **Archive the deck it replaces**, so two files of the same name never sit in one
   folder. Rename, do not trash: `ARCHIVE <date> — Cycle NN (VT deck), before
   <what changed>`. That prefix is already Katherine's convention in Drive.
4. **Repoint every `/copy` link.** Find them with
   `GOOGLEDRIVE_FIND_FILE q="fullText contains '<old file id>'"`. A `/copy` link
   in a Slides deck is a **hyperlink on a text run**, not visible text, so
   `replaceAllText` cannot touch it. Use
   `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE` with `updateTextStyle`, the run's
   `objectId`, a `FIXED_RANGE` covering the run, `style.link.url` set to the new
   `/copy` URL, and `fields: "link"`.
5. **Verify the relink** by re-reading the deck and counting occurrences of the old
   and new IDs, and by re-running the Drive search for the old ID until it returns
   nothing.

### 9.3 Every place a deck ID is written (mapped 2026-08-18)

A deck ID lives in **two kinds of surface**, and a Drive search finds only some of
them. Repoint both on every deck, before archiving the old file.

**A. The Master Agenda spreadsheet — the larger carrier.**
`1i6D-QT5nQWdVpltW14XB7OZ9lWFrMbMO8ZnZQvpUw-w`, tab `🌿 Biology Agenda 26-27`
(gid `901875884`). Column **G**, one `=HYPERLINK("…/copy","🎞 Deck ↗")` per class
day, so **two or three cells per cycle**, not one. Cycle 02 was G6, G7, G8. The tab
references 25 distinct deck IDs. These are ordinary formulas: read with
`GOOGLESHEETS_VALUES_GET` at `value_render_option: FORMULA`, write with
`GOOGLESHEETS_BATCH_UPDATE` at `valueInputOption: USER_ENTERED`.

**B. The five START HERE decks.** Every `/copy` link sits on **slide 4** of each,
as a hyperlink on a text run — see §9.2 step 4 for how to change one.

| START HERE deck | ID | Cycles it links |
|---|---|---|
| `▶ START HERE — Ecology Starter (FREE)` | `1eXMmYJFYQ8SgE9-PztzA824XaAla8M41WjeH0VQ7QFU` | 02, 03 |
| `▶ START HERE — From Sunlight to Populations` | `1d7mIwNRIUru1ydo6QqZ4o6ZYSwx37etL6wHoARDRhWo` | 01, 04, 05, 06, 07a, 07b |
| `▶ START HERE — The Cell as a System` | `1QVW9VYXOy2RS2USvxJ7_KuwfDvDITYfI9zKw2MzBl_4` | 08, 09, 10, 11 |
| `▶ START HERE — Inheritance & Information` | `1wHLloTLm9eXXvYz4eL6GUkiUFQNRWPTsCETBbcZuSWs` | 13a, 14, 15a, 15b, 16a, 16b |
| `▶ START HERE — Change Over Time` | `1C8vj5Plr67uC5dHphNeLTqKu4gC1S1KTwTqPCYDbi10` | 17, 18, 19, 20 |

`TPT🧭 Biology v3 — Teacher Dashboard (start here)` carries no deck links.
**Cycles 12, 16c and 16d are linked from no START HERE deck** — check whether that
is deliberate before assuming a deck has no callers.

### 9.3a The agenda and the product answer different questions

The Master Agenda and the START HERE decks legitimately hold different sets of
cycles, and the difference is not a defect to reconcile.

- **The Master Agenda is Katherine's own teaching schedule.** It lists what she
  will actually teach, on dates. It carries fewer lessons than the product ships,
  **on purpose**. In her words: *I teach less to go slower.* The manual already
  states the same principle twice — §2 says a cycle carries two or three critical
  aspects, "not eight facts", and §9 says "Pace destroys depth." Do not "fix" the
  agenda by adding every shipped deck to it, and do not read a missing cycle there
  as an error.
- **A START HERE deck is the customer's index of the product.** It must list
  **every** deck in its arc, CORE and EXTEND both, because a customer who bought
  the set cannot reach a deck that is not listed. A missing deck here **is** a
  defect.

**Open gap, found 2026-08-18.** `▶ START HERE — Inheritance & Information` lists
13a, 14, 15a, 15b, 16a and 16b. It is missing **Cycle 12 (CORE)**, **Cycle 12
(EXTEND)**, **16c** and **16d**. No START HERE deck lists Cycle 12 at all.

**How slide 4 is built**, for when those rows get added. Each lesson is a **pair of
text boxes**: a title box (`Cycle NN — <title>`) and, below it, a box whose single
run reads `▶ Copy link ↗` carrying the `/copy` hyperlink. The pairs run in cycle
order between the intro text and the footer box
(`Answerable Biology · <arc name>`). Adding a lesson means cloning a pair and
placing it below the last one, then shifting the footer — a layout edit, so render
the slide and look at it before shipping.

**The order matters.** Repoint every caller *first*, then archive the old deck. On
2026-08-18 the old Cycle 02 deck was archived before the agenda was checked, and
the agenda's three deck links pointed at a file named `ARCHIVE …` until Katherine
noticed. A Drive `fullText` search for the old ID returned **zero** files at that
moment — it had found the START HERE deck but never the spreadsheet.

[Challenge, and it is the durable fix: the agenda already has a
`File IDs (do not delete)` tab, and it holds no deck IDs at all. Put the 24 deck
IDs there, one row per cycle, and make column G a formula that builds the link from
that row. Repointing a deck then becomes one cell edit instead of three, and any
other surface that reads the sheet follows automatically. That does not fix the
START HERE decks, which would still need their own pass, but it removes the larger
half of the work and the part most likely to be missed.]

**Correction to a standing note.** The project notes say Drive `fullText` does not
index hyperlink URL targets. On 2026-08-18 it did: the search for the old Cycle 02
ID returned `▶ START HERE — Ecology Starter (FREE)`, where the ID appears **only**
as a link target on a run whose visible text is `▶ Copy link ↗`. But it did **not**
find the Master Agenda, whose three `=HYPERLINK()` formulas carried the same ID.
So `fullText` is a partial index in both directions: use it as a first pass, never
as proof there are no callers left. Walk the surfaces in §9.3 by hand every time.
Do not spend a session hunting for an upload route; this is the answer until
Composio gains a way to stage local bytes.

[Challenge, worth raising once: the whole relink problem exists because a new
upload gets a new file ID. If the deck's identity moved to a stable Drive shortcut
that the product links to, and the shortcut were repointed at each new version,
the `/copy` URL in §9 would never change and nothing downstream would need
touching. That is a change to how the product links decks, not to a deck.]

**Never ship a date.** The year of a customer does not start when Katherine's year
starts. A customer copy carries the cycle number and the length only. Use
`Unit N · 3 class cycles`. A cycle is 3 class cycles. A cycle takes 2 to 4 class
meetings. The number depends on the schedule of the school.

---

## 10. What the finished deck feeds

The batch pipeline is retired for the customer product. Three prompts ship.

| Output | Who reads it | Which prompt |
|---|---|---|
| Coached revision, during the lesson | The student, in the AI of the student | Student prompt, section 3 |
| Individual Growth Report with the completion score | The student, on paper | Teacher prompt 1 |
| Completion record as a CSV file | The teacher, for the gradebook | Teacher prompt 1 |
| Teacher summary for the year to date | The teacher only | Teacher prompt 2 |

The gradebook holds completion only. Proficiency lives in the Growth Report.

Integrity is a flag for review, on first answers only. Nothing fails automatically.
Nothing posts by itself. The teacher decides.

"Workflow A → B1 → B2 → C" is retired. Do not use it in a customer template. Bio
v3, in `Pipeline (do not delete)`, is Katherine's own system. It never ships to a
customer.

---

## 11. Checks before delivery

1. Make a text dump with `markitdown`. Check the content, the order, and that no
   placeholder text is left.
2. Compare the text against the source deck. Name the reason for each difference.
3. Count the marker strings. See section 7. Each count must equal the number of
   slides of that type.
4. Read the `markers present:` line from `deck_lint.py`, and read its `notes`
   block even when the last line says `clean`. See §3c.
5. Render the slides you changed. Look at each one. Find text that overflows, shapes
   that touch, images over a writing box, and text that a border cuts.
6. Compare the slide count to the page count of the render. The two must be equal.
7. Run `validate.py out.pptx --original src.pptx`.
8. Run `deck_link_check.py out.pptx`.
9. Run `scripts/deck_lint.py` from the repository clone. It is the last gate: zero HARD
   findings or the deck does not ship; read the ADVISORY block and the `markers present:`
   line either way (§3c). `deck_link_check.py` is beside it at `scripts/deck_link_check.py`
   and needs network access; `deck_lint.py` does not. Never write the linter again.
   (Rewritten 2026-09-03. The Drive IDs formerly listed here — `1-TenYZr2…`,
   `1eh8cG3J…`, `1PR5_74Xi…` — do resolve from the answerableteaching Drive, which is
   why a stale copy was run that morning; they are not to be used. The old note about
   an ignorable `#EFDF85` warning described the pre-2026-08-29 linter, which reported
   it as a warning; the current linter reports it as ADVISORY A-TIER-COLOR and accepts
   `111111` or `EFDF85`.)

**Checks added 2026-08-29.**

- **The teacher note slide is present** and carries all seven declarations, §2.0a.
  Six is a fail. The two that go missing most often are which simultaneity the
  cycle works on and the visibility rung.
- **The visibility-ladder slide is present**, sits immediately after the teacher
  note, and still carries `do not project` (§2.0b). Then confirm the two numbers
  that the slide must not move: the diagnostic count, and every slide-type marker
  count from check 3. Both must read exactly what they read before the slide went
  in. A marker count that rose by one means a move name was written plainly
  somewhere on the slide.
- **Every "slide N" reference in the deck still points where it says.** Inserting
  anything in the front block moves the rest of the deck down by one. Grep the
  slide text AND the speaker notes for `[Ss]lide \d+` and check each hit against
  the render.
- **The What if is individual and written.** Not group work, whatever the
  coordination structure above it did, and its question names what changes and
  what is held.
- **The Concept Bank asks for a relation**, not only for definitions. §3b.
- **Every conditional slide type present has a stated reason** in the teacher
  note's slide-type map, and every one left out has a reason too.
- **Every Critical Aspect question carries a difference in its own text** — a
  comparison, a choice between named alternatives, or a stated change condition.
  A question that names the aspect and waits for the Contrast Set on the next
  slide is structurally the polar bear question and the room will go quiet before
  the contrast arrives. This is mechanically checkable.

[Only the teacher note slide's presence is a hard failure. The other four are
advisory: they are reported and they do not stop a deck shipping. Most decks will
not carry a coordination structure the first time this runs, and that is not yet a
defect. A linter that fails every deck gets ignored inside a week.]

**Concept Bank checks (added 2026-08-18).** Confirm that the slide is present,
that it sits immediately before the Day 3 divider, that every definition cell is
empty, that the term count is fourteen or fewer per slide and that there are at
most two slides, that the terms run in order of
first appearance, and that both source links match the ones on the Bellringer.
Render the slide. A full grid is the densest slide in the deck, so text overflow
appears there first. Then confirm that the diagnostic count from
`extract_and_grade.py` equals the count from `deck_lint.py`, and that neither
counts the Concept Bank. A disagreement of one means the section 7.1 exclusion is
in one file and not the other. A Concept Bank counted by both means a tier label
survived the clone.

You must render the slides and look at them. A slide can pass every text check and
still ship with a fault. The What if slide of Cycle 02 shipped with the last line
cut by a box border. The text checks did not find it.

---

## 12. Licenses

The deck holds three different kinds of material.

- **Open license.** Reuse, change, and redistribution are granted in advance. This
  covers CC licenses and public domain material. The images, the icons, and the
  interactive models of Katherine are in this group.
- **Free of charge, but proprietary.** BioMan and HHMI BioInteractive are in this
  group. You can show these and link to them. Do not publish them again outside the
  school. Some BioInteractive resources carry a CC license on their own page. Check
  that page before you change one.
- **Free to link.** A link is not use, so a link never needs permission.

The deck links out. It does not embed. The deck therefore stays inside all three
groups. Watch one thing: a PDF file that Katherine hosts in Drive. To host and to
distribute is redistribution, not display. You must know where that file came from.

---

## 13. Design tokens — the visual standard

Every deck must look like the reference build. These values come from Cycle 02.
Do not invent a color, a size, or a position. Do not approximate a color by eye.

### 13.1 Page and font

| Item | Value |
|---|---|
| Slide size | 9144000 x 6858000 EMU (10 x 7.5 in, 4:3) |
| Font | Arial, every run, every slide |

### 13.2 Colors

| Token | Hex | Where it is used |
|---|---|---|
| Teal | `028090` | Kickers, slide headings, section labels, CASE A and CASE B labels, day divider band |
| Body black | `111111` | All body text. Not `000000` |
| Muted gray | `666666` | "TEACHER REFERENCE" line, small labels, the "Think first" footer, word bank label |
| Alert red | `C0392B` | The Pattern break kicker, and the "Getting Started" tier label |
| Green | `1E8449` | The "Mastery" tier label |
| Box fill | `F2F6F9` | The writing box |
| Box border | `CCCCCC` | The writing box |
| Panel gray | `F5F5F5` | A light panel behind a question |
| Divider pale | `EAF6F7` | The small line on the day divider band |
| Divider white | `FFFFFF` | The headline on the day divider band |

The "Working On It" tier label is body black `111111`, not a color. Only the first
and last tier labels carry a color.

### 13.3 Geometry

| Element | x | y | w | h | Size |
|---|---|---|---|---|---|
| Kicker line | 502920 | 109728 | 8321040 | 274320 | 11pt bold |
| Slide heading | 548640 | 822960 | 8046720 | 457200 | 16pt bold |
| Lead sentence | 548640 | 731520 | 8046720 | 457200 | 13pt bold |
| Body text | 548640 | — | 8046720 | — | 12pt to 14pt |
| "Think first" footer | 457200 | 6455664 | 8229600 | 274320 | 10pt, gray |
| Icon, normal slide | 7863840 | 502920 | 502920 | 502920 | — |
| Icon, day divider | 7863840 | 502920 | 731520 | 731520 | — |
| Day divider band | 0 | 2194560 | 9144000 | 1554480 | fill `028090` |
| Divider small line | 548640 | 2331720 | 8046720 | 457200 | 16pt bold `EAF6F7` |
| Divider headline | 548640 | 2788920 | 8046720 | 822960 | 26pt bold `FFFFFF` |
| Divider body | 548640 | 4114800 | 8046720 | 2286000 | 13pt `111111` |
| Writing box | 548640 | — | 8046720 | 1965960 | fill `F2F6F9` |
| Concept Bank heading | 548640 | 640080 | 8046720 | 457200 | 18pt bold `111111` |
| Concept Bank instruction | 548640 | 1097280 | 8046720 | 457200 | 12pt |
| Concept Bank term, column 1 | 548640 | row y | 1554480 | 292500 | 12pt bold `028090` |
| Concept Bank cell, column 1 | 2194560 | row y | 2286000 | 548640 | fill `F2F6F9` |
| Concept Bank term, column 2 | 4663440 | row y | 1554480 | 292500 | 12pt bold `028090` |
| Concept Bank cell, column 2 | 6309360 | row y | 2286000 | 548640 | fill `F2F6F9` |
| Concept Bank links block | 548640 | 5852160 | 8046720 | 457200 | 11pt |
| Visibility ladder, subhead | 548640 | 1042000 | 8046720 | 457200 | 11pt, gray |
| Visibility ladder, body | 548640 | 1554480 | 8046720 | 5120640 | 11pt, one column |

The seven Concept Bank row y values are **1554480, 2148840, 2743200, 3337560,
3931920, 4526280, 5120640**. The row pitch is 594360 and the row height is 548640.
Column 2 begins at 4663440, which is column 1 plus its width of 3931920 plus a gap
of 182880. Inside a column the term box is 1554480 wide, then a gap of 91440, then
the cell at 2286000. The grid ends at 5669280 and the links block starts at
5852160. The Concept Bank slide carries no "Think first" footer, so nothing sits
below the links block.

The term box is centred on its row: its y is the row y plus 128070, which is half
the difference between the 548640 row and the 292500 box.

These values are as built and verified against a render on 2026-08-18. The first
build used a 1097280 term column and a 274320 instruction line. Both failed on the
render: `Decomposer` and `Commensalism` wrapped mid-word, and the third line of the
instruction was cut by the top of the grid. Text checks passed on that build. Only
the render found it, which is why §11 requires one.

The left margin is **548640** and the content width is **8046720**. The kicker and
the footer are the only two elements that sit outside that column.

### 13.4 Type scale

**Revised 2026-08-17 by Katherine: student-displayed body text is now 18pt,
bulleted where it reads as a list, with 8–10pt paragraph space after every
bulleted item so items breathe.** Same slide role = same size in every deck.

| Text | Size | Weight | Color |
|---|---|---|---|
| Teacher reference title | 20pt | bold | `111111` |
| Section label (ESSENTIAL CLAIM, OBJECTIVES) | 10pt | bold | `028090` |
| Kicker | 11pt | bold | `028090`, or `C0392B` on a Pattern break |
| Slide heading | 20pt max | bold | `111111`, or `028090` on Build a Rule |
| Lead / question / rule sentence, main teaching prose | **18pt** | bold (leads) / plain (body) | `111111` |
| Day-divider body | **18pt**, bulleted | plain | `111111` |
| CASE A / CASE B label | 11–12pt | bold | `028090` |
| Case body (dense paired columns) | 12–14pt | plain | `111111` |
| Activity steps | 14–16pt | plain | `111111` |
| Tier label | 12pt | bold | `C0392B`, `111111`, `1E8449` |
| Tier question | 12pt | plain | `111111` |
| Word bank label | 9pt | plain | `666666` |
| Word bank items | 10–11pt | plain | `111111` |
| Response-slide instruction + box labels | 14pt | plain | `111111` |
| "Write your answer in the next slide" arrow | 14pt | bold | teal or gray (Arial — the old 32pt Calibri is a defect) |
| Concept Bank instruction | 12pt | plain | `111111` |
| Concept Bank term | 12pt | bold | `028090` |
| Concept Bank source link, label | 11pt | bold | `111111` |
| Concept Bank source link, linked text | 11pt | plain, underlined | `028090` |
| "Think first" footer | 10pt | plain | `666666` |

Titles are **20pt at the largest**. Main student-facing prose is **18pt**; dense
slide roles (case pairs, 3-Tier, word banks, bellringer sidebar) sit consistently
below it. Where 18pt collides with an image or a writing box, fix the geometry
from a render — or apply the dense-slide exception consistently, never ad hoc.

### 13.5 How to check

After each build, list every text run with its size and color. Compare the list
to the tables above. Then compare it to the same list from Cycle 02. A color or a
size that appears in your deck but not in Cycle 02 is an error.

---

## 14. Build new. Do not restyle the old deck.

Decided 2026-08-12, after two failed attempts to restyle Cycle 16 in place.

**The rule.** To bring an old deck to the standard, build a new deck from the
reference build. Read the old deck for its content. Copy none of its shapes.

### 14.1 Why

An old lecture deck carries formatting that a restyle pass cannot reliably find.
Cycle 16 held all of these, and each one needed a separate repair:

- Shape fills of bright green `00FF00` on 19 shapes.
- Dark bars filled with the theme color `schemeClr val="dk1"`. A check that reads
  `srgbClr` does not see a theme color at all, so the first two passes missed them.
- Title panels with a fill and a border, centered inside a small box.
- Titles at 32pt against the 16pt of the reference build.
- A title slide whose title is artwork, so a text dump reports the slide as empty.

Each repair found the next fault. That is the signature of the wrong method. A new
deck built from the reference has none of these, because every shape on it came
from the reference.

### 14.2 The method

1. Copy the reference build. It is now the template. It carries the page size, the
   fonts, the colors, the writing box, and the layout of every slide type.
2. List the slide types the new cycle needs. Use section 2 for the order.
3. For each slide the new cycle needs, **clone the matching slide from the
   template** and replace its text. Clone the Contrast Set slide to make a Contrast
   Set. Clone the 3-Tier slide to make a 3-Tier.
4. Delete every template slide you did not use.
5. Put in the images and the icons. See section 6 and section 7.
6. Run the checks in section 11.

The reference build carried no Concept Bank slide before 2026-08-18. Build the
Concept Bank on Cycle 02 first, to the geometry in section 13.3, and confirm it
with a render. Cycle 02 is then the clone source for every other deck, and no other
deck builds the grid by hand. Until that is done, step 3 has nothing to clone for
this slide type.

Cloning a slide keeps its fills, its type sizes, its colors, and its positions. You
then change only the words. The new deck cannot drift, because you never set a
color or a size by hand.

### 14.3 What to take from the old deck, and what to leave

**Take.** The science. The worked examples, such as THE DOG SAT and the codon
tables. The questions the teacher already wrote. The links. The teacher notes.
The order of ideas, where it is sound.

**Leave.** Every shape. Every fill. Every font size. Every position. Every border.
Every color. The title artwork.

If a sentence in the old deck is good, retype it into the cloned slide. Do not copy
the text box that holds it, because the box brings its formatting with it.

### 14.4 The one thing to check first

Open the old deck and render slide 1. A deck whose title is artwork reports as
empty in a text dump. Two builds wrote a teacher reference on top of the title
picture before anybody looked at a render. Look at the render, not the text dump.

---

## 15. Course scope, and the sibling skills (added 2026-08-18)

This file covers **Biology only**. From 2026-08-18 Katherine labels the
deck-finishing skills by course. Forensics and Anatomy & Physiology get their own
files, forked from this one.

**Naming.** `vt-bio-skill`, and on the same pattern `vt-forensics-skill` and
`vt-anatomy-skill`. Each description names its course and says the other two exist,
so a request that names a course loads one file and not three.

The `name` field takes lowercase letters, digits and hyphens only. Write it that
way in the file. Uppercase and underscores are normalised on save, so a file
written as `VT_Bio_skill` installs as `vt-bio-skill` and the file then disagrees
with the installed skill — write the normalised form and the two stay the same.

**What is course-neutral.** Sections 1, 2, 3, 3b, 4, 4b, 6, 7, 7.1, 8, 9, 11, 12,
13, and 14 hold structure, tokens, geometry, and process. Section 7.1 is more than
course-neutral: the two scripts are shared, so the exclusion list is edited one
time for all three courses, not one time per course file. A fork copies them without
change. A change to any of them must be made in every course file in the same pass,
or the three files drift apart silently.

**What is course-specific.**

- **The reference build.** Biology uses `Cycle 02 — Ecosystems & Feeding
  Relationships (VT deck)`. Each course names its own. The rule that the reference
  build wins over this file applies per course.
- **The two source links** in section 2.0 and section 3b. The CK-12 Biology
  FlexBook 2.0 and the Khan Academy biology set are Biology sources.
- **The standards line** in section 5. Biology drafts NGSS performance
  expectations, verified verbatim against nextgenscience.org.
- **The examples.** The bee orchid, the dodder, and the anglerfish in section 6,
  and THE DOG SAT and the codon tables in section 14.3, are Biology examples. A
  fork replaces them rather than carrying them.
- **The pedagogy note for Forensics.** Every Forensics lesson opens with a real
  foundational case, evidence shown and outcome hidden, student verdict before
  instruction, reveal at the end. The pig autopsy is excluded. That rule has no
  Biology equivalent and belongs only in the Forensics fork.

[Challenge, for the forks: Forensics has no CK-12 FlexBook section and no Khan
Academy unit to point at. The `FOR READERS:` and `FOR TESTERS:` pair in sections
2.0 and 3b cannot be carried across by substitution, because the second half of it
has no Forensics equivalent. That fork needs a decision from you before it ships,
and the honest answer may be that Forensics carries one named source rather than a
reader and tester pair. The same question applies to Anatomy & Physiology, which
has a CK-12 Human Biology FlexBook but a thinner Khan set.]

[Challenge, on drift: three files that share fourteen sections will diverge the
first time a change is made in a hurry to one of them. The alternative is one file
with a short course-specific block at the top and a single course-neutral body.
That costs you the clean per-course trigger you asked for, so I have written the
three-file version. Flag it if the drift matters more than the trigger.]

---

## 16. Restore, enhance, codes, agenda links (added 2026-10-15)

Katherine's direction, 2026-10-15: build these passes into the deck skill so that
lessons don't have to be repaired afterward. This section is course-neutral. It
applies to Biology, Forensics and A&P until the forks in §15 exist. Run the passes in
order, and finish all five before a deck counts as delivered.

The passes keep their existing owners. The workflow contract
`ai-ops/workflow-contracts/school-lesson-review-and-code-repair.md` names who runs
them. This section is the standard each pass is held to.

| Pass | Slash name (Katherine's) | Runs in |
|---|---|---|
| 16.1 Restore | `/restore-vt-slides` | School ChatGPT (Katherine) |
| 16.2 Enhance | `/vt-gemini-enhance` | School Claude Ext |
| 16.3 Codes | part of `/vt-gemini-enhance` | School Claude Ext |
| 16.4 Agenda links | after the deck and activities exist | the agent that built them |
| 16.5 Archive original | last, after all checks and relinks | the agent that ran 16.1 |

Sources for the work: the school Drive course folders and the original lesson
material in them. Don't use outside copies when the school Drive has the lesson.

### 16.1 Restore: merge the original lesson and the VT deck

This applies to Forensics and A&P, and to any Biology cycle that still has an original deck.

1. **Find both decks** in the week/cycle folder: the VT deck and the original lesson
   deck (including `.pptx` originals and `Copy of …` decks).
2. **Merge into the VT deck.** Use the VT structure (§1, §2) as the spine. Carry
   the original's content slides, **pictures, diagrams, data tables, case material,
   labs and worksheet links** into the matching critical-aspect block (§2.1).
3. **Cut nothing.** A picture or piece of lesson material that has no obvious place
   goes in an appendix slide after the end of the deck (§2.2). Never delete it. If
   the deck gets long, raise that with Katherine instead of trimming material.
4. **Keep the deck native.** Merge in Google Slides. Don't round-trip a native deck
   through PowerPoint (it drops codes and links). A `.pptx`-only VT deck is
   converted to Slides first, then merged.
5. **Leave the original live for now.** Don't rename or archive it during 16.1. It is
   archived in 16.5, after every check and relink has passed.
6. **Check:** the slide count of the merged deck is at least the VT deck's count
   plus the original's content slides; every image in the original appears in the
   merged deck (count images in both); `deck_lint.py` passes.

### 16.2 Enhance: `/vt-gemini-enhance`

Run it on the merged deck. The rules already in this skill hold: the enhance pass skips
answer slides; enhanced textboxes get no gray; answer textbox colours stay unchanged;
marker strings stay intact (§3c, §7). After the pass, run the post-enhancement check
(`docs/curriculum/post_enhancement_check.md`) and `deck_lint.py`. When the
marker layer and the deck disagree, fix the deck, never the prompt.

### 16.3 Embedded codes, including new student textboxes

The enhance pass also checks the embedded codes. The syntax comes from Master Agenda
`Agenda 26-27 CLEAN`, tab **Feedback Prompts**, **Prompt 00 (Embed Codes)**. Read it
fresh each time and don't copy it here. The observed schema is `[[NOTES:CYCLE:ID]]`
paired with `[[DRAFT:CYCLE:ID]]`, plus `[[OPTIONAL:…]]` and `[[BANK:CYCLE:TERM]]`, with the
slide-one `[[MARKER-INVENTORY:CYCLE]]` line.

**The prompt to run when Katherine adds new student textboxes.** Paste it as is:

```
I added new student textboxes to this deck. For each student textbox that has no
embedded code: add the code from Agenda Prompt 00 as small native text on the label
above the response area, outside the student's writing. Concept Bank boxes get
[[BANK:CYCLE:TERM]] with this cycle number and the term. Response boxes get the
paired [[NOTES:CYCLE:ID]] / [[DRAFT:CYCLE:ID]]. Keep every existing code and ID
unchanged and add no duplicates. Then update the slide-one [[MARKER-INVENTORY:CYCLE]]
counts and ID lists, and report which slides you changed.
```

**Check:** each student textbox has exactly one code; NOTES/DRAFT pair by ID, not by
slide position; and the inventory counts match the codes found.

### 16.4 Agenda links: after lessons and activities are created

Once a deck and its activities exist in the course folder, link them from the
Master Agenda `Agenda 26-27 CLEAN`
(`1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY`, school account) on that course's
tab, in the row for each class day that teaches the lesson:

- the deck (the teacher deck, and the student `/copy` link where the row has one);
- each activity, worksheet or lab created for the lesson;
- the week/cycle folder.

Rules:
- Write only into the row's existing link cells, in the format the row already uses.
  Don't add columns or restructure the tab, and don't change dates, pacing or notes
  (§9.3a: the agenda is Katherine's schedule).
- Fill a blank link cell, or replace a link that points at an `ARCHIVE …` file or a
  file *confirmed* missing. A 404 from one account doesn't prove the file is missing:
  decks can be invisible to the school connection and still exist under another account.
  Before replacing a link, check the file's owner and sharing across the authorized
  accounts. If you still can't tell whether it exists, leave the link, and report it as an
  access blocker in #kathy with the cell and the file ID.
- If a cell already holds a different live link, leave it and ask Katherine.
- Verify each new link with the school account (katherine.vonduyke@redclay.k12.de.us).
  The agenda and students use that account, not whichever account happens to open the file.
- Read the row back after writing. Every link must open the intended file, and none
  may point at an `ARCHIVE …` file.
- §9.3 above still describes the superseded agenda
  (`1i6D-QT5nQWdVpltW14XB7OZ9lWFrMbMO8ZnZQvpUw-w`). New links go to
  `Agenda 26-27 CLEAN` (ai-ops/NAMES.md). Before repointing §9.3 itself, get
  Katherine's confirmation, as the open gap in ai-ops/HANDOFF.md records.

### 16.5 Archive the original, last

Do this only after 16.1–16.3 pass their checks, `deck_lint.py` is clean, and the 16.4
links read back correctly. The order follows §9.3: repoint every caller and verify it
before archiving.

1. Read back every caller of the original's file ID: the agenda rows, START HERE
   decks, `/copy` links (§9.3), and a Drive `fullText` search as a first pass, never as
   proof. None may still point at the original.
2. Only then rename the original, never trash it:
   `ARCHIVE <date> — <original title>, merged into <VT deck title>` (§9.2 step 3).
3. If any earlier step stopped, skip this one. The original stays live and unrenamed,
   and the stop is reported.

**A deck is delivered when** 16.1–16.3 pass their checks, `deck_lint.py` is clean,
the 16.4 agenda links read back correctly, and 16.5 is done.

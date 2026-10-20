---
name: vt-skill
description: Finish an Answerable VT cycle deck to the shipping standard (Biology; §16 and the §17 lesson renewal standard also cover Forensics and A&P until their forks exist). Covers the 5 core questions, the four conditional slide types, the teacher note, response slides and revision prompt, What if, Concept Bank, images, icons, marker strings, links slide, /copy distribution, restoring original lessons into VT decks without losing pictures or material (/restore-vt-slides), the enhance pass (/vt-gemini-enhance), embedded codes for new student textboxes ([[BANK:CYCLE:TERM]]), adding deck and activity links to the Master Agenda, and the checks before delivery. Use it to build, repair, merge, enhance, code or complete a cycle deck, or to ask whether a deck is ready. Triggers - "VT deck", "finish the deck", "restore VT slides", "merge original and VT", "gemini enhance", "embed codes", "add agenda links", "is this deck ready".
---

# vt-skill — VT Deck Finishing

Run this skill after the text of a cycle is final. Run it before you give the
deck to Katherine. It covers slide order, response slides, images, icons,
appendix slides, and link tests. It sits above `deck_lint.py`. `deck_lint.py`
stays the last gate.

Katherine established this skill on 2026-08-06, on Cycle 2. Its dated revision history is in
[`reference/00-revision-history.md`](reference/00-revision-history.md).

**Where the long sections live (split 2026-10-19, wording unchanged).** This file keeps the
decision rules and short sections. These sections are in `reference/`, under their original
numbers; open the one the step needs:

| § | File |
|---|---|
| 2 | [`reference/02-slide-order.md`](reference/02-slide-order.md) |
| 3b | [`reference/03b-concept-bank.md`](reference/03b-concept-bank.md) |
| 3c | [`reference/03c-marker-fault.md`](reference/03c-marker-fault.md) |
| 6 | [`reference/06-images.md`](reference/06-images.md) |
| 7 | [`reference/07-icons-and-marker-strings.md`](reference/07-icons-and-marker-strings.md) |
| 9 | [`reference/09-distribution-and-closing-checklist.md`](reference/09-distribution-and-closing-checklist.md) |
| 13 | [`reference/13-design-tokens.md`](reference/13-design-tokens.md) |
| 15 | [`reference/15-course-scope.md`](reference/15-course-scope.md) |
| 16 | [`reference/16-restore-enhance-codes-agenda.md`](reference/16-restore-enhance-codes-agenda.md) |
| 17 | [`reference/17-lesson-renewal.md`](reference/17-lesson-renewal.md) |

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

Moved verbatim to [`reference/02-slide-order.md`](reference/02-slide-order.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§2.x` reference in this skill and elsewhere still points there.


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

Moved verbatim to [`reference/03b-concept-bank.md`](reference/03b-concept-bank.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§3b.x` reference in this skill and elsewhere still points there.



---

## 3c. The marker fault, and the `markers present:` line (added 2026-08-18)

Moved verbatim to [`reference/03c-marker-fault.md`](reference/03c-marker-fault.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§3c.x` reference in this skill and elsewhere still points there.


---

## 4. Organization and clarity

A deck is not finished when it has the correct slide types in the correct order. A
deck is finished when each slide does one job, and when the title of the slide
names that job.

**Apply the current learning-design standard during initial construction as well
as renewal.** Read [§17.7–17.9](reference/17-lesson-renewal.md#177-visual-reasoning-response-mode-and-titles)
before designing slides: visual relationships, deliberate response modes,
before/during/after discernment, provisional 90-minute days, and verified release
links are required review steps. Older examples do not override these later
requirements. Preserve the original-first course rules in §16.1 when applying
the organization advice below.

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

Moved verbatim to [`reference/06-images.md`](reference/06-images.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§6.x` reference in this skill and elsewhere still points there.


---

## 7. Icons, and the marker strings

Moved verbatim to [`reference/07-icons-and-marker-strings.md`](reference/07-icons-and-marker-strings.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§7.x` reference in this skill and elsewhere still points there.


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

Moved verbatim to [`reference/09-distribution-and-closing-checklist.md`](reference/09-distribution-and-closing-checklist.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§9.x` reference in this skill and elsewhere still points there.


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
   Also complete the learning-design, pacing and release checks in §17.6–17.9;
   marker and link scripts cannot establish those outcomes.
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
- **Every VT comparison has useful case pictures.** Inspect each slide asking
  students to discern differences or contrasts; add missing pictures and verify
  the visible comparison in the saved render. Follow §6 and §17.7 for sources,
  neutral labels and preserved response space. Text and image counts alone do not
  establish this check.

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

Moved verbatim to [`reference/13-design-tokens.md`](reference/13-design-tokens.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§13.x` reference in this skill and elsewhere still points there.


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

Moved verbatim to [`reference/15-course-scope.md`](reference/15-course-scope.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§15.x` reference in this skill and elsewhere still points there.


---

## 16. Restore, enhance, codes, agenda links (added 2026-10-15)

Moved verbatim to [`reference/16-restore-enhance-codes-agenda.md`](reference/16-restore-enhance-codes-agenda.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§16.x` reference in this skill and elsewhere still points there.


## 17. Lesson renewal standard (added 2026-10-16)

Moved verbatim to [`reference/17-lesson-renewal.md`](reference/17-lesson-renewal.md) on 2026-10-19. Read that file in full before any step this section governs. Section and subsection numbers are unchanged, so every `§17.x` reference in this skill and elsewhere still points there.


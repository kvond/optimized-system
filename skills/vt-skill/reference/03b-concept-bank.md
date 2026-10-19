<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

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

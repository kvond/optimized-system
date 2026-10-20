<!-- Part of vt-skill. Split from SKILL.md on 2026-10-19; updated with the October 17 learning-design requirements. -->

## 17. Lesson renewal standard (added 2026-10-16)

Katherine's specifications of October 16–17 for every lesson deck in Biology, Forensics and
A&P. They apply to new decks as they are built and to already-made decks through the
`renew-lesson-slides` skill, which runs this section on one deck or a batch. A deck is
not ready until §17.6 passes. When Katherine adds a specification, it goes here first,
with its acceptance check, and `renew-lesson-slides` picks it up from here.

Never write to a deck Katherine is editing herself. The Photosynthesis reference deck
(`1CVdbvDC20ZSShGPA9SLh018A54JnF0tkaRwzP75bJ1A`) is hers: read it, never write it.

### 17.1 Morphemes: a word-part slide at the start of each lesson

- **One new morpheme per lesson**, building across the course; earlier ones may recur.
  The breakdown goes near the start of the lesson, so it supports what follows.
- **The activity:** a vertical stack of individually movable, pale word-part cards,
  with a second column of distinct meaning targets. Leave enough room to drag a card
  without covering a neighbour. Below that, separate pale construction boxes for each
  word part, with plus signs between them; each word being built gets its own group.
  Never use a cramped line of underscores.
- **Directions, word for word, on two lines:**
  `Move each word-part card beside its meaning.`
  `Then combine the parts to build the two words asked for from this lesson.`
- **Questions** are short, concrete and connected to the lesson, at the students'
  level, for example "Make a word that names a process." and "Make a word that
  explains where that process takes place." Avoid abstract framing (process versus
  pigment) before students have the words.
- **Science must be right.** Verify word parts against a dictionary or science
  reference, and keep the sources outside the deck. Example correction: chloro- +
  -phyll builds chlorophyll (the green, light-absorbing substance); "where the
  process takes place" needs -plast and builds chloroplast.
- **Speaker notes hold the key and nothing else:** just the answers, e.g.
  `photosynthesis; chloroplast` plus the matching pairs. No "Answer key:" label, no
  sources, no directions.
- **Unscored.** No marker codes, counts, participation requirement or homework for
  morpheme activities.

### 17.2 Definitions: own words, then a mind map

- `Define these in your own words` comes **after** the morpheme activity, never
  before it. Keep a later practice or reveal slide where it already sits; do not move
  every vocabulary slide to the front. Reveal answers only after students attempt.
- **Mind map after the definition slide:** give the lesson's word list as movable
  word boxes, with room on the slide for students to arrange them and draw connecting
  lines. Unscored, like 17.1.

### 17.3 "Relates to me": every personal-connection page

Every "Relates to me" / personal-connection page in every lesson, all of them per
deck, not a sample:

- A `PERSONAL CONNECTION` label and a clear `Relates to me` title.
- The lesson's real critical aspects in distinct pale cards with teal top borders and
  numbered badges, side by side or stacked, keeping type readable.
- A separate pale green prompt panel: `Pick ONE. In your own words, how does it
  connect to you — your body, your food, your home, someone you know, or something you
  have wondered about?`
- A large, editable, pale response panel with a contrasting `YOUR RESPONSE` header
  strip and generous margins.
- Footer: `There is no right answer here. Write what is true for you.` No answer key.
- **Scored as Notes.** One response-bound `[[NOTES:CYCLE:ID]]` using the deck's
  existing stable ID. If the response has `[[OPTIONAL:CYCLE:ID]]`, convert it (e.g.
  `OPTIONAL:C05:OPT-RELATES` → `NOTES:C05:OPT-RELATES`), move it in the slide-one
  inventory from OPTIONAL to NOTES, and reconcile the counts. Never two codes for one
  response (§16.3).

### 17.4 Links: every link works before the deck is ready

Open every link on every slide and in the speaker notes: lesson material, videos,
interactives, `/copy` and form links. Fix or replace each broken one. A link that
cannot be fixed is listed for Katherine with its slide number. Run
`scripts/deck_link_check.py` as well, but it does not replace opening the links.

### 17.5 Sharing: AI duPont High School, viewer

Every lesson deck is shared with the AI duPont High School domain as **viewer**.
Check it, and set it if needed, without removing any existing access. Never make a
deck public, and never give edit access to the domain.

### 17.6 Renewal checks: a deck is ready when all of these pass

1. Introductory morpheme breakdown near the start; movable practice before own-words
   definitions, followed by the mind map (17.1, 17.2). Preserve a verified later
   practice/reveal placement; do not move all vocabulary work to the beginning.
2. Word parts, questions and keys are scientifically right; keys hold answers only.
3. Cards and boxes are editable and movable, at native size, with nothing clipped or
   colliding (render and look, §11 check 5).
4. Every "Relates to me" page matches 17.3; NOTES codes, inventory and counts
   reconcile; `deck_lint.py` is clean (§11 check 9).
5. Every link opens (17.4), and sharing is domain viewer (17.5).
6. Original content, media, unrelated codes, student work and grades are unchanged.
   Slide-number references still point where they say (§11).
7. A saved readback of the changed slides. Report exactly what was checked, never a
   whole-deck pass from a partial look.
8. Visual reasoning, response mode, consecutive-writing review and
   before/during/after-discernment titles pass 17.7 on every relevant slide.
9. Provisional day divisions pass the 90-minute activity-aware review in 17.8.
10. Report reviewed-deck readiness separately from classroom release. A lesson is
    not complete until the authorized Agenda and Schoology link checks in 17.9
    are verified; a deferred release stays explicitly open.

### 17.7 Visual reasoning, response mode and titles

These rules apply to initial lesson construction and retrospective renewal in all
three courses. The [initial-build additions](https://answerableteaching.slack.com/archives/C0C8YU5RDDM/p1792045219351809)
and [renewal additions](https://answerableteaching.slack.com/archives/C0C8YU5RDDM/p1792161778598399)
record Katherine's October 17 requirements.

- **Show the thinking.** Represent relationships visually, place comparison cases
  side by side, show change with sequence/arrows/before-and-after states, and make
  mechanisms visible. Reserve most text for questions, assertions, labels and
  response directions. Ask whether a student could recover the central
  relationship if most of the prose disappeared; if not, improve the representation
  before final QA. In Anatomy, each picture must have an intellectual job: locating,
  comparing, labeling, tracing or connecting structure to function when appropriate.
- **Choose the response mode on every student-response slide:** writing,
  annotation/manipulation of the representation, or a short combination. Prefer
  annotation/manipulation for noticing, locating, comparing, change/invariance,
  sequencing, connecting, tracing flow, selecting evidence, pattern/pattern-break,
  structure/function and mechanism. Use writing for explanation, justification,
  generalization, rule-building, synthesis and transfer when marks alone cannot
  express the thinking. An existing textbox is not a reason to retain that mode.
- **Review every run of two or more writing slides.** Deliberately retain writing
  when it best expresses the thinking; otherwise improve the sequence, for example
  mark/notice → connect/trace → write the rule/explanation. Do not change modes
  merely for variety.
- **Directions name the action and target.** Examples: circle the part that
  changes; box what stays the same; trace the flow of matter; connect structure to
  function; number the steps; mark where the pattern breaks; underline evidence
  and connect it to the claim. Prefer acting on the scientific representation
  itself over a detached response box. Avoid vague “annotate this” directions and
  directions that give away the answer.
- **Before discernment:** title the question, phenomenon or contrast without
  revealing the answer or conceptual assertion.
- **During discernment:** provide visual evidence and a meaningful student
  response. Do not reveal a conclusion merely to make every title a claim.
- **After discernment:** use an Alley-style sentence assertion naming the full
  conceptual takeaway, supported by the visual evidence. Explanation, synthesis and
  return slides use this form. On an annotated explanation slide, the title is the
  claim and annotations supply its evidence/reasoning. The final return crystallizes
  what the variation made visible rather than merely repeating an answer.

Preserve existing response bindings, marker identities, student work and grading
policy. A visual response is not proof that the current text-reading pipeline can
assess it. Record any parser/response-evidence gap for review rather than dropping
an existing scored response, inventing codes or claiming ingestion from layout.
Morpheme, definition and mind-map practice remains unscored; personal-connection
Notes treatment remains governed by 17.3.

### 17.8 Provisional DAY 1 / DAY 2 / DAY 3 divisions

Place teacher-adjustable day dividers at coherent conceptual boundaries, not equal
slide counts. Each proposed day must plausibly fill a **90-minute class**, including
its linked labs, investigations, guided notes, manipulatives, videos, discussion and
other companion work.

Before placing a divider, inventory that stretch of slides and attached activities.
Review the load qualitatively: direct instruction, annotation/manipulation,
discussion, transitions/setup, substantial activity time, cleanup and synthesis.
Avoid a thin day of a few slides beside an overloaded day. Keep a question with its
response/reveal, a manipulation with the synthesis it supports, and mechanism
sequences intact. Introduce an activity before students do it and preserve time for
the activity and its immediate sense-making. Dividers are pacing recommendations
for Katherine to adjust; they do not authorize date or assignment-setting changes.

### 17.9 Finalization and classroom links

Use this order within the existing authorized release scope and current ownership:
deck pass → rendered/saved readback and link/sharing checks → live deck and
student-copy links in `Agenda 26-27 CLEAN` → corresponding Schoology lesson/material
links. Follow §16.4–16.5 for exact lesson/source identity, existing-link conflicts,
preserving originals and saved readback. Distinct lessons retain distinct sources
and Forms even when they share a week or folder.

Verify final destinations from the school account. Do not change dates, pacing,
grades or assignment settings during the link pass. Respect Katherine's current
School Claude handoff for Schoology; prepare the exact reviewed targets and report
the remaining owner action rather than starting a competing writer. Pilot acceptance
and bulk-dispatch gates remain in `renew-lesson-slides` and
[issue #33](https://github.com/kvond/optimized-system/issues/33). A reviewed
draft, passing linter or completed plan is not a released lesson: keep any unverified
Agenda/Schoology transition open, and archive nothing before verified relinking.

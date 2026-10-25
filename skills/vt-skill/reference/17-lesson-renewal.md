<!-- Part of vt-skill. Split from SKILL.md on 2026-10-19; updated with the October 17 learning-design requirements. -->

## 17. Lesson renewal standard (added 2026-10-16)

Katherine's specifications of October 16–20 for every lesson deck in Biology, Forensics and
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
8. Visual reasoning, comparison-picture coverage, response mode, consecutive-writing
   review and before/during/after-discernment titles pass 17.7 on every relevant
   slide. Verify the actual pictures in the saved render, not just their count.
9. Provisional day divisions pass the 90-minute activity-aware review in 17.8.
10. Report reviewed-deck readiness separately from classroom release. A lesson is
    not complete until the authorized Agenda and Schoology link checks in 17.9
    are verified; a deferred release stays explicitly open.
11. Every slide type has the clear, course-appropriate student-facing wording
    review in 17.10. Record exact coverage and inspect saved renders of changed
    slides; a few improved core questions do not establish a whole-deck pass.

### 17.7 Visual reasoning, response mode and titles

These rules apply to initial lesson construction and retrospective renewal in all
three courses. The [initial-build additions](https://answerableteaching.slack.com/archives/C0C8YU5RDDM/p1792045219351809)
and [renewal additions](https://answerableteaching.slack.com/archives/C0C8YU5RDDM/p1792161778598399)
record Katherine's October 17 requirements.

- **Pictures for differences and contrasts (October 20):** in initial deck setup
  and renewal, inspect every VT slide that asks students to compare or discern a
  difference. If pictures illustrating that contrast are absent, add them. Retain
  useful existing pictures; decoration and icons do not count as comparison
  evidence. Put the cases side by side with comparable size, crop and placement
  so the intended feature is visible without introducing unrelated differences.
  Keep labels neutral until students attempt the question and preserve editable
  response space. Use the sourcing, attribution and visual checks in
  [§6](06-images.md). This is required even when the comparison is on a question
  slide. [Katherine's request](https://answerableteaching.slack.com/archives/C0C8YU5RDDM/p1792509885252479).
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

### 17.10 Clear student-facing wording on every slide

Apply this during new-deck origination and finishing, and when renewing this year's
existing Biology, Forensics and A&P decks. Katherine's [wording request](https://answerableteaching.slack.com/archives/C0C8YU5RDDM/p1792514789742109)
and [all-slides, all-decks clarification](https://answerableteaching.slack.com/archives/C0C8YU5RDDM/p1792516114272639)
cover every slide type, not just the 5 core questions. Her Body Tissues example
shows the desired outcome: necessary conditions in short sentences, followed by
one clear ask at a time.

- Inspect titles, explanations, case/data labels, directions, questions and
  response prompts. Use language suited to the course, topic and students; retain
  scientific terms students are learning and clarify an unfamiliar term when the
  task needs it. Leave wording that is already clear alone.
- State the situation and necessary conditions before the question. Name the cases
  and what changes or stays the same explicitly. Break stacked clauses and several
  embedded asks into short sentences or a short numbered sequence, preserving their
  order and relationships. Directions name the action and target.
- Preserve the scientific point and reasoning demand: prediction, comparison,
  explanation, justification, rule-building and transfer remain the same tasks.
  Keep variable/invariant conditions and the limits of a model or inference.
  Do not replace an explanation with a recall question, add grading criteria, or
  give students the conclusion they are meant to discern. A clearer question must
  remain neutral before discernment (17.7).
- For example, instead of “Which should allow faster diffusion? Explain which one
  condition changes,” state the actual comparison: “The barriers differ only in
  thickness. A is 1 unit thick. B is 2 units thick. [Keep the source's other stated
  conditions.] Which lets gas through faster? Then name the one difference.” The
  bracketed instruction is for the author, never text to paste into a deck. Do not
  copy example facts or proposed answers into an unrelated lesson.
- For an existing deck, read the current source before editing; Katherine may have
  already simplified it. Make object-precise changes only where needed. Preserve
  answer keys, teacher notes, media, response space, stable marker strings and
  response bindings. Keep source-original and student work intact. Record the
  slide/object ID, before/after wording and reason for each change; use a fresh
  revision guard, saved readback and changed-slide render QA.

For a retrospective batch, keep one writer per exact deck and independently review
one concrete wording pilot per course before expansion. This narrow wording review
does not replace the full renewal pilot/Claude review or classroom-release gates.
Track decks and slides audited, edited, unchanged, deferred and unavailable
separately. Protected teacher-edited decks remain deferred; uncertain lesson/source
identity remains unresolved rather than being inferred from a title or week.

### 17.11 Audit-first, course-specific renewal and paper revisions (2026-10-25)

Source: Katherine's direct October 25 lesson-renewal instructions, consolidated
in her 14:11 UTC request for a systematic checklist and usable teaching outputs,
with the same-day follow-on scope, alignment and access clarifications below.
This dated clarification supplements §§17.1–17.10; it supersedes conflicting
digital-revision defaults only for explicitly authorized paper-revision lessons,
beginning with Biology C08. It does not retroactively change distributed copies,
C02–C07 assessments, student work, grades or delivery history.

**Audit before editing.** Read the actual source deck, companion resources and
teacher notes in order. First produce a slide/object-specific defect list covering
logic and transitions, scientific accuracy, completeness, text density, visual
evidence and editable response space. Audit NGSS alignment, needed vocabulary and
the expected reasoning demand before editing; preserve the intended demand rather
than substituting recall or inventing standards coverage. Distinguish a verified defect from an
unresolved teaching decision. Fix authorized defects rather than pasting audit
language, repair instructions or internal status into the teaching body. Keep the
existing one-writer claim and revision guards; this rule grants no new access,
publishing or grading authority.

**Course-specific sequence, not one template for all courses.**

- **Biology:** plan the opening lab/investigation for approximately 30 minutes
  within a 90-minute lesson, including realistic setup and cleanup. For C08 use
  case → organelle evidence → student noticing → huddle; the teacher records or
  consolidates ideas only after students offer them. For other Biology lessons,
  use the relevant biological evidence rather than forcing an organelle case.
  Keep the whole 90-minute plan explicit, including discussion, transitions and
  synthesis; the lab is not an additional 30 minutes outside that total.
- **Forensics:** write for grades 11–12. Build a 90-minute case sequence with an
  initial position/vote, evidence-based debate, further evidence and a revisit of
  the original position. Preserve uncertainty and alternative interpretations.
  Do not impose Biology's lab-first or organelle format.
- **Anatomy:** the original-source deck remains the backbone in its original
  order (§16.1). Map every original slide, image, diagram, video, table and linked
  activity to its retained location. VT questions and active review add to that
  source, never replace it with a shortened reconstruction. Counts alone do not
  establish coverage; inspect each original element.

**Rolling scope and observation material.** Maintain the renewal/preflight window
of two lessons ahead and one lesson behind the current teaching point, using the
verified lesson sequence rather than guessing from filenames. Queue respiration
for its future place in that sequence; this clarification is not an instruction
to redo it immediately. Observation cases and images support classroom talk and
noticing. They are not automatically new student assignments or a generic
optional activity; preserve their actual instructional purpose and create no
submission or grading requirement without authorization.

**Support material serves the next question (clarified 2026-10-25, 22:52 UTC).**
Katherine's instruction to make this rule canonical refines the existing
pre-review requirement, not the course-specific sequences above. In Biology,
place the relevant clinic/case/organelle reference near its corresponding
reasoning question rather than collecting references into large standalone
blocks. Reference and noticing slides support looking and discussion; they are
not automatically extra activities, submitted answers or graded assignments.
The observed sequence is rough-ER reference → smooth-ER reference → prerequisite
review → reasoning question. Use that relationship, not those organelles, when
the next question concerns different content.

Immediately before every instructional question, place active, editable review
that rehearses precisely the prerequisites needed for that question. Students
notice, sort, label, compare, move or trace as appropriate; a passive summary,
a generic activity or review elsewhere in the deck is insufficient. Do not
manufacture extra assignments or reveal the reasoning answer. Retain existing
unscored practice and scored-response distinctions, with no new participation
marks. Acceptance: in the ordered native outline and saved render, identify each
question's relevant nearby support and immediately preceding prerequisite
review, and verify that reference/noticing slides gained no submission demand.
Inspect every actual answer slide for its existing response-bound embedded code
and reconcile the inventory under §16.3 and the paper-only override below;
do not add assessment codes to reference/review slides merely because they exist.

**Resources and teacher delivery.** Use readable 18-point icon/resource-link
labels and verify the actual target, including resources enhanced with Google's
tools. Enhancement is not evidence of accuracy, accessibility or useful placement.
The existing per-lesson teacher pack must explain purpose, background, teacher and
student actions, transitions, grouping plans and directly usable print links.
Put delivery guidance in the appropriate speaker notes and teacher pack, not
student-facing repair prose. Preserve §17.1's answer-only morpheme notes. Review
the pack against the final deck order; it must be usable to teach, not just an
audit or a list of links.

**Paper-only revision override and C08 processing gate.**

- For the authorized Biology lesson, remove digital second-answer boxes,
  revision-prompt speaker notes and paper-revision reminders from the deck.
  Preserve the original first-answer NOTES and BANK fields. Keep the revision
  questions/identities in the teacher pack and give each lesson its own separate
  Schoology paper-revision assignment; never borrow another lesson's assignment.
- For new C08, remove only the authorized DRAFT bindings
  `CA1-MASTERY`, `CA2-MASTERY`, `WHATIF`. Reconcile the one readable
  first-slide inventory shape to the actual retained codes, with
  `DRAFT=0 DRAFT_IDS=-`; do not leave an inventory only in speaker notes.
  The currently reviewed C08 counts are NOTES=17, OPTIONAL=1, BANK_TERMS=7;
  verify those counts and exact IDs against the saved source, not this prose alone.
- Preflight the actual downstream behavior before release: digital revision is
  not applicable (`None`), never a zero or three missing responses. Use the exact
  digital NOTES-only mapping and separate paper-revision mapping/evidence;
  verify that absence handling cannot generate a digital revision zero.
  A paper teaching-readiness role does not establish assessment compatibility.
- Verify a supported feedback path for the intended first-answer/paper evidence.
  The existing DRAFT-dependent feedback route is not automatically compatible.
  Do not fabricate DRAFT evidence, restore removed boxes to satisfy a parser,
  bypass a hold or claim end-to-end readiness from marker counts alone. Route an
  integration gap to the existing Teaching Hub owner; keep release status explicit.

**Access clarification (2026-10-25).** §17.5's default remains: preserve existing
access unless explicitly authorized otherwise. An explicit user grant to restrict
the exact lesson materials to district-only access permits removal of public
`ANYONE` access while preserving the owner and named collaborators; verify the
intended district viewer permission and read back the result. Do not infer that
grant from this checklist or remove other permissions. Purchased materials must
not be made public; use their authorized access and licensing conditions.

**Final evidence and usable outcome.** Re-read the final ordered native outline,
render the saved changed slides and inspect the whole instructional sequence.
Check scientific content, original-element coverage, density, visuals, editability,
speaker notes, teacher-pack usability, all links, intended-account access and
Teaching Hub processability. Apply §17.9's existing Agenda/Schoology release order
and permissions. Report each defect as fixed with exact saved/render/readback
evidence, still open with its repair owner, or awaiting a specific user decision.
Do not report a plan, linter pass, partial sample or draft link as a released,
processable lesson.

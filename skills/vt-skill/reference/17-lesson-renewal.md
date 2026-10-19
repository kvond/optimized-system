<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

## 17. Lesson renewal standard (added 2026-10-16)

Katherine's specifications of 2026-10-16 for every lesson deck in Biology, Forensics and
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

1. Morpheme slide at the start, then the activity, then own-words definitions, then
   the mind map, in that order (17.1, 17.2).
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

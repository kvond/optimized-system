<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

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

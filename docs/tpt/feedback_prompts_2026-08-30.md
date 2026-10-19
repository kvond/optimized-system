# Feedback prompts — paste these into your AI

*Marker version · replaces prompts 1 and 2 · revised 30 August 2026*

---

## Read this first: what is actually markered today

[This section is new, and it is here because the rest of the document describes a
system the decks do not yet carry. Checked against all 24 finished decks on
30 August:]

| Marker | Found | Design expects |
|---|---|---|
| `MARKER-INVENTORY` | 2 decks — Cycles 02 and 03 | all 24 |
| `NOTES` | 30 across all decks | roughly 15 per deck |
| `DRAFT` | 6 | roughly 3 per deck |
| `OPTIONAL` | 4 | 2–3 per deck |
| `BANK` | **none, in any deck** | one per Concept Bank term |

[So Prompt 1 and Prompt 2 will return nothing for 22 of the 24 cycles, and the
Concept Bank cannot be scored anywhere, because nothing marks it. This is not a
prompt problem and rewriting the prompts will not fix it — the markers have to be
embedded in the decks first. Until that happens, these prompts work on Cycle 02
and Cycle 03 and nothing else.]

---

## Two scores, read off hidden markers

Every student writing box in the deck carries an invisible tag naming *which
question it is* — not which slide it sits on. Answer types move around between
decks; the tags don't, so one prompt reads any cycle and the NOTES score and the
DRAFT score can never be read off the same boxes by mistake.

## What the markers mean

Every tag reads `[[KIND:CYCLE:QUESTION-ID]]`. No slide numbers anywhere.

**`[[NOTES:C02:CA1-MASTERY]]`** — an in-class writing box, including the *first
answer* on a response slide. These are the NOTES formative.

**`[[DRAFT:C02:CA1-MASTERY]]`** — the *revised answer* to that same question —
same id, so the pair survives any reshuffling. These, and only these, are the
DRAFT summative.

**`[[OPTIONAL:C02:OPT-SQUID]]`** — optional challenge and "relates to me" boxes.
Reported as bonus, never scored.

**`[[BANK:C02:niche]]`** — one Concept Bank term. The whole bank counts as a
single NOTES item.

[A note on this one, because it caused a real deletion. Section 3b of
`vt-skill` says the Concept Bank "carries no slide-type marker from section
7". Section 7 markers are the diagnostic strings — `Pattern break`, `Getting
Started` and so on — and a `[[BANK:…]]` tag is not one of those; it is a grading
marker like `[[NOTES:…]]`. The two rules do not conflict, but they read as though
they do. On 30 August, fourteen `[[NOTES:C02:CA1-MASTERY]]` tags were stripped
from Cycle 02's bank cells — correctly, since they were the wrong kind, copied in
from a response slide — but nothing was put back in their place. The bank needs
`[[BANK:…]]` tags, one per term, and has none.]

**`[[MARKER-INVENTORY…]]`** — on slide 1. Lists this deck's cycle, its totals,
and every question id it should contain — so a deck the AI half-read shows up as
a mismatch instead of as a low score.

**This cycle (C02):** NOTES out of 15 (14 response boxes + the Concept Bank),
DRAFT out of 3 — CA1-MASTERY, CA2-MASTERY, WHATIF-DECOMPOSERS — and 2 optional
boxes unscored. Later cycles carry their own totals in their own inventory line;
the prompts don't need editing for them.

[Corrected from 3 optional to 2. `OPT-THENANDNOW` was still listed after the
Then and Now slide was deleted on 29 August.]

---

## Prompt 1 — Completion check

Fills your ROSTER & SCORES sheet. Two independent numbers per student.

---

I am a high school teacher. I am attaching student slide decks from one lesson.

The decks contain hidden text markers that tell you which boxes to read. A marker
sits immediately above the box it names, in the text of the label. Every marker
reads `[[KIND:CYCLE:QUESTION-ID]]` — for example `[[NOTES:C02:CA1-MASTERY]]`.
Find them by that literal bracket form:

- **NOTES** — the student's in-class writing box, including a first answer
- **DRAFT** — the student's revised answer, written after working with an AI
- **OPTIONAL** — optional work
- **BANK** — the Concept Bank header, and one marker per term
- **MARKER-INVENTORY** — on slide 1: this deck's cycle, its totals, and every
  question id it contains

The text belonging to a marker is the student writing that follows it, up to the
next marker.

Identify every box by its marker, never by slide number or page position. The
same question appears at different points in different decks, and slide order
carries no meaning here.

Before you score anything, read the MARKER-INVENTORY line and use its NOTES and
DRAFT totals as your denominators. Check the question ids you actually found
against the id lists in that line; if any are missing, say which, for that
student, before you give a number. If you cannot find the inventory line at all,
say so and do not guess.

For EACH file, give me one table row:

1. Student name, from the file name.
2. **NOTES SCORE, 0 to 10.** Look ONLY at NOTES markers plus the Concept Bank.
   Count how many carry writing in the student's own words — not blank, not the
   printed question, not the word bank, not the placeholder text. Count the
   Concept Bank as ONE item, credited if at least two thirds of its terms are
   defined in the student's own words. Score = that count divided by the NOTES
   total, times 10, rounded to a whole number.
3. **DRAFT SCORE, 0 to 10.** Look ONLY at DRAFT markers. Never let a NOTES box
   contribute to this number, even when it sits on the same slide. Same
   arithmetic against the DRAFT total.
4. **OPTIONAL** — just list the question ids of the OPTIONAL boxes that have
   writing. No score.
5. **FLAG** — only if a NOTES answer is word-for-word the printed slide text. Do
   not flag weak grammar, short answers or unusual phrasing; those are not
   evidence of anything.
6. One short quote of the student's own words from a DRAFT box.

Do not score correctness. These numbers measure how much of the deck the student
filled in, nothing else. Do not rank students. Do not rewrite anything. Do not
include the markers themselves in any quote.

---

## Prompt 2 — Growth Reports

Only the opening paragraph changes from your current Prompt 2. Everything after
"Write ONE report per student" stays exactly as you have it.

---

I am a high school teacher. I am attaching student slide decks from one lesson.

The decks carry hidden text markers naming each student writing box. Every marker
reads `[[KIND:CYCLE:QUESTION-ID]]` — for example `[[NOTES:C02:CA1-MASTERY]]`. A
marker sits in the label immediately above its box, and the writing that follows
a marker, up to the next marker, is what belongs to it:

- **NOTES** — written in class, before instruction. This is the student's first
  thinking.
- **DRAFT** — written after the student worked with an AI that questioned them.
  The revision.
- **OPTIONAL** — optional work, only mention it if there is writing there.
- **BANK** — a Concept Bank definition.

A NOTES and a DRAFT sharing the same QUESTION-ID are the same question, before
and after. Pair them by that id — never by slide number, never by position on the
page. The same question sits at different points in different decks, so page
order tells you nothing.

"Where my thinking started" comes from NOTES. "How my thinking changed" and every
quote in "Evidence from my final answer" come from DRAFT. Never quote a marker
itself, and never quote a NOTES box as if it were the revision.

Give one Current understanding line per DRAFT question id in the deck, and name
the id you are judging.

If a marker's box is empty, say that box is empty rather than filling it in.

---

The over-20-decks compiling paragraph also gets simpler — replace "list every
question in the deck" with: for every NOTES / DRAFT pair sharing a question id,
give the id, the slide title, the NOTES text copied exactly, and the DRAFT text
copied exactly. Question ids are also what lets Prompt 3 line students up against
each other when the decks aren't identical.

---

## What the student runs, and where it lives

*Revised 30 August 2026. This is the prompt in the speaker notes of every
response slide and every What if slide — 77 slides across the 24 decks. It is
reproduced here so the teacher-facing document and the student-facing note say
the same thing.*

The `QUESTION:` line is filled in per slide with the question that slide actually
asked, so the student is not asked to retype it.

---

REVISION PROMPT — Open an AI and copy and paste the following:

QUESTION: *(the question that slide asked)*

`-----`

[PASTE IN YOUR FIRST ANSWER]:

`-----`

I am a high school student. Below is a science question and my first answer. Do
NOT rewrite my answer and do NOT give me the answer. Instead:

1. Tell me one thing I got right, or was interesting.
2. Quote my own words back to me as You said, "".
3. Ask me two questions that make me look again at one idea I might have wrong or
   left out or could be made more complete.
4. Illustrate it with one distinction or example worth thinking about.

—-

Keep it short and in plain language, then stop so I can write my own revised
answer.

`-----`

Once you get your feedback: write your revised answer in "Your revised answer" on
the slide — in your own words.

---

[Two things in that prompt, neither changed without saying so. Your draft
numbered the items 1, 2, 2, 3; they are renumbered 1–4, which is the only
substantive edit. And item 2 ends with an empty pair of quotation marks — `You
said, ""` — which reads as the slot the AI fills. If it is meant to show the AI
the form of the quotation, it works; if a student reads it as a typo, adding an
ellipsis inside the quotes would remove the doubt.]

---

## Two things to check on your first run

Open one markered deck in presentation view and confirm you cannot see the tags.
They are 1pt grey at 6% opacity, sitting under the label text — visible if you
zoom to 400% in the editor, invisible to a room.

Ask the AI, once, to list the markers it found in one deck before you ask it to
score. If the count matches the inventory line, the pipeline is reading
everything. If it doesn't, the file didn't upload cleanly — and that is the
failure mode that otherwise looks like a student who wrote nothing.

[On current coverage that check will fail on 22 of 24 decks, and it will fail for
the right reason: the markers are not there. Running it once on Cycle 02 tells you
the prompt works. Running it on Cycle 12 tells you the embedding job has not been
done yet.]

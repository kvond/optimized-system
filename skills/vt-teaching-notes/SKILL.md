---
name: vt-teaching-notes
description: Write the "VT Questions Teaching Notes" Google Doc for one VT deck (Biology, A&P or Forensics) and save it in that lesson's week/cycle folder, so Katherine can review the lesson's critical aspects, invariant, substitution test, dependencies, slide types, simultaneity and visibility before class. Reads the live deck; never edits it. Use for one deck, or as a sweep over a course (Biology first, then A&P, then Forensics). Triggers - "teaching notes", "VT questions teaching notes", "explain the VT questions", "notes for this lesson", "teacher notes doc".
---

# VT Questions Teaching Notes

Katherine's request, 2026-10-20 (#vt-decks): every lesson gets a teacher-facing doc that
"goes over the critical aspects, the object of the order and VT questions and explains
concepts", added to each week per lesson. Course order: Biology, then A&P, then
Forensics. With the decks done, she reviews these before class.

**Reference example** (Katherine's, A&P Week 07 Body Tissues):
[VT Questions Teaching Notes](https://docs.google.com/document/d/1jQRWW8vYGWcpU8ok6XE7wvvbRMOk2AV7IAm2xRVsq0U/edit),
ID `1jQRWW8vYGWcpU8ok6XE7wvvbRMOk2AV7IAm2xRVsq0U`. If this file and the example
disagree on form, the example wins.

This skill reads decks and creates or refreshes one doc per lesson. It changes no
deck, Agenda cell, Form, grade or student file. Katherine's October 20 follow-up,
"use these better questions for teaching notes", authorizes refreshing existing notes
from the approved clearer questions; use the current vt-skill §17.10 wording rule.

## 1. Find the lesson and its deck

- Resolve the lesson from Master Agenda `Agenda 26-27 CLEAN`
  (`1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY`): course tab, week, lesson name,
  teacher deck link. Use the `🔗 Lesson names` tab to match names across the Agenda,
  folders and decks. Never match on week number alone (A&P folders run one week
  behind the Agenda from Cell Structure on; Forensics one week ahead from Mock Crime
  Scene on).
- Biology deck IDs: `docs/decks_live_ids.csv`. A&P from Week 8 on: the original-first
  merged deck (vt-skill §16.1), not the old VT-only deck.
- One doc per lesson. Two lessons in one week folder get two docs.

## 2. Check before writing

Search the target folder for a doc whose title starts `VT Questions Teaching Notes`.
If one exists for this lesson, do not create a second. Report it, and update it only
if Katherine asked for a refresh, including the October 20 clearer-question refresh.
Preserve Katherine's additions and revise only the affected question explanations
and references; do not replace her document wholesale. If her edits and the proposed
correction conflict, retain her text and identify the specific decision needed.
Reconcile the current School Claude handoff and exact document writer claim before
writing; an unresolved overlapping claim stays on hold.

## 3. Read the deck

Read the whole live deck, speaker notes included where the connector shows them:
slide 1 critical aspects, the teacher note slide (the seven declarations written by
`scripts/add_teacher_note.py`), each critical-aspect block, Contrast Set, Build a Rule,
Pattern Break, 3-Tier, What if, Concept Bank, activities, response slides and the
teacher slide index. Cite slide numbers as the deck stands today.

Use the latest verified saved clearer questions, including their comparison
conditions, for the question explanations and teaching answers. An approved wording
proposal that is not saved in the deck stays explicitly proposed; never describe it
as the current slide. Record the exact source deck ID, revision (or available
modified timestamp) and date read. If any slides or notes could not be read, name
the partial coverage rather than claiming a whole-deck review.

## 4. Write the doc

Title: `VT Questions Teaching Notes — <Cycle NN | A&P Wk NN | Forensics Wk NN> — <lesson title>`.
First line, italic: `Drafted by Claude from <deck title> on <date> for Katherine's review.`

Sections, in this order (the example's structure):

1. **Critical aspect(s).** The central idea, the key distinction, the science at a
   teacher's level, and the oversimplification the lesson is built to challenge.
2. **Invariant.** What stays the same so the one varied feature can carry the
   explanation, and why each held factor matters.
3. **Substitution test.** Which comparison isolates the cause and which only
   illustrates it, and why the deck keeps each.
4. **Dependencies.** What earlier cycles/weeks this lesson builds on and what it sets
   up next.
5. **Slide types.** The five core questions in order and the job each does in the
   progression; then the supporting activities, What if, Concept Bank and response
   slides. For each core question: a strong answer and the likely misconception.
6. **Simultaneity.** Which ideas students must hold together, with a worked strong
   answer.
7. **Visibility.** Private writing first, partner, teacher-chosen sharing; no
   readiness inferred from the week number.

Then **Science checks before you teach** (slide-numbered wording that is inaccurate or
would undercut a later cycle; omit the section if there are none), and
**How all seven points fit together** ending with "The most important idea is this: …".

Rules:
- Each "The teaching goal:" line says what students should be able to do.
- When the deck does not state a declaration, say so in bold at the top of that
  section ("The deck does not yet state an invariant."), describe what the slides
  actually do, and offer a wording for Katherine to decide. Never invent a
  declaration and present it as the deck's.
- Use only Katherine's constructs and terms (VT = Variation Theory). No new rubric
  criteria, scales or tallies.
- No student names, work or grades.
- Plain teacher prose; short paragraphs; no filler.

## 5. Save and verify

Create the doc as a native Google Doc in the lesson's week/cycle folder (school account
`katherine.vonduyke@redclay.k12.de.us` owns it; sharing is inherited from the folder,
not changed), or update the exact existing doc resolved in §2. Read it back: title,
folder, first line, all section headings, current question explanations and slide
references. Record the saved doc ID and the deck revision/date reviewed. Re-read
before each refresh; stop if another writer changed the affected text. A skill
commit alone does not prove the school task's saved prompt or live docs were updated.

## 6. Sweep (a course at a time)

- Claim the batch in #work-que before writing, one writer per course. Run the folder
  search in §2 immediately before each create, so a parallel or earlier run never makes
  a duplicate.
- Order within a course: the coming two weeks first, then forward through the year,
  then earlier weeks.
- Report in the request thread: one line per lesson (doc link, or the reason it was
  skipped: no deck, deck not yet merged, current doc verified, refresh held). State
  created, refreshed and partial coverage separately. Course and week only; no
  student details.

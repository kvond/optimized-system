---
name: student-feedback
description: Write students' lesson feedback and science-writing reports for Biology, Forensics and A&P in Katherine's approved formats, and render them as printable PDFs. Holds the canonical feedback prompt (Prompt 2), the rating scale, the class-by-class report layouts, the teacher-only flag rules and the renderer. The Master Agenda Feedback Prompts tab is Katherine's quick reference; this skill is the source. Use for any feedback or writing report on student work, a catch-up of lessons without feedback, or a question about which format a class uses. Triggers - "feedback", "writing feedback", "feedback on latest work", "catch up feedback", "science writing report", "which feedback format".
---

# Student feedback and science-writing reports

Katherine's request, 2026-10-20: the feedback prompt "should be a skill saved in
github and that page is just a quick reference for me", and the report models she
uses must be in the GitHub directions. This skill is that home.

- **Source:** this skill. Prompt 2 is in
  [reference/prompt-2-feedback-for-students.md](reference/prompt-2-feedback-for-students.md).
- **Quick reference:** Master Agenda `Agenda 26-27 CLEAN`, tab `Feedback Prompts`.
  When the two disagree, this skill wins. Change the skill first, then the items in
  that tab's "Update together" row: the Agenda Prompt 2 cell, the Answerable
  Teaching Manual (§12 and Appendices B and F, the feedback formats), the copyable
  prompts and the worked example.
- **Approved exemplars:** one per format, listed in the private Doc
  `Feedback exemplars — private locator`
  (`1vuhyFO_r9oKy2WwcWeLah3dj696MrTweTfxtPH9qIcM`). They are student reports, so
  they stay in Drive.
- **Who runs it:** the weekday [Spreadsheet feedback](../../prompts/school-spreadsheet-feedback.md)
  task, or any agent asked for feedback. The Teaching Hub does not write feedback.
  Packets, the yellow/white status colours and the IC check belong to that prompt,
  not to this skill.

This skill reads student work and writes report files. It never changes a grade, IC,
a Form, a deck or a student's original work.

## 1. Before writing anything: find what already exists

1. Resolve the class, the exact lesson and the student's exact submission from the
   Master Agenda, the `🔗 Lesson names` tab and the turn-in records. Never match on
   week number alone. Forensics folders and Forms run one week ahead of the Agenda
   from Mock Crime Scene on; A&P folders and Forms run one week behind from Cell
   Structure on; Biology Forms use Cycle numbers. A&P "Cell Structure" and "Cell Structure (continued)" are one
   grade but two lessons.
2. List the student's folder. If a report already exists for the same student,
   lesson, report type and reviewed submission, reuse it. Never save a second report
   for work that already has one. A newer file date does not mean newer work was
   read.
3. Check that no other agent holds a claim on the same student and lesson (see the
   ownership rule in the Spreadsheet feedback prompt). Two agents rating the same
   work produce conflicting reports in a student's folder.

## 2. Read the work

- Google Slides decks: Slides API `read_presentation`, then
  [scripts/answers.py](scripts/answers.py) to print the response slides. `.pptx`
  uploads: the Drive text reader.
- Student text sits at the `[[NOTES:…]]` / `[[DRAFT:…]]` markers ("Your first
  answer" / "Your revised answer"), bellringers and tables. Everything else is
  template. [scripts/unique.py](scripts/unique.py) compares decks of the same lesson
  and prints only the lines a student typed.
- An empty box is empty. A deck copy with no student text is reported as such.
- Forensics decks carry an AI revision prompt by design, so a more polished
  revision is expected and is not a flag. A revised box that holds the AI's
  feedback instead of the student's own revision is a flag: rate the first answer.

## 3. Rate

Follow Prompt 2. The essentials:

- Scale: **Beginning** names an idea, relationship missing or inaccurate ·
  **Developing** partly explains the relationship · **Proficient** accurately
  explains it · **Extending** uses it on a new case, distinguishes similar cases or
  names a limit. A blank or unreadable answer is **Evidence unavailable**, never
  Beginning.
- Critical-aspect names come from the deck. Do not invent, merge or rename them.
- Concepts before vocabulary. A correct term without the relationship is not full
  understanding. A clear explanation of a wrong relationship is Beginning.
- Rate the revised answer when there is one. Claim growth only from a genuine
  earlier submission, never from the first-answer box alone.

**Science writing** is a separate judgment from the critical aspects. Four areas:
science vocabulary, conceptual explanation, specific evidence, scientific
reasoning. For each area quote the student's exact words with where they came from
(slide/box), give the level, and write one or two sentences: what works and one
concrete next move. Plot one point per distinct reviewed piece; a piece not
reviewed is a gap, not a zero. Do not re-rate saved work just to redraw a chart.

## 4. Formats by class

Katherine supplied one approved exemplar per format on 2026-10-20 (see the private
locator above). The layouts below reproduce them, and
[scripts/render.py](scripts/render.py) draws them.

| Class | Lesson feedback | Science writing |
|---|---|---|
| Biology | `lesson_onepage` | `writing_bio`: page 2 opens with the big heading **10 pts summative extra credit**, then a writing challenge on the latest lesson |
| Forensics | `lesson_onepage` | `writing_cer` (the Forensics writing exemplar) |
| A&P | `lessons_grouped`: critical aspects organised under lesson names, **no more than three per lesson** | `writing_cer` |

- **`lesson_onepage`** (one page, Prompt 2 Step 4): class kicker, student's first
  name and last initial, lesson and submission date; 1 Your growth (one dot scale per
  critical aspect at its current level, Evidence unavailable shown as text with no
  dot, under the exemplar's line "A single report does not establish a growth
  trend"; like the exemplar, it does not plot earlier lessons); 2 How you did
  (two or three sentences in "you", quoting or paraphrasing the student); 3 One
  question to think about (one contrast question built on the student's own words)
  with writing lines; 4 What I understand now that I didn't before; 5 How I can
  improve my responses next time.
- **`lessons_grouped`** (A&P, two pages): page 1 lists each lesson as a band with up
  to three critical aspects, the current level and what the answer shows. Page 2:
  how my thinking changed (only when an earlier submission supports it; otherwise
  leave `thinking_changed` out and the page says no earlier submission is
  available), one question, evidence quotes with their slide, and reflection lines.
- **`writing_bio`** (two pages): page 1 lists the reviewed work (L1, L2…) and, per
  area, the prompt, level, lesson/date/code, the quote, the comment and a small
  chart. Page 2: **10 pts summative extra credit** in large type, the challenge
  title and task, writing lines and a discussion question.
- **`writing_cer`** (three pages): page 1 the four areas with source, level, quote
  and comment. Page 2 every submitted source (S1, S2… by date, each file once) and a
  2×2 grid of area charts. Page 3 CER practice on the latest reviewed lesson: one
  why/how question, three accurate facts from the lesson slides (practice
  information, never attributed to the student), and Claim / Evidence / Reasoning
  lines.

Data fields for each layout are shown in [examples/](examples/); the examples use
invented content only. Render one report:

```
python3 skills/student-feedback/scripts/render.py /private/scratch/report.json /private/scratch/out.pdf
```

Keep report JSON and PDFs in a private scratch folder outside any Git checkout:
they hold student names, quotes and levels, and the renderer refuses an output path
inside a checkout. It also stops with an error, rather than drawing a wrong page,
when a level is outside Katherine's scale, an A&P lesson has more than three
aspects, a writing report does not have four areas or one point per source, or the
PDF does not come out at the layout's page count (1, 2, 2 and 3 pages). The
renderer needs `reportlab` and draws charts as vector graphics, so a report is a
few kilobytes.

## 5. Teacher-only notes

Keep these out of every student page and out of Slack: pasted AI feedback, pasted
URLs, keyboard mash, copied web or slide text, near-identical answers between
students, shared partner decks, and identity or file anomalies. Record them in the
teacher-only growth record or notes beside the reports (Prompt 2 Steps 3, 5 and 6).
Authorship alerts reach a student only after Katherine approves the wording.

## 6. Files

Prompt 2 names a student feedback Doc. For the student reports, the PDF formats in
this skill are what gets filed and printed. The growth record and the class growth
summary remain teacher-only Docs, as Prompt 2 Steps 5 and 6 describe.

- One PDF per report, saved in the student's existing folder under the class
  records folder:
  `YYYY-MM-DD — Last, First — <Lesson> — Feedback.pdf` and
  `YYYY-MM-DD — Last, First — <Lesson> — Writing.pdf`, using the roster's exact
  name.
- Reopen each saved file and check its size and text. A failed filing step resumes
  from the saved file; it never triggers a new assessment.
- Student names, quotes and ratings never go into GitHub or Slack.

## 7. Before you say it is done

- Every student and lesson in scope has a report, an existing report reused, or a
  stated reason (no submission, blank deck, unclear identity).
- Aspect names came from the deck; quotes are exact; levels match across the
  student report and the teacher records.
- Teacher-only flags appear on no student page.
- Each PDF opened, has the expected page count and sits in the right folder.
- No grade, completion score, IC entry or original file changed.

---
name: formative-pipeline-v2
description: The v2 formative pipeline that replaces Workflow A→B1→B2→C. From one annotated deck per student, produce a printable Conceptual Growth Report (student) plus a class summary and agency coding (teacher); gradebook is completion-only and proficiency lives only in the report. Carries the student revision-coaching prompt (speaker notes), the teacher batch prompt, the integrity gate (copied or AI first answer → flag for teacher review; nothing auto-fails), the Growth Report standards (deeply positive, 9th-grade readable, no coding vocabulary to students; rubric key as page 2 of every report), and cross-unit rollups. Applies to Biology, Anatomy & Physiology, and Forensics. Triggers: "formative pipeline", "v2 pipeline", "run the growth reports", "batch the decks", "growth report run", teacher batch over annotated decks.
---

# Formative Pipeline v2 — Answerable growth-report flow (SKILL)

**Status:** authored 2026-08-07. Consolidated spec for the pipeline that **replaces
Workflow A→B1→B2→C**. Judgment layer lives here; `.py` stays dumb (deterministic
extraction only). Applies to **Biology, Anatomy & Physiology, and Forensics** (Forensics
keeps its case-first opener). Resolves the v2 PENDING INPUTS in the MANIFEST.

**One line:** from one annotated deck per student, produce one **printable Growth Report**
(student) and one **research/class output** (teacher) — grading is completion-only, and the
student's proficiency lives only in the report.

---

## The three outputs

1. **One artifact — the annotated deck.** Students answer on the slides. Each response slide
   has two stacked, labeled areas: **"Your first answer"** and **"Your revised answer."** The
   revision-coaching prompt lives in that slide's **speaker notes**.
2. **One summary — the Conceptual Growth Report.** Per student, printable, handed back.
   Two pages: page 1 the report, page 2 the rubric key (same key every time).
3. **One research output.** Class summary (proficiency spread, misconceptions, next
   instructional contrast) + agency coding + the cross-unit rollups.

---

## Student flow (in class + one day later)

1. In class, the student writes the **first answer** on the response slide.
2. They open the slide's **speaker notes**, copy the **revision-coaching prompt** (below) into
   their own AI, and use the feedback to think again — the prompt is built so the AI will
   **not** write the answer for them.
3. **The next A/B class**, they write the **revised answer** in the second area on the same
   slide. Both answers stay visible — seeing their own thinking change is the point, and they
   are told this.
4. The deck is submitted (Chrome-extension Drive upload, as now). No separate doc, no email.

### Revision-coaching prompt — goes verbatim in each response slide's speaker notes

```
You are my science learning coach. We are working on ONE question — the question on this
slide. Do not give me the answer. Help me make my own answer better.

1. Ask me to paste my first answer to the question on this slide, then wait.
2. Respond in this order, in plain language:
   - Name one specific thing I did well, and quote my own words back to me.
   - If any idea I wrote is original or interesting, tell me so and why it is worth developing.
   - Point to one place where my thinking is unclear or incomplete, and ask me ONE question
     that helps me see it. Do not tell me the answer.
3. Ask me to write my revised answer in the "Your revised answer" box on this slide, in my
   own words. Then stop.
```

---

## Teacher batch (over the folder of submitted decks)

Model routing: **Haiku** for deterministic extraction, **Sonnet** for report + coding judgment.
Class membership from the **Dashboard** (source of truth), never from filename/folder.

### Teacher batch prompt — goes verbatim in the Manual (run over the folder of student work)

```
You are my Answerable Biology feedback assistant. I will give you a class set of student work
for ONE lesson. Each student's work has, for every question, a FIRST answer (written in class)
and a REVISED answer (written the next class). Use only what the students actually wrote. Never
invent data; every quote must be a real substring of that student's own words.

Produce four things:

1) ONE CONCEPTUAL GROWTH REPORT PER STUDENT — printable, one student per page, then a second
page. Write it TO the student, in the first person, plain enough for a striving 9th-grader,
with no coding or grading jargon (never the words agency, epistemic, warrant, proficient, or
approaching). Sections:
   - Where my thinking started — my first idea, in plain terms.
   - How my thinking changed — the distinction or correction between my first and revised answer.
   - Evidence from my final answer — a verbatim quote of my own words that carries the change.
   - Current understanding — one bar per critical aspect in the lesson, plus one for Using
     Evidence and one for Explaining the Mechanism, each marked Getting Started, Working On It,
     or Mastery with a short colored bar. Never use Proficient or Approaching.
   - My next step — one doable move, framed as an invitation.
   - "What I understand now that I didn't understand before:" — leave this line blank for me.
   - An idea worth chasing (only if I wrote one) — name a genuinely original idea, even at low
     proficiency, and invite me to bring it to class.
   Every affirming line must be anchored to something I actually did — a verbatim quote or a
   named move. No generic praise. Proficiency is a place on a path, never a deficit.
   PAGE 2 of each student's report is the rubric key "What Good Thinking Looks Like" — append
   it unchanged.

2) ONE CLASS LEARNING MAP (for me only). A table, one row per student: name, the same bars,
growth (Yes / Partial / No), biggest misconception (verbatim), a copy/AI flag if any (see
integrity), and one interesting idea to follow up (verbatim). Then: class proficiency bars per
item; the 2–4 most common misconceptions, each with a count and one verbatim example; EVIDENCE
TOWARD THE PERFORMANCE EXPECTATION in NGSS terms — Conceptual understanding / Scientific
reasoning / Mathematical representation as Proficient / Approaching / Developing (the ONLY place
those words appear); and NEXT INSTRUCTIONAL MOVE — the single contrast to teach next, aimed at
the most common misconception.

3) AGENCY CODING (research, for my records only — technical vocabulary allowed here). For each
student, code their answers: presence (ENG / EPI / AUT / DEC / CAND); capability/warrant
(practical / interpretive / epistemic); generativity (does the idea open a distinction, a
shared misconception, or a testable case); provenance (student / AI / prompt / peer). Record a
verbatim excerpt for each code. Capability and generativity sit beside the presence code and
never change it — a wrong-but-original move still counts as origination.

4) A COMPLETION CSV — one row per student: name, and Completion (full credit when both a first
answer and a revised answer are present for the lesson). Completion is the only thing that goes
in the gradebook; never put quality or proficiency here.

INTEGRITY (first answer only; the revision is exempt, because students are told to use AI to
revise): if a student's FIRST answer looks copied or AI-written, add a flag to their row and
hold their report for my review. Do not auto-fail, do not lower any grade, and do not post
anything automatically. Copy/AI detection misfires most on English-learners and unusual
writers, so treat a flag as "look at this," not a verdict.

Begin by telling me how many students' work you received, then produce the four outputs in order.
```

The numbered steps below are the internal mechanics that back this prompt:

1. **Extract** — reuse the deployed deterministic extractor to pull, per response slide, the
   first answer and the revised answer. No new judgment here.
2. **Integrity gate (first answer only)** — see below. Sets each first answer to
   `clean | flag-copied | flag-ai`, visible to the teacher. A flag holds that entry for
   Katherine's review; nothing auto-fails and nothing posts automatically.
3. **Growth Report** — generate one per student from the two answers, under the report
   standards below. Deeply positive, plain, no coding vocabulary. **Append the rubric key as
   page 2** (`What_Good_Thinking_Looks_Like_student_handout.docx`) so every summary doc ends
   with the same standard.
4. **Agency coding** — code the answers into `Coding Master` (research rail; technical
   vocabulary allowed here only). Codebook per `16-agency-scan-SKILL.md`, refined:
   presence codes **ENG / EPI / AUT + DEC + CAND**; two axes recorded beside the presence
   code and **never gating it** — capability/warrant (practical / interpretive / epistemic)
   and generativity (does the idea open a distinction, a shared misconception, or a testable
   case — by what it opens, not by correctness); provenance (student / AI / prompt / peer).
   Verbatim excerpt only; SELF_CHECK before writing; append-only.
5. **Class summary** — proficiency spread, recurring misconceptions, the next instructional
   contrast to teach.
6. **Completion CSV** — the only thing that reaches Schoology (below).
7. **Cross-unit rollups** — update the accumulation layer and regenerate the two rollups.

---

## Integrity gate

- Runs on the **first answer only** — written in class, should be the student's own. The
  **revision is exempt**: students are told to run the coaching prompt through their AI, so
  "AI" in the revision is the design, not a violation.
- **Copied OR AI-authored first answer → flag for Katherine's review.** Nothing auto-fails and
  nothing posts automatically — the flag holds that entry and she decides. One outcome, human-
  reviewed: the simpler rule.
- **The detector never penalizes a student on its own.** Automated copy/AI detection misfires
  most on ESL and atypical writers, so a machine verdict is a prompt to look, not a judgment.
  Because the gradebook is completion-only, a flag costs at most a cycle's feedback, never a
  grade; a held entry that turns out authentic simply gets its Growth Report restored.
- Rationale: authentic feedback requires authentic work — a flag pauses feedback until a human
  confirms the work is the student's, protecting the feedback loop without ever auto-failing a
  real student for how they write.

---

## Growth Report standards (student-facing) — every report, no exceptions

**Structure (first-person, plain headers):**
- *Where my thinking started* — their initial idea, in plain terms.
- *How my thinking changed* — the distinction or correction between first and revised answer.
- *Evidence from my final answer* — a verbatim quote of their own words carrying the change.
- *Current understanding* — proficiency bars on the **Getting Started / Working On It /
  Mastery** scale (the settled student-facing labels; never "Proficient/Approaching," which
  live only on the teacher NGSS line). One bar per critical aspect on the slide, plus Using
  evidence and Explaining the mechanism.
- *My next step* — one forward, doable move, framed as an invitation.
- *What I understand now that I didn't before* — **left blank for the student to complete.**
- *An idea worth chasing* (when present) — names a generative idea, even at low proficiency,
  and invites them to bring it to class.

**Rules:**
- **Deeply positive AND true.** Every affirming line anchored to something they actually did
  (verbatim quote or named move). Proficiency is a position on a path, never a deficit. No
  generic or unearned praise — teenagers read that as fake and it buries the next step.
- **Understandable by them.** Written for a striving 9th-grader; plain, without dumbing down
  the science.
- **No coding vocabulary reaches the student.** No NGSS codes, no "epistemic," "warrant,"
  "agency," or proficiency jargon. That vocabulary lives ONLY on the research/teacher rail
  (two-rail split).
- **Print-friendly** — the teacher prints and hands it back.
- **Rubric key = page 2 of every report [HARD].** Each student summary doc is two pages:
  page 1 = their Growth Report; page 2 = the **"What Good Thinking Looks Like" rubric key**,
  the same key every time. The key shows the three student-facing rubrics — **Conceptual
  Accuracy · Using Evidence · Explaining the Mechanism** — on the Getting Started / Working On
  It / Mastery scale, plus "what I never grade you down for" (length, grammar) and the "use
  your own words" note. Canonical file: `What_Good_Thinking_Looks_Like_student_handout.docx`.
  Students always read their report against the standard. The three rubric names are the
  **on-spec trio** — never "Scientific Writing Quality" or "Depth of Explanation," which imply
  writing or length is graded (it is not).

---

## Cross-unit rollups

An accumulation layer keyed by **student × cycle** (fed by the per-cycle reports + the
append-only `Coding Master`, re-collecting nothing) produces:
- **Student year-arc** — "how your thinking has grown across the year," under the same
  positive + readable rules; a longitudinal companion to the per-cycle report.
- **Course-level trend** (teacher) — recurring misconceptions, and agency + capability moving
  across the 20 cycles / four marking periods.

---

## Gradebook = completion only [HARD]

- Schoology records **completion**: both answer areas filled = done. Never quality.
- Completion CSV reuses the repurposed Workflow A completion logic; header `DRAFT.<Lesson>`
  (or `Notes.<Lesson>` per the existing gradebook column), one row per student.
- All proficiency/growth lives in the Growth Report, never the gradebook.

---

## Invariants that must not drift

- **Two-rail split** — technical/coding vocabulary never appears in a student report; only on
  the research rail.
- **Presence, not quality, for the agency codes** — the capability and generativity axes sit
  beside the presence code and never gate it (a wrong-but-original move still codes as
  origination).
- **Integrity on the first answer only; revision exempt; flags visible.**
- **Append-only `Coding Master`; never write to `Before Class`** (formula view).
- **Pseudonymize at transcript/rollup export** for anything feeding the book.
- **Completion-only gradebook**; proficiency never posts to Schoology.
- **On-demand only** — batch runs when Katherine runs it, never at session start.

---

## Staging (do not skip)

Build and validate this flow on **one real cycle** before retiring the old scripts. Until
then, `01/08/11/15`, `PIPELINE_CHECKLIST`, and `KICKOFF_SCAN` keep a "superseded by v2"
pointer but are not deleted, so there is no mid-year gap in grade-posting.

# Claude Code kickoff — Forensics course build

You are working on Katherine von Duyke's (Dr. von Duyke's) Forensics course, on her Mac.
Forensics meets **B Day** on a block schedule, 2026–27.

Read this whole file before touching anything. Do not create files until Phase 0 is
reported back and approved.

---

## 1. Where things are

Google Drive for Desktop mounts the working account here:

```
/Users/katherinevonduyke/Library/CloudStorage/GoogleDrive-kvd@answerableteaching.com/My Drive/
```

That is the only account with course material. `kvond@udel.edu` is university work and
`kvond12@gmail.com` is personal — do not write to either.

**The Forensics folder name ends in a space.** It is literally `FORENSICS ` — quote every
path and do not "helpfully" trim it. If a tool rejects the path, that trailing space is why.

| What | Path (relative to `My Drive/`) |
|---|---|
| Forensics (raw) | `FORENSICS /` |
| Anatomy course (the model) | `ANATOMY AND PHYSIOLOGY/` |
| Anatomy build kit | `ANATOMY AND PHYSIOLOGY/COWORK REFERENCES/` |
| Biology pipeline (the full reference) | `Teacher Pay Teachers/CLAUDE SKILL FILES/` |
| Forensics mini-unit already written | `ANATOMY AND PHYSIOLOGY/01 Anatomy and Physiology Weekly/Week 19 - Forensics Mini Unit/` |
| Forensics mini-unit agendas | `ANATOMY AND PHYSIOLOGY/03 Biology Corner Anatomy Originals/Forensics Mini Unit/` |

---

## 2. Ground truth — read these first

Read, in this order, before planning anything:

1. `ANATOMY AND PHYSIOLOGY/COWORK REFERENCES/COWORK_KICKOFF.md`
2. `ANATOMY AND PHYSIOLOGY/COWORK REFERENCES/vt-anatomy-batch-SKILL.md`
3. `ANATOMY AND PHYSIOLOGY/COWORK REFERENCES/vt-deck-finishing-anatomy-SKILL.md`
4. `Teacher Pay Teachers/CLAUDE SKILL FILES/05-vt-deck-finishing-SKILL.md`
5. `Teacher Pay Teachers/CLAUDE SKILL FILES/Cowork prompts for TPT docs/How_to_Teach_a_VT_Cycle.md`
6. `Teacher Pay Teachers/CLAUDE SKILL FILES/19_Bio_Pipeline v2 (do not delete)/formative-pipeline-v2_SKILL.md`

Those files, not this one, define the deck standard, the slide-type sequence, the marker
strings the teacher prompts match on, and the grading pipeline. This file only says what
is *different* for Forensics.

Also inspect, do not modify:
- `ANATOMY AND PHYSIOLOGY/COWORK REFERENCES/deck_lint.py`
- `ANATOMY AND PHYSIOLOGY/COWORK REFERENCES/extract_and_grade.py`
- `ANATOMY AND PHYSIOLOGY/COWORK REFERENCES/IntroToAnatomy_VT — REFERENCE BUILD.gslides`

---

## 3. What Forensics actually has right now

This is the part that makes Forensics **not** a repeat of the Anatomy job. Anatomy had
21 existing decks to convert. Forensics has none.

The entire Forensics tree is a raw vendor download, nested five levels inside its own
path:

```
FORENSICS /
└── 02 Original Files/UNIT 3 - Death and the Human Body/2. Death Investigation/FORENSICS/
    ├── 03 - FORENSIC EVIDENCE UNIT/FINGERPRINTS/Day 1/
    │     └── Fingerprints Lesson- Day 1.pptx            2.85 MB   (vendor deck, not VT)
    └── 04 - Death and the Human Body_ Forensics Unit/
          ├── ENTOMOLOGY LESSON PLAN BUNDLE.zip          178.3 MB  (unopened)
          ├── ENTOMOLOGY LESSON PLAN BUNDLE (2).zip      178.5 MB  (unopened, likely dup)
          ├── TOXICOLOGY LESSON PLAN BUNDLE.zip          172.3 MB  (unopened)
          └── FAce skulpting/02-ForensicArtistryStudent-Sculpture.docx
```

Nothing has been authored. Nothing has changed since 2025-05-01. There is no week
skeleton, no agenda, no VT deck, no supply list, no SKILL file, no year plan.

**The three zips are the largest unknown in this project.** They are 529 MB of unopened
third-party curriculum, and what is inside them determines how much of the year is
already covered and how much must be written. Opening and inventorying them is Phase 0
and nothing else starts until it is done.

---

## 4. What Anatomy did — the shape to follow

Anatomy is organized by **week**, not by numbered cycle. 37 folders: `Week 01` …
`Week 36`, plus a combined `Week 37-38`. Each week folder holds:

- `Lesson Links.docx`
- `Wk NN — <date range> · <Topic> (Weekly Agenda).docx`
- a VT deck `.pptx`
- source/legacy materials

Two defects in Anatomy you should **not** reproduce in Forensics:

- **Folder number and agenda number drift apart from Week 13 onward** (`Week 13/` holds
  `Wk 14 — …`). Keep them locked together in Forensics, and make `deck_lint.py` — or a
  Forensics equivalent — check it.
- **Sixteen of 37 week folders carry no topic in the name** (`Week 03`, `Week 05`, …),
  and three naming conventions for decks coexist. Pick one convention for Forensics and
  hold it: `Week NN - <Topic>` for folders, `Week NN — <Topic> VT.pptx` for decks.

---

## 5. What is different for Forensics

### 5a. The case-and-vote slide type — new, and required in every cycle

The Variation Theory slide-type sequence stays as the Biology and Anatomy skill files
define it: five core questions, plus the four conditional structures — Continuity
question, Stock-and-flow model, Compensatory pair, Conflict case. Forensics adds **one
course-specific slide type, placed after the bellringer and before the first core
question.**

[Resolved 2026-08-29. This file previously said two conditional structures and called
the stock-and-flow model "tank-and-fill"; both were out of date. The Biology skill file
now agrees: vt-skill §1 reads "The 4 conditional slide types". Note that this file
refers above to "the Biology and Anatomy skill files" — there is no Anatomy VT skill file
in this repo, only vt-skill. Anatomy decks currently have no skill to read this count
from.]

**Slide type: The Case.**

The slide sets up a real, documented case and asks students to commit to a verdict before
they have the evidence the cycle is about.

The slide must carry:

- Case name and year.
- Four to six sentences of setup: what happened, who was accused, what the prosecution
  claimed. Written plainly, at a ninth-grade reading level.
- **Deliberately withheld:** the forensic evidence this cycle teaches. If the cycle is
  fingerprints, the setup does not say what the print analysis found.
- The vote: **Guilty / Not guilty.**
- A writing box: *Why? What would have to be true for you to change your mind?*

Speaker notes tell the teacher to take the vote by hands, record the tally on the board,
and **leave it unresolved.** Do not reveal the outcome here.

**The cycle closes by returning to it.** After the evidence slides, students vote a second
time and write what moved them, or why nothing did. That second write is the cycle's
strongest piece of formative evidence and should be picked up by the feedback pipeline
the same way the response slides are.

Why this belongs there, pedagogically: the vote makes students commit to a discernment
they are currently capable of, before the cycle varies the critical aspect. The contrast
set then has something to act against, and the change in the tally is a visible record of
what the variation did. Without the commitment, the evidence is just information; with
it, the evidence is consequential. The "and why" is what makes it answerable — the
reasoning, not the verdict, is the data.

**Case integrity rules — non-negotiable:**

- Cases must be **real and citable.** Do not invent a case, a defendant, a date, or a
  finding. If you cannot verify a detail from a source you can name, leave it out.
- Put the source on the slide's speaker notes, not the slide face.
- Flag for Katherine, do not silently include, any case involving a child victim, a
  sexual offence, or an execution. She teaches at a Title I high school and decides what
  her room can carry.

**Candidate cases, by unit — for her to approve, not for you to lock in:**

| Unit | Case | Why it fits |
|---|---|---|
| Fingerprints | Brandon Mayfield, 2004 | The FBI matched him to the Madrid bombing and was wrong. Teaches that the method has an error rate. |
| DNA | Colin Pitchfork, 1986 | First conviction by DNA; the same test first cleared an innocent suspect. |
| Hair & fiber | Wayne Williams, 1981 | Fiber evidence carried the case; the reasoning is contested to this day. |
| Ballistics / toolmarks | Sacco and Vanzetti, 1921 | Re-examined for a century. Good for "what counts as a match." |
| Questioned documents | Bruno Hauptmann, 1935 | Handwriting and the ransom notes. |
| Blood pattern | Sam Sheppard, 1954 | Convicted, then acquitted at retrial. |
| Toxicology | Harold Shipman | Long-undetected. Raises what toxicology can and cannot see after time passes. |
| Entomology | Buck Ruxton, 1935 | Larval development set time of death; also the first facial superimposition. |
| Forensic anthropology | Buck Ruxton, 1935 | Same case, different evidence — a good deliberate reuse. |
| Arson | Cameron Todd Willingham, 2004 | The fire science was wrong and he was executed. **Flag before use.** |

**Challenge before you build this:** [a Guilty / Not guilty binary presumes an accused
person. Several forensic units have no defendant — fingerprint classification,
entomological time-of-death estimation, evidence collection procedure. Forcing a verdict
onto those cycles produces a fake question and students will feel it. Consider a second
approved form of the slide type for evidence-only cycles: same commitment structure, different
question — *Is this enough to identify one person? Yes / No, and why.* Raise this with
Katherine and get a decision before building any deck.]

### 5b. No exams

This course gives **no exams.** Do not build, port, or reference a unit test, a final, or
a midterm, and do not carry over the Anatomy exam bank in
`ANATOMY AND PHYSIOLOGY/02 Biology Corner Unit Exams/`.

Assessment runs entirely through the formative pipeline defined in
`formative-pipeline-v2_SKILL.md`: the gradebook records completion only, and proficiency
lives in the Conceptual Growth Report. That pipeline already supports Forensics by name —
read it rather than adapting it.

Two consequences to handle explicitly:

- The **second vote** is new evidence the pipeline has never seen. Decide where it lands:
  a response slide the extractor already reads, or a new marker string. Prefer the former.
  Do not invent a new artifact type without asking.
- The year plan needs something in the place exams occupied in the Anatomy calendar.
  Propose what — a case-file capstone is the obvious candidate — but do not build it
  without approval.

---

## 6. Order of work

**Phase 0 — inventory. Nothing is created in this phase.**

1. Unzip the three bundles to a scratch folder **outside** Drive
   (`~/forensics-scratch/`), not in place. Do not write 529 MB of extracted files into a
   syncing folder.
2. Diff `ENTOMOLOGY LESSON PLAN BUNDLE.zip` against `ENTOMOLOGY LESSON PLAN BUNDLE (2).zip`.
   If identical, say so; do not delete either.
3. Produce `FORENSICS_INVENTORY.md`: every file in the three bundles and in the existing
   tree, what it is, what unit it serves, and whether it is usable, adaptable, or waste.
4. Read the Week 19 Forensics Mini Unit agendas — she has already written forensics
   material and it should seed the year plan.
5. **Stop and report.** Do not proceed to Phase 1 without approval.

**Phase 1 — the year plan.** A Forensics equivalent of the Anatomy weekly structure:
week count, topic per week, which unit each week belongs to, what evidence type each
cycle teaches, and the candidate case for each. Delivered as one document for approval.
Nothing is built from it until it comes back approved.

**Phase 2 — the build kit.** A `COWORK REFERENCES/` folder for Forensics, modeled on the
Anatomy one: `vt-forensics-batch-SKILL.md`, `vt-deck-finishing-forensics-SKILL.md`, a
Forensics `deck_lint.py`, and one reference build deck. The finishing skill must specify
the case-and-vote slide type, its marker strings, and the folder/agenda numbering lock.

**Phase 3 — one deck.** Build a single complete cycle end to end and get it approved
before batching. Fingerprints is the natural first, since a vendor deck already exists to
work from.

**Phase 4 — batch.** Only after Phase 3 is signed off.

---

## 7. Standing rules

- **Work on copies.** Anything under `RAW_ORIGINALS`, and the three zips, are frozen.
  Extract elsewhere; never modify in place.
- **`.pptx` is canonical**, not the Google Slides copy. This bit her on the Biology decks.
- **No student names, ever**, in anything that leaves the machine.
- **Ask before creating documents.** She has asked repeatedly not to receive
  doc-generation she did not approve.
- **One job at a time.** When you need a decision from her, ask one question, give your
  recommendation, and wait. Do not hand her a paragraph of choices to sort through.
- **Do not fabricate.** Case facts, citations, statistics, vendor contents. If you have
  not read it, say you have not read it.

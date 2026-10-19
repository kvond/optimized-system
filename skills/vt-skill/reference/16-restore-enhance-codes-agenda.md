<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

## 16. Restore, enhance, codes, agenda links (added 2026-10-15)

Katherine's direction, 2026-10-15: build these passes into the deck skill so that
lessons don't have to be repaired afterward. This section is course-neutral. It
applies to Biology, Forensics and A&P until the forks in §15 exist. Run the passes in
order, and finish all five before a deck counts as delivered.

The passes keep their existing owners. The workflow contract
`ai-ops/workflow-contracts/school-lesson-review-and-code-repair.md` names who runs
them. This section is the standard each pass is held to.

| Pass | Slash name (Katherine's) | Runs in |
|---|---|---|
| 16.1 Restore | `/restore-vt-slides` | School ChatGPT (Katherine) |
| 16.2 Enhance | `/vt-gemini-enhance` | School Claude Ext |
| 16.3 Codes | part of `/vt-gemini-enhance` | School Claude Ext |
| 16.4 Agenda links | after the deck and activities exist | the agent that built them |
| 16.5 Archive original | last, after all checks and relinks | the agent that ran 16.1 |

Sources for the work: the school Drive course folders and the original lesson
material in them. Don't use outside copies when the school Drive has the lesson.

### 16.1 Restore: merge the original lesson and the VT deck

This applies to Forensics and A&P, and to any Biology cycle that still has an original deck.

**A&P is original-first (Katherine, 2026-10-15).** For Anatomy, Week 8 to the end of the
year, the original free Biology Corner deck is the backbone, not the VT deck. Steps 2 and
6 below change for A&P:

- **Spine.** Keep the original deck whole and in its own order, with every slide,
  picture, diagram and video. Insert the existing VT question slides into it at the point
  where the original teaches that critical aspect. Do not rebuild the lesson from a
  shortened reconstruction.
- **Less telling, more doing.** Use the matching guided notes to turn reference slides
  into student work placed before the slide that tells: students type an answer, or move
  parts of the slide to match or label. Then show the original slide as the answer.
- **Logic check.** Read the merged deck once for critical-aspect logic: each VT question
  sits after the material it depends on and before the answer it would give away.
- **Check (replaces step 6 for A&P).** The merged deck has at least the original's slide
  and image counts plus the inserted VT and activity slides, and `deck_lint.py` passes.

The rest of §16 (codes, Agenda links, archive last) is unchanged.

1. **Find both decks** in the week/cycle folder: the VT deck and the original lesson
   deck (including `.pptx` originals and `Copy of …` decks).
2. **Merge into the VT deck.** Use the VT structure (§1, §2) as the spine. Carry
   the original's content slides, **pictures, diagrams, data tables, case material,
   labs and worksheet links** into the matching critical-aspect block (§2.1).
3. **Cut nothing.** A picture or piece of lesson material that has no obvious place
   goes in an appendix slide after the end of the deck (§2.2). Never delete it. If
   the deck gets long, raise that with Katherine instead of trimming material.
4. **Keep the deck native.** Merge in Google Slides. Don't round-trip a native deck
   through PowerPoint (it drops codes and links). A `.pptx`-only VT deck is
   converted to Slides first, then merged.
5. **Leave the original live for now.** Don't rename or archive it during 16.1. It is
   archived in 16.5, after every check and relink has passed.
6. **Check:** the slide count of the merged deck is at least the VT deck's count
   plus the original's content slides; every image in the original appears in the
   merged deck (count images in both); `deck_lint.py` passes.

### 16.2 Enhance: `/vt-gemini-enhance`

Run it on the merged deck. The rules already in this skill hold: the enhance pass skips
answer slides; enhanced textboxes get no gray; answer textbox colours stay unchanged;
marker strings stay intact (§3c, §7). After the pass, run the post-enhancement check
(`docs/curriculum/post_enhancement_check.md`) and `deck_lint.py`. When the
marker layer and the deck disagree, fix the deck, never the prompt.

### 16.3 Embedded codes, including new student textboxes

The enhance pass also checks the embedded codes. The syntax comes from Master Agenda
`Agenda 26-27 CLEAN`, tab **Feedback Prompts**, **Prompt 00 (Embed Codes)**. Read it
fresh each time and don't copy it here. The observed schema is `[[NOTES:CYCLE:ID]]`
paired with `[[DRAFT:CYCLE:ID]]`, plus `[[OPTIONAL:…]]` and `[[BANK:CYCLE:TERM]]`, with the
slide-one `[[MARKER-INVENTORY:CYCLE]]` line.

**The prompt to run when Katherine adds new student textboxes.** Paste it as is:

```
I added new student textboxes to this deck. For each student textbox that has no
embedded code: add the code from Agenda Prompt 00 as small native text on the label
above the response area, outside the student's writing. Concept Bank boxes get
[[BANK:CYCLE:TERM]] with this cycle number and the term. Response boxes get the
paired [[NOTES:CYCLE:ID]] / [[DRAFT:CYCLE:ID]]. Keep every existing code and ID
unchanged and add no duplicates. Then update the slide-one [[MARKER-INVENTORY:CYCLE]]
counts and ID lists, and report which slides you changed.
```

**Check:** each student textbox has exactly one code; NOTES/DRAFT pair by ID, not by
slide position; and the inventory counts match the codes found.

### 16.4 Agenda links: after lessons and activities are created

Once a deck and its activities exist in the course folder, link them from the
Master Agenda `Agenda 26-27 CLEAN`
(`1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY`, school account) on that course's
tab, in the row for each class day that teaches the lesson:

- the deck: the teacher deck URL in Q (§9.3); the student `/copy` link in P fills in from it;
- each activity, worksheet or lab created for the lesson;
- the week/cycle folder.

Rules:
- Write only into the row's existing link cells, in the format the row already uses.
  Don't add columns or restructure the tab, and don't change dates, pacing or notes
  (§9.3a: the agenda is Katherine's schedule).
- Fill a blank link cell, or replace a link that points at an `ARCHIVE …` file or a
  file *confirmed* missing. A 404 from one account doesn't prove the file is missing:
  decks can be invisible to the school connection and still exist under another account.
  Before replacing a link, check the file's owner and sharing across the authorized
  accounts. If you still can't tell whether it exists, leave the link, and report it as an
  access blocker in #kathy with the cell and the file ID.
- If a cell already holds a different live link, leave it and ask Katherine.
- Verify each new link with the school account (katherine.vonduyke@redclay.k12.de.us).
  The agenda and students use that account, not whichever account happens to open the file.
- Read the row back after writing. Every link must open the intended file, and none
  may point at an `ARCHIVE …` file.

### 16.5 Archive the original, last

Do this only after 16.1–16.3 pass their checks, `deck_lint.py` is clean, and the 16.4
links read back correctly. The order follows §9.3: repoint every caller and verify it
before archiving.

1. Read back every caller of the original's file ID: the agenda rows, START HERE
   decks, `/copy` links (§9.3), and a Drive `fullText` search as a first pass, never as
   proof. None may still point at the original.
2. Only then rename the original, never trash it:
   `ARCHIVE <date> — <original title>, merged into <VT deck title>` (§9.2 step 3).
3. If any earlier step stopped, skip this one. The original stays live and unrenamed,
   and the stop is reported.

**A deck is delivered when** 16.1–16.3 pass their checks, `deck_lint.py` is clean,
the 16.4 agenda links read back correctly, and 16.5 is done.

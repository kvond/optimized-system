# Claude Code — Job 1: Deck Inventory (read-only)

Rewritten 2026-08-29 against the actual file layout. Supersedes an earlier
inventory prompt that was never committed here.

---

## What changed, and why it matters

The original prompt assumed the `.pptx` twin test from `vt-skill` §0 — a
`.pptx` sitting beside its live Slides file in each cycle folder. That is not the
layout on disk.

The 24 `.pptx` files are in one flat archive folder,
`ZZ ARCHIVE — original .pptx builds`, on the kvd@answerableteaching.com account.
The cycle folders themselves hold live `.gslides` files, which contain no readable
bytes.

**Two gaps visible before the run starts.** Cycle 01 (Lab Safety) and Cycle 02
(Ecosystems & Feeding Relationships) have no `.pptx` in the archive. Cycle 01 is
your stated first target, so it needs a Slides export before it can be worked on
at all.

**One thing the run has to establish.** The folder is called "original builds,"
and the filenames use a sublettering scheme — 07a/07b, 13a, 15a/15b, 16a–16d —
that does not match the current 20-cycle structure. These may predate the VT
restructure. The inventory has to report what is actually in the files rather
than assume they match the live decks.

---

## The prompt

```
Read ~/.claude/skills/vt-skill/SKILL.md first. It defines the 5 core
questions, the slide types, the marker strings, and the format tokens. Use its
vocabulary exactly: these are "core questions" and "slide types". The word
"beat" is not used.

Also read ~/.claude/skills/vt-fusion-retrofit/SKILL.md for the definitions of
separation, fusion, synchronic and diachronic simultaneity, and the three
coordination structures.

IGNORE the .pptx twin test in vt-skill §0. It describes a layout that no
longer exists. The source files are all in one flat archive folder, named
below.

TASK: Build a read-only inventory of all 24 archived Biology .pptx decks.

Source: ~/AT/BIOLOGY (Shared)/ZZ ARCHIVE — original .pptx builds/
Output:  ~/deck_work/deck_inventory_2026-08-29.csv
         ~/deck_work/deck_inventory_2026-08-29.md

Create ~/deck_work if it does not exist. Write NOTHING outside it. Do not
modify, move, rename, or delete any file in the source folder. Open every
.pptx read-only. The source folder is a Google Drive mount and is the only
copy of these files.

Use python-pptx. Install it if needed.

For each of the 24 files record:

  - filename, cycle number and sublabel as they appear in the name
  - slide count
  - the ordered list of slide types you can identify, by title text and by
    the marker strings vt-skill specifies
  - which of the 5 core questions are present, and for which critical aspect
  - Continuity question present? (yes/no)
  - Stock-and-flow model present? (yes/no)
  - Concept Bank present? (yes/no, and its position)
  - Teacher Prep slide present? (yes/no)
  - response slides present? do their speaker notes carry the revision prompt?
  - links slide present? count of links, and how many are /copy versus /edit,
    /view, or /edit?usp=sharing
  - format: slide dimensions, fonts used, hex colors used

Then three judgments, all advisory. Record what you find; propose nothing.

  a. STRUCTURE MATCH. Does this file look like a VT cycle deck built to the
     vt-skill standard, or like a pre-VT lecture deck? State which and
     give your evidence. The folder is named "original builds" and the
     sublettering (07a/07b, 15a/15b, 16a-16d) does not match the current
     20-cycle structure, so some of these may predate the VT restructure.

  b. MOVE 1 CARRIES A DIFFERENCE. Read the text of the Critical Aspect
     question slide. Does it contain a comparison, a choice between named
     alternatives, or a stated change condition? A question that names the
     aspect and leaves the contrast to the following slide produces silence
     in a room. Record yes/no and quote the question text verbatim so I can
     judge the borderline cases myself.

  c. COORDINATION. Is there any slide where two critical aspects must be held
     together to answer? Record which structure if so (stock-and-flow /
     compensatory pair / conflict case), or "none". Do not judge whether one
     SHOULD be there.

Emit the CSV with one row per file, and a readable summary answering:
  - which files are VT-structured and which are not
  - which are missing a required slide type
  - which links slides carry non-/copy links
  - which fail a format token
  - the distribution of coordination structures
  - which fail check (b)

Do not propose fixes. Report only.

When done, state the file count you processed and list any file you could not
open.
```

---

## Before running

`~/deck_work` sits outside the Drive mount on purpose, so a partial write never
syncs into Drive.

The archive folder must be set to **Available offline** in Finder, or python-pptx
will find no bytes to read. Confirm with:

```
find ~/AT/"BIOLOGY (Shared)"/"ZZ ARCHIVE — original .pptx builds" -name "*.pptx" | wc -l
```

24 means ready.

---

## After the run

Two questions the output should settle, and both change what comes next:

1. **How many of the 24 are actually VT decks?** If a substantial number are
   pre-VT lecture builds, the retrofit job is larger than adding fusion slides —
   it includes converting them, which `vt-skill` already covers.

2. **Do the archived files match the live Slides decks?** The inventory reads
   the archive. Students see the Slides files. If the archive predates edits made
   in Slides, the archive is a stale source and the export question comes back.

## Still outstanding

- Cycle 01 (Lab Safety) and Cycle 02 need `.pptx` exports from their live Slides
  files before they can be worked on.
- The 24 files are the only copies, on an account with roughly a month left.
  Download the archive folder as a zip from the browser.

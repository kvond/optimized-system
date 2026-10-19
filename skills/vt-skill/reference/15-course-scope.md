<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

## 15. Course scope, and the sibling skills (added 2026-08-18)

This file covers **Biology only**. From 2026-08-18 Katherine labels the
deck-finishing skills by course. Forensics and Anatomy & Physiology get their own
files, forked from this one.

**Naming.** Renamed `vt-skill` on 2026-10-19 on Katherine's instruction (formerly
`vt-bio-skill`). The planned course forks keep their names, `vt-forensics-skill` and
`vt-anatomy-skill`, until they exist. Each description names its course and says the other two exist,
so a request that names a course loads one file and not three.

The `name` field takes lowercase letters, digits and hyphens only. Write it that
way in the file. Uppercase and underscores are normalised on save, so a file
written as `VT_Bio_skill` installs as `vt-bio-skill` and the file then disagrees
with the installed skill — write the normalised form and the two stay the same.

**What is course-neutral.** Sections 1, 2, 3, 3b, 4, 4b, 6, 7, 7.1, 8, 9, 11, 12,
13, and 14 hold structure, tokens, geometry, and process. Section 7.1 is more than
course-neutral: the two scripts are shared, so the exclusion list is edited one
time for all three courses, not one time per course file. A fork copies them without
change. A change to any of them must be made in every course file in the same pass,
or the three files drift apart silently.

**What is course-specific.**

- **The reference build.** Biology uses `Cycle 02 — Ecosystems & Feeding
  Relationships (VT deck)`. Each course names its own. The rule that the reference
  build wins over this file applies per course.
- **The two source links** in section 2.0 and section 3b. The CK-12 Biology
  FlexBook 2.0 and the Khan Academy biology set are Biology sources.
- **The standards line** in section 5. Biology drafts NGSS performance
  expectations, verified verbatim against nextgenscience.org.
- **The examples.** The bee orchid, the dodder, and the anglerfish in section 6,
  and THE DOG SAT and the codon tables in section 14.3, are Biology examples. A
  fork replaces them rather than carrying them.
- **The pedagogy note for Forensics.** Every Forensics lesson opens with a real
  foundational case, evidence shown and outcome hidden, student verdict before
  instruction, reveal at the end. The pig autopsy is excluded. That rule has no
  Biology equivalent and belongs only in the Forensics fork.

[Challenge, for the forks: Forensics has no CK-12 FlexBook section and no Khan
Academy unit to point at. The `FOR READERS:` and `FOR TESTERS:` pair in sections
2.0 and 3b cannot be carried across by substitution, because the second half of it
has no Forensics equivalent. That fork needs a decision from you before it ships,
and the honest answer may be that Forensics carries one named source rather than a
reader and tester pair. The same question applies to Anatomy & Physiology, which
has a CK-12 Human Biology FlexBook but a thinner Khan set.]

[Challenge, on drift: three files that share fourteen sections will diverge the
first time a change is made in a hurry to one of them. The alternative is one file
with a short course-specific block at the top and a single course-neutral body.
That costs you the clean per-course trigger you asked for, so I have written the
three-file version. Flag it if the drift matters more than the trigger.]

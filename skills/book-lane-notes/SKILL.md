---
name: book-lane-notes
description: The notes lane of the Answerable Teaching revision. Sets one endnote convention for the volume, puts markers in order and anchors every note, moves academic apparatus from the body to the notes where Katherine's ruling allows, verifies every attribution to a named researcher, repairs citations, and builds the sources manifest. Writes packets only; never edits the manuscript. Load book-revision first. Triggers - "notes lane", "endnotes", "verify attributions", "citation pass", "sources manifest".
---

# Notes lane

You own the apparatus: the notes, the citations, what the book says a scholar said, and what belongs in a note rather than the body. You do not own the body argument (arc), the wording of definitions (terms), or how a claim is seated (claims); you own whether the scholar the claim leans on actually said it.

Read first: `book-revision/SKILL.md`; `decisions.md` (R3, R11, R22; P16, P21); `book-revision/reference/manuscript-checks.md` (her checks 7 and 8 are this lane's: Matusov and von Duyke is cited as 2010 and as 2014 and each citation must carry the right year, Lima and von Duyke 2016 likewise, and the claims attributed to them must be what those works say; "lurking" is Katherine's term and Ito et al. (2010) get hanging out, messing around, geeking out and nothing more); the voice guide's marker 10 (theory in the endnotes, teacher in the body; every theoretical term touches a concrete classroom object within two sentences) and Part 3's attribution rule (check every attribution on every pass, at the level of the specific term or finding). Then the chapter, with the checker's endnote-marker list and cross-reference list beside it.

## Entry: scope and degrees of freedom

Always preserve the current source, author wording, citation integrity and notes-lane ownership. This skill writes packets, not manuscript text. Chapter workers supply deltas; only the designated notes-lane integrating writer updates the shared manifest. Read the chapter procedure before running a citation pass; use the flagged-attribution reference only for relevant passages.

- **Low freedom — sources and verification:** verify exact works, years, quotations and attribution; unresolved evidence stays open, never guessed. Preserve unrelated manifest entries and verify its saved result.
- **Medium freedom — approved process:** choose the relevant chapter and order of evidence checks, retaining all checks required for that scope.
- **High freedom — requested brainstorming only:** suggest research avenues or apparatus options as proposals; never invent sources or substitute speculation for verification.

## Contents — read only what this task needs

Always read the entry constraints first. Then load only the selected detail; do not crawl every reference.

| Task | Read |
|---|---|
| Every invocation | Entry, packet and self-check in this file |
| Run notes/citation pass | [Chapter procedure](reference/chapter-procedure.md) |
| Check a known flagged passage | [Flagged attributions](reference/flagged-attributions.md), relevant rows only |

## Procedure, per chapter

Before a notes pass, read the [chapter procedure](reference/chapter-procedure.md); apply its exact citation and source-manifest ownership requirements.

## Attributions already flagged

When a passage matches a known attribution concern, consult [flagged attributions](reference/flagged-attributions.md). These are questions to verify, not established corrections.

## Packet

`revision/packets/notes/<chapter-id>.md` in the spine's format. Relocation rows carry the note text (her words) and the Find string of the carrying sentence. Attribution rows carry the verdict and the bracket. Include the chapter's source delta in that packet commit. The designated notes-lane integrating writer commits the merged `revision/sources.json` separately after reconciling the chapter deltas; a packet commit is not proof the shared manifest was updated.

## Self-check

No relocation writes a new carrying sentence; where none exists, the row is a bracket. Every attribution row names the source checked. Nothing invented: an unfound source is an open item, never a guess. Find strings verified.

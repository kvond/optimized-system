---
name: book-lane-notes
description: The notes lane of the Answerable Teaching revision. Sets one endnote convention for the volume, puts markers in order and anchors every note, moves academic apparatus from the body to the notes where Katherine's ruling allows, verifies every attribution to a named researcher, repairs citations, and builds the sources manifest. Writes packets only; never edits the manuscript. Load book-revision first. Triggers - "notes lane", "endnotes", "verify attributions", "citation pass", "sources manifest".
---

# Notes lane

You own the apparatus: the notes, the citations, what the book says a scholar said, and what belongs in a note rather than the body. You do not own the body argument (arc), the wording of definitions (terms), or how a claim is seated (claims); you own whether the scholar the claim leans on actually said it.

Read first: `book-revision/SKILL.md`; `decisions.md` (R3, R11, R22; P16, P21); `book-revision/reference/manuscript-checks.md` (her checks 7 and 8 are this lane's: Matusov and von Duyke is cited as 2010 and as 2014 and each citation must carry the right year, Lima and von Duyke 2016 likewise, and the claims attributed to them must be what those works say; "lurking" is Katherine's term and Ito et al. (2010) get hanging out, messing around, geeking out and nothing more); the voice guide's marker 10 (theory in the endnotes, teacher in the body; every theoretical term touches a concrete classroom object within two sentences) and Part 3's attribution rule (check every attribution on every pass, at the level of the specific term or finding). Then the chapter, with the checker's endnote-marker list and cross-reference list beside it.

## Procedure, per chapter

1. **Convention (P16).** Confirm what the chapter uses now (superscript markers, bracketed numbers, plain numerals, asterisks, no notes). One row per chapter, class `fix-direct`, stating the conversion to the volume convention: superscript numerals in the body, numbered from 1 in order of appearance, notes at chapter end under "Notes — Chapter N". Then one row per marker out of order, reused, or unanchored, with the Find string of the sentence it sits on and the note it should carry. The continuity pass, section G, lists the known cases in Chapters 1, 2, 3, and 4.

2. **Apparatus to the notes (R3).** Read the body for theory discussions, literature comparisons, definitional disputes, and lists of citations that do not touch a classroom object within two sentences. For each, one `relocate` row: the block that moves (her words, unaltered), the note it becomes, and the carrying sentence that stays, quoted from her own text (never written new; if no sentence of hers can carry it, the row is a `bracket` proposing where she might write one). The Preface, Introduction, and Chapter 1 were already thinned this way in August (Lampert; classic versus radical constructivism; the epistemic-agency literature); Chapters 2, 3, 4, 8, and 10 are where the apparatus still sits in the body.

3. **Attributions.** For every named researcher in the chapter, one row: what the text says they claimed, the source you checked (web search for published work is allowed; the dissertation is not reachable and gets `open-item: she checks`), and the verdict: `stands`, `narrows` (the text overstates), `drifts` (the text says something adjacent), or `misattributed`. Where the verdict is not `stands`, the Proposed column carries the bracket: what the source actually says and where. The voice guide names the ones a scholarly reviewer will catch first: Bakhtin's otvetstvennost, Bateson's unit of mind, Reeve's agentic engagement construct, Mortimer and Scott's communicative approaches, Emanuelsson's constitutive framing, Patall's backfire finding.

4. **The reframing epistemic agency note (R2).** Once: supply to the terms lane, and put in `revision/packets/notes/epistemic-agency-literature.md`, the sources for the learning-sciences usage the book departs from (Stroupe 2014; Miller, Manz, Russ, Stroupe & Berland 2018; Ko & Krist 2019; Damşa, Kirschner, Andriessen, Erkens & Sins 2010 are the ones project memory already names; verify each and add what the search turns up), with one line each on what the term means there. This becomes the endnote at the canonical home. Outline only.

5. **Citations.** Every in-text citation in the chapter: present in a note or reference list, year present, format consistent (cf. not c.f.; period outside the parentheses; author named once in a sentence). Missing years are `fix-direct` when the source is unambiguous and verified, `open-item` otherwise. Build `revision/sources.json` (author, year, title, container, where cited) as you go; every lane's chapter adds to it; the file is the manifest the citation check runs against.

6. **Cross-references into notes.** Where a body sentence points the reader to a note that does not exist, or a note refers to a body sentence that was cut ("the cut item (c)"), one row each.

## Attributions already flagged

Each is a row in the chapter where it lives; verify, do not assume the flag is right.

| Where | Find | The question |
|---|---|---|
| Chapter 2 | `Ito's "agency genres," as she calls them` | Ito et al. call them genres of participation; "genres of agency" is Katherine's |
| Chapter 6A | `Marton's line is the one I keep returning to` | "a difference that makes a difference" is Bateson's; does Marton use it, or should both be credited |
| Chapter 2, 4, 9 | `Patall (2024) offers a detailed account of engaged agency` | which Patall paper; her construct is agentic engagement and autonomy support, not "engaged agency" |
| Chapter 4 | `Patall, Cooper, and Wynn (2010) found` | is the competence moderation in the 2010 classroom study or the 2008 meta-analysis |
| Chapter 7 | `disproportionately the students most exposed to stereotype threat` | are both moderators (achievement; stereotype threat) in Patall, Kennedy et al. 2022 |
| Chapter 4 | `perceived their teachers as less supportive of their autonomy` | which 2022 paper: Kennedy et al. or Zambrano et al.; keep them distinct |
| Chapter 5 | `two communicative approaches` | Mortimer and Scott's scheme has two dimensions and four classes |
| Chapter 5 | `dances the tension` | Moore-Anderson: year and edition |
| Chapter 2, 8 | `benevolent control`; `benevolent dictators` | Matusov quoted two ways; which, and what year |
| Chapter 2, note 4 | `first described in Llewellyn's` | zombies, zombification, and "agency sickness": what Llewellyn actually wrote (P21) |
| Chapter 2 | `Mostly dead, but not all dead` | the Princess Bride line as spoken |
| Chapter 3 | `turn-off to curiosity` | Greenberg 1985: which book |
| Chapter 3 | `catalyzed by John Holt's` | Growing Without Schooling began in 1977; the free-school wave predates it |
| Chapter 3 | `approaching its fourth decade` | The Circle School's founding year |
| Chapter 4 | `which I will refer to as the Germantown study` | Neuman and Celano's neighborhoods were Chestnut Hill and the Badlands; is "Germantown" her label or a slip (eleven occurrences) |
| Chapter 3 | `The third goal echoes the Enlightenment aspiration` | Labaree's social mobility goal is the credentialing goal; the Enlightenment aspiration maps to democratic equality |
| Chapter 9 | `destroyed property` | Lewin, Lippitt, and White 1939: what the paper records when the adult left |
| Chapter 9 | `concentric circles of participation` | not a standard Habermas image; confirm or reattribute |
| Chapter 9 | `Two education professors once observed` | the Oregon Trail anecdote has no source |
| Chapter 9 | `In museum education, researchers followed a father and daughter` | the heart-exhibit study has no source |
| Chapter 2, note 1 | `no alibi in Being` | edition and wording |
| Chapter 10 | Bhaer and Tom quotations | against the dissertation: `open-item: she checks` |
| Chapter 10 | Berlin, Sen, Arendt | invoked without citations; the notes carry them |
| Chapter 3, note 4 | `"Effortful agency" is my own term` | coined in Matusov, von Duyke, and Kayumova 2016 (P21); note anchored to the wrong sentence |
| Chapter 7 | Raver, Blair, and Willoughby 2013; Bibok, Carpendale, and Müller 2009 | the executive-function claims: what each study supports |
| Chapter 9 | Big Picture Learning; Mastery Transcript Consortium | current status and URLs |
| Chapter 4 | KIPP outcomes; the SAT and income; Neuman and Celano | what the cited work supports |

## Packet

`revision/packets/notes/<chapter-id>.md` in the spine's format. Relocation rows carry the note text (her words) and the Find string of the carrying sentence. Attribution rows carry the verdict and the bracket. `revision/sources.json` is updated in the same commit.

## Self-check

No relocation writes a new carrying sentence; where none exists, the row is a bracket. Every attribution row names the source checked. Nothing invented: an unfound source is an open item, never a guess. Find strings verified.

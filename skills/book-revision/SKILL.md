---
name: book-revision
description: The spine for revising Answerable Teaching. Load it first in any session that revises, restructures, tightens, or checks the manuscript. It sets the rules every revision agent shares (where the text lives, the prose rule, the argument arc, the glossary and its analytical levels, the claim types, the decisions ledger, the lane system and packet format), and it tells an agent which lane to load next. Triggers - "revise the book", "revision pass", "tighten the argument", "run a lane", "integrate the packets", "book-revision".
---

# Book revision: the spine

Read this before any lane. It is short on purpose; the lanes carry the work lists.

## What a revision pass is

A pass takes one dated snapshot of the manuscript, runs six lanes over it in parallel, and then runs one integration step. A lane is a single concern (the argument arc, the terms, the claims, the notes and attributions, the continuity of cases and pointers, the residue and mechanics). Each lane reads the snapshot and writes packets, one packet per chapter, into its own folder. No lane touches the manuscript. The integrator reads every packet for a chapter, applies what the prose rule allows, and leaves the rest in brackets for Katherine. Several agents can run at once because they never write to the same place: a lane owns its packet folder and nothing else.

## Where things are

| What | Where | Account or route |
|---|---|---|
| The current draft (68,000 words, Preface through Chapter 11 plus a capstone stub) | Google Doc "(4 and 5 next 6 , first 3 chapters feed website)AnswerableTeachingPrefaceCh5 (Working Copy)", id `1RuY6yj9mhqBajj-UYhF_WCQwEpvLKinMma9fKNAStlM` | owned by kvond@udel.edu; shared to the Red Clay and kvond12 accounts |
| The snapshot a pass works from | `revision/manuscript/working-copy-<date>.md` in `kvond/Answerable-Teaching` | git; export the Doc to markdown at the start of a pass |
| The AI chapter as assembled 2026-09-11 ("Doable, Not the Doer") | `book-compile/ch6-doable-not-the-doer-assembled.md` in `kvond/Answerable-Teaching` | git; not yet in the Doc |
| The practice chapter ("Before Inquiry", subtitle "Inquiry Has Prerequisites"), missing from the Doc | `book-compile/ch6-intellectual-mentorship-rewrite.md` (Aug 23, the fuller form) and `revision/reference/ch05-earlier-draft-2026-05.md` (May, her supply of 2026-09-12) in `kvond/Answerable-Teaching` | git; R16, R20, and R21 in the ledger |
| Rulings recovered from the retired provenance register (title, "the adult who lingers", the pseudonym ledger and name-change log, Moore-Anderson placements) | `revision/reference/rulings-from-register-2026-08.md` in `kvond/Answerable-Teaching` | git |
| The voice instruction and the hard bans | `book-compile/voice-guide.md`, `book-compile/tics-list.md` in `kvond/Answerable-Teaching` | git |
| The argument arc, the glossary, the six analytical levels | `reference/argument-arc-and-glossary.md` beside this file | git (`kvond/answerable-skills`) |
| The decisions ledger | `reference/decisions.md` beside this file | git |
| The findings the lanes work from | `reference/findings/` beside this file (the external reader's review and the continuity pass of 2026-09-12) | git |
| The mechanical checker | `scripts/manuscript_check.py` beside this file | run it on the snapshot before and after a pass |
| Lane packets and the integrator's output | `revision/packets/<lane>/<chapter>.md` and `revision/integrated/` in `kvond/Answerable-Teaching` | git |
| Roam graph `kvond`, "Answerable Teaching/" pages, and the repo's `source/` and `writing/` folders | older exports (last nightly publish 2026-07-02). Not the current draft. Reconciliation is decision P18. | read only during a pass |

Engine start: a Cowork session reaches the repos through the GitHub connector and the Doc through the Drive connector on the kvond12 or Red Clay account. A Claude Code session on the Mac reads this skill through `~/.claude/skills` (a symlink into `~/code/answerable-skills/skills`) and works in the clone of `kvond/Answerable-Teaching` (`SYNC.md` names `~/Documents/projects/Answerable-Teaching`, but on 2026-09-12 that folder held only the nightly-publish log; where the clone now lives is an open item for her). If a path here does not resolve, the account or the clone is wrong; the skill is not broken.

## The four documents that govern every lane

1. **The voice guide** (`voice-guide.md`, with `tics-list.md`). What her prose sounds like, what never goes into the book, and what to fix versus flag. Part 3 of it is the editing pass rule and is repeated in the next section because nothing else matters as much.
2. **The argument arc and glossary** (`reference/argument-arc-and-glossary.md`). Twelve propositions the book advances, the chapter that advances each, the load-bearing terms with their "not this" boundaries, and the six analytical levels every term belongs to, under the master concept, standing as a knower. Katherine ratified this as the spine of the pass on 2026-09-11.
3. **The decisions ledger** (`reference/decisions.md`). Rulings she has made (R-items) and defaults applied until she rules (P-items). A lane never re-argues an R-item. A lane applies a P-item's default and writes `assumes P-nn` in the packet row so the integrator can find every consequence if she rules the other way.
4. **The findings** (`reference/findings/`). The external reader's critique and the continuity pass. The lanes have already taken their work items from these; go back to them for the reasoning behind an item, not for new items.

## The prose rule

Her words are not altered except mechanically and grammatically, with minor phrasing and removal of redundancies. Everything else appears in the manuscript only inside [brackets] as a suggestion she chooses to act on or not, including any challenge to her thinking. Her latest draft is always canonical. No new marker system is introduced: no provenance tags (retired 2026-09-11), no status codes in prose. A bracket is the only thing an agent adds to her text.

What the integrator may apply directly: agreement and pronoun slips, doubled words, homophones, spacing, punctuation, citation format and missing years, a comma-spliced appositive resolved with parentheses or a second sentence, redundant restatement within a paragraph, an em dash replaced by the hinge she uses (colon, semicolon, comma, parentheses, period), a ruled rename applied at every occurrence (R2, R9), an ordering or relocation of her own unaltered words when a ruling or the canonical-home convention calls for it, and deletion of editorial residue that is not prose once its content is logged in the ledger.

What stays in brackets: any new sentence, any rewording beyond minor phrasing, any cut of her prose, any change to what a passage claims, the wording of a pointer sentence, and every challenge. Scaffolding (a proposed passage she will rewrite) goes in the packet, and enters the manuscript only as a bracket that names the packet row.

Never invent a student scene or a classroom detail. Never invent a citation. Never write the disclosure statement for her.

## Claim types

Every categorical statement in the book is one of five kinds, and the revision seats each in its kind rather than flattening it. An **interpretive** claim reads a case: what Nancy's arrangement was doing. A **normative** claim says what teaching or schooling ought to recognize. An **empirical** claim says what generally occurs across schools and needs a source or a scope. A **causal** claim says what a condition produces and needs the mechanism stated. A **rhetorical** diagnosis makes a professional experience vivid and is allowed to overreach in a single clause as voice, with the reviewer risk marked. The claims lane owns this work; every lane respects the seating it proposes.

## The analytical levels

Every term belongs to one level, and a reader should always be able to tell which is in play. Student–object relation (origination, sense making, meaning making, the five generative configurations). Teacher response (recognition, uptake, answerability, dialogism, the moves). Object design (shared object, critical aspect, Variation Theory, control of variation). Developmental process (lurking, messing around, geeking out, adjacent agency, intellectual apprenticeship). Institutional condition (legibility in Scott's sense, chronotope, governance, credit, pacing). Breakdown (pseudo-agency, dysfunctional agency, the double bind). The master concept, standing as a knower, is what all of it describes; agency is its capacity side, not the whole. The terms lane owns this; every lane writes with it.

## The argument, in twelve lines

Students make bids to act as knowers. Schools recognize legible completion before live thinking. That produces systematic misrecognition, not isolated error. Misrecognition damages standing as a knower. Standing is unevenly distributed through the apprenticeships students get. Answerable teaching (dialogism, Variation Theory, intellectual apprenticeship) is the classroom response. The capacity develops in phases and through bridges. AI matters only insofar as it offloads production and returns presence. Classroom craft hits institutional ceilings. Agency develops in the held tension, not in one ethic winning. Teachers need moves, not only perception. All of it is an apprenticeship in intellectual authorship. The full statements and the chapter map are in the reference file; every chapter must visibly advance at least one line, and the arc lane checks that.

## The lanes and who owns what

| Lane | Skill | Owns | Does not own |
|---|---|---|---|
| Arc | `book-lane-arc` | proposition mapping per chapter, bringing the arc forward, what advances nothing (shorten, move, cut), the practitioner promise pointers, AI durability framing, whole-school tightening, The Moves as process not lookup | duplicates (continuity), term homes (terms), endnote moves (notes) |
| Terms | `book-lane-terms` | one canonical home per term, level marking, the rename to reframing epistemic agency and its why, demotions of borrowed terms, the taxonomy table, "moments not labels" | claim wording (claims), attributions (notes) |
| Claims | `book-lane-claims` | claim-type seating, the equity passages, the AI estimates, the evidentiary contract ("How to Read the Cases" outline) | citations and years (notes) |
| Notes | `book-lane-notes` | one note convention, markers in order, academic apparatus moved to endnotes, every attribution verified, the sources manifest | the body argument (arc) |
| Continuity | `book-lane-continuity` | pseudonyms and case facts, chapter pointers, passages told twice, canonical home of scenes, the Moves chapter's copied scenes | term definitions (terms) |
| Residue | `book-lane-residue` | editorial residue logged then removed, mechanics fixed directly, em-dash reduction, ban-list hits flagged, headings and note apparatus formatting | anything that changes meaning |
| Integrate | `book-integrate` | reading all packets for a chapter, applying what the prose rule allows, bracketing the rest, the change log, rerunning the checker | ruling on a P-item |

If two lanes propose different things for the same sentence, the owning lane's row wins and the other lane's row is kept as a note in the integrated packet. If neither owns it, the integrator brackets both.

## The packet

A packet is one markdown file per chapter per lane: `revision/packets/<lane>/<chapter-id>.md`, where the chapter id is the number or letter as the snapshot names it (`preface`, `intro`, `ch01`, `ch06a`, `ch11`); the practice chapter, which is not in the snapshot, is `before-inquiry`, and its text is the Aug file named in the table above. It opens with a five-line header and then one table.

```
Lane: terms
Chapter: ch02 (Chapter 2 — What Is Agency? Why Do We Want It?)
Snapshot: revision/manuscript/working-copy-2026-09-12.md
Assumes: P4, P5, P7
Checker run: revision/reports/check-2026-09-12.md
```

| ID | Find | Class | What | Proposed | Why |
|---|---|---|---|---|---|
| terms-ch02-01 | `Decision-making and capability drop out of this definition` | bracket | agency is defined five times and the components disagree | [text of the bracket] | glossary: agency; canonical home |

The columns mean this. **ID** is lane, chapter, running number. **Find** is a string the integrator pastes into Ctrl+F, long enough to match once, copied exactly from the snapshot (curly quotes and all). **Class** is one of `fix-direct` (mechanical), `relocate` (her unaltered words move; say where), `delete-duplicate` (one of two copies goes; say which home keeps it), `rename` (a ruled rename), `bracket` (a suggestion or challenge she decides), `decision` (needs a ruling; name the P-item or propose a new one), `open-item` (something only she can supply). **What** states the observation in one or two sentences. **Proposed** carries the exact replacement text for a fix, the exact bracket text for a bracket, or the outline for scaffolding; it is empty for a pure observation. **Why** names the governing thing: a proposition number, a glossary term, a claim type, a ruling, a voice-guide marker, a findings item.

Run `python3 scripts/manuscript_check.py --in <snapshot> --packets revision/packets/` before handing a packet in; every Find string must match exactly once.

## Running a pass

1. Snapshot. Export the Working Copy to markdown into `revision/manuscript/working-copy-<date>.md`; commit. Run the checker into `revision/reports/check-<date>.md`; commit.
2. Read the ledger. If a P-item you depend on has been ruled since the last pass, the ruling wins.
3. Launch the six lanes, one agent each, on all chapters or on a chapter range. In Claude Code: `claude "Load the book-revision skill, then the book-lane-arc skill, and run it on chapters 1 through 5 of the current snapshot."` (one line per lane; the lane names are in the table above). In Cowork: start a session with the same sentence.
4. When the lanes have committed their packets, run the integrator on each chapter. It produces `revision/integrated/<chapter-id>.md` (the chapter text with direct fixes applied and brackets in place) and `revision/integrated/<chapter-id>-changes.md` (every applied change, every bracket, every open item).
5. Rerun the checker on the integrated text and compare with the first report: dash density down, residue at zero, no pointer to a chapter that does not exist, duplicates only where the ledger says the return is deliberate.
6. Write-back to the Doc follows decision P18.

## What an agent never does

Ask Katherine a question mid-lane that a P-item default already answers. Change a word of hers outside the direct-fix list. Reproduce a student scene from memory or invention. Add a marker system. Delete a file. Work outside its packet folder. Re-argue a ruling.

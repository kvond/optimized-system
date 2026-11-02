---
name: book-revision
description: The spine for revising Answerable Teaching. Load it first in any session that revises, restructures, tightens, or checks the manuscript. It sets the rules every revision agent shares (where the text lives, the prose rule, the argument arc, the glossary and its analytical levels, the claim types, the decisions ledger, the lane system and packet format), and it tells an agent which lane to load next. Triggers - "revise the book", "revision pass", "run a lane", "book-revision".
---

# Book revision: the spine

Read this before any lane. It is short on purpose; the lanes carry the work lists.

Before drafting or running a lane, read the current live manuscript and [current writing-voice guidance](../../ai-ops/knowledge/writing-voice.md), including the linked October 17 author corrections. The manuscript is the primary voice evidence. Later author rulings govern over older findings or an editor's preferred structure; structural suggestions remain suggestions until authorized.

## Entry: scope and degrees of freedom

Always read this entry, including the prose rule, ownership boundaries and completion loop, before selecting detail. Read the latest author draft and rulings before editorial work. Do not infer write-back, publication, merge or graph-change authority from this skill.

- **Low freedom — integrity and delivery:** exact source/version, citations, author-text preservation, lane ownership, approved changes and save/readback evidence. Follow the current delivery rule; no invented facts or unverified completion.
- **Medium freedom — approved editorial process:** choose the smallest relevant lane/chapter scope and useful order of checks within the requested pass. Do not change her meaning or bypass the prose rule.
- **High freedom — requested brainstorming only:** explore alternatives when Katherine asks; label them as proposals, not accepted text. No autonomous substantive rewrite.

Load only the references required by the selected work below, not every file. A requested full-lane pass still requires all six packets.

## Contents — read only what this task needs

Always read the entry constraints first. Then load only the selected detail; do not crawl every reference.

| Task | Read |
|---|---|
| Every invocation | Entry, prose rule, ownership and completion loop in this file |
| Find current inputs | [Source map](reference/source-map.md) |
| Run a lane or analyze claims/terms/argument | [Lane framework](reference/lane-framework.md), then selected lane |
| Write/check packets; run full pass; authorized delivery | [Pass protocol](reference/pass-protocol.md) |

## What a revision pass is

A requested full-lane revision pass takes one dated snapshot of the manuscript, runs six lanes over it in parallel, and then runs one integration step. A narrowly scoped editing or checking request does not automatically launch all six lanes; use only the work needed for that request and do not describe it as a complete six-lane pass. Once the full-lane pipeline is invoked, preserve its six-packet integration requirements. A lane is a single concern (the argument arc, the terms, the claims, the notes and attributions, the continuity of cases and pointers, the residue and mechanics). Each lane reads the snapshot and writes packets, one packet per chapter, into its own folder. No lane touches the manuscript. The integrator reads every packet for a chapter, applies what the prose rule allows, and leaves the rest in brackets for Katherine. Several agents can run at once because they never write to the same place: a lane owns its packet folder and nothing else.

## Where things are

Before locating or reading manuscript inputs, read the [source map](reference/source-map.md). Resolve current bindings; do not substitute historical copies.

## The four documents that govern every lane

Before running any lane, read the [governing documents and analytical framework](reference/lane-framework.md), then the applicable existing linked sources.

## The prose rule

Her words are not altered except mechanically and grammatically, with minor phrasing and removal of redundancies. Everything else appears in the manuscript only inside [brackets] as a suggestion she chooses to act on or not, including any challenge to her thinking. The single live Google Doc is always canonical. No new marker system is introduced: no provenance tags (retired 2026-09-11), no status codes in prose. A bracket is the only thing an agent adds to her text.

What the integrator may apply directly: agreement and pronoun slips, doubled words, homophones, spacing, punctuation, citation format and missing years, a comma-spliced appositive resolved with parentheses or a second sentence, redundant restatement within a paragraph, an em dash replaced by the hinge she uses (colon, semicolon, comma, parentheses, period), a ruled rename applied at every occurrence (R2, R9), an ordering or relocation of her own unaltered words when a ruling or the canonical-home convention calls for it, and deletion of editorial residue that is not prose once its content is logged in the ledger.

What stays in brackets: any new sentence, any rewording beyond minor phrasing, any cut of her prose, any change to what a passage claims, the wording of a pointer sentence, and every challenge. Scaffolding (a proposed passage she will rewrite) goes in the packet, and enters the manuscript only as a bracket that names the packet row.

Never invent a student scene or a classroom detail. Never invent a citation. Never write the disclosure statement for her.

## Claim types

For claim analysis, read the claim types in [lane framework](reference/lane-framework.md).

## The analytical levels

For term or conceptual analysis, read the analytical levels in [lane framework](reference/lane-framework.md).

## The argument, in twelve lines

For argument analysis, read the argument in [lane framework](reference/lane-framework.md).

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

Before writing or checking a packet, read the exact [packet and pass protocol](reference/pass-protocol.md).

## Running a pass

Before a full revision pass or authorized delivery, read the [pass protocol](reference/pass-protocol.md). Scope still follows this entry; do not launch six lanes for a narrow request.

## Recursive improvement after actual use

Finish the requested work before reviewing the procedure. In the existing pass report or change list, compare the promised result with the actual verified result and Katherine's feedback. Revisit the previous procedural improvement on its next applicable real use: keep it if the evidence supports its benefit, revise or reverse it within existing authorization if it adds errors or unnecessary work, or leave it pending when evidence is insufficient. A test or instruction edit is not proof of improvement in the manuscript or delivery.

For a worthwhile bounded change, record the observed problem or opportunity, expected benefit, exact procedural change, verification evidence, owner and next actual-use check. Do not force a change after every use, invent measures, create another tracker or recursively launch more agents. Broader changes need the specific approval they require. Preserve the author's judgment, latest draft, voice and accepted passages; procedural improvement grants no substantive editing or publication authority. The whole-book handoff review is defined in the existing [book operations contract](../../ai-ops/workflow-contracts/non-school-contracts.md#book-manuscript-operations).

## What an agent never does

Ask Katherine a question mid-lane that a P-item default already answers. Change a word of hers outside the direct-fix list. Reproduce a student scene from memory or invention. Add a marker system. Delete a file. Work outside its packet folder. Re-argue a ruling. Propose a bracket that pulls the argument toward the field's consensus (engagement as the goal, voice and choice as the method, direct instruction as suspect): her check 9 says such a suggestion is probably wrong, and it does not go in a packet.

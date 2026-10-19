---
name: repaginate-taught-lesson
description: "Repair slide-number references after Katherine teaches a lesson and adds or rearranges slides. Use for post-teaching repagination of a selected teacher deck while retaining added material and separate lesson identities. This is reference cleanup, not lesson renewal or publication."
---

# Repaginate a taught lesson

Bring revision instructions, teacher indexes, speaker notes, and other slide references into agreement with the teacher deck's actual saved order. Preserve the lesson Katherine taught, including everything she added. A repaired reference is not a release approval.

## Bind the lesson and scope

- Read the repository's `AGENTS.md`, `ai-ops/NAMES.md`, `ai-ops/HANDOFF.md`, and `ai-ops/worker-registry/roles-and-schedules.md` before acting. Use the connected account authorized for the selected teacher file.
- Bind course, lesson title/cycle, exact teacher deck ID, and the relevant Master Agenda row(s). Use current `Agenda 26-27 CLEAN` from `ai-ops/NAMES.md`; older VT examples cite a superseded Agenda.
- A week is a scheduling container, not lesson identity. Keep two lessons in one week separate; a lesson spanning two weeks remains one lesson. Do not merge decks, infer identity from week number alone, or change teaching/due dates.
- Confirm that this is the intended taught teacher version, not an older original, repair draft, public release, or student copy. If the supplied link and Agenda disagree, explain the exact conflicting IDs and resolve the target before writing.
- Respect protected-deck restrictions and existing writer claims. If Katherine is editing the deck, inspect and prepare the patch only. In coordinated work, confirm one writer owns this deck and any dependent Agenda cells.

The selected deck's reference edits are within a request to repaginate it. An Agenda edit needs authorization covering that dependent change; use existing authorization when present rather than asking again. No permission, sharing, Schoology, student-copy, public-link, or release changes are implied.

## Resolve references before changing them

1. Save a private before-snapshot: source revision, ordered slide IDs and one-based positions, titles/content anchors, speaker notes, internal links, media, and scoring markers/inventory. Work from the native source; do not round-trip a Google Slides deck through PPTX to repair numbers.
2. Inventory references in visible text, tables, speaker notes, revision steps, teacher navigation, teacher notes, image credits, and hyperlink labels/targets. Search variants such as `slide 12`, `slides 12–14`, `p. 12`, and numbered indexes; distinguish actual slide references from dates, question/item numbers, citations, quantities, and codes.
3. Resolve each intended target by stable slide ID, a prior verified ID-to-position map, or a unique content anchor corroborated by its context. The old number alone is not evidence: slide12 today may be different from the slide meant by an old instruction. Duplicate titles, missing targets, and conflicting text/link destinations require investigation, not a nearest-title guess.
4. Prepare a small ledger: source slide ID/current number or Agenda cell, exact old text, intended target ID(s), evidence, current number(s), and proposed replacement. A range refers to a set of slides: retain that set if moves make it noncontiguous, using an explicit list where needed rather than silently including different work.

Preserve internal links that already use the correct stable target ID; update their stale displayed number only. A positional or broken link can be repaired when its intended target is established. Do not replace an unrelated live destination or normalize every URL. For an ambiguous/deleted target, leave that reference intact, record the exact source slide/cell and candidate targets, and continue independent unambiguous repairs. Ask only for the smallest unresolved decision.

Reference precedents: `skills/vt-skill/SKILL.md` §2.0b **Renumbering** and §11 require checking prose and speaker-note references against the render. Its §16.4 supplies Agenda preservation rules. Consult those relevant passages; this skill does not invoke the full renewal, content-rewrite, code-embedding, or archive workflow.

## Apply and verify

- Preserve the saved slide order and all existing slides, added content, media, response boxes, answer keys, and codes. Do not create page-number furniture, reorder to make old numbers fit, or renumber cycle/lesson/code identifiers. Change only resolved reference text and necessary reference targets, preserving surrounding formatting.
- Read the revision immediately before writing and require it to match the prepared patch when the API supports a revision guard. If it changed, discard the stale patch, re-read, and recompute; do not overwrite newer work. If conditional writes are unavailable, confirm the writer is idle and compare the exact source elements immediately before the smallest write. An uncertain save requires readback reconciliation before any retry.
- For authorized dependent Agenda repairs, freshly read the exact lesson cells. Update only their verified reference fragments; preserve formulas, rich links, unrelated lesson text, dates, and formatting. Leave other lessons in the same week alone. A deck and Agenda are separate saves: report partial completion if one succeeds and the other cannot be verified.
- Read the saved deck back. Verify each changed reference resolves to the intended current target; compare slide IDs/order/count, non-reference text, notes, media, and exact scoring markers/inventory against the snapshot. Ignore only provider-generated transient fields such as expiring image URLs. Added content must still be present.
- Render and inspect every changed visible page and its referenced target; read changed speaker notes and Agenda cells back separately. Confirm no clipping or altered meaning. Use current repository checks when relevant; fixture/lint success alone does not verify the native save or every reference.

Report the deck link, saved revision, changed slide references/cells, preservation checks, and unresolved references with exact context. Distinguish **references repaired** from **lesson ready for release**. If all references were already correct, report the verified no-op without rewriting the deck. Publication, next-year rollout, renewal, grading, and evidence-code redesign remain separate work.

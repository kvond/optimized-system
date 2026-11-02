---
name: manuscript-ops
description: "Operations over the current manuscript: stage verified read-only inputs, render reading copies, run continuity checks, report citation gaps, and compile derived deliverable docx. Roam exports are historical reconciliation inputs. Never generates or edits prose. Triggers: staging/exporting the manuscript, consistency or citation pass, \"compile for editor/committee\"."
---

# Manuscript-Ops — operations over the manuscript files

The mechanical, structural work around the manuscript, kept strictly separate from the
thinking. This skill never writes prose and never edits a chapter — argument generation and
revision stay in the Book Project. Here Cowork only renders, checks, compiles, and flags.

Read [current writing-voice guidance](../../ai-ops/knowledge/writing-voice.md), the
[book-revision source table](../book-revision/SKILL.md) and the
[manuscript operations contract](../../ai-ops/workflow-contracts/definitions/book-manuscript-operations.json).
The single live manuscript is **Answerable Teaching — Full added notes**, at the existing
Google Doc bound in that source table. Katherine's latest draft controls. Roam, older
Working Copy documents and `source/`/`writing/` exports are historical reconciliation
sources, never a replacement for current text. The September P18 observation is history,
not an instruction to reopen the source decision.

GitHub backup/version history belongs in the designated private manuscript repository under
its [delivery rule](https://github.com/kvond/Answerable-Teaching/blob/main/revision/MANUSCRIPT-DELIVERY-RULE.md).
This skill produces derived checks/artifacts only; it does not perform canonical writeback,
backup commits or publishing. Keep private prose and identifying cases out of this repo.

## Entry: scope and degrees of freedom

Always read this entry and its Safety section. This is a derived-check/artifact skill: no prose edits, canonical write-back, publishing or backup commits. Preserve the latest author draft and exact source binding; use historical exports only for explicitly scoped reconciliation. Read only the selected job reference, plus the staging/defaults reference when obtaining inputs or choosing a checker.

- **Low freedom — source and artifact integrity:** exact revision, complete authorized inputs, supported checker, citations and verified output. Do not represent a planned checker as executable or a derived file as accepted manuscript text.
- **Medium freedom — approved process:** choose an appropriate existing checker/rendering route and useful report organization within the requested job.
- **High freedom — requested brainstorming only:** propose future checks or presentation options; no new claim, implementation, prose change or publication follows automatically.

## Contents — read only what this task needs

Always read the entry constraints first. Then load only the selected detail; do not crawl every reference.

| Task | Read |
|---|---|
| Every invocation | Entry, authorship, retention and Safety in this file |
| Stage inputs or select supported tools | [Staging and tools](reference/staging-and-tools.md) |
| Consistency or citation check; derived deliverable | [Checks and derived deliverables](reference/check-and-deliver.md), selected job only |

## Authorship (ruled Sept 11, 2026)

The provenance record keeping is retired. No [Y] / [CO] / [C] tags, no contribution ledger,
no entries to the Roam "Provenance & AI-Use" page, and no provenance note prepended to a
compiled deliverable. The book is Katherine's intellectual work, produced through her own
drafting, conversation with AI, and her redrafting. The voice file
(`book-compile/voice-guide.md` in `kvond/Answerable-Teaching`) carries the same ruling.

## Bundled scripts

Before selecting a checker or renderer, read [staging and tools](reference/staging-and-tools.md); planned tools must not be reported as run.

## Defaults for this manuscript

Before obtaining input, read the exact source and artifact defaults in [staging and tools](reference/staging-and-tools.md).

## Version retention (Drive working copies)

The existing Full added notes Doc remains the single live manuscript. Preserve its identity,
history and current author text; derived deliverables do not become additional live copies.

- **One live doc.** Use the existing **Answerable Teaching — Full added notes** binding;
  do not rename it to the historical `Answerable Teaching — LIVE` title. Authorized
  apparatus, formatting, APA-7, and HEP-flag passes happen
  *in place* in that doc, versioned through File → Version history (name each version per
  pass: "Ch2 notes renumbered", "APA-7", "mechanical + HEP flags"). Never clone-and-suffix
  into a new copy — that habit is what produced the swarm.
- **Preserve history.** This invocation does not move, delete, rename or change access to
  existing documents. Any separate archive action follows its own authorization.
- **Preserve the binding.** Verify the account/source specified by the source table rather
  than creating another copy or changing ownership.
- **No Roam paste-back.** Roam remains archive/source. Current manuscript delivery follows
  the designated repository's GitHub-first rule, with exact commit and Doc readback; this
  derived-check invocation does not execute that write sequence.

Retention convention only — never touches argument or wording.

## Invoking

One-line requests trigger the matching job with these defaults; nothing writes to Roam or
to the manuscript without showing you the result first:
- "stage the manuscript" / "sync the chapters" → job 2
- "run a consistency pass" / "check cross-references" → job 1
- "check the citations" → job 3
- "compile the manuscript" / "make a docx for the editor" → job 4

## Job 2 — staging / export (the foundation)

For staging, read [staging and tools](reference/staging-and-tools.md).

## Job 1 — consistency pass (on-demand, e.g. pre-submission)

For consistency checks, read the relevant job in [checks and derived deliverables](reference/check-and-deliver.md).

## Job 3 — citation integrity (on-demand)

For citation checks, read [checks and derived deliverables](reference/check-and-deliver.md); the planned checker limitation remains mandatory.

## Job 4 — deliverables (on-demand)

For a derived reading deliverable, read [checks and derived deliverables](reference/check-and-deliver.md); this grants no manuscript-write authority.

## Safety

- Never edit the manuscript. Reading copies and reports are derived and advisory; canonical
  changes require their own accepted change list and authorized writeback/readback.
- Verify the current Doc revision and completeness before checks; historical `source/`
  exports do not establish current state or authorize a backup commit.
- The reading render is a convenience copy, not a typeset proof — an inline editorial aside
  left next to a stripped `{{TODO}}` may survive into `writing/`. Don't treat it as final.

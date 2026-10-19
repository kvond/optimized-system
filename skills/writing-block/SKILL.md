---
name: writing-block
description: >
  Build the ≤2-hour Writing Brief — separate from the morning brief. Reads each chapter's Writing
  Status, picks ONE focus chapter, sequences prep → write → place, flags overflow past 2h.
  Triggers: "writing brief", "author block", "what do I write today", writing-brief trigger link,
  scheduled writing-brief run.
---

# writing-block — the ≤2h Writing Brief + the chapter pipeline

A sibling to daily-agenda, not a section of it. The morning brief stays for capture and
musings; this brief is triggered when you're ready to write. It never writes prose — it
sequences your session, advances the chapter through a fixed pipeline, and points the
supporting skills at the right work.

## Why separate + on-demand [HARD]

Mornings are for musings. So writing-block: is **never merged into the daily-agenda morning
brief** (separate output, separate trigger); is launched by the ✍️ AUTHOR BLOCK trigger line in
the daily brief; and **caps the suggested session at 2 hours [HARD]**.

## The [[Author Block]] page (home)

One board page, parallel to `[[AIHS Block]]` / `[[WilmU Block]]`. It holds:

- **`Status::`** — one line: focus chapter · current stage · single next action (same shape as
  the block-update status notes; feeds the daily brief's AUTHOR line).
- **The Stage Board** — one row per chapter, Intro → Ch 11, each with a `Stage::` value
  (vocabulary below) and a compact `Sections::` checklist for chapters in drafting.
- The rendered Writing Brief for the current session (regenerated each run, not accreted).

Roam remains canonical. The board is a pointer/status layer — prose lives in the chapter
pages, deep material in chapter-bank, compiled copy in manuscript-ops.

## Stage vocabulary (the pipeline) [HARD ordering]

Each chapter advances through these in order; the Stage value makes the pipeline resumable.

1. **drafting** — section loop. Draft one section at a time from banked notes + open QUE.
   Provenance is enforced here, at draft time: a section draws from promoted CLM/EVD nodes, so
   each claim already traces to its evidence. Light per-section self-check (does this earn its
   place · is the move clear) — not full HEP.
2. **feedback** — chapter-level, once all sections are drafted. Full Claude critique + full
   hep-scout. Heavy critique once per chapter, not per section.
3. **redraft** — incorporate chapter-level feedback in one consolidated pass.
4. **integrity** — fused check pass, delegated to manuscript-ops: references + endnotes +
   provenance-confirmation read as ONE pass. Extraction + flagging only; fixes go back into
   Roam, by you.
5. **in-docs** — handoff. The Roam chapter is **frozen (read-only)** the moment it crosses to
   Google Docs (treat like RAW_ORIGINALS). One Docs session, in order: **Grammarly** pass
   (external — Claude doesn't do this well) → **Perplexity** pass (final feedback + a
   "literature I should consider" sweep against a different database; surfaced lit is filed to
   chapter-bank, doesn't silently reopen the chapter) → **final read**. One crossing per
   chapter — all three in the same session.
6. **paste-back** — paste the final Docs chapter over the Roam chapter, restoring Roam as the
   single system of record. Unfreeze. (Docs is authority only during in-docs; paste-back
   collapses the fork.)
7. **done** — eligible to hand focus to the next held chapter.

**Pre-handoff gate [HARD]** — a chapter may not enter in-docs until: no open QUE · notes bank
drained · integrity flags resolved. Stops a half-baked chapter from eating a
Grammarly/Perplexity pass.

**Intro + front matter [HARD]** — lock a one-paragraph thesis early so chapters stay coherent,
but draft the Intro last: it's a board row held until the body chapters are done. Front matter ·
Intro · whole-manuscript references get a final cross-manuscript check after the last body
chapter clears — run via manuscript-ops, never re-derived here.

## Inputs (read-only)

- The Stage Board on `[[Author Block]]` — each chapter's `Stage::` + `Sections::`.
- Per-chapter notes banks (chapter-bank) + the Claims Hub — the depth signal for prep-readiness.
- `[[Answerable Teaching/Writing Log]]` + the latest State-of-book note — your running read,
  which **overrides heuristics**.
- The `Chapter notes to add` roadmap on `[[**Book**]]` — seeds the `Sections::` checklist.

## Focus selection — ONE chapter

- Honor an explicit current chapter if your Status/Log names one; others are named as **held**,
  not scheduled.
- Else pick the highest-priority chapter that is unblocked (reconfigure flag clear) with ready
  inputs — a drafting chapter with a drained-enough bank beats a nearly-done one with an empty
  bank. An integrity/paste-back chapter needing only a mechanical pass can ride alongside as a
  quick-clear.
- Surface the choice with a one-line rationale; you can override. Never propose two chapters'
  *writing* in one session.

## The slice — phase-sequenced by current stage

Each phase time-estimated, running total ≤2h:

- **drafting** → (a) **Prep** [I do]: organize the section's banked notes + best-phrasing into
  an outline you write from (scaffold only, `(Claude)`-tagged where I phrased anything, no
  prose) → (b) **Write** [you do]: draft in small chunks; paste Perplexity/Scite returns into
  the research-anchor lane (filed by chapter-bank) → (c) **Place** [you do]: drop the section
  in, tick `Sections::`.
- **feedback** → I run Claude critique + hep-scout; you get a consolidated findings list.
- **redraft** → I lay out the change-list by section; you revise.
- **integrity** → I trigger the manuscript-ops fused pass; you resolve flags in Roam.
- **in-docs** → checklist for the single Docs session (Grammarly → Perplexity → final read).
  I don't enter Docs; I sequence it.
- **paste-back** → reminder + the one action: paste final over the Roam chapter, unfreeze,
  mark done.

**The 2-hour cap [HARD].** Suggested writing never exceeds 2h; overflow is flagged "next
session." Prep, placement, and mechanical stages are light; the cap protects the deep-write
middle of drafting/redraft.

## The hour-3 close (adopted Aug 4 2026 — [[✍ Session Protocol — the 3-hour engine]])

The full session shape is 2h deep write + 1h mechanical close; the close feeds the Substack
and journal lanes so neither needs its own deep session. The brief sequences the close after
the cap, as checklist acts (they survive a low-bandwidth day):

- **Place** (2:00–2:15) — section into the chapter page, tick `Sections::`.
- **Substack stamp** (2:15–2:35) — ONE candidate from today's writing (a zettel leaned on, or
  a cut passage) → one row on `[[📰 Publication Registry]]` with its source link.
- **Reference stamp** (2:35–2:50) — every citation touched, doubted, or wished for → one row
  on `[[📚 Reading Queue]]`, linked to the argument it serves; statuses ticked forward.
- **Exit stamp** (2:50–3:00) — `Writing Status::` gets stage · section · **the next sentence
  you would have written** (the Hemingway stop); one summary line to the daily page.

Short day: close compresses to Place + Exit stamp; lane stamps roll forward. The deep write
is never cut short mid-paragraph. Full beats live on the Session Protocol page in Roam.

## Delegate, don't reimplement [HARD]

Notes bank + claim/evidence + filed lit → **chapter-bank**. References, endnotes,
provenance-confirmation, reading render, consistency, compiled docx, whole-manuscript citation
check → **manuscript-ops**. HEP critique → **hep-scout**. Page mints → **book-ops
on_create_check**. Morning time-blocking → **daily-agenda**. writing-block only sequences,
advances the Stage, and points. Never writes prose; never edits the manuscript or the Docs copy.

## Reconfigure path

If the focus chapter's reconfigure flag is set, don't propose writing it. Route to
chapter-bank's reconfigure path (re-route banked material → reset Stage to drafting + clear
`Sections::` → re-enter), then re-select a focus chapter.

## Output

A standalone Writing Brief, rendered onto `[[Author Block]]`:

```
✍️ WRITING BRIEF — [date] · Focus: Ch N — [title] · Stage: [stage]   (held: Ch …, Ch …)
   Why this chapter: [one line]
   ── slice for [stage] ──
   (a) PREP [~Xm] …   (b) WRITE [~Ym] …   (c) PLACE [~Zm] …
   ───────────  suggested writing ≤ 2h   [OVERFLOW → next session: …]
   Pre-handoff gate: ☐ no open QUE  ☐ bank drained  ☐ integrity flags clear
   Next action: [the single next thing]
   ── board ──  Intro:held · Ch1:done · Ch2:in-docs · Ch3:drafting · … · Ch11:held
```

## Scheduling

Manual, from the daily-brief trigger link, or a local Cowork scheduled task (e.g. an afternoon
writing window). Cloud Routine is fine; the output is the same Brief.

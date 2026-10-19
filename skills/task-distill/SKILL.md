---
name: task-distill
description: >
  Distill open {{[[TODO]]}}s on [[📋 TASKS]] into one ordered two-way view — area → month → day,
  rendered as embeds (not refs) so ticks propagate. Composes with daily-agenda; leaves Admin Queue
  + registry untouched. Triggers: "distill my tasks", "task distill", "rebuild the task view",
  scheduled task-distill run.
---

# task-distill — one ordered, two-way view of the task page

Turns `[[📋 TASKS]]` into a single distilled list grouped **by area, then month, then day** —
rendered as live **embeds** of the source TODOs so it is a *view*, not a copy: tick a box
anywhere and every appearance flips together. General task utility; **no book dependency** —
never calls book-ops, chapter-bank, or manuscript-ops.

**Reference file:** the raw-import **leftover sweep** (propose-then-delete culling of the
bottom-of-page remnant) lives in `reference/leftover-sweep.md` — read it only when running that
sweep. The remnant is otherwise simply **not a source** for the view.

## Why a separate view — composition with daily-agenda [HARD]

`daily-agenda` already reads two regions of `[[📋 TASKS]]`: the `## 🗂️ Admin Queue` embeds and
the `Categories → where they route` registry. task-distill **must not disturb either** — it
writes only its **own** block (default heading `## ⏱ Distilled — area × month`). So:

- It **reads** the registry to resolve areas (single source of truth — never hardcode).
- It **leaves** the Admin Queue and the MONTH scan-ahead exactly as they are.
- Its output is **derived and regenerable** — re-running replaces its own block in place and
  touches nothing else.

## The two-way mechanism — embeds, not refs [HARD]

The whole point is tick-sync. Each line is `{{[[embed]]: ((<source-uid>))}}` — an **embed of the
source TODO block**, so its checkbox is the *same* checkbox as the source. A plain `((ref))`
renders read-only and breaks the sync; never use one here.

- **End-to-end validation (first run).** Before building the full view, prove the mechanism on
  one block: embed a single source TODO, confirm with Katherine that ticking it in the view
  flips the source (and vice-versa), then proceed. This is the acceptance test for the skill.
- task-distill **never edits the source TODO's text or status** — it only references it.

## Defaults for this graph (override per run only if needed)

- **Source page** — `[[📋 TASKS]]`, the **organized** layer. Default scope = open `{{[[TODO]]}}`
  blocks in the organized regions: Admin Queue embeds, the
  `[[AIHS]]/[[CALLS]]/[[FINANCE]]/[[ERRANDS]]` area lines, and the MONTH section. *Confirmed:*
  graph-wide category-tagged TODOs on daily/project pages are **out of scope** by default — set
  `scope: graph` to include them.
- **The raw-import remnant** at the bottom of the page (old Google Takeout dumps) is **not a
  source** — see the reference file for its cull.
- **Area registry** — read live from the `Categories → where they route` block. Current mapping:
  `[[AIHS]]·[[CALLS]]·[[FINANCE]]·#[[Curriculum 26-27]]·#[[AI Workflows]]·#[[AI Agents]]·
  #[[Wilmington University 7106]]·[[FAMILY]] → Admin`; `[[ERRANDS]] → Errands`;
  `#Book/#[[Beyond Motivation]] → Author`. Within **Admin**, surface **Finance · Errands ·
  Calls** first, then the rest (Teaching/Schoology, AI Systems, WilmU, Family).
- **Month + day tags** — month from `#JULY/#AUG/#SEPT/…`; day from a **bare number after the
  month** (`#AUG 25` → Aug 25). No month tag → a **Standing / undated** bucket, shown last.
- **Status** — include `{{[[TODO]]}}` only; **exclude `{{[[DONE]]}}`**. (The view shrinks
  naturally as boxes get ticked, since embeds reflect live status.)
- **Output block** — `## ⏱ Distilled — area × month  [[<today>]]`, near the top of
  `[[📋 TASKS]]`, below the Admin Queue. Regenerated in place each run.

If anything reads as stale (renamed registry, new category tag), ask rather than guess.

## Algorithm

1. **Collect.** Pull open `{{[[TODO]]}}` blocks in scope, each with uid, text, tags.
2. **Resolve area.** Match tags against the live registry. A block with no registry tag sitting
   under a labelled Admin Queue sub-header inherits that header's area. Unresolved → an
   **Unfiled** bucket surfaced for you to tag (never force-fit).
3. **Resolve month + day.** Read `#MONTH` + bare day. Multiple month tags → surface for you to
   pick; none → Standing/undated.
4. **Order.** Areas in fixed order **Admin (Finance · Errands · Calls · Teaching · AI Systems ·
   WilmU · Family) → Author → anything else**; within each, month ascending then day ascending;
   undated last.
5. **Render.** Each item as `{{[[embed]]: ((uid))}}` under its area / month subheading.
6. **Stage + confirm.** Build the proposed block, show it, write **only on approval** —
   replacing the prior distilled block, touching nothing else.

## 🛑 Confirm + safety

- **Roam is canonical. Confirm-before-write.** Show the proposed block; write only on OK.
- [HARD] Never edit, reorder, or re-status a **source** TODO. The distilled view is the only
  thing this skill writes, and it is fully regenerable.
- [HARD] Never touch the `## 🗂️ Admin Queue`, the MONTH scan-ahead, or the
  `Categories → route` registry — those are daily-agenda's inputs.
- [HARD] Use `{{[[embed]]: ((uid))}}`, never a read-only `((uid))`, so tick-sync holds.
- No resolvable area or ambiguous month → **surfaced, not guessed**.

## Trigger line & scheduling

The daily brief carries one on-demand launcher line (daily-agenda owns the line; this skill
owns what it launches):
`📋 TASKS → run task-distill · [n] open · [m] dated this month`. Emitting it writes nothing;
running the skill does the work + confirm-gated write.

- **Schedulable** as a local Cowork task (morning or Sunday rebuild) or manual.
- **Outputs:** the regenerated `## ⏱ Distilled — area × month` block; a short run summary
  (counts per area/month · Unfiled or ambiguous items held); the leftover-sweep report when
  that sweep is run.

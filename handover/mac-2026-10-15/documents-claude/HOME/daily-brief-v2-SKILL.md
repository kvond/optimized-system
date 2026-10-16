---
name: daily-brief-v2
description: Assemble Katherine's daily brief — deliver the full brief in chat AND write today's Roam daily page. Schedule-first: work lanes, habit ticks, and look-ahead all live inside the schedule spine so the day reads top-to-bottom with no cross-referencing.
---

# daily-brief-v2

Assemble the daily brief for TODAY. Deliver the FULL brief in CHAT (run output) AND write it to today's Roam daily page.

## Design principle

**The day reads top-to-bottom, once.** Everything that belongs to a block of time sits *inside* that block of time. There is no separate Status section, no separate Habits section, no separate Week-at-a-glance — those all required visual coordination across the page and are gone.

Roam blocks live in multiple places, so this costs nothing: the schedule EMBEDS source blocks (`{{[[embed]]: ((uid))}}`) rather than restating them. One block appears on its home page, on the daily page, and in any block page at once, and ticks propagate everywhere.

**The lane embed is the stopping point.** Each work block's lane sits as the LAST child of its schedule window. At the end of that window you tick what's done and write tomorrow's next item into the lane — same place you were already looking. Tomorrow's brief reads it back out.

## Model of the graph

- **Status SSOT** remains the page **[[🧱 Status of the blocks]]** (lowercase "blocks"). FOUR lanes, each label a page ref: 🍎 [[AIHS Block]] · ✍ [[Author Block]] · 🎓 [[WilmU Block]] · 🗂️ [[Admin Block]]. This page is unchanged and is still where next-items live. **The daily page no longer mirrors it as a section** — the lanes are embedded inside their schedule windows instead.
- The first three are WORK lanes Katherine writes TODOs under directly. The 🗂️ Admin lane carries the admin task window as embeds of [[Admin Block]]'s own sections (🔜 NEXT first, then selected backlog sections per §2).
- **[[Admin Block]]** is THE personal task page: 🔜 NEXT at the top, then backlog (areas · [[MONTH]] buckets · 🗂️ Admin Queue · ⚙️ System registry · ✉️ Emails).
- **Work next-items** (AIHS, WilmU, Book/writing, curriculum, AI-systems) flow through the Status page. **Personal life-admin** lives on [[Admin Block]]. Nothing is in both.

**RETIRED — never fetch, write to, or re-mint:** `📋 TASKS` · `AIHS` page · `Status of the Blocks retired shell` · `Strength Block` (use [[Strength]]) · `Swim Block`. Do not re-create [[Tasks]] or [[TODO]]. **Also retired: the 🌙 End-of-Day habit block** — habit ticks now live in the schedule (§Habits).

## Efficiency rules

- **PARALLEL GATHER:** fire all independent source reads concurrently (email, Tiller snapshot, Roam pages, calendar). Presentation order is NOT fetch order.
- **RETRIES:** on any failed or timed-out call, retry ONCE with short backoff, then move on and note the gap. Never hang the run on a slow source.
- **EMBEDS:** resolve ALL needed uids in ONE `roam_datomic_query` (batch by uid) — never one `roam_fetch_block` per embed.
- **SEASON GATE:** through **Aug 24, 2026** it is SUMMER — do NOT load the daily-agenda skill; build the spine from the inline summer rhythm in §Schedule. From **Aug 25, 2026** on, use the daily-agenda skill for the bell-schedule spine, with the source rules in THIS task superseding its SOURCES section.
- **ROAM WRITE:** the date page ALWAYS already exists. NEVER use `roam_create_page` for the daily note. ALWAYS fetch the page by title for its `page_uid` + current blocks, then write the MISSING sections with ONE `roam_process_batch_actions` (the Status-page prune and the Admin NEXT prune ride in the same batch). Roam rejects empty strings — use `" "` for a blank scaffold child, `"{{[[TODO]]}} "` for an empty checkbox.

## Rendering rule

- **PAGE copy:** work lanes and the admin task window are EMBEDS of source blocks — never restated text. Email, Tiller, Look-ahead are plain text. In plain-text lines avoid bare routing tags (`#near`, `#FINANCE`) so the nightly daily-route doesn't treat brief lines as captures; `[[rhythm-block]]` page refs are fine.
- **CHAT copy:** embeds don't render in chat, so render the lanes as plain-text lines that note the source (e.g. "[[Admin Block]] · NEXT") so items can be found and ticked at the source.
- **Lists, not paragraphs.** Email and Tiller are bullet lists. This is not optional.

## Re-run / idempotency (check FIRST, before writing)

The ONLY signal for whether to write a section is whether **that section's header already exists on today's daily page**. Fetch today's page with `roam_fetch_page_by_title` (format "structure") and check for each header. Do NOT infer "a brief already ran today" from anything else — the `Processed:` marker on [[🧱 Status of the blocks]] governs ONLY the Status-page prune loop.

Sections this task writes: **📝 Quick Notes** · **🗓 Schedule** · **📋 Daily Brief** · **✍ Journal**. Exactly ONE of each per day, in that order. If a header is ABSENT, create it. If PRESENT, do NOT duplicate or overwrite — LEAVE UNTOUCHED anything filled in by hand (Quick Notes captures, ticked habits, Journal entries, edits). When in doubt whether a block is hers, never delete it. Other tasks (nightly distill, weekly sweep) own their own blocks — never delete those.

---

# Sources

## 1. Email (bullet list)

All four accounts forward into ONE inbox: kvond12@gmail.com (the only connected Gmail).

**GATE — direct-to-me only.** Surface a message ONLY if one of Katherine's four addresses is in the **To** line. This is the SINGLE gate and it applies to EVERYTHING, including school and WilmU: if she is only CC'd/BCC'd, on a distribution list, or the message is automated / no-reply / notification / digest / marketing / survey (Proofpoint quarantine digests, Canvas / instructure.com notifications, course surveys, loan-servicer alerts), DROP it — even from redcly.k12.de.us or wilmu.edu.

**WINDOW — no repeats, no gaps.** Compute `after:<epoch>` where:

```
epoch = MAX( previous scheduled run , 12:00 local yesterday )
```

On a normal daily cadence the previous run is earlier than yesterday noon, so the floor wins and the window is **yesterday 12:00 → now**. If a run was skipped, the previous-run anchor wins and nothing falls through the gap. If neither can be computed, fall back to `newer_than:22h`.

**QUERY — one call** (substitute the computed epoch):

```
after:<epoch> -in:sent -category:promotions -category:social -category:updates -category:forums
-from:historyfacts.com -from:tldrnewsletter.com -from:email.informeddelivery.usps.com
-from:updates.jobescape.me -from:substack.com -from:no-reply@equifax.com -from:amazon.com
```

Then apply the direct-to-me gate per message from headers. Extend the exclusion list as new recurring senders appear, but never exclude a correspondent who writes directly.

**RENDER:** a bullet list, grouped by source account (detect from the Gmail label, Delivered-To / X-Forwarded-To header, or forwarding address; if undetectable, mark source unknown). One bullet per message: **sender · subject · one-line context**. Do not mark anything read.

If a dropped message is clearly time-anchored (names a date/day within the next 7 days), add ONE bullet under a `Filtered but time-anchored` sub-bullet. Do not expand this beyond one line each.

## 2. Tasks — [[Admin Block]]

Read [[Admin Block]] with ONE `roam_fetch_page_by_title` (format "structure"). Do NOT read Google Tasks. Do NOT fetch [[Tasks]], [[TODO]], or [[📋 TASKS]].

**NEXT-section prune** (rides in the single write batch): delete `{{[[DONE]]}}` children of the 🔜 NEXT section; if it has no open child, seed ONE empty `"{{[[TODO]]}} "` slot; keep exact wording on open items; **never touch the backlog sections' DONE items** — those are hers to cull.

**Admin lane composition (on the Status page, §4):** DISCOVER [[Admin Block]]'s top-level sections at run time — never assume a fixed list, never hard-code uids. As children of the 🗂️ Admin lane block, write one embed per top-level section (🔜 NEXT first, in page order) plus the CURRENT month bucket. SKIP ⚙️ System registry and ✉️ Emails, and skip empty scaffolding-only sections.

**Selection rules** (what surfaces today): current month bucket only; never surface a task anchored more than ONE MONTH ahead; a bare number after a month tag = day-of-month due; FINANCE items are today-relevant only on Sundays; `#Next` (or `#near` when no `#Next` exists) are the NEXT-slot candidates; propose an errand window (near the 10a gym in summer) when open ERRANDS exist.

## 3. Calendar

Scan ONLY the "Appts" calendar (calendarId `1afa0atpk8s5e0c1hu9950ekd4@group.calendar.google.com`) for today's appointments and the 14-day look-ahead, in ONE `list_events` call. Do NOT scan the Routine/primary calendar.

Today's events are OVERRIDES inside the schedule spine (§Schedule). The 14-day look-ahead goes under 👀 Look-ahead, which lives at the BOTTOM OF THE SCHEDULE — not in the Daily Brief.

## 4. Status of the blocks

Fetch **[[🧱 Status of the blocks]]** (format "structure", ONE call). Keep the lane order found on the page; preserve any annotation on a label.

Each morning, over the THREE WORK lanes only (AIHS · Author · WilmU):

1. **PRUNE:** delete children marked `{{[[DONE]]}}` (do not log or restate them).
2. **SEED:** if a work lane has no open child, seed ONE empty `"{{[[TODO]]}} "` slot — never fabricate a task.
3. Keep exact wording. Plain-note children (e.g. `WAIT:` notes) stay.
4. Update the `Processed: [[date]]` block to today. This marker is for the prune loop ONLY.

The 🗂️ Admin lane is **read-only here** — never prune or seed it on the Status page (its NEXT is pruned via §2). Recompose its section embeds per §2.

**Lanes are NOT written as a daily-page section.** Look the lane uids up fresh each run and embed each lane as the LAST child of its schedule window (§Schedule). A lane with **no schedule window today** (e.g. AIHS in summer) gets ONE plain line under 👀 Look-ahead — `🍎 AIHS — no window today · <its single open item or WAIT note>` — so nothing vanishes silently.

## 5. Habits — ticks live in the schedule

Tracked: **Strength · Uke · Voice · Spanish**. (Voice superseded Swim as of the Jul 9, 2026 row.)

The 🌙 End-of-Day block is **retired**. Instead, each habit appears in the schedule spine as its own checkbox block at its natural time:

```
{{[[TODO]]}} [[Spanish]]
{{[[TODO]]}} [[Strength]] — gym
{{[[TODO]]}} [[Voice]]
{{[[TODO]]}} [[Uke]]
```

**Convention:** ticked → ✓ · left open → ✗ · the word `rest` typed anywhere in the block → rest (does not break a streak). Journal-style notes may be nested as CHILDREN of a habit block; never touch, restate, or harvest the child notes.

The **nightly distill** reads these schedule blocks (not an End-of-Day block) and appends the row to [[Habit Tracker]]. **This task does not compute or display streaks** and does not write to [[Habit Tracker]]. There is no 🌙 Habits subsection in the brief. Full month grid → the Habit Calendar artifact.

**HEALTH FIREWALL** still applies: habit data never appears in book/teaching/summary outputs.

## 6. Tiller (daily, read-only — independent of the Sunday FINANCE gate)

**Source:** the snapshot doc **"TILLER SNAPSHOT — daily (auto)"** in Drive, written each morning by the `tiller_margins_snapshot` Apps Script from the MARGINS v2 dashboard tab. Read it with ONE `read_file_content` call (find by title if the id is not stored). Do NOT read the Tiller workbook directly — its text export starts at Transactions and truncates before the dashboard ever appears.

**RENDER as 💰 Tiller (heading-3) — a LIST, never a paragraph:**

- **Deposits since yesterday** — one bullet each: source · amount.
- **Balances** — one bullet per account: name · balance. Flag any account below its margin target in **red**; note plainly when the savings margin covers a low checking balance (this is normal — do not re-alarm).
- **Budget: plan vs. spent** — one bullet per flow row: `Category · $spent of $plan · $left` — **green** when at or under plan, **red** when over. Sort over-plan rows first, then rows ≥90% of plan, then the rest.
- **Status line** — whatever the dashboard's status cell says (bound warnings, missing budget column, etc.).

If the snapshot doc is missing or stale (generated more than 36h ago), say so in one line and fall back to the newest 8–12 transactions from the workbook, flagging only genuinely anomalous items.

**Retiring recurring flags.** Read the `Muted merchants` list under ⚙️ System registry on [[Admin Block]]. Never flag a merchant on that list. Every NEW flag must terminate in one of two ways — it becomes a TODO on [[Admin Block]], or it gets muted by name. Say so explicitly when raising a new flag, so the same merchant never surfaces twice unresolved.

---

# Output — two destinations

- **CHAT (run output):** the FULL brief — the schedule (with lanes rendered plain-text) and the Daily Brief sections.
- **ROAM (single write call):** fetch today's date page for its `page_uid`, then write the MISSING sections via ONE `roam_process_batch_actions` as children of `page_uid`.

Today's daily note (ordinal-dated title, e.g. "July 12th, 2026") gets these FOUR sections, in this order:

## (1) 📝 Quick Notes — heading-1, TOP of page

Header + ONE empty child (`" "`) as quick-capture scaffold. Above the blank child, add the "🌞 Summer 2026 — orientation" block with refs to [[Summer 2026 Timeline]] and [[Summer 2026 Goals]] and the current dated window (summer only). No generated content beyond that.

## (2) 🗓 Schedule — [Weekday · Date] — heading-1

The day, complete. Everything time-bound lives here.

**First child = the day in one line:** season window · day type · countdown to the next hard deadline · today's single must-do. Nothing else at this level.

**Then the spine, top to bottom.** Standing rhythm blocks — [[Spanish]] → [[Author Block]] → [[Admin Block]] → [[WilmU Block]] — with habit ticks placed at their natural times and real commitments OVERRIDING at their real times (Appts-calendar events prefixed 📅; flag ⚠ on any overlap).

**Each work block carries its lane as its LAST child:**

```
1:00–2:00 · 🗂️ [[Admin Block]]
  └ {{[[embed]]: ((admin-lane-uid))}}
```

The lane embed renders the open items AND is where the next item gets written at the end of the window. That is the stopping point — do not add anything below it inside that block.

**Standing durations & rules:**

- [[Author Block]] ≈ 3h (a real 3h window when the day allows; split around the 10a gym in summer).
- [[Admin Block]] ≤ 1h — 🔜 NEXT list first, backlog second.
- **SUMMER:** gym / [[Strength]] at 10:00a. Fold an ERRANDS window just before or after it when open errands exist.
- **MONDAYS:** add a WilmU research-course lesson-work block — DEEP work in a primary free window, NOT inside Admin.
- **SCHOOL DAY** (from Aug 25, via daily-agenda): the bell schedule replaces the rhythm.
- **TRAVEL DAY:** flights dominate — departures/arrivals with times, layovers as read/write windows, collapse rhythm blocks that don't fit.

**LAST child of the Schedule section = 👀 Look-ahead** (heading-3): the 14-day Appts look-ahead · off-calendar anchors · any lane with no window today (§4) · pull-forward / quick-win candidates. Bullets only.

## (3) 📋 Daily Brief — [Weekday · Date] — heading-1

Only what is NOT time-bound. Two heading-3 subsections, both **bullet lists**, omit either if empty:

- **✉ Email** — grouped by source account (§1).
- **💰 Tiller** — deposits · balances · budget plan vs. spent, green/red (§6).

There is no Status subsection, no Habits subsection, no Week-at-a-glance, and no Look-ahead here. Set these children `open: false` so the page opens as a spine.

## (4) ✍ Journal — heading-1, BOTTOM of page — nothing after it

Header + ONE child as entry point: `[[Strength]]` (training notes accumulate on the [[Strength]] page via linked refs). Plus one blank capture child (`" "`) and one `Reflection:: ` line.

**Nothing is appended after Journal.** It is the terminal section — the visual end of the day.

---

# Resilience

Retry a failed call ONCE with short backoff, then move on. If Roam is unreachable, still deliver the full brief in chat and note "⚠ ROAM SCAFFOLD NOT WRITTEN — Roam unreachable" (idempotency prevents duplicates next run). If Gmail errors, note briefly and continue. If the Tiller snapshot is unreadable, fall back per §6. Never abort the whole run because one source failed.

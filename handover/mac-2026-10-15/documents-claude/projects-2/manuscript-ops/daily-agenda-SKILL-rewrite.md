---
name: daily-agenda
description: >
  Build Katherine's time-blocked agenda for a given day. Detects A-day vs B-day,
  loads that day's period schedule and non-teaching capacity (deep / work / short-tasks),
  reads the Master Agenda (2026-27) for mode + today's topics, pulls Google Calendar
  appointments and Google Tasks due, reads the daily-note Journal → #Status of the Blocks
  to carry each life/work block forward, then assembles one time-blocked plan plus a short
  "attend-to-first" list and a per-block status line. Invoke for "daily agenda", "plan my
  day", "morning brief", or run on a schedule (Cowork scheduled task = local; Claude Code
  Routine = cloud).
---

# Daily Agenda

Produce ONE time-blocked agenda for the target day. Default target = today.

## SOURCES (read-only)
- **Master Agenda — 2026-27 v5** (Google Sheet) ID `1Tqh7eB_I3z-eP9FYMCPvNVclmR9VGXVaae0ZdRICy1g`
  Weekly grid: Wk, MP, "Dates / Off-days", Biology + A&P topic/day columns. Off-days flagged
  with ⚠ and "OFF"/"IN-SERVICE". "Notes due" / "DRAFT due" embedded in cells.
- **Google Calendar** — appointments (today + look-ahead horizon). Read live; never copied.
- **Google Tasks** — one-time todos, lists = groups (due today/overdue + upcoming). Read live; never copied.
- **Daily-note Journal → #Status of the Blocks** — the per-block state notes (one `{{[[TODO]]}}`
  per life/work block: book · WilmU · learning · admin · strength · AI-HS · family). Read the most
  recent daily page that carries this section and carry forward each block's unresolved state.
  Read-only unless `status_of_blocks.write_back` is on AND `output_target: roam_api`.

## CONFIG

```yaml
# Day type: M/W = A day, T/R = B day, Fri = A or B (read which from the agenda / school calendar)
schedule:
  bell:  # same every day (arrival 7:25)
    pd1:   "7:30-9:00"
    pd2:   "9:05-10:35"
    pd3:   "10:40-12:10"
    lunch: "12:15-12:45"
    pd4:   "12:45-2:15"
  A_day:   # Mon, Wed, + some Fridays
    pd1: { slot: "Planning",              capacity: deep }    # primary free block
    pd2: { slot: "Forensics (sec 1)",     capacity: teach }
    pd3: { slot: "Forensics (sec 2)",     capacity: teach }
    pd4: { slot: "Biology",               capacity: teach }
  B_day:   # Tue, Thu, + some Fridays
    pd1: { slot: "IEP coverage",          capacity: short_tasks }  # sitting in class(es); short items only — TENTATIVE
    pd2: { slot: "Planning",              capacity: deep }         # primary free block
    pd3: { slot: "Anatomy & Physiology",  capacity: teach }
    pd4: { slot: "Study Hall",            capacity: work }         # usable work block

rhythm:                   # by weekday: deep/work blocks vs the short-task (IEP) block
  Mon: { day: A, deep: "Grading + weekly reset" }                       # pd1 Plan
  Tue: { day: B, deep: ["WilmU grad class (seminar prep + grading)", "Deep work (your choice)"],
                 iep: "WilmU attendance + grading (in fragments)" }      # deep = pd2 + pd4 ; iep = pd1
  Wed: { day: A, deep: "Deep work (your choice)" }                      # pd1 Plan
  Thu: { day: B, deep: ["Review NEXT week labs & lessons (links)",
                        "Grading scans: new Notes + finished Drafts"],
                 iep: "Short tasks: email triage, quick grading, approvals" }  # deep = pd2 + pd4 ; iep = pd1
  Fri: { day: "A or B", focus: ["Set up NEXT week labs", "Grocery / materials list"] }

summer:                   # when NO week covers the date (until school starts) — except travel days
  blocks: ["Deep work", "Gym", "Deep work", "Practice — vocal / Spanish / uke (rotates)"]
  travel_day: "blocks off"

status_of_blocks:         # the life/work "blocks" tracked in the daily-note Journal
  source: "daily-note Journal → #Status of the Blocks"   # most recent daily page carrying the section
  blocks: [book, WilmU, learning, admin, strength, AI-HS, family]
  carry_forward: true     # pull each block's unresolved state note into today's brief
  write_back: false       # if true AND output_target=roam_api on an approved routine, refresh
                          # today's #Status of the Blocks with one line per block (see RULES)
  writing_cap_hours: 2    # book block is capped at ~2h/day of deep writing; don't over-allocate it

lookahead_days: 14        # how far ahead the coordinator scans Calendar + Tasks to anticipate / pull forward
output_target: "draft"    # draft | roam_api | email | drive_doc
```

## ALGORITHM
1. **Mode.** Find the week row whose date range contains the target date. No row → SUMMER/BREAK.
   Date in off-days or cell says OFF/IN-SERVICE → OFF-DAY. Else → SCHOOL DAY.
2. **Day type.** Mon/Wed → A_day; Tue/Thu → B_day; Fri → read A/B from the agenda/calendar.
   Load that day's `schedule`.
3. **Teaching = locked.** Each `capacity: teach` period is a fixed block; pull its topic + any
   Notes/Draft due from the Master Agenda.
4. **Non-teaching = filled by capacity:**
   - `deep` (Planning + Study Hall) → the weekday `rhythm.deep` items. WilmU GRAD CLASS
     (seminar prep + grading) is a DEEP item, never an IEP item — default to a Tue deep block,
     or whichever deep block precedes the seminar. The **book** block is capped at
     `status_of_blocks.writing_cap_hours` (~2h) of deep writing — don't fill a whole day with it.
   - `short_tasks` (IEP coverage, B days, pd1):
       Tue → WilmU attendance + grading (in fragments)
       Thu → email triage, quick grading, approvals
     [HARD] Never schedule deep work here. Mark "(tentative — adjust after you live it)".
5. **Today's live data.** Calendar appointments slotted at real times (flag collisions with
   teaching); Google Tasks due today + overdue.
6. **Look-ahead & pull-forward** (this is the coordination layer — inputs stay in their own apps):
   - Calendar: list appointments across the next `lookahead_days` so the week+ ahead is visible
     to anticipate around.
   - Tasks: list upcoming (due within `lookahead_days`). If today has spare deep/work capacity
     beyond what the rhythm needs, surface those upcoming Tasks as PULL-FORWARD candidates
     ("a block is open — you could knock these out now"), quick wins first.
7. **Block status.** Read the most recent daily page's Journal → #Status of the Blocks (per
   `status_of_blocks.source`). For each block in `status_of_blocks.blocks`, carry its current
   one-line state into the brief (so a block can be picked up where it was left, not restarted).
   Tie a block to today's capacity where it fits: a `deep` block → book / AI-HS / WilmU; a
   `short_tasks` or open evening → admin / learning / family; gym time → strength. If
   `carry_forward`, an unresolved `{{[[TODO]]}}` block-state from a prior day rides forward to today.
8. **Assemble & write** to `output_target`. If `status_of_blocks.write_back` is true AND
   `output_target: roam_api` on an approved routine, refresh today's #Status of the Blocks with
   one line per active block (otherwise leave the section untouched — see RULES).

## OUTPUT
```
📅 [Weekday], [Date] — [SCHOOL · A-day | B-day | OFF-DAY | SUMMER]
Wk [n] · [MP] · [Bio] / [A&P]
⏰  pd1 [time]  [slot] — [teach topic | rhythm focus | short tasks]
    pd2 [time]  ...
    pd3 ...   pd4 ...
✅ ATTEND-TO-FIRST (max 3)
🧱 STATE OF THE BLOCKS: [block — one-line state · next action] · …   (book · WilmU · learning · admin · strength · AI-HS · family)
🔁 CARRY-FORWARD: due today [Notes/Drafts · Tasks] · prep for next wk [Thu/Fri links/setup]
👀 LOOK-AHEAD (next [lookahead_days]d): upcoming appts [date — event] · due soon [task — due]
⏩ PULL-FORWARD (only if a block is open today): [task] — could do now
```

## RULES
- [HARD] Stamp every block with its `bell` time. Lunch 12:15-12:45 is fixed and never scheduled over.
- [HARD] Thu review + Fri setup always reference the NEXT week.
- [HARD] IEP coverage block = short tasks only, never deep work.
- [HARD] The book block is capped at ~`writing_cap_hours` of deep writing/day; surface the rest of
  its state, don't schedule more than the cap.
- [FORBIDDEN] Don't touch the grading pipeline (Teacher Dashboard) — separate system.
- [FORBIDDEN] No sends/writes to mail, Roam, calendar, or tasks without per-run confirmation
  unless `output_target` is preset on an approved scheduled routine. Writing back to
  #Status of the Blocks counts as a Roam write: it happens only when BOTH
  `status_of_blocks.write_back` is true AND `output_target: roam_api` on an approved routine;
  otherwise the section is read-only and only mirrored into the brief.
- [HARD] Read Calendar/Tasks/#Status-of-the-Blocks live every run; never copy them into the
  Master Agenda sheet (stale data).
- Inputs stay sovereign: this skill coordinates, it does not own or duplicate any source.
- OFF-DAY: never fabricate classes.
- SUMMER: no classes or bell times — lay out `summer.blocks` as open blocks; on a travel day, blocks off.
```

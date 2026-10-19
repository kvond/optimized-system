---
name: learning-block
description: >
  Stamp today's practice slice onto the daily page: 4 Spanish tasks + one-tick Voice + one-tick
  Ukulele with micro-prompts, from the protocols on [[Learn Block]]. Separate from the morning
  brief. Triggers: "learning block", "practice block", "what do I practice today", 🎧 LEARNING BLOCK
  AGENDA trigger line, scheduled learning-block run.
---

# learning-block — the daily Practice slice

A sibling to `daily-agenda` and `writing-block`, not a section of the morning brief. The morning
brief carries the `learning` block only as a one-line state + a compact **trigger line**; the full
practice slice appears only when this skill runs. Spanish is the heavier-concentration lane (four
tasks); Voice and Ukulele are single ticks. It never teaches and never practices for you — it
sequences the session and points each lane at its source page.

## Why separate + on-demand [HARD]

Mornings stay for musings (same rule as `writing-block`). Practice decisions don't belong in the
morning brief, so `learning-block`:
- is **never merged into the daily-agenda morning brief** — separate output, separate trigger;
- is launched by **the `🎧 LEARNING` trigger line in the daily brief** (which names the day's focus
  + current Stu Fuchs goal, nothing more — see *Daily-brief contract*);
- can also run as a **local Cowork scheduled task** (e.g. a fixed practice window).

## Sources (read-only unless writing the render)

- **[[Learn Block]]** — the spec parent. Holds the three **Protocols** (Spanish / Voice / Uke) and
  the **render template** this skill stamps. The template's `▢` lines become live `{{[[TODO]]}}`.
- **[[Spanish]]** — the daily protocol and the reflection 4-question set.
- **[[Voice Practice]]** — the passaggio sequence; supplies the day's voice micro-focus.
- **[[Ukulele]]** — the `Stu Fuchs goal::`, `Current song::`, `Technique focus::`, and the Ukesters
  practice-list links (the play-and-sing tick).
- **Daily-note Journal → EOD habit line** — `Uke::` / `Spanish::` (and `Reflection::`). Read to
  confirm whether today already logged; never auto-filled (reflection is yours).

## CONFIG

```yaml
spanish:
  tasks: 4                      # the heavier-concentration set, in order:
    - "Pimsleur — next lesson (30 min)"
    - "10–15 high-frequency words (review + new)"
    - "Dreaming Spanish — 15–20 min listening (Beginner)"
    - "AI voice convo (10–15 min) → top-5 phrases + evening reflection (4 Qs)"
  reflection: ["¿Qué hice hoy?", "¿Qué aprendí?", "¿Qué quiero hacer mañana?", "¿Cómo me siento?"]

voice:
  tick: true
  micro_focus_rotation:         # one per run, cycled; default = first
    - "lip trills + sirens through the passaggio, then apply to a song"
    - "cry/sob 'mum'/'nay' to thin the folds, then apply to a song"
    - "head-voice strengthening — soft hooty 'woo', gentle scales"
    - "octave slides ah→oo, narrow vowels going up"
  guard: "no pushing through the break; cervical-fusion history — no aggressive belting"  # [HARD]

ukulele:
  tick: true
  core: "play & sing through the Ukesters practice list (also strengthens the voice)"
  goal_field: "[[Ukulele]] → `Stu Fuchs goal::`"            # surfaced verbatim
  links: "[[Ukulele]] → Ukesters songbooks / Strum files"

eod_habit_line: ["Uke::", "Spanish::"]   # remind to log; never auto-fill
output_target: "draft"                   # draft | roam_api  (roam_api = stamp the daily page)
target_day: "today"
```

## ALGORITHM

1. **Load protocols + template** from [[Learn Block]]; resolve the source pages.
2. **STEP-0.5 — idempotency guard [HARD].** Check whether a `🎧 LEARNING BLOCK — [[<target_day>]]`
   block already exists on the target daily page. If present, run **report-only** (show today's
   slice, no new stamp) — never double-stamp. (Carried from `distill-ritual-learnings`: the
   scheduler can both skip and double-fire within 48h; the guard verifies before any write.)
3. **Spanish (4).** Render the four `spanish.tasks` as plain ticks (Pimsleur is just a checkbox —
   no lesson-number tracking). Reflection ride-along stays inside task 4.
4. **Voice (1 tick).** Pick the next `voice.micro_focus_rotation` entry (cycle from last run);
   attach as the tick's micro-prompt. Always carry the `guard`.
5. **Ukulele (1 tick).** Compose: `core` + " · Stu Fuchs goal: " + the verbatim `Stu Fuchs goal::`
   from [[Ukulele]]. Link the page so the Ukesters list is one hop away.
6. **Assemble & write** to `output_target`. If `roam_api` on an approved routine (or on per-run
   confirmation), stamp the live render under today's Learning block (4 real Spanish `{{[[TODO]]}}`
   + Voice tick + Uke tick). Otherwise return the Brief as a draft only.
7. **On confirm of a completed run:** advance the voice-rotation index (the only state this skill
   owns). Pimsleur and the other lanes are stateless tickboxes.
8. **EOD nudge.** Remind to log `Uke::` / `Spanish::` on the habit line — do not fill them.

## OUTPUT

```
🎧 LEARNING BLOCK — [date]
  Spanish (focus · 4)
    ☐ Pimsleur — next lesson (30 min)
    ☐ 10–15 high-frequency words (review + new)
    ☐ Dreaming Spanish — 15–20 min listening (Beginner)
    ☐ AI voice convo (10–15 min) → top-5 phrases + evening reflection (4 Qs)
  Voice — ☐ [today's micro-focus]   (no pushing through the break)
  Ukulele — ☐ play & sing Ukesters list · Stu Fuchs goal: [verbatim from [[Ukulele]]]
  EOD: log Uke:: / Spanish:: on the habit line
```

## RULES

- [HARD] STEP-0.5 idempotency guard runs before any write; an existing `🎧 LEARNING BLOCK` for the
  day → report-only, zero new blocks.
- [HARD] Voice always carries the no-push / no-belt guard (cervical-fusion history).
- [HARD] Spanish is the only multi-task lane (4); Voice and Uke are single ticks — don't expand them
  into checklists.
- [HARD] The template's `▢` placeholders on [[Learn Block]] stay inert (out of TODO queries); only
  the daily render uses live `{{[[TODO]]}}`.
- [FORBIDDEN] No Roam write without per-run confirmation unless `output_target: roam_api` on an
  approved scheduled routine. Never auto-fill the EOD habit line or the reflection.
- Inputs stay sovereign: this skill reads the protocols + source pages and owns only the
  voice-rotation index. Edit practice content on the source pages, not here.
- Delegate: Spanish/Voice/Uke *content* lives on its page; this skill sequences and stamps.

## Daily-brief contract (the trigger)

`daily-agenda` emits a **dedicated `🎧 LEARNING` block-trigger line** (its own line, alongside
AUTHOR BLOCK / ADMIN — not folded into #Status of the Blocks). It names the day's focus only and
launches this skill; the full practice slice appears only when `learning-block` runs, so the
morning stays for musings. Exact line:

```
🎧 LEARNING → run `learning-block`  ·  Spanish ×4 · Voice: [today's micro-focus] · Uke: [Stu Fuchs goal from [[Ukulele]]]
```

- The brief **computes the three hints only** (Spanish is always ×4; voice micro-focus = next
  rotation entry; uke goal = verbatim `Stu Fuchs goal::` from [[Ukulele]]). It does **not** expand
  the four Spanish tasks inline.
- Acting on the line (type/click "learning block") runs this skill, which does the STEP-0.5
  idempotency check, then stamps the live slice on the daily page.

## Scheduling

Trigger **manually**, from the **daily-brief trigger link**, or as a **local Cowork scheduled task**
(a fixed practice window). Cloud Routine is fine; output is the same Brief.

---

## Open decisions / flags (resolve before promoting to a live skill)

1. **Voice micro-focus rotation is proposed, not authored.** I derived the 4-entry cycle from
   [[Voice Practice]]. Confirm the order, or set it to "always lip trills + sirens" if you'd rather
   not rotate (then the skill owns no state at all).
2. **Trigger model.** Drafted as on-demand + daily-brief trigger (the writing-block pattern). If you
   want it to also fire on a fixed clock (e.g., post-dinner), add the scheduled task — say the time.
3. **Reflection placement.** Kept inside Spanish task 4 (your earlier choice). If you'd rather it be
   a separate evening tick, move it out of `spanish.tasks` into its own line.
4. **AI / reading lanes.** [[Learn Block]] says it also folds in AI-practice and reading. This spec
   covers only Spanish/Voice/Uke per your request; flag if you want those as additional ticks later.
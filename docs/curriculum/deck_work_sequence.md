# Deck Work — Order of Operations

Written 2026-08-29. Four jobs. Each one depends on the one before it.

---

## Correction carried into all of this

`deck_lint.py` exists and is the last gate under `vt-skill`. The work below
extends it. It does not replace it.

The vocabulary is **5 core questions** and **slide types**. `vt-skill` §1
forbids "beat" in a deck, in the manual, in sales copy, and in the skill file.

**The nine, resolved 2026-08-29:** five core questions, plus four conditional
structures — Continuity question, Stock-and-flow model, Compensatory pair,
Conflict case.

[Still open: the **what-if question** does a different job from the four
conditional structures. It does not create coordination, it requires it, so it is
evidence that fusion happened rather than an occasion for it. That may make it a
tenth move, or a required companion to whichever fusion structure a cycle
carries. See `08_nine_moves_attribution.md`.]

---

## Job 1 — Inventory run (read-only)

**What it does.** Walks the 20 cycle folders. For each live deck, found by the
`.pptx` twin test in `vt-skill` §0, emits: cycle number, deck name,
CORE or EXTEND, slide count, slide types present in order, which of the 5 core
questions appear and for which critical aspect, whether a Continuity question is
present, whether a Stock-and-flow model is present, whether a Concept Bank is
present, whether a Teacher Prep slide is present, marker strings found, and the
links slide state.

**What it touches.** Nothing. It reads and writes one report file.

**Why first.** Four things now wait on it: the linter rules, the retrofit skill's
diagnostic logic, the fusion table across the arc, and the NGSS coverage question.
All four are currently guesses about what is in the decks.

**Deliverable.** `deck_inventory_YYYY-MM-DD.csv` plus a readable summary.

---

## Job 2 — Extend `deck_lint.py` to two tiers

**Hard failures** — the deck does not ship:

- Format tokens: 4:3, Arial, palette hex, type scale (§13)
- Marker strings present and unbroken (§3c — the ellipsis fault)
- Links slide present and resolving
- Teacher Prep slide present
- Concept Bank present and positioned before the Day 3 divider
- Teacher note slide present (new — see job 3)

**Advisory** — reported, does not fail the deck:

- No declared fusion device on any critical aspect
- Critical aspect not declared in the teacher note
- Conditional slide types present without a stated reason
- **Move 1 carries no difference.** Does the Critical Aspect question text
  contain a comparison, a choice between named alternatives, or a stated change
  condition? A question that names the aspect and waits for slide 2 to supply the
  contrast is structurally "how are polar bears adapted?" and produces silence.
  Mechanically checkable across all 26.
- Visibility not declared in the teacher note

**Why two tiers.** A linter that fails every deck gets ignored inside a week.
Most decks will not carry a fusion device when this first runs, and that is not a
defect yet.

---

## Job 3 — Fusion retrofit skill (private, your 26 decks)

Diagnoses and proposes. Does not decide. See `04_vt_deck_fusion_retrofit_SKILL.md`.

Runs one deck at a time. Reads the critical aspects, states whether they can vary
simultaneously and by what structure, drafts a candidate slide, and stops for you.

**Second output, and it is the reason to run this by hand rather than in batch:**
every accept or reject you make is a documented decision with the content in view.
That is the case file, produced as a byproduct rather than as a separate writing
task.

---

## Job 4 — Authoring skill (public-facing, new decks)

Generative. See `05_vt_deck_authoring_public_SKILL.md`.

Written for a teacher who is not you, running her own Claude, on her own content.
Ships with the rationale document and the case file. Job 4 cannot ship before job
3, because the case file does not exist until the retrofit runs.

---

## Fusion table across the arc

Falls out of job 1 plus job 3. One row per cycle: critical aspects, fusion device
or none, and the reason for none. This is what makes an NGSS gap visible, and it
is what a teacher needs to plan across weeks.

[An absence in that table is not automatically a hole. A standard addressed
without a fusion device because the content carries no compensatory relationship
and no genuine conflict case is a design decision, not a gap. The table tells you
which one you are looking at. Name the standard you suspect and it can be checked
directly.]

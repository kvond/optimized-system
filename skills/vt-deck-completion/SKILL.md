---
name: vt-deck-completion
description: For school Claude (School Claude Ext, school Chrome profile), run when triggered on a VT deck that was only partly updated. Finds which vt-skill §16 passes are missing (Gemini enhancement not run, student textboxes left plain white, embedded codes missing or unpaired) and finishes them in place in the live Google Slides file, then reports. Use from the manual school task or on the deck Katherine has open. Triggers - "finish this deck", "deck only partly done", "partial VT deck", "complete the VT update", "missing gemini enhancement", "white text boxes", "check embedded codes".
---

# VT deck completion (school Claude, on trigger)

Katherine, 2026-10-20 (#vt-decks): an updated VT deck she found was only partly done:
no Gemini enhancement, white text boxes, and possibly no embedded codes. Gemini in
Slides and the school Drive are reachable only from the school computer, not her home
Mac. So this skill runs in **school Claude**, when triggered: from the existing manual
school task (`ai-ops/workflow-contracts/school-lesson-review-and-code-repair.md`,
task `trig_01A9JrvwJsRizEc7fnTakTCp`), or when Katherine asks on the deck she has open.
It adds no schedule of its own.

It holds no new standard. The standards are vt-skill §16.2 (enhance), §16.3 (codes),
§7 (marker strings), §13 (design tokens) and the #vt-decks standards post. Read them
fresh each run.

## 1. Identify the deck

- Exact file ID, course, week/cycle, from Master Agenda `Agenda 26-27 CLEAN`
  (`1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY`) or the deck Katherine has open.
- Confirm the account is `katherine.vonduyke@redclay.k12.de.us`.
- If Katherine is editing the deck right now (revision changed in the last minutes),
  report only; do not write.
- Work in the native Google Slides file. No PowerPoint round trip; no re-upload (it
  drops codes and links and changes the ID).

## 2. Find what is missing (read only)

One row per slide:

| Check | Missing when |
|---|---|
| Restore (§16.1) | A&P or Forensics deck lacks the original's slides/pictures. Stop: restore is owned by School ChatGPT (`/restore-vt-slides`). Report it; do not enhance an unrestored deck. |
| Enhance (§16.2) | An eligible lecture slide still has plain text-only layout (no Gemini visual) |
| Textboxes | A student response or Concept Bank box is plain white with no fill or border, where §13 and the deck's own finished slides use the writing-box tokens (fill `F2F6F9`, border `CCCCCC`) or the yellow Workflow A answer box |
| Codes (§16.3) | A student textbox has no code, a code is duplicated, NOTES/DRAFT do not pair by ID, or the slide-one `[[MARKER-INVENTORY:CYCLE]]` counts disagree with the codes found |
| Markers (§7) | A marker string is not character-for-character intact |

Not eligible for enhancement, ever: answer slides, response/diagnostic slides, Concept
Bank, slides 1–2, and any slide carrying a protected marker. Do not re-enhance a slide
that is already enhanced (`Inter` font runs mark Gemini-rebuilt slides).

## 3. Finish, in order

1. **Enhance** each eligible slide that still needs it with Gemini (`/vt-gemini-enhance`).
   Inspect the result; fill any empty visual placeholder; keep the deck's style.
   Enhanced textboxes get no gray. Answer textbox colours stay unchanged.
2. **Textboxes.** Give each plain-white student box the token fill and border the deck
   already uses for that box type. Change fill and border only; never the text,
   position or size, and never an answer box's colour.
3. **Codes.** Run the §16.3 prompt (read the syntax fresh from Agenda tab Feedback
   Prompts, Prompt 00). Keep every existing code and ID; add no duplicates; update the
   inventory.
4. **Markers.** If the enhance pass broke a marker string, restore the exact string.
   Fix the deck, never the prompt.

Before each write, re-read the slide's revision; stop that write if it changed.

## 4. Verify

- Re-read every changed slide and render it.
- Each student textbox has exactly one code; NOTES/DRAFT pair by ID; inventory counts
  match.
- Run the post-enhancement check (`docs/curriculum/post_enhancement_check.md`): live
  check, then `deck_lint.py` on an export. Same file ID before and after.

## 5. Report

In the request thread (or #work-que for a triggered run): deck link; slides enhanced;
textboxes fixed; codes added and inventory before/after; checks passed; anything still
open with the one next step. A restore gap goes to #kathy only if it needs Katherine.
No student names, work or grades.

Never: change grades, sharing, schedules or the Agenda; delete or trash a slide or file;
send or publish.

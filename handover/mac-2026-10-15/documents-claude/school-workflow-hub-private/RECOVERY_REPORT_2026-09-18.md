# Student-file recovery — outcome (2026-09-18)

## What was added
A bounded, reversible recovery toolkit was pasted into the live Apps Script
project **📤 Turn-in system** (script id `133uC3RCEDVNBQsJEYM_N5smRp3jr2PykYsm6eNbWHAZgUWN3H0QSpgD-`,
which lives inside "Agenda 26-27 CLEAN"). Pre-change backup:
`turn-in-system-Code.gs.backup-2026-09-18.js` (this folder).

Functions:
- `A_RUN_RECOVERY` — the FIRST runnable function, so the editor's Run button
  always executes it (the editor runs the first non-underscore function; the
  function-picker dropdown does not actually commit in this build). It steps the
  recovery once per Run via Script Property `RECOVERY_STEP`:
  inventory → one → rest → done.
- `RECOVERY_INVENTORY_20260918` — READ-ONLY dry run. Walks the deprecated root
  tree (even in trash), scans account trash for router-renamed / Log-named /
  student-work-type (Slides/Docs/PDF/PPTX) files, and lists live UNSORTED files.
  Writes a plan to the "🛟 Recovery 2026-09-18" sheet. Moves nothing.
- `RECOVER_ONE_20260918` / `RECOVER_UNMATCHED_20260918` — restore planned files
  one at a time (untrash + move + readback receipt), never emptying trash,
  never deleting, preserving file IDs.

## What running it found — NOTHING TO RECOVER
The inventory (including the broadened trash scan) reported, every run:

> Recovery inventory (read-only): **0 files seen, 0 new rows**. Nothing was moved or untrashed.

Cross-checked independently with the Drive API (school-account identity):
- **Deprecated root** `1oEpTa873f1cKWxGH_NbPXx-PQ3yOK0AN`: unreachable / empty
  (Drive API "not found"; Apps Script walk saw 0 files).
- **UNSORTED** (`1IJ3DrkhK8jyOCy6_MvEVP-HfguOgUoUB`, under the active root): empty.
- **Account trash**: 0 student-work files (broadened scan by mime type).
- **Student work is intact** in the original Forms-based turn-in structure under
  the active root "00 ALL TURN IN" (`1KvWrI5EbYG_pzWxv3lQLzQ2tVkMFWaBq`):
  - `Biology` (`1C8yWS8iGZFfQ_BsI8tQndUsR_ENvCdEN`) → "Biology — Cycle NN — … — Turn In" (Cycles 01–20), each with a Form + "(File responses)" subfolder.
  - `Forensics` (`13doSQMlouDWy973Cy5U1aHBDrf1uyRZJ`) → "Forensics — Wk NN — … — Turn In" (Wk 01–36), each with a Form + "(File responses)".
  - `Anatomy` (`1kk0RX21tJz8X6KbTF5worfCAmRNpK07s`).

The earlier checkpoint's "8 live unmatched + ~35 backlog + trashed originals"
figures were explicitly flagged as estimates; they do not match the current
verified state. No orphaned or trashed student files exist in the places the
reorganization would have put them.

## One real observation (not data loss, a tidiness issue)
There are now TWO parallel folder trees under "00 ALL TURN IN":
- the ORIGINAL Sep-2 Forms-based "— Turn In" folders that actually hold student work, and
- a NEW set of emoji course folders (`🔬 Forensics`, `🫀 A&P`, `🌿 Biology`) with
  dated "📥 Wk NN — … — YYYY-MM-DD" subfolders, created empty by SETUP/BUILD_FOLDERS.
New Form submissions route into the emoji tree; historical work sits in the old
tree. This is a routing-consolidation question for a later cleanup pass, not a
recovery emergency. Do NOT delete either tree without confirming source coverage.

## Note on SETUP
The editor's Run kept executing SETUP before the dispatcher was made the first
function; SETUP ran to completion a few times. SETUP is idempotent by design
("0 folders created, 31 already existed"; the 120-row TurnIn Map is intact) and
never touches student files or trash, so this caused no harm. Verified the map
(40 Biology + 40 A&P + 40 Forensics rows) is well-formed.

## Left state
`RECOVERY_STEP` = `one` (harmless: the plan sheet has 0 rows, so a further Run
is a no-op that advances the step). To re-run the read-only inventory later, set
`RECOVERY_STEP` = `inventory` in Project Settings → Script properties.

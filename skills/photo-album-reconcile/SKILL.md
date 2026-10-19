---
name: photo-album-reconcile
description: >
  Catalog the local photo library and verify per-kid album picks resolve to real files, flagging
  misses before anything is ordered, edited, or arranged. Use before any step that copies or
  arranges selected photos. Triggers: album selection, photo manifest, pick reconciliation, "check my album picks".
---

# Photo Album Reconcile

Keeps three layers in sync while building photo albums, so a beautiful selection
never ends up pointing at files that can't be found:

- **Discovery** — Google Photos (who is in each photo).
- **Selection (canon)** — the per-kid files in the working folder (what was chosen).
- **Catalog** — `manifest.db` (where the real file lives on the drive, plus its date and event).

This skill links **Selection → Catalog**. It is **READ-ONLY** on photos and on the
kid files: it never moves, edits, renames, or deletes anything. It only reports and
writes review CSVs. Do not move or edit any photo on the user's behalf without an
explicit go-ahead.

## Bundled scripts

- `scripts/photo_index.py` — walks a photo library, records one row per image in
  `manifest.db`, flags exact duplicates by content hash, and groups photos into
  "events" by gaps in time. Read-only on photos.
- `scripts/reconcile_picks.py` — reads the per-kid selection files, extracts the
  photos they name (works with `.md`, `.txt`, `.docx`), and checks each against
  `manifest.db`.

## Placeholders to fill from the user's setup

- `[WorkingFolder]` — folder holding `manifest.db` and the report outputs (the existing photo-album folder).
- `[KidsDir]` — folder of per-kid selection files (often the same as the working folder, or a subfolder).
- `[DriveRoot]` — the photo library root on the external drive (only needed when (re)building the catalog).

If any placeholder is unknown, first list the working folder's tree and ask the user
to confirm which folder is which. Do not guess paths.

## Prerequisite — build the catalog (needs the drive mounted)

Run once, and again whenever photos are added:

```
python3 scripts/photo_index.py --root "[DriveRoot]" --db "[WorkingFolder]/manifest.db" --export "[WorkingFolder]/catalog.csv"
```

## Each run — reconcile

1. Confirm `[WorkingFolder]` contains `manifest.db`. If it is missing or older than the
   newest kid file, tell the user the catalog may be stale and offer to rebuild it first.
2. Run:
   ```
   python3 scripts/reconcile_picks.py --db "[WorkingFolder]/manifest.db" --kids-dir "[KidsDir]" \
       --report "[WorkingFolder]/report.csv" --resolved "[WorkingFolder]/resolved_picks.csv"
   ```
3. Read `report.csv` and summarize per kid: how many picks **resolved**, how many are
   **ambiguous**, how many are **missing**.

## 🛑 STOP-AND-CONFIRM checkpoint

If any pick is **ambiguous** or **missing**, do not proceed to ordering, editing, or
arranging. Present the specific items to the user and wait for a decision:

- **missing** — the kid file names a photo not in the catalog (typo, renamed file, or
  not yet indexed). Fix the name in the kid file, or rebuild the catalog, then reconcile again.
- **ambiguous** — the same filename exists in more than one place on the drive. Ask which
  path is correct and record the full path in the kid file to break the tie.

Only when the report is clean, or the user explicitly approves the exceptions, does the
pipeline move on.

## Outputs

- `report.csv` — every mention, its status, and (when resolved) the real path, event, and date. The human review surface.
- `resolved_picks.csv` — the clean, file-linked selection, already sorted chronologically
  within each kid. This is the input to the next stage (order → edit → arrange).

## Notes

- A photo chosen for two kids (a group shot) resolves independently in each — expected, not an error.
- Re-running is always safe; it overwrites only the two report CSVs.
- Always edit the original on the drive, never a re-compressed cloud export.

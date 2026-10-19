# Post-enhancement deck check — directions

Written 2026-09-02 from the check run on `▶ LIVE — Cycle 01 — Lab Safety (VT)`.
Companion to `docs/curriculum/after_you_enhance_a_deck.docx` (30 August), which is the
short version for the moment after you enhance. This file is the operator's version:
what Claude runs, where each thing lives, and what the result means.

## 1. Definitions

- **Marker string.** An exact piece of text Workflow A and the deck checks search for to decide what
  kind of slide they are looking at: `Critical aspect:`, `Pattern break`,
  `Finish this sentence as a rule`, `What if?`, `Keep going`, `Compensatory pair`,
  `Conflict case`, and the three tier labels `Getting Started` / `Working On It` /
  `Mastery`. The list is `TYPE_STRINGS` in `scripts/live_deck_check.py` and §7 of
  `vt-bio-skill`. Matching is by machine, character for character. A curly apostrophe, an
  ellipsis in place of a question mark, or a Gemini rewrite of a heading breaks the match
  without anything looking wrong.
- **Live check.** `scripts/live_deck_check.py`. Reads the live Slides file through the
  Slides API, so it sees Gemini's work. It reports the slide types still detectable, retired
  types present, the Critical aspect labels, the Day 3 divider, fonts, and sizes, and
  compares against `docs/live_baseline.json`. Run it first. It reads text only, so it cannot
  see speaker notes, hyperlinks, pictures, or QR codes.
- **Linter.** `scripts/deck_lint.py`. Reads a built or exported `.pptx`. Two tiers since
  2026-08-29. It is a script, not a skill; the skill that governs it is `vt-bio-skill`.
- **Grader.** `scripts/extract_and_grade.py`. What will later score student copies. Its
  `classify_slide()` and the live check must agree on which slides are diagnostic.
- **Link check.** `scripts/deck_link_check.py`. Walks hyperlinks on text runs in a `.pptx`.
  It does not see a link attached to a picture or a shape, so those are walked separately.
- **Stub.** Anything an enhancement pass leaves that is not finished content: an icon name
  showing as text (`flash_on`), an empty box, a heading with nothing under it, placeholder
  wording.
- **ID.** The string after `/d/` in the deck URL. The agenda column G, the START HERE decks,
  every `/copy` link, and the QR image on slide 1 of Cycle 01 all point at it. Editing a deck
  in place, by hand, by Gemini, or through the Slides API, never changes it. Only uploading a
  new file does.

The rule that follows: **a post-enhancement fix is made in place, in the live file, through
the Slides API. Never by rebuilding a `.pptx` and uploading it.** Rebuild and upload is the
`vt-bio-skill` §14 route for a new deck; it creates a new ID and forces the whole §9 relink.

## 2. Where everything is

| Thing | Where | Reached by |
|---|---|---|
| Live decks | Red Clay Drive → `03 BIOLOGY (Public)` → `Cycle NN — …` → `▶ LIVE — …` | Composio Drive and Slides on **kvond12** (`googledrive_purity-marish`, `googleslides_katha-rusine`). The school account is not connected; the folders are shared to kvond12. A deck kvond12 cannot see needs Share on the Red Clay side, not a restart. |
| Deck IDs | `docs/decks_live_ids.csv` in this repo | Never work from names. |
| Scripts | `scripts/` in this repo, `kvond/answerable-skills` | Pull at run time. The copies in the two Drive `scripts (Do NOT Delete)` folders are the 2026-08-10 versions on the expiring answerableteaching account; the repo `deck_lint.py` is the rewritten two-tier one. |
| Skills | `skills/` in this repo; `~/.claude/skills` on the Mac is a symlink into it | Every local Claude reads the repo. The claude.ai skill uploads are a separate copy and go stale (see §6). |

## 3. The prompt to send

```
Run the live check on Cycle NN.
```

That line is enough for the read-only pass. If a full pass is wanted, or the deck is not in
`docs/decks_live_ids.csv` yet:

```
Post-enhancement check. Deck: ▶ LIVE — Cycle NN — <title> (VT).
ID: <from the URL>.
Run live_deck_check, then the export pass (lint, grader classify, link check, notes, stubs,
render). Report against vt-bio-skill §7 and §11. List every fix as an in-place Slides API
edit and wait for my yes. No new file, no re-upload.
```

If you know what Gemini touched, add `Gemini touched slides 4, 12, 14.`

## 4. What Claude does, in order

Read only:

1. Confirm the file by ID and owner; confirm the `▶ LIVE —` name.
2. `GOOGLESLIDES_PRESENTATIONS_GET` with the `fields` string in the docstring of
   `live_deck_check.py`; save as `<key>.json`; run the script with
   `--csv docs/decks_live_ids.csv --baseline docs/live_baseline.json`.
3. Export to `.pptx` (`GOOGLEDRIVE_DOWNLOAD_FILE` with the pptx MIME type). An export does
   not touch the live file.
4. `deck_lint.py`; read `markers present:` and the notes block, not only the last line.
5. Run the grader's `classify_slide()` over every slide; its diagnostic count must equal the
   live check's.
6. `deck_link_check.py`; then walk picture and shape level links by hand; decode any QR image
   and confirm it carries this ID.
7. Read the speaker notes of every response slide for the revision prompt.
8. Search the text for stubs: lowercase words with an underscore (Material icon names), empty
   boxes, `Lorem`, `[insert`, `TODO`.
9. Render every slide and look at each one.
10. Report as one table (check, result, meaning for grading), then the proposed fixes, then
    the one question if there is one.

Written only after a yes:

11. Each fix is a `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE` on the live file: `insertText`
    and `deleteText` for a marker, `updateTextStyle` with `link` for a hyperlink,
    `replaceAllText` for wording. Same ID before and after.
12. Re-run steps 2 to 9. Save the new fingerprint with `--save-baseline` and commit
    `docs/live_baseline.json`.

## 5. Cycle 01 Lab Safety, 2026-09-02

`live_deck_check.py`: **FAIL** — no 3-Tier Question slide; 1 distinct `Critical aspect:`
label where the script expects 2; slide 1 has no CRITICAL ASPECTS block; no Day 3 divider;
font `Inter` on 8 runs; 9 runs above 26pt. `Pattern Break ×1` detected.

| Check | Result | Meaning |
|---|---|---|
| Slides, size | 25, 4:3 | Standard |
| Markers | `Critical aspect:` and `Pattern break`, both on slide 14, ASCII | Intact. Gemini did not touch them |
| Live check, linter, grader agree | All three count one diagnostic slide (14, `pattern_break`) | Only slide 14 is scorable |
| Tier labels, Build a Rule, What if?, Concept Bank, day dividers, Teacher Prep, links slide, credits | Absent | Never built to the standard; `vt-bio-skill` §0 already records Cycle 01 as the cycle that needs Katherine's eye. Her decision 2026-09-02: slide 14 alone is the scoring surface for this launch cycle |
| Speaker notes | None on any slide | Slide 14 has no revision prompt (§3). Fix: the wording in `set_revision_prompt.py`, applied through the API |
| Hyperlinks | Lab Sim (slide 3) HTTP 200. PurposeGames (slide 25) HTTP 200, attached to the picture, invisible to `deck_link_check.py` | Both live |
| Turn in link | None. The folder exists beside the deck: `18Zk-agYcfbqKmyTkeGbUgUPhRBGYVwNV` | Missing on the revision page |
| QR, slide 1 | Encodes this deck's own `/edit` URL | ID intact. It resolves to `/edit`, not `/copy`, so a student scanning it lands on the master |
| Stubs | Slide 12: `flash_on` and `!` are Material icon names as text; they render as icons only inside Slides | Stubs in any export or text dump |
| Fonts | `Inter` ×8, `Calibri` ×1, the rest Arial | `Inter` marks the slides Gemini rebuilt |

Nothing was written to the deck. Cycle 01 was added to `docs/decks_live_ids.csv`
(`google_native` 2026-09-02, 25 slides) and its fingerprint to `docs/live_baseline.json`, so
the next run compares against today.

## 6. Two things only Katherine can do

1. **Refresh the claude.ai skill uploads.** On 2026-09-02 the copies claude.ai holds are
   behind the repo for `vt-bio-skill` (72 KB against 92 KB; the old one still points scripts
   at Drive), `vt-deck-authoring`, and `vt-fusion-retrofit`, and `hep-scout` and
   `vt-post-import` are not uploaded at all. Re-upload from
   `~/code/answerable-skills/skills/<name>/` after `git pull`.
2. **Repo visibility.** `README.md` says private; GitHub reports `kvond/answerable-skills` as
   **public** on 2026-09-02. It carries Drive file IDs. GitHub → the repo → Settings → Danger
   Zone → Change visibility.

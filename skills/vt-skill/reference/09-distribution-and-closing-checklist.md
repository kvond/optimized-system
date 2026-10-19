<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

## 9. Distribution, and the closing checklist

A teacher does not get a copy of the Slides file. A teacher gets a link to the
master deck with `/copy` at the end. Google then asks the teacher to make a copy
in the Drive of the teacher.

```
https://docs.google.com/presentation/d/<DECK_ID>/copy
```

Change every `/edit`, `/edit?usp=sharing`, and `/view` link to `/copy`. Do this on
each form and each template. Keep the master decks viewable by link. No teacher
gets edit access to a master deck. Each product section holds its part of the
course. Each section links only to the master decks for that part.

**A customer deck names no LMS.** Katherine uses Infinite Campus. A customer uses
neither Infinite Campus nor Schoology. Use this closing checklist:

```
Think → Write → Submit
☐  Finish your notes on every slide.
☐  On each response slide, open the Notes, run the revision prompt in your own AI, and write your revised answer under your first one. Leave both showing.
☐  Turn in your finished deck to the assignment.
Do not name your file. Your name is already attached where you turn it in.
Completion = both answers present on every response slide. Your growth shows in your printed Growth Report, not the grade.
```

A student does not name the file. The name of the student is already attached at
the place where the student turns the file in.

### 9.1 A built deck cannot be uploaded through Composio (found 2026-08-18)

`GOOGLEDRIVE_UPLOAD_FILE` does not take a file. It takes an `s3key` — a reference
to content **already inside Composio's own storage**, put there by an earlier
Composio download. A `.pptx` built anywhere else has no such reference, so the
upload fails with "Failed to retrieve uploaded file content. The file does not
exist in storage." Tested on 2026-08-18 four ways, all of which failed the same
way:

1. Local path passed as `file_to_upload` — rejected as not a dictionary.
2. Local path passed as `s3key` — file not in storage.
3. Deck rebuilt inside `COMPOSIO_REMOTE_BASH_TOOL` (Python 3.13 and python-pptx
   1.0.2 are both present there, and the rebuild succeeded), then uploaded by its
   sandbox path — file not in storage.
4. Same file copied to the sandbox's cloud-backed `/mnt/files/` mount and uploaded
   through `run_composio_tool` — the workbench crashed.

Nothing partial was written to Drive by any of the four. Verify the destination
folder afterwards regardless.

`GOOGLEDRIVE_EDIT_FILE` is not a way round it either, and it is the one that looks
like it should be. It preserves the file ID, so it would remove the relink problem
completely — but its `content` parameter is **a string, UTF-8 encoded on upload**.
A `.pptx` is binary. Pushing one through that parameter corrupts it. That is the
same failure Katherine's notes record as "base64 corruption on programmatic
upload", and it is visible in the tool schema rather than only in experience. The
schema also says the action does not work on Google Workspace native files at all,
so the Slides master is out of reach by that route regardless.

**There is therefore no write path for a deck through Composio.** Reading is free:
every live deck has a `.pptx` in Drive (see §0), so a build never needs a Slides
export. Writing back is manual, per deck.

**So the last step is Katherine's, and there is no way around it.** Hand her the
`.pptx`. She places it in Drive. Then take the new file ID and do the §9 relink.

### 9.2 What to do after she places a deck (proved on Cycle 02, 2026-08-18)

1. **Verify the placed file before anything else.** Export it back to `.pptx` and
   compare against the deck you built: slide count, slide size, and the text of
   every slide. Cycle 02 came back 35 slides, 9144000 x 6858000, zero slides
   differing, Concept Bank cells still `F2F6F9`, all 14 empty, both source links
   live. Do not assume the conversion was clean — check it.
2. **Rename it. Drive mangles the name on conversion.** `Cycle 02 — Ecosystems &
   Feeding Relationships (VT deck) — with Concept Bank.pptx` arrived as
   `Cycle_02___Ecosystems__Feeding_Relationships_VT_deck___with_Concept_Bank` —
   em dashes, the ampersand, the parentheses and the spaces all became
   underscores. That breaks the §0 live-deck test, which needs the Slides name to
   match the `.pptx` name. Rename with `GOOGLEDRIVE_UPDATE_FILE_PUT` to the
   canonical `Cycle NN — <title> (VT deck)`.
3. **Archive the deck it replaces**, so two files of the same name never sit in one
   folder. Rename, do not trash: `ARCHIVE <date> — Cycle NN (VT deck), before
   <what changed>`. That prefix is already Katherine's convention in Drive.
4. **Repoint every `/copy` link.** Find them with
   `GOOGLEDRIVE_FIND_FILE q="fullText contains '<old file id>'"`. A `/copy` link
   in a Slides deck is a **hyperlink on a text run**, not visible text, so
   `replaceAllText` cannot touch it. Use
   `GOOGLESLIDES_PRESENTATIONS_BATCH_UPDATE` with `updateTextStyle`, the run's
   `objectId`, a `FIXED_RANGE` covering the run, `style.link.url` set to the new
   `/copy` URL, and `fields: "link"`.
5. **Verify the relink** by re-reading the deck and counting occurrences of the old
   and new IDs, and by re-running the Drive search for the old ID until it returns
   nothing.

### 9.3 Every place a deck ID is written (mapped 2026-08-18)

A deck ID lives in **two kinds of surface**, and a Drive search finds only some of
them. Repoint both on every deck, before archiving the old file.

**A. The Master Agenda spreadsheet — the larger carrier.**
Master Agenda `Agenda 26-27 CLEAN` (`1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY`,
school account; ai-ops/NAMES.md). One tab per course: `🌿 Biology` (gid
`2088972437`), `🫀 A&P` (gid `170607847`), `🔬 Forensics` (gid `1634834686`).
The deck ID is written **once per lesson row**, as a plain URL in column **Q**
(`_teacherURL`), on all three tabs. Column **P** (`_studentURL`) derives the `/copy`
link from Q by formula, and the display columns **L** (🎞 Student deck) and **M**
(👩‍🏫 Teacher deck) are `HYPERLINK` formulas over P and Q. Repoint a deck by writing
Q only; never overwrite the formulas in L, M or P. The other columns differ by tab, so
read that tab's header row before writing anything else:

| Tab | Header row | Folder URL | Extra/activity URL | Turn-in URL |
|---|---|---|---|---|
| `🌿 Biology` | 3 | R (`_folderURL`) | S (`_extraURL`) | U (`_turnInURL`) |
| `🫀 A&P` | 4 | R (`_folderURL`) | S (`_extraURL`) | U (`_turnInURL`) |
| `🔬 Forensics` | 4 | S (`_folderURL`; R is blank) | T (`_extraURL`) | V (`_turnInURL`) |

The list tabs (`Bio as List`, `A&P as List`, `Forensics as List`, `🌿 Biology List`)
read P, so check them after the write. Read cells with the formula render option and
write plain URLs as user-entered values. Verified against the sheet 2026-10-19.

The superseded v9 agenda (`1i6D-QT5nQWdVpltW14XB7OZ9lWFrMbMO8ZnZQvpUw-w`, tab
`🌿 Biology Agenda 26-27`, one `/copy` HYPERLINK per class day in column G) is no
longer written. Read it only to trace an old link.

**B. The five START HERE decks.** Every `/copy` link sits on **slide 4** of each,
as a hyperlink on a text run — see §9.2 step 4 for how to change one.

| START HERE deck | ID | Cycles it links |
|---|---|---|
| `▶ START HERE — Ecology Starter (FREE)` | `1eXMmYJFYQ8SgE9-PztzA824XaAla8M41WjeH0VQ7QFU` | 02, 03 |
| `▶ START HERE — From Sunlight to Populations` | `1d7mIwNRIUru1ydo6QqZ4o6ZYSwx37etL6wHoARDRhWo` | 01, 04, 05, 06, 07a, 07b |
| `▶ START HERE — The Cell as a System` | `1QVW9VYXOy2RS2USvxJ7_KuwfDvDITYfI9zKw2MzBl_4` | 08, 09, 10, 11 |
| `▶ START HERE — Inheritance & Information` | `1wHLloTLm9eXXvYz4eL6GUkiUFQNRWPTsCETBbcZuSWs` | 13a, 14, 15a, 15b, 16a, 16b |
| `▶ START HERE — Change Over Time` | `1C8vj5Plr67uC5dHphNeLTqKu4gC1S1KTwTqPCYDbi10` | 17, 18, 19, 20 |

`TPT🧭 Biology v3 — Teacher Dashboard (start here)` carries no deck links.
**Cycles 12, 16c and 16d are linked from no START HERE deck** — check whether that
is deliberate before assuming a deck has no callers.

### 9.3a The agenda and the product answer different questions

The Master Agenda and the START HERE decks legitimately hold different sets of
cycles, and the difference is not a defect to reconcile.

- **The Master Agenda is Katherine's own teaching schedule.** It lists what she
  will actually teach, on dates. It carries fewer lessons than the product ships,
  **on purpose**. In her words: *I teach less to go slower.* The manual already
  states the same principle twice — §2 says a cycle carries two or three critical
  aspects, "not eight facts", and §9 says "Pace destroys depth." Do not "fix" the
  agenda by adding every shipped deck to it, and do not read a missing cycle there
  as an error.
- **A START HERE deck is the customer's index of the product.** It must list
  **every** deck in its arc, CORE and EXTEND both, because a customer who bought
  the set cannot reach a deck that is not listed. A missing deck here **is** a
  defect.

**Open gap, found 2026-08-18.** `▶ START HERE — Inheritance & Information` lists
13a, 14, 15a, 15b, 16a and 16b. It is missing **Cycle 12 (CORE)**, **Cycle 12
(EXTEND)**, **16c** and **16d**. No START HERE deck lists Cycle 12 at all.

**How slide 4 is built**, for when those rows get added. Each lesson is a **pair of
text boxes**: a title box (`Cycle NN — <title>`) and, below it, a box whose single
run reads `▶ Copy link ↗` carrying the `/copy` hyperlink. The pairs run in cycle
order between the intro text and the footer box
(`Answerable Biology · <arc name>`). Adding a lesson means cloning a pair and
placing it below the last one, then shifting the footer — a layout edit, so render
the slide and look at it before shipping.

**The order matters.** Repoint every caller *first*, then archive the old deck. On
2026-08-18 the old Cycle 02 deck was archived before the agenda was checked, and
the agenda's three deck links pointed at a file named `ARCHIVE …` until Katherine
noticed. A Drive `fullText` search for the old ID returned **zero** files at that
moment — it had found the START HERE deck but never the spreadsheet.

[Challenge, and it is the durable fix: the agenda already has a
`File IDs (do not delete)` tab, and it holds no deck IDs at all. Put the 24 deck
IDs there, one row per cycle, and make column G a formula that builds the link from
that row. Repointing a deck then becomes one cell edit instead of three, and any
other surface that reads the sheet follows automatically. That does not fix the
START HERE decks, which would still need their own pass, but it removes the larger
half of the work and the part most likely to be missed.]

**Correction to a standing note.** The project notes say Drive `fullText` does not
index hyperlink URL targets. On 2026-08-18 it did: the search for the old Cycle 02
ID returned `▶ START HERE — Ecology Starter (FREE)`, where the ID appears **only**
as a link target on a run whose visible text is `▶ Copy link ↗`. But it did **not**
find the Master Agenda, whose three `=HYPERLINK()` formulas carried the same ID.
So `fullText` is a partial index in both directions: use it as a first pass, never
as proof there are no callers left. Walk the surfaces in §9.3 by hand every time.
Do not spend a session hunting for an upload route; this is the answer until
Composio gains a way to stage local bytes.

[Challenge, worth raising once: the whole relink problem exists because a new
upload gets a new file ID. If the deck's identity moved to a stable Drive shortcut
that the product links to, and the shortcut were repointed at each new version,
the `/copy` URL in §9 would never change and nothing downstream would need
touching. That is a change to how the product links decks, not to a deck.]

**Never ship a date.** The year of a customer does not start when Katherine's year
starts. A customer copy carries the cycle number and the length only. Use
`Unit N · 3 class cycles`. A cycle is 3 class cycles. A cycle takes 2 to 4 class
meetings. The number depends on the schedule of the school.

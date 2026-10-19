<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19; section numbers unchanged. -->

## 13. Design tokens — the visual standard

Every deck must look like the reference build. These values come from Cycle 02.
Do not invent a color, a size, or a position. Do not approximate a color by eye.

### 13.1 Page and font

| Item | Value |
|---|---|
| Slide size | 9144000 x 6858000 EMU (10 x 7.5 in, 4:3) |
| Font | Arial, every run, every slide |

### 13.2 Colors

| Token | Hex | Where it is used |
|---|---|---|
| Teal | `028090` | Kickers, slide headings, section labels, CASE A and CASE B labels, day divider band |
| Body black | `111111` | All body text. Not `000000` |
| Muted gray | `666666` | "TEACHER REFERENCE" line, small labels, the "Think first" footer, word bank label |
| Alert red | `C0392B` | The Pattern break kicker, and the "Getting Started" tier label |
| Green | `1E8449` | The "Mastery" tier label |
| Box fill | `F2F6F9` | The writing box |
| Box border | `CCCCCC` | The writing box |
| Panel gray | `F5F5F5` | A light panel behind a question |
| Divider pale | `EAF6F7` | The small line on the day divider band |
| Divider white | `FFFFFF` | The headline on the day divider band |

The "Working On It" tier label is body black `111111`, not a color. Only the first
and last tier labels carry a color.

### 13.3 Geometry

| Element | x | y | w | h | Size |
|---|---|---|---|---|---|
| Kicker line | 502920 | 109728 | 8321040 | 274320 | 11pt bold |
| Slide heading | 548640 | 822960 | 8046720 | 457200 | 16pt bold |
| Lead sentence | 548640 | 731520 | 8046720 | 457200 | 13pt bold |
| Body text | 548640 | — | 8046720 | — | 12pt to 14pt |
| "Think first" footer | 457200 | 6455664 | 8229600 | 274320 | 10pt, gray |
| Icon, normal slide | 7863840 | 502920 | 502920 | 502920 | — |
| Icon, day divider | 7863840 | 502920 | 731520 | 731520 | — |
| Day divider band | 0 | 2194560 | 9144000 | 1554480 | fill `028090` |
| Divider small line | 548640 | 2331720 | 8046720 | 457200 | 16pt bold `EAF6F7` |
| Divider headline | 548640 | 2788920 | 8046720 | 822960 | 26pt bold `FFFFFF` |
| Divider body | 548640 | 4114800 | 8046720 | 2286000 | 13pt `111111` |
| Writing box | 548640 | — | 8046720 | 1965960 | fill `F2F6F9` |
| Concept Bank heading | 548640 | 640080 | 8046720 | 457200 | 18pt bold `111111` |
| Concept Bank instruction | 548640 | 1097280 | 8046720 | 457200 | 12pt |
| Concept Bank term, column 1 | 548640 | row y | 1554480 | 292500 | 12pt bold `028090` |
| Concept Bank cell, column 1 | 2194560 | row y | 2286000 | 548640 | fill `F2F6F9` |
| Concept Bank term, column 2 | 4663440 | row y | 1554480 | 292500 | 12pt bold `028090` |
| Concept Bank cell, column 2 | 6309360 | row y | 2286000 | 548640 | fill `F2F6F9` |
| Concept Bank links block | 548640 | 5852160 | 8046720 | 457200 | 11pt |
| Visibility ladder, subhead | 548640 | 1042000 | 8046720 | 457200 | 11pt, gray |
| Visibility ladder, body | 548640 | 1554480 | 8046720 | 5120640 | 11pt, one column |

The seven Concept Bank row y values are **1554480, 2148840, 2743200, 3337560,
3931920, 4526280, 5120640**. The row pitch is 594360 and the row height is 548640.
Column 2 begins at 4663440, which is column 1 plus its width of 3931920 plus a gap
of 182880. Inside a column the term box is 1554480 wide, then a gap of 91440, then
the cell at 2286000. The grid ends at 5669280 and the links block starts at
5852160. The Concept Bank slide carries no "Think first" footer, so nothing sits
below the links block.

The term box is centred on its row: its y is the row y plus 128070, which is half
the difference between the 548640 row and the 292500 box.

These values are as built and verified against a render on 2026-08-18. The first
build used a 1097280 term column and a 274320 instruction line. Both failed on the
render: `Decomposer` and `Commensalism` wrapped mid-word, and the third line of the
instruction was cut by the top of the grid. Text checks passed on that build. Only
the render found it, which is why §11 requires one.

The left margin is **548640** and the content width is **8046720**. The kicker and
the footer are the only two elements that sit outside that column.

### 13.4 Type scale

**Revised 2026-08-17 by Katherine: student-displayed body text is now 18pt,
bulleted where it reads as a list, with 8–10pt paragraph space after every
bulleted item so items breathe.** Same slide role = same size in every deck.

| Text | Size | Weight | Color |
|---|---|---|---|
| Teacher reference title | 20pt | bold | `111111` |
| Section label (ESSENTIAL CLAIM, OBJECTIVES) | 10pt | bold | `028090` |
| Kicker | 11pt | bold | `028090`, or `C0392B` on a Pattern break |
| Slide heading | 20pt max | bold | `111111`, or `028090` on Build a Rule |
| Lead / question / rule sentence, main teaching prose | **18pt** | bold (leads) / plain (body) | `111111` |
| Day-divider body | **18pt**, bulleted | plain | `111111` |
| CASE A / CASE B label | 11–12pt | bold | `028090` |
| Case body (dense paired columns) | 12–14pt | plain | `111111` |
| Activity steps | 14–16pt | plain | `111111` |
| Tier label | 12pt | bold | `C0392B`, `111111`, `1E8449` |
| Tier question | 12pt | plain | `111111` |
| Word bank label | 9pt | plain | `666666` |
| Word bank items | 10–11pt | plain | `111111` |
| Response-slide instruction + box labels | 14pt | plain | `111111` |
| "Write your answer in the next slide" arrow | 14pt | bold | teal or gray (Arial — the old 32pt Calibri is a defect) |
| Concept Bank instruction | 12pt | plain | `111111` |
| Concept Bank term | 12pt | bold | `028090` |
| Concept Bank source link, label | 11pt | bold | `111111` |
| Concept Bank source link, linked text | 11pt | plain, underlined | `028090` |
| "Think first" footer | 10pt | plain | `666666` |

Titles are **20pt at the largest**. Main student-facing prose is **18pt**; dense
slide roles (case pairs, 3-Tier, word banks, bellringer sidebar) sit consistently
below it. Where 18pt collides with an image or a writing box, fix the geometry
from a render — or apply the dense-slide exception consistently, never ad hoc.

### 13.5 How to check

After each build, list every text run with its size and color. Compare the list
to the tables above. Then compare it to the same list from Cycle 02. A color or a
size that appears in your deck but not in Cycle 02 is an error.

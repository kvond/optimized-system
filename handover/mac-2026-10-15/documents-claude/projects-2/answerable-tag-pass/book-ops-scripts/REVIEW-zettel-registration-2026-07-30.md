# Zettel registration review — 2026-07-30

**Status: HOLD. Nothing written to the graph.** Registration is on hold pending Katherine's
adjudication — see the correction below.

Read-only scan of graph `kvond` found **295 `📇` pages; 257 carry the
`Index:: [[🌿 Evergreen Notes]]` registry backlink; 38 do not.** My first pass proposed
bulk-registering 34 of the 38. **That was wrong** — a per-page inspection showed these are
not built-out zettels.

## Correction — what the 38 actually are

Registration (per chapter-bank `reference/zettelkasten.md`) presupposes canonical form:
title + `[[Template - Zettel Claim]]` body + `Meta::` (`Provenance::`, `Index::`, `Origin::`).
None of the 38 have that. Inspecting all 34 "Group A" pages:

- **4** — empty (title only, zero blocks)
- **25** — only a `Processed:: [[July 21st, 2026]]` stamp, nothing else
- **5** — a little more (relation links `Extends::`/`Related::`, a duplicate-fork warning,
  or Claude-tagged working notes) but still no template body, no `Meta::`

The claim exists only as the **page title**. These are **harvest artifacts from a July 21
processing pass** — pre-registration candidates in the harvest pipeline whose adjudication is
Katherine's ([[Zettel-harvest]] · [[zettel-harvest review]]). Stamping
`Index:: [[🌿 Evergreen Notes]]` onto them would file hollow shells into the evergreen index.

**`roam_bulk_ops.py` is guarded** — `--apply` now refuses to run without an explicit override
flag. Do not lift the guard until you've decided these title-claims are worth registering as-is.

---

_Original (superseded) grouping kept below for reference._

The 38 split two ways.

## Group A — register (34)

Genuine claim/concept zettels missing only the registry backlink. Adding
`Index:: [[🌿 Evergreen Notes]]` is reversible and loses no distinction, so
`roam_bulk_ops.py` will apply just this one backlink per page (under an existing `Meta::`
if present; otherwise it mints a `Meta::` parent first). It does **not** fill `Provenance::`
(auctor | grounded) or `Origin::` — those need your judgment and stay a separate pass.

| # | uid | title |
|---|-----|-------|
| 1 | w0YRFWyr0 | 📇 Adjacency is developmental |
| 2 | kgy2Q5CLN | 📇 What a teacher cannot see, a teacher cannot support |
| 3 | k4jjJ7YJo | 📇 Marcus didn't need rebuilding; he needed translation |
| 4 | edmnP3_yO | 📇 AI is a presence-augmenter, not a teacher replacement |
| 5 | 5Gjv-yPjd | 📇 AI trained on correct outputs will replicate the misreading of high-poverty students |
| 6 | Wt7OGplmg | 📇 The teacher curates the object and retains evaluation while protecting the knower-stance |
| 7 | 3HWzVky4g | 📇 Under-prescription can exhaust curiosity as surely as over-prescription |
| 8 | IlCYwOG64 | 📇 The Germantown gap is the arithmetic of exhaustion, not a failure of parental love |
| 9 | AjDW96_jQ | 📇 The school's engagement measure counts only engagement flowing toward the teacher's frame |
| 10 | KaZlVd_aX | 📇 Prepare the play around the critical aspect rather than wait for interest to appear |
| 11 | XTivY-9BQ | 📇 Nancy — epistemic agency (coin flowers) |
| 12 | L62rRTiB4 | 📇 Agency is a capacity built from the outside in, not a personality trait |
| 13 | 2evDOtfG8 | 📇 A well-built question generates interest; interest is an output of design, not a precondition |
| 14 | g1bLmDssm | 📇 Inquiry is a consequence of teaching, not its precondition |
| 15 | dLjHYl0FQ | 📇 Being responsible for one's words means one's identity and self are present in them |
| 16 | xpRI62PA6 | 📇 Reading the room for knowers is a learnable skill, not a metaphysical gift |
| 17 | qZpJd04cE | 📇 Structure that hands itself over — the developmental warrant |
| 18 | pS_aF6-kF | 📇 The teacher's agency is also at stake and develops through these encounters |
| 19 | 50h8hWvs2 | 📇 Authorial and epistemic agency are orthogonal, not sequential — they can coexist but need not |
| 20 | 0IDhT3nVi | 📇 The agency taxonomy is a perceptual instrument, not a production rubric |
| 21 | WLXpvsk7g | 📇 Cultural capital is the experiences school expects; wealthy children can lack it too |
| 22 | 0Xo0g4DlZ | 📇 Agency lives in the held tension between centripetal curriculum and centrifugal student purposes |
| 23 | EOsdpeh28 | 📇 Biesta names the event, Bakhtin the medium, the taxonomy the terrain |
| 24 | GoOo9gdZp | 📇 Unread thinking is invisible; misread thinking is seen as its opposite |
| 25 | L3xgscROU | 📇 The book is diagnostic before it is prescriptive |
| 26 | tKmlRGrGC | 📇 A property of a relation exists only in the relation, so stripping context strips the thing itself |
| 27 | KVUlBw0I1 | 📇 The five movements are not a recipe but the conditions under which the teacher's perceptual capacity sustains itself |
| 28 | 4dcHyt1kO | 📇 A student's originating move is legitimate at its source, which removes two gates the field erected — intentionality and teacher perception |
| 29 | 66wKZFjmc | 📇 Even a few experiences of being seen matter, most of all in high-poverty schools |
| 30 | gGIwtL1tg | 📇 The progressive model suppresses origination; naive progressivism presupposes it; neither cultivates it |
| 31 | NDq96NrY- | 📇 None of the agency forms is a goal; when a teacher perceives how a student is already engaging, they can support it to emerge and become answerable to others |
| 32 | ts7MpqFMl | 📇 The equity injury is double: first the misreading, then the substitution |
| 33 | Caz8piXo1 | 📇 The seams are the perceptual frontier where a teacher feels a difference but cannot name it — where mētis operates |
| 34 | 8PZPlzbUL | 📇 Autonomy support works only for students who already have authorship (the Patall backfire) |

## Group B — flagged, NOT touched (4)

Format anomalies. Per chapter-bank ("strays flagged, not fixed"), the script leaves these
alone; each needs a decision from you.

| uid | title | why flagged | suggested fix |
|-----|-------|-------------|---------------|
| c_tBTzTLB | 📇 Projects | not a claim — looks like a mis-minted/junk page | inspect; likely quarantine or delete via UI |
| dECUV6a54 | 📇 QUE — … | empty template stub (the literal placeholder) | delete via UI |
| 6UkBW8y7H | 📇 QUE — Is agency the book's aim, or a symptom of intellectual authorship whose real aim is answerability? | a `QUE —` question mis-prefixed with `📇` (question, not claim) | UI-rename to drop the `📇` (make it a real `QUE —` node), then it registers as a question, not a zettel |
| 0-mfN-DBE | 📇 QUE — Is withholding he teacher's opinion respect, or its own evasion? | same `📇`/`QUE` mix-up, plus typo "he" → "the" | UI-rename: drop `📇`, fix "he" → "the" |

## #Book captures

106 blocks reference `#Book` cumulatively. I did **not** isolate the unrouted subset —
that needs more queries and I stopped to protect fable usage. If you want, a follow-up run
can list exactly which `#Book` blocks are still unrouted before spending more.

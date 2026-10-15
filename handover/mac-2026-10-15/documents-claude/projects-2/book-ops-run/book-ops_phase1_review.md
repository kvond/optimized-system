# Book-Ops — Phase 1 Review (read-and-propose)

**Nothing has been written to Roam.** This is the surface you adjudicate. Mark each item
keep / merge / alias / edit. Default, where unsure, is **keep separate** — a split is
recoverable, a merge is not.

**Run summary**
- Pull via Roam MCP Datalog (PAGES_Q, EDGES_Q, SNIPPET_Q). EDGES_Q returned reference
  edges fine — **no read-token fallback needed**.
- Daily-note pages excluded at query time (by DNP uid pattern). **467 non-daily pages**,
  1,000 backlink edges retained → `inventory.json`.
- `dedup_sweep.py` run as-is → **130 candidate pairs** (22 MERGE/high, 8 REVIEW/medium,
  100 keep-separate/low) + 306 residual titles for the semantic pass.
- Snippets were left empty in the inventory (the 185k-line SNIPPET pull was impractical to
  transport); the semantic layer was done by reading page **content** directly for the
  pairs that mattered, which is stronger than a 400-char snippet anyway.

Artifacts in this folder: `inventory.json`, `dedup_review.md` (raw script output),
`dedup_candidates.json`, `semantic_candidates.json`, `semantic_clusters.json`,
`proposed_q_pages.json`.

---

## Part A — Dedup merge candidates (deterministic layers 1–4)

### A1. MERGE / high — safe formatting/punctuation duplicates (recommend merge)

These are the same page split by punctuation, case, spacing, or smart-quotes. Low risk.

| canonical (keep) | fold (loser) | why |
|---|---|---|
| `2a` | `2a.` | trailing period |
| `2b` | `2b.` | trailing period |
| `AIHS` | `AIHS:` | trailing colon (loser empty) |
| `Book` | `Book.` | trailing period (loser empty) |
| `Teaching` | `Teaching.` | trailing period (loser empty) |
| `near` | `near.` | trailing period |
| `Weekly Distill` | `Weekly Distill ` | trailing space |
| `Are the goals of democratic pedagogy beyond the interests of students` | …`students?` | trailing `?` |
| `Arendt — totalitarianism eliminates the intermediaries` | `Arendt: totalitarianism…` | em-dash vs colon |
| `The developmental sequence — ability, agency, autonomy` | `The developmental sequence: ability → agency → autonomy` | em-dash vs colon/arrows |
| `The infantilizing–adultifying double error` | `The infantilizing/adultifying double error` | en-dash vs slash (canonical = higher backlinks) |
| `Gutmann, A. (1987). Democratic education. Princeton University Press.` | …without trailing period | citation punctuation |
| `Matusov, E. (2011). …An educational perspective…` | smart-quote twin | curly vs straight apostrophes |

### A2. MERGE / high — agency-taxonomy space-vs-hyphen variants ⚠ pick a convention first

Same concept, two naming schemes: prose uses **spaced**, your June-10 zettelkasten import
uses **hyphenated** (the Permanent Notes Index links the hyphenated forms). The script
picked spaced (more backlinks), but **canonical direction is yours to set** — and you
should set it once for the whole family so the permanent-note index stays consistent.

| spaced (script's canonical) | hyphenated | backlinks |
|---|---|---|
| `Authorial agency` | `Authorial-Agency` | 8 / 6 |
| `Democratic agency` | `Democratic-Agency` | 8 / 4 |
| `Engaged agency` | `Engaged-Agency` | 8 / 4 |
| `Epistemic agency` | `Epistemic-Agency` | 7 / 6 |

**Recommendation:** merge each pair, but decide spaced-vs-hyphenated deliberately. If the
zettelkasten index is canonical for you, flip these to the hyphenated form.

### A3. MERGE / high — NON-book pages (your call; out of manuscript scope)

Case variants among task/tracker tags, used in disjoint contexts (backlink overlap 0):

- `FINANCE` / `Finance` (loser empty) · `CALLS` / `calls` · `ERRANDS` / `errands`

Merge for tidiness if you like, but these aren't book vocabulary.

### A4. MERGE / high — ⚠ OVERRIDE: do NOT auto-merge

- **`agency` ⇄ `student agency`** — the script recommends folding `student agency` into
  `agency` (the skill's own worked-example case). **I recommend KEEP SEPARATE.** Your
  Book Summary uses them as distinct: `[[student agency]]` names the classroom-level
  emergent work specifically; `[[agency]]` is the general construct. The merge signal is
  weak — each has only 1 backlink, so the "1.0 overlap" is a single shared page. This is
  exactly the distinction the book would lose in a merge.
- *(`Health` / `Health Summary` and all other tracker/system pages dropped from scope per
  your instruction — no action.)*

### A5. REVIEW / medium — substring matches (recommend KEEP SEPARATE, all 8)

The fuzzy layer flagged these on shared words, but backlink overlap is low and they're
genuinely different pages:

- `Book` vs `Book Summary` · `Book` vs `Book Draft 2 (sourced notes)`
- `Teaching` vs `Teaching Summary` · `Personal` vs `Personal & Intuition Summary`
- `Distill` vs `Distill Routine` · `Tasks` vs `Google Tasks Inbox`
- `Next` vs `AI Agents.School.Planning Next Steps`
- `The imaginary chronotope` vs `Lima & von Duyke (2016) — the imaginary chronotope`
  (concept vs its citation — keep separate, or make the citation an **alias**)

(The 100 low-confidence keep-separate pairs are in `dedup_candidates.json` if you want them.)

---

## Part B — Semantic clusters (layer 5, by me)

306 residual titles clustered by meaning; the top candidates were **verified by reading
the actual pages**.

### B1. Verified duplicates — recommend MERGE

1. **`Burgh — democracy is a process, not something to educate toward`** (keep, has the
   full note) ⇐ fold **`Burgh — democracy is a process, not a destination`** (empty stub).
2. **`Real (2022), Us — the relational critique of individualism`** (keep) ⇐ fold
   **`Real (2022), Us…`** (empty stub). *The full note's source-trail explicitly says the
   original page "can be safely deleted."*
3. **`Individualism is a theory of society, not its opposite`** (has content) ⇐ fold
   **`Individualism is a theory of society, not of the lone individual (Hayek)`** (empty).
   ⚠ *Canonical direction:* content lives in "not its opposite," but the empty "(Hayek)"
   title is arguably clearer and is the one the Real note links to. Your pick.
4. **`Dialogism dissolves the intrinsic/extrinsic motivation dualism`** (correct spelling,
   the title to keep) ⇐ **`Dialogism dissovles the internal/external divide`** (typo title
   — but this is where the **content actually lives**). ⚠ *This is a content-move merge:*
   move the prose into the correctly-spelled page, then fold the typo page.

### B2. Related-but-distinct — recommend KEEP SEPARATE

- **`Autonomy, Agency, Individualism & Equity`** vs **`Individualism and Society, Agency,
  Autonomy and Equity`** — *verified:* the first is an overview/map that references the
  second as its "synthesis spine." Cross-cutting, **not** a duplicate.
- `Dialogism is not dialogue` vs `Dialogism-Is-Not-Discussion` — both substantive notes;
  dialogue ≠ discussion is likely intentional. (Look only if you consider them redundant.)
- `Equality of intelligence (Rancière)` vs `…and resistance as voice (Rancière, via
  Waghid)` — possible stub vs expanded (bl 1 vs 7); unverified, worth a glance.
- `Communities of Practice` vs `Communities of practice and legitimate peripheral
  participation` — possible stub; distinct from `Communities of inquiry` (different lineage).
- `The four levels where democracy lives in a school` vs `Democratic Institutions and
  Schooling Practices Across Levels` — overlapping theme, likely one claim + one matrix.

### B3. Out-of-scope noise (not merges, FYI)

~60+ of the 467 pages are not book vocabulary: `roam/js/pdf/data/*` (24 plugin-data pages,
all bl=0), health/daily-brief trackers (Calories, Carbs, Protein, Weight, Sleep Hours,
Neck, Morning Headache…), photo pages (Childhood/Christie/Heidi/James/Scott Photos, Photo
Archive…), and system pages (`roam/css`, `roam/js`, `kvond`, `s`, `table`). Candidates to
**exclude from future vocab pulls**, not to merge.

---

## Part C — Proposed `QUE —` pages (from criticism / unresolved spots)

✅ **Convention resolved: `QUE —`** (plugs into your depot program's evidence-link writing
section; keeps all questions in one queryable namespace). I patched `on_create_check.py`
and `dedup_sweep.py` so `is_q` recognizes the `QUE —` prefix, then **re-ran the real
on-create check** for all 18 drafts against your 19 existing question-type pages — every
one returned **clear** (no true duplicates). Two stay adjacent-but-distinct: #8 near
`QUE — Is withholding the teacher's opinion respect…`; #12 near both the `The shadow of
dialogue` concept page and `QUE — Does the "as if" protection make the dialogue less
real?`. Full per-draft results in `proposed_q_pages.json`; the script patch is logged in
`change_log.md`.

Sources read: `Addressing Criticisms` (primary), `Beyond Motivation` (conceptual core),
`Book Summary`, `Author Block - finishing Map`. `Anthropic prospectus` exists but is
**empty** — nothing to extract. (`Author Block` is almost entirely WRITE/DECIDE/FIX/VERIFY
editorial tasks, not conceptual questions, so its items are folded into the structural one
below rather than minted as Q-pages.)

### C1. High-priority drafts (recommend mint)

1. **QUE — what stops the legibility regime from capturing the AI-freed time as throughput
   rather than presence?** — *Addressing Criticisms* (the capture critique).
2. **QUE — does the agency taxonomy finalize students in a book committed to
   unfinalizability?** — *Addressing Criticisms* (the Bakhtinian objection).
3. **QUE — does the apprenticeship produce more emergent authorship than autonomy alone?** —
   *Beyond Motivation* (your stated falsification test).
4. **QUE — does autonomy support help the students who need it most, or only the
   already-prepared?** — *Beyond Motivation* (the Patall backfire).
5. **QUE — can AI's pedagogical defaults be bent toward a knower-stance at scale?** — *Beyond
   Motivation*. (Related to #1 but distinct: the tool's defaults vs institutional capture.)
6. **QUE — how can a teacher receive an epistemic bid without correcting it into
   compliance?** — *Beyond Motivation* (chapter-driving question). *Near:* `QUE — Is
   withholding the teacher's opinion respect, or its own evasion?` (distinct).
7. **QUE — how does direct instruction create the perceptual conditions for dialogue instead
   of replacing it?** — *Beyond Motivation*. *Near concepts:* `Conceptualization-vs-
   Explanation`, `The constitutive epistemology`.
8. **QUE — when does dialogic teaching become covert coercion?** — *Beyond Motivation* (the
   shadow of dialogue; Bhaer/Tom double-bind). ⚠ *Near:* concept page **`The shadow of
   dialogue`** (bl=5) — fold into it, or mint as its explicit Q form.
9. **QUE — does naming both regimes "legibility failures" flatten the political asymmetry
   between them?** — *Book Summary* (Tensions).
10. **QUE — does the agency framework quietly re-center the very self it decenters?** —
    *Book Summary* (Real's ego-to-eco margin question, turned on the book).

### C2. Medium-priority drafts

11. **QUE — who is the standard curriculum actually built for?** — *Beyond Motivation*.
12. **QUE — how does giving students voice at school affect their authority relationships at
    home?** — *Beyond Motivation* (the professor's question).
13. **QUE — is the dialogism–Variation Theory bridge original, or already made in the
    literature?** — *Beyond Motivation* ("worth a literature check"). *Near concept:*
    `Bakhtin-Variation-Theory-Bridge`.
14. **QUE — how to reconcile the no-excuses critique with evidence that such schools reduce
    dropout?** — *Beyond Motivation* (standing caution).
15. **QUE — does the method-enacts-the-claim self-exemplification prove too much?** —
    *Book Summary* (Tensions).
16. **QUE — is authorship counted across modalities, or only in writing?** — *Book Summary*
    (the engaged→epistemic bridge). *Near concept:* `Engaged-to-Epistemic-Bridge`.

### C3. Low-priority / maybe-not-a-Q

17. **QUE — is the pacing-guide mismatch district-specific or systemic?** — *Beyond
    Motivation*. Empirical scope question; might be a footnote, not a page.
18. **QUE — should legibility be its own chapter or the framing device for the
    motivation→agency move?** — *Book Summary*. Structural/editorial decision (this is also
    where the `Author Block` "DECIDE" items live).

---

## What I need from you

1. **Dedup:** approve A1 as a batch? Set the agency-family canonical (A2: spaced or
   hyphenated)? Confirm the A4 override (`student agency` stays separate)?
2. **Semantic:** approve the four B1 merges — note #3 needs a canonical pick and #4 is a
   content-move, not a plain repoint.
3. **Questions:** which of the 18 `QUE —` drafts to mint. (Convention already resolved =
   `QUE —`; the on-create check ran clean against existing pages.) For #12, decide whether
   to mint it or instead hang evidence on the existing `The shadow of dialogue` page.
4. Then I run the apply steps (repoint references, stub/alias losers, create approved
   `QUE —` pages, update `vocabulary.json` + `change_log.md`) — and I'll snapshot/export the
   graph before any merge touches it.

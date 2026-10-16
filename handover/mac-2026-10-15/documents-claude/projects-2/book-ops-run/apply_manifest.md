# Book-Ops Phase 1 — APPLY MANIFEST (awaiting snapshot + final OK)

Status: **NOT YET EXECUTED.** Merges run only after you confirm a graph export exists.
Applies against the CURRENT inventory: `inventory2.json` (485 pages, pulled after your pass).

Graph note: the book hub `Beyond Motivation` was **renamed to `Answerable Teaching`** in
your pass; Roam auto-repoints the old links. Question-page source attributions that read
"Beyond Motivation" are updated to `Answerable Teaching`.

## Step 0 — Snapshot (YOU)
- Roam: File → Export All → EDN (or confirm git `source/` is current). This is the only
  restore point; merges are not reversible without it.

## Step 1 — Create 18 QUE pages (additive, safe)
Each page seeded with one block: `Type: #<tag> · Source: [[<source>]] (<descriptor>)`.
(Sources formerly citing "Beyond Motivation" now cite `Answerable Teaching`.)

Type 1 — `#q-book-resolves`: 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 17
Type 2 — `#q-about-book`: 1, 2, 11, 15, 16, 18

(Full titles + sources in `proposed_q_pages.json`. #12 noted as overlapping the existing
`The shadow of dialogue` concept page — minting per your "all," flag stands.)

## Step 2 — Merges (DESTRUCTIVE — after snapshot)
Method per skill: repoint every `[[loser]]` reference to canonical, then stub/alias loser.

### A2 — agency taxonomy, canonical = HYPHENATED (your call)
- `Authorial-Agency` ⇐ `Authorial agency`
- `Democratic-Agency` ⇐ `Democratic agency`
- `Engaged-Agency` ⇐ `Engaged agency`
- `Epistemic-Agency` ⇐ `Epistemic agency`

### B1 — semantic merges (verified)
1. `Burgh — democracy is a process, not something to educate toward` ⇐ `…not a destination` (empty; repoint)
2. `Real (2022), Us — the relational critique of individualism` ⇐ `Real (2022), Us…` (empty; repoint)
3. `Individualism is a theory of society, not of the lone individual (Hayek)` ⇐ `…not its opposite`
   — **content-move:** move prose into the Hayek title, then fold "not its opposite."
4. `Dialogism dissolves the intrinsic/extrinsic motivation dualism` ⇐ `Dialogism dissovles the internal/external divide`
   — **content-move:** move prose into the correctly-spelled title, then fold the typo page.

### A1 — punctuation cleanup: JUST `Book` (your call — rest of batch deferred)
- `Book` ⇐ `Book.` (empty page)
- *(Deferred, not this run: the Gutmann/Matusov citation twins, `Arendt —`/`Arendt:`,
  the developmental-sequence and infantilizing variants, `2a`/`2a.`, `AIHS`/`AIHS:`,
  `Teaching`/`Teaching.`, `near`/`near.`, `Weekly Distill`, the trailing-`?` page.)*

### A3 — non-book case variants (approved, all-caps canonical)
- `FINANCE` ⇐ `Finance` · `CALLS` ⇐ `calls` · `ERRANDS` ⇐ `errands`

### A4 — chapter tag case variant (your add)
- `Ch5` ⇐ `CH5` (canonical matches your `Ch 5` / `Ch 3` / `Ch N` house style)

## Step 3 — Bookkeeping
- Update `vocabulary.json` (canonical names + approved aliases) and append one line per
  change to `change_log.md`.

## Explicitly NOT touched
- `agency` / `student agency` (kept separate). Health/tracker/system pages (out of scope).
- All B2 related-but-distinct pairs; all REVIEW/medium pairs (keep separate).

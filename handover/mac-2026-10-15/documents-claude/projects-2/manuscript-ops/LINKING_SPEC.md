# Answerable Teaching — Inline Linking Spec

How concepts, questions, and criticisms get wired into the chapter pages. Captured 2026-06-16.
Status: Chapter 1 ✅, Chapter 2 ✅. Chapters 3–11 pending.

## Rules
- **Aliased links only**, preserving the displayed prose exactly: `[displayed words]([[Target Page]])`.
  Never change wording, punctuation, or smart quotes — only wrap existing text.
- **Link the first meaningful occurrence** of a concept per chapter (don't over-link repeats).
- Pull verbatim block strings before editing (datomic `:block/string`) to avoid transcription drift.
- Only link to pages that already exist (verify first) — never create stub pages by linking.

## Criticisms placement
- Default: a top-of-chapter block `**⚠ Criticisms to address — review before writing**` with the
  relevant `QUE —` link(s) + source `[[Addressing Criticisms]]`, on the FIRST chapter each applies to.
- Katherine repositions per chapter logic (e.g., Ch 1's was moved to the end so the fluidity-of-agency
  point lands after the reader grasps that there is more than one kind of agency).

## Controlled vocabulary (term in prose → target page)
**Taxonomy / agency notes (hyphenated zettelkasten):**
engaged agency→[[Engaged-Agency]] · epistemic agency→[[Epistemic-Agency]] · effortful agency→[[Effortful-Agency]] ·
pseudo-agency→[[Pseudo-Agency]] · democratic agency→[[Democratic-Agency]] · authorial agency→[[Authorial-Agency]] ·
the agency taxonomy→[[The-Agency-Taxonomy]] · teacher perception / reading the room→[[Teacher-Perception-Is-the-Variable]] ·
autonomy≠authorship→[[Autonomy-Is-Not-Authorship]] · autonomy precedes agency→[[Autonomy-Precedes-Agency]] ·
motivation vs agency→[[Motivation-vs-Agency]] · centripetal/centrifugal→[[Centripetal-Centrifugal-Infrastructure]] ·
head down is data→[[Head-Down-Is-Data]] · controlling environments→[[Controlling-Environments-Produce-Compliance]] ·
conceptualization vs explanation→[[Conceptualization-vs-Explanation]] · ed-tech/AI changes delivery→[[EdTech-Changes-Delivery-Not-Pedagogy]] ·
dialogism is not discussion→[[Dialogism-Is-Not-Discussion]] · Bakhtin–VT bridge / Variation Theory→[[Bakhtin-Variation-Theory-Bridge]] or [[Variation Theory]]

**Claim / concept notes (spaced):**
access (is not enough)→[[Access-Is-Not-Enough]] · footing→[[Footing]] · Germantown→[[Germantown library study]] ·
legibility / legibility regime→[[legibility]] · motivation misdiagnoses→[[Motivation misdiagnoses demotivation]] ·
fit meaning rather than make it→[[Fit meaning rather than make it]] · pseudo-agency is a system product→[[Pseudo-agency is a system product, not a student failure]] ·
intrinsic/extrinsic boundary dissolves→[[Dialogism dissolves the intrinsic/extrinsic motivation dualism]] ·
dysfunctional agency→[[Dysfunctional agency]] · agency is ecological→[[Agency is ecological]]

**Open questions (QUE):** link the relevant `QUE —` page at the sentence that raises it (e.g. "imagined
student"→who-is-curriculum; autonomy backfire→does-autonomy-support-help; epistemic bid unread→receive-an-epistemic-bid).

## Citation links (compact reference pages)
Each in-text citation links to a compact **[[Author, Year]]** page (NOT the full-citation string).
- **Page title = the in-text cite form**: `[[Bakhtin, 1981]]`, `[[Anderson & Winthrop, 2025]]`,
  `[[Patall et al., 2022]]` (first author + et al. when 3+). The full APA reference lives in the page
  body (first block), tagged `#reference`, with `Master entry: [[Answerable Teaching/References]]` and a
  `Discussion::` block. "Where cited" is automatic via the page's Linked References (edit the book → page updates).
- **Aliased, prose-preserving**: wrap the existing in-text cite, e.g. `[(Bakhtin, 1981)]([[Bakhtin, 1981]])`
  or `[Patall, Kennedy, et al., 2022]([[Patall et al., 2022]])`. Never alter the displayed words.
- **One page per source** — never the full-citation string as a page title (that older convention is
  retired; the Patall/Matusov full-citation pages were migrated to compact form 2026-06-26 — see
  `migration-restore-2026-06-26.md` for the rollback record).
- **Per-chapter section**: each chapter ends with a `### References cited in this chapter` list of the
  linked pages (doubles as backlink fodder). The tag-pass appends to it as it links each cite.
- Year-less mentions (e.g. a bare "Patall") stay unlinked until a year is supplied.
- Status: Ch 1 citations ✅ (prototype, 2026-06-26). Ch 2–11 pending.

## Criticism → first chapter map (extend as chapters are tagged)
- Ch 1: [[QUE — Does the agency taxonomy finalize students in a book committed to unfinalizability?]] (taxonomy renders students into categories)
- Ch 2: [[QUE — How do you reconcile the no-excuses critique with evidence that such schools reduce dropout?]] (structural/deficit-model argument)
- Ch 6 (planned): the AI "capture" critique → [[QUE — What stops the legibility regime from capturing the AI-freed time as throughput rather than presence?]]
- Closing chapters (planned): self-exemplification / re-centering critiques.

## Tag hub
`[[Answerable Teaching/Tag Hub]]` — alphabetical index of every link in use; refresh (full rewrite) after each chapter.

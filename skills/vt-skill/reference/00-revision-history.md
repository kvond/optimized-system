<!-- Part of vt-skill. Moved verbatim from SKILL.md on 2026-10-19. -->

# vt-skill — revision history

Katherine established this skill on 2026-08-06, on Cycle 2.

Revised 2026-08-12. The revision changed the reference build, removed three slide
types, removed the slide numbers in the corner, moved the revision prompt into the
speaker notes, and replaced the batch pipeline with three prompts.

Revised 2026-08-17, by Katherine's direction. This revision changed the type scale
(student body text is now 18pt, bulleted, with space after each item — see §13.4),
permitted Claude to draft NGSS codes (see §5), retired standalone activity guides
(see §4b), added the Teacher Prep slide as standard slide 2 (see §2.0), added the
Bellringer FOR READERS / FOR TESTERS lines (see §2.0), made the closing checklist
conditional on non-duplication (see §2.2), and corrected the stale script IDs in
§11. All 26 decks were brought to this standard on 2026-08-17.

Revised 2026-08-18, by Katherine's direction. This revision added the **Concept
Bank slide** as a required slide immediately before the Day 3 divider (see §3b and
§2.2), and **scoped this file to Biology**, because Katherine now labels the
deck-finishing skills by course (see §15). The file was renamed
`vt-bio-skill` on Katherine's instruction. She asked for `VT_Bio_skill`; skill
`name` values take lowercase letters, digits and hyphens only, and the save
normalises anything else, so the file now carries the normalised form directly
rather than relying on the save to fix it. All 26 Biology decks need the Concept Bank retrofit;
the reference build takes it first (see §14.2). It added **§9.1**, which records
that a locally built deck cannot be uploaded through Composio. It recorded the
measured finding that the exclusion list matches nothing in Cycle 02 (see §7.1). The revision also wrote down the
**diagnostic-count exclusion list** and the rule that it is edited in two files in
one pass, and recorded the Continuation / Continuity name mismatch as an open
defect (see §7.1). It also permitted a
second Concept Bank slide where a cycle carries more than fourteen terms (see §3b).
It recorded that a
second `.pptx` in a cycle folder is an EXTEND deck (§0), and that the agenda
carrying fewer cycles than the product is deliberate (§9.3a). It added **§3c**,
which documents the marker fault the
Concept Bank build surfaced — an ellipsis broke the linter while the grader kept
working — and makes reading the `markers present:` line a standing check.

Revised 2026-08-29, by Katherine's direction. The conditional slide types are now
**four**, not two — the compensatory pair and the conflict case join the Continuity
question and the Stock-and-flow model as moves 8 and 9 (see §1). This revision
added **§2.0a, the teacher note slide**, one slide rather than speaker notes,
carrying seven declarations, its absence a hard failure. It made the **What if
individual and written** without exception and gave it its two constraints (§2.2).
It made the Concept Bank ask the student **how two terms connect**, because
co-presence is the precondition and not the achievement (§3b). It added the
delivery checks that follow, and marked which of them are advisory rather than
hard (§11). The word forbidden by §1 was removed from §1 itself, which had been
the last place in this file it appeared.

Revised 2026-09-03, by Katherine's direction. §0 and §11 now name the repository as the
only place a script is fetched from, and the Drive IDs are retired. Cause: a Cycle 01
check that morning ran the stale Drive `deck_lint.py` and under-reported by nine hard
failures. Also recorded in §7.1a: the exclusion-list sync rule is now a repository edit,
not a four-copy edit.

Revised 2026-10-15, by Katherine's direction (Slack #vt-decks). Added **§16**, which brings
the restore, enhance, code and agenda-link passes into this skill, so a deck comes out
finished and doesn't need repairing later. §16 is course-neutral. Until the Forensics and
A&P forks exist (§15), it is the rule for those courses' decks too.

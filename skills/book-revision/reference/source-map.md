# Source map

Read `../SKILL.md` first; its mandatory boundaries still govern. Path bases do not change when detail moves here: own `scripts/` and `reference/` paths are relative to the original skill root; named sibling-skill paths such as `book-revision/scripts/` are relative to the shared `skills/` directory. Manuscript `revision/` and `book-compile/` paths belong to the designated private manuscript repository; data and derived artifacts belong only in authorized private staging. Never interpret them as paths inside this reference directory or publish private artifacts to the public skills repository. These extracted instructions preserve existing rules; they grant no new authority.

## Where things are

| What | Where | Account or route |
|---|---|---|
| The single live working copy and canonical source | Google Doc "Answerable Teaching — Full added notes", id `1O5it34GtqSnwNu5CReDt_5X7Kx05m8xEWUcROD9cgk8` | higher-ed Drive (`kvond@udel.edu`); this is the only live source |
| The earlier Working Copy | Google Doc id `1RuY6yj9mhqBajj-UYhF_WCQwEpvLKinMma9fKNAStlM` | historical only; recover from it only when Katherine explicitly asks |
| The snapshot a pass works from | `revision/manuscript/working-copy-<date>.md` in `kvond/Answerable-Teaching` | git backup/version-history layer; export from the live Doc at the start of a pass; never treat as a competing source |
| The AI chapter as assembled 2026-09-11 ("Doable, Not the Doer") | `book-compile/ch6-doable-not-the-doer-assembled.md` in `kvond/Answerable-Teaching` | git; not yet in the Doc |
| The practice chapter ("Before Inquiry", subtitle "Inquiry Has Prerequisites"), missing from the Doc | `book-compile/ch6-intellectual-mentorship-rewrite.md` (Aug 23, the fuller form) and `revision/reference/ch05-earlier-draft-2026-05.md` (May, her supply of 2026-09-12) in `kvond/Answerable-Teaching` | git; R16, R20, and R21 in the ledger |
| Rulings recovered from the retired provenance register (title, "the adult who lingers", the pseudonym ledger and name-change log, Moore-Anderson placements) | `revision/reference/rulings-from-register-2026-08.md` in `kvond/Answerable-Teaching` | git |
| The voice instruction and the hard bans | `book-compile/voice-guide.md` (marker 15 and four Part 3 checks added by her on 2026-09-12), `book-compile/tics-list.md` in `kvond/Answerable-Teaching` | git |
| Her manuscript checks of 2026-09-12 (nine checks: student visibility, move names, the theory-movements-moves pipeline, causal overclaims, equity caution, the doubt passage, the IPD citations, the Ito framework, AI voice resistance) | `reference/manuscript-checks.md` beside this file, a verbatim copy of the file inside her `book-compile/answerable-teaching-review.zip` (the review skill she built for another tool; its SKILL.md is not used here) | git; R22 in the ledger |
| The argument arc, the glossary, the six analytical levels | `reference/argument-arc-and-glossary.md` beside this file | git (`kvond/answerable-skills`) |
| The decisions ledger | `reference/decisions.md` beside this file | git |
| The findings the lanes work from | `reference/findings/` beside this file (the external reader's review and the continuity pass of 2026-09-12) | git |
| The mechanical checker | `scripts/manuscript_check.py` beside this file | run it on the snapshot before and after a pass |
| Lane packets and the integrator's output | `revision/packets/<lane>/<chapter>.md` and `revision/integrated/` in `kvond/Answerable-Teaching` | git |
| Roam graph `kvond`, "Answerable Teaching/" pages, and the repo's `source/` and `writing/` folders | older exports (last nightly publish 2026-07-02). Not the current draft. Reconciliation is decision P18. | read only during a pass |

Engine start: a Cowork session reaches the repos through the GitHub connector and the canonical Doc through the higher-ed Drive connection. A Claude Code session on the Mac reads this skill through `~/.claude/skills` (a symlink into `~/code/answerable-skills/skills`) and works in the clone of `kvond/Answerable-Teaching` (`SYNC.md` names `~/Documents/projects/Answerable-Teaching`, but on 2026-09-12 that folder held only the nightly-publish log; where the clone now lives is an open item for her). If a path here does not resolve, the account or the clone is wrong; the skill is not broken.

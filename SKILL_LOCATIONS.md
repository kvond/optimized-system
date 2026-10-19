# Where skills live, and why

Settled 2026-08-29 after a reconciliation across every location.
At that point every duplicated skill was byte-identical, so nothing
was overwritten and no version was lost.

Reconciled again later on 2026-08-29. A second clone at `~/answerable`
had been carrying twelve skills, `reference/`, and this file on an
unpushed commit, against a stale `origin/main`. They are all here now
and pushed. See Retired.

## Here — `skills/`

Every skill used interactively. This repo is the canonical one:
`kvond/optimized-system` (formerly `kvond/answerable-skills`), cloned at
`~/code/optimized-system`.

`~/.claude/skills` is a symlink to `~/code/optimized-system/skills`,
so editing through `~/.claude/skills` edits the repo. Commit and push
to update every machine. If that symlink ever points somewhere else,
edits are landing outside the repo — repoint it.

`daily-route` was removed on purpose (7a84b6a) and should not come
back from an older copy.

## Not here — `kvond/scheduled-runs`

Thirteen job definitions, each with its own SKILL.md: aihs-update,
answerable-nightly-distill, author-block, book-ops-inventory-rebuild,
book-ops-monthly-full-sweep, daily-brief-v2, daily-spanish-lesson,
learning-block-agenda, overnight-book-graph-build, second-brain-distill,
sunday-weekly-sweep, tags-pages-sweep, wilmu-update.

They stay there because the scheduler reads them from that repo. Moving
them would break running jobs for no benefit.

## Not here — `kvond/Answerable-Teaching`

The book publishing pipeline: book-compile, scripts, source, writing,
nightly-publish.sh, and com.kvond.answerable-publish.plist. It contains
no SKILL.md files. `com.kvond.answerable-publish` is loaded and running
on the Mac — do not disturb it.

## Not here — Google Drive

Decks and other artifacts. Drive is their source of truth. `.gitignore`
blocks .pptx, .gslides, and credentials.

## Retired

`~/Desktop/claude/katherine-ops` was merged into this repo and moved to
`~/skills_recon/`. Nothing was lost; every skill it held is either here
now or was already here identically.

`~/answerable` — a full second clone of this same repo, on a stale
`origin/main`. Its unique content was merged here on 2026-08-29 and
pushed. It is left on disk but is no longer authoritative: it does not
have `scripts/`, `docs/tpt/`, or any of this repo's commits after the
initial one (its own unpushed `dbd6244` aside), and its
`skills/vt-bio-skill/SKILL.md` predates the corrections in 556a514.
Do not edit skills there. Backup of both trees, with their git
histories, is in `~/skills_recon/pre_reconcile_2026-08-29_1542/`.

# Answerable Teaching

Canonical source for the skills, specifications, prompts, and working documents
behind the Answerable Teaching curriculum and book.

**Private repository.** `skills/vt-skill/SKILL.md` contains Google Drive
file IDs, and several skills touch student work.

---

## What is here, and what is not

**Here:** text that governs the work — skills, specs, prompts, scripts, notes.
Versioned, diffable, read identically by every machine and every Claude surface.

**Not here:** the artifacts the work produces. Decks live in Google Drive.
They are binary, they change constantly, and they already have a source of
truth. Adding them to git would create a second one. `.gitignore` enforces this.

---

## Layout

```
skills/     Active skills. Symlinked to ~/.claude/skills so every local
            Claude reads the repo directly.
archive/    Retired skills. Kept for reference, not loaded.
docs/book/  Manuscript-side notes, positioning, reading.
docs/curriculum/  Teacher-facing and deck-design documents.
prompts/    Claude Code job prompts.
tools/      Scripts that operate on this repo.
```

## Setup on a new machine

```
git clone <repo-url> ~/answerable
mv ~/.claude/skills ~/.claude/skills.backup
ln -sfn ~/answerable/skills ~/.claude/skills
```

After that, `git pull` in `~/answerable` updates what every local Claude reads.

## The one rule

Skills change in the repo, nowhere else. Editing through the symlink at
`~/.claude/skills` is editing the repo, which is correct. Editing a copy
somewhere else is not.

## Drive paths this repo refers to

| Symlink | Account | Holds |
|---|---|---|
| `~/School` | katherine.vonduyke@redclay.k12.de.us | Live course folders |
| `~/AT` | kvd@answerableteaching.com | Biology cycle folders, `.pptx` archive |
| `~/UDel` | kvond@udel.edu | Doctoral work |

`~/AT` is on an account with limited time remaining. Its contents need
migrating.

## Audit the skills

```
python3 tools/skills_audit.py --path skills
```

## Open items

- `vt-skill/SKILL.md` is 72KB. Split decision rules from run-time detail
  into `reference/`.
- `vt-forensics-skill` and `vt-anatomy-skill` are referenced but do not exist.
- Live Slides decks are newer than the archived `.pptx` files. Export needed
  before any deck job runs.
- Cycles 01 and 02 have no `.pptx` source at all.

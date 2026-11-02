# Pass protocol

Read `../SKILL.md` first; its mandatory boundaries still govern. Path bases do not change when detail moves here: own `scripts/` and `reference/` paths are relative to the original skill root; named sibling-skill paths such as `book-revision/scripts/` are relative to the shared `skills/` directory. Manuscript `revision/` and `book-compile/` paths belong to the designated private manuscript repository; data and derived artifacts belong only in authorized private staging. Never interpret them as paths inside this reference directory or publish private artifacts to the public skills repository. These extracted instructions preserve existing rules; they grant no new authority.

## The packet

A packet is one markdown file per chapter per lane: `revision/packets/<lane>/<chapter-id>.md`, where the chapter id is the number or letter as the snapshot names it (`preface`, `intro`, `ch01`, `ch06a`, `ch11`); the practice chapter, which is not in the snapshot, is `before-inquiry`, and its text is the Aug file named in the table above; the AI chapter in its assembled form (P19), also not in the snapshot, is `doable-not-the-doer`, with the Doc's [6A], [6B], and the principles table read beside it for what the assembly absorbed and what it did not. It opens with a five-line header and then one table.

```
Lane: terms
Chapter: ch02 (Chapter 2 — What Is Agency? Why Do We Want It?)
Snapshot: revision/manuscript/working-copy-2026-09-12.md
Assumes: P4, P5, P7
Checker run: revision/reports/check-2026-09-12.md
```

| ID | Find | Class | What | Proposed | Why |
|---|---|---|---|---|---|
| terms-ch02-01 | `Decision-making and capability drop out of this definition` | bracket | agency is defined five times and the components disagree | [text of the bracket] | glossary: agency; canonical home |

The columns mean this. **ID** is lane, chapter, running number. **Find** is a string the integrator pastes into Ctrl+F, long enough to match once, copied exactly from the snapshot (curly quotes and all). **Class** is one of `fix-direct` (mechanical), `relocate` (her unaltered words move; say where), `delete-duplicate` (one of two copies goes; say which home keeps it), `rename` (a ruled rename), `bracket` (a suggestion or challenge she decides), `decision` (needs a ruling; name the P-item or propose a new one), `open-item` (something only she can supply). **What** states the observation in one or two sentences. **Proposed** carries the exact replacement text for a fix, the exact bracket text for a bracket, or the outline for scaffolding; it is empty for a pure observation. **Why** names the governing thing: a proposition number, a glossary term, a claim type, a ruling, a voice-guide marker, a findings item.

Run `python3 scripts/manuscript_check.py --in <snapshot> --packets revision/packets/` before handing a packet in; every Find string must match exactly once.

## Running a pass

1. Snapshot. Export the single live Google Doc to markdown into `revision/manuscript/working-copy-<date>.md`; commit it as backup/version history. Run the checker into `revision/reports/check-<date>.md`; commit.
2. Read the ledger. If a P-item you depend on has been ruled since the last pass, the ruling wins.
3. Launch the six lanes, one agent each, on all chapters or on a chapter range. In Claude Code: `claude "Load the book-revision skill, then the book-lane-arc skill, and run it on chapters 1 through 5 of the current snapshot."` (one line per lane; the lane names are in the table above). In Cowork: start a session with the same sentence.
4. When the lanes have committed their packets, run the integrator on each chapter. It produces `revision/integrated/<chapter-id>.md` (the chapter text with direct fixes applied and brackets in place) and `revision/integrated/<chapter-id>-changes.md` (every applied change, every bracket, every open item).
5. Rerun the checker on the integrated text and compare with the first report: dash density down, residue at zero, no pointer to a chapter that does not exist, duplicates only where the ledger says the return is deliberate.
6. When Katherine authorizes write-back, follow the current [Manuscript delivery rule](https://github.com/kvond/Answerable-Teaching/blob/main/revision/MANUSCRIPT-DELIVERY-RULE.md): commit the authorized revision to the designated private manuscript repository, retrieve and verify that exact commit, then update and verify the same live Google Doc. Do not create or update a second live Google Doc. Keep the one current manuscript backup required by that rule; dated lane-input snapshots remain a separate input to this pipeline. A prepared revision or commit is not a verified Doc update.

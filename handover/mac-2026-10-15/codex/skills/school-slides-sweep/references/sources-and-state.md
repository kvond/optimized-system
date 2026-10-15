# Sources and persisted state

Workspace: `/Users/katherinevonduyke/Documents/Codex/2026-09-09/referenced-chatgpt-conversation-this-is-an`

| Role | Verified ID |
| --- | --- |
| Manual, Answerable_Teaching_Manual | `1kUWjxAnxK1qrTNlmI72ugYYOj85EGRA2gc5M0bwhYZA` |
| Agenda 26-27 CLEAN | `1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY` |
| Running list, Deck queue | `1G45VX3CixZdlG7EfzDVD5sxSoe7_cHyAWumdIzmUK00` |
| Biology Public | `1GvlqU7JGJaYOOQlus38Fa7JgiSu-C6Hq` |
| School Forensics Weekly | `1Swy106QK-YL5Yq2jsgwwKgVkdoJnkZfa` |
| Forensics Unit 1 | `11r-SWHJCRwlES4-I-kw3YLzLfc5-oOa3` |
| Forensics Unit 2 | `1RDtGarOuS_8ptg-4vC6llmkzwD18qsLT` |
| Forensics Unit 3 | `13lq5md5eKF_CX7oXoelEMJUItQk8O7im` |
| School Week 03 folder | `1mX-vejMxdurgAHazIcPS-VqgUJADNIf2` |
| Week 03 deck found there, not yet confirmed as user's edited target | `1R2juNZ4T13m30FW64LLyHWXHkJ-jN1nKIj8cI-O-UbI` |
| Unit 3 curriculum guide PDF | `1nQG0JIZnl5-yJ-RKzJAIYN5TbLQwPpa0` |

IDs establish identity, not current access. Check them live. September 10 Drive connector identified `kvond12@gmail.com`; school Chrome identified `katherine.vonduyke@redclay.k12.de.us`. Home Mac can run the school Chrome profile. Shared-file access is distinct from which Google account owns new copies. Resolve school upload ownership before creating files.

State directories relative to the workspace:

- `work/sweep/`: raw snapshots and generated change baselines. `latest-decks.json` stores successful observations keyed by immutable Drive ID. Merge partial runs; never replace it with only the current batch. Keep unresolved changes in `pending.json` until reviewed, even after a content baseline advances.
- `work/sweep/release-checks/`: dated final-check records tied to the exact deck and manual rule versions. Preserve historical results. Missing records or stale rule/deck matches mean no current release verification, not a failed student grade.
- `outputs/native-slides-workflow/manual-current/`: complete current extracted rules plus manifest. `manual-history/` keeps old versions. `manual-skill-3.txt` and `manual-enhancement-rules.txt` are legacy cache paths, not authorities.
- `outputs/native-slides-workflow/Sweep-*.md`: user-facing reports and instructions.
- `work/native-slides/review-checkpoints.json` and `additional-decks.json`: historical inventory seeds, not proof of current completion. Follow their source IDs and the live queue to expand inventory.

The existing Apps Script controller is not a verified deployed worker. Do not trigger it during a sweep. Its Sonnet dependency and existing-ID compatibility issue must be resolved and separately tested before use. Local skill creation does not activate the cloud controller.

## Helper usage

Use the bundled Node executable from `load_workspace_dependencies`. Commands below run locally from the task workspace; use absolute skill paths in scheduled work.

```text
node <skill>/scripts/sweep-state.mjs manual work/sweep/manual-live-DATE.json outputs/native-slides-workflow --commit
node <skill>/scripts/sweep-state.mjs deck work/sweep/deck-ID-DATE.json
node <skill>/scripts/sweep-state.mjs compare work/sweep/previous-deck.json work/sweep/current-deck.json
node --test <skill>/scripts/sweep-state.test.mjs
```

`manual` defaults to preview. `--commit` only refreshes generated local manual caches and dated history. It does not alter the Google Doc or any slide. Read the full current source before using its new instructions. A content fingerprint records text identity, not a publisher's version date or approval.

`deck` emits a snapshot to stdout; persist it using the file editing tool. `compare` accepts snapshot objects, reports slide additions/removals/changes/reordering and theme changes, and never mutates a deck. Exclude known Biology 02 at dispatch as well as by course/week metadata, before reading source contents. Hashes ignore ephemeral content URLs; changed image contents behind unchanged URLs need revision/metadata or visual review. No hashing tool can validate teaching quality or grading semantics.

Current schedule: first weekday of each month at 7 AM America/New_York, starting October 1, 2026. At the user's direction, the old 7 AM and 2 PM weekday reminders were removed. The existing automation ID `google-enhance-and-embed-codes` now has the name `Monthly school slides sweep` and a monthly-only schedule; its old ID is retained for continuity, not reminder behavior. `work/sweep/monthly-state.json` records first due month, last completed month and resumable progress. Resume incomplete work at the next manual invocation or scheduled monthly run; do not recreate weekday reminders or duplicate an already-completed month. Search existing automations and update in place, not a workaround cron.

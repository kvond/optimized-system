# MacBook Air handover, 15 October 2026

What lived only on the MacBook Air before it was erased, kept as text and code. Use it to rebuild the setup on the next machine or to move the jobs to the cloud.

| Folder | What it is | Came from |
|---|---|---|
| `codex/automations/` | The five Codex automations (prompt + schedule). Four were active and ran on this Mac | `~/.codex/automations` |
| `codex/AGENTS.md`, `codex/config.toml`, `codex/skills/` | Codex's standing instructions, its config, and the two skills that were not links | `~/.codex` |
| `codex/skills-links.txt` | Skills that were links into a repo, and where they pointed | `~/.codex/skills` |
| `claude-code/scheduled-tasks/` | The Claude Code scheduled task (weekly lesson preflight) | `~/.claude/scheduled-tasks` |
| `claude-code/settings.json` | Claude Code user settings | `~/.claude/settings.json` |
| `cowork-scheduled/` | The nine Cowork scheduled task prompts (book distill, book-ops, Spanish, second brain) | `~/Documents/Claude/Scheduled` |
| `documents-claude/` | Loose scripts, the HOME and Artifacts folders, the hub companion and private recovery code, the voice project, and the two School Hub plans | `~/Documents/Claude`, `~/Documents` |

Only text and code were copied (md, py, js, mjs, ts, gs, html, css, sh, toml, yml, txt). Spreadsheets, CSVs, zips, PDFs and Word files were left out.

Deliberately not here, under `ai-ops/privacy-rules/storage.md`:
- Claude and Codex memory files (`~/.claude/projects/*/memory`, `~/.codex/memories`). They are memory dumps and one names a student. They belong in the encrypted storage, not git.
- Student rosters, the 2026-27 agenda spreadsheet and the Tiller finance workbook. Those moved to Google Drive.
- Run folders' work copies. Every clone's branches and uncommitted edits went to the private repo `kvond/mac-rescue-2026-10-15`.

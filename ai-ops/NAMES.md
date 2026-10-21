# Canonical names

One name per thing. Agents write the canonical name; aliases are read, never written.
A new tool gets a row here before it is built. Decisions about names are recorded in Slack #decisions (answerableteaching.slack.com).

## Systems
| Canonical | What it is | Read as, never write |
|---|---|---|
| Teaching Hub | Cloud Run app that reads Turn-in Forms and scores Notes and Revision | schoolwork hub, the dashboard. `school-workflow-hub` is only its repo and service name |
| Teaching Hub operations | Daily roster, filing and completion preparation; `prompts/school-hub-operations.md` | |
| Spreadsheet feedback | Source-backed feedback/writing reports and independent printable packets; `prompts/school-spreadsheet-feedback.md` | |
| Feedback Pipeline | Workflows A, B, B1, B2 | grading scripts, feedback system |
| Workflow A | Extracts student answers from Slides answer boxes | the parser, the extractor |
| Workflow B1 | Personalized rewrite feedback docs and emails | feedback emails |
| Weekly Lesson Preflight | Audits next week's readiness across Drive, Master Agenda, Schoology | lesson audits, Lesson-Audits |
| System Review | Weekly scheduled review of the whole system | review routine |
| VT | Variation Theory | Visible Thinking (wrong) |
| VT deck / cycle deck | Lesson deck built to VT structure | lesson slides |
| vt-skill | Deck-finishing skill, `skills/vt-skill/` (renamed 2026-10-19) | vt-bio-skill, VT_Bio_skill |
| vt-deck-completion | School Claude skill that finishes a partly updated VT deck (enhance, textboxes, codes), `skills/vt-deck-completion/` (added 2026-10-20) | deck repair |
| student-feedback | Feedback prompt (Prompt 2), rating scale, class report formats and renderer, `skills/student-feedback/` (added 2026-10-21). The Agenda `Feedback Prompts` tab is Katherine's quick reference | feedback skill, feedback prompts |
| vt-teaching-notes | Writes the per-lesson `VT Questions Teaching Notes` Google Doc, `skills/vt-teaching-notes/` (added 2026-10-20) | teacher notes doc |
| Answerable Teaching | Katherine's method; the Answerable Teaching Manual | AT |
| IC | Infinite Campus gradebook | eSchool, TAC |
| I-Tracker | I-Tracker Pro family contact notes | parent log |

## Files and folders (canonical = current Drive title, bound to ID)
| Canonical | ID | Notes |
|---|---|---|
| Master Agenda = `Agenda 26-27 CLEAN` | `1m4qhXb5M7y0nMNJHeuxu2J4eFXokIKYxiGVyOfpg-uY` | School account. Workflow contracts read this. |
| superseded: `Master_Agenda__2026-27_v9 — LIVE (app reads this)` | `1i6D-QT5nQWdVpltW14XB7OZ9lWFrMbMO8ZnZQvpUw-w` | kvd@answerableteaching.com, last edited 2026-09-03. Read only to trace old links; `skills/vt-skill/SKILL.md` repointed to Master Agenda 2026-10-19. |
| `📤 TurnIt in Folders` | `1KvWrI5EbYG_pzWxv3lQLzQ2tVkMFWaBq` | Submissions by course: 🌿 Biology, 🫀 A&P, 🔬 Forensics, 📥 UNSORTED submissions. Formerly noted as "00 ALL TURN IN" / "00 REAL ALL TURN IN". |
| `📤 Turn it in_Google Forms` | `1XempHqoETg-Pv0O0-7vACtABa7wIzABN` | Holds `Assignment Google Forms` (`176_HMDjg7fqacEal6giPsjuHqaVPs8vB`): preserve each actual lesson/assignment's exact Form and source binding, even when lessons share a week or folder. |
| Answerable Teaching Manual | `1kUWjxAnxK1qrTNlmI72ugYYOj85EGRA2gc5M0bwhYZA` | Feedback formats, §12 and Appendices B and F. |

## Repositories
| Canonical | Formerly |
|---|---|
| `kvond/optimized-system` | `kvond/answerable-skills` |
| `kvond/lesson-preflight` | `kvond/Lesson-Audits` (renamed 2026-10-15); retirement candidate, not the implementation home. See the conditional retirement gate in `ai-ops/worker-registry/roles-and-schedules.md`. |
| `kvond/school-workflow-hub` | Teaching Hub code, including Weekly Lesson Preflight / Week ahead. |

## Accounts
| Account | Use |
|---|---|
| katherine.vonduyke@redclay.k12.de.us | School. Pipeline outputs, Forms, course folders. The IC helper runs in this account's Chrome profile on Katherine's home Mac; it is unavailable on her school computer. District Claude browser limits are separate from home Mac capabilities. See `ai-ops/worker-registry/roles-and-schedules.md`. |
| kvond12@gmail.com | Composio Drive/Gmail; all Gmail drafts; canonical scripts. |
| kvd@answerableteaching.com | Answerable product; A&P "ANATOMY" resources. |
| answerableteaching.slack.com | Decisions and discussion. No student names, grades or feedback text. |

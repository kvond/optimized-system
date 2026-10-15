# Prompt packet: deep audit of the UD Claude account

**Why this file exists.** Katherine asked for this audit from her kvond12 Claude
session on 11 October 2026. It could not run there. An account can only inspect
itself, and the browser extension pairing that would have let one account read
the other's session is itself per account, so the UD profile's extension is
invisible from kvond12 rather than merely disconnected.

**How to use it.** Open the UD Claude, the account signed in inside the Chrome
profile named PROFESSIONAL. Paste everything below the line into a new
conversation there. If instead you sign the Claude desktop app into the UD
account and paste it there, that session has Desktop Commander and can write its
own result into this folder, which saves you copying anything back.

**What was changed from the original request.** Three steps were removed because
that session cannot perform them, and one block was added because that session
cannot see the facts it needs. Everything else is as Katherine wrote it.

---

You are auditing THIS Claude account: the higher-ed account associated with
kvond@udel.edu. You are inside it, so inspect yourself. Do not attempt to inspect
the kvond12 account; you cannot reach it, and the facts you need about it are
supplied below.

## Boundaries

Do not delete anything, sign out, change subscriptions or passwords, move files,
alter projects, change grading settings, change extensions, modify automations,
or publish anything. Do not expose credentials, tokens, cookies or API keys. If
something cannot be confirmed, mark it UNVERIFIED rather than guessing.

Do not expose sensitive student content. Summarise only to the level needed to
identify a dependency.

## Context

This account is intended to remain. One role is already known: it must support
higher-ed grading, because a grading extension is used there.

The long-term goal is a simpler system. School accounts handle school work, UD
accounts handle higher-ed and scholarly work, personal accounts handle home life,
and durable prompts, skills and workflows live outside individual chat history
wherever possible.

## What has already been established, 11 October 2026

Read this before you start. It is the result of a full audit of the machine and
of the kvond12 account, and it is the comparison material you need.

**This UD account, seen from outside.** It is signed in inside the Chrome profile
named PROFESSIONAL, whose Google account is kvond@udel.edu. Its claude.ai greeting
reads "Katherine Duyke", without the "von", which is how it was distinguished from
kvond12, whose greeting reads "Katherine von Duyke". It runs Opus 5.5. It is
almost certainly organisation d260f204-a04f-4988-9d93-560e0ffe5a7e, which was
used heavily from 11 to 24 September 2026, reaching the ceiling of its five hour
window, and has been quiet since. Confirm your own organisation ID and say whether
it matches.

**The PROFESSIONAL profile holds exactly four extensions:** Claude, ChatGPT,
Grammarly and Google Docs Offline. Nothing is named for grading. So the grading
extension is almost certainly the Claude extension itself. Confirm or correct this,
because it decides whether the grading setup can be moved independently of the
account.

**The kvond12 account holds**, and you should not duplicate any of it:

| What | Amount | Note |
|---|---|---|
| Claude Pro subscription | one | the paid plan sits there, not here |
| Projects | 9 | website, TPT, book, scholarly writing, WilmU 7106, AI HS, master agenda, finances, critical aspect activities |
| Project documents | 110 | none of them in version control |
| Uploaded account skills | 7 | vt-deck-authoring, vt-fusion-retrofit, vt-bio-skill, ste, book-ops, chapter-bank, manuscript-ops |
| Published artifacts | 5 | hub audit, turn-in runbook, engine start-up, concept bank terms, file map |
| Memory store | 30 files | profile, preferences, and subject files |
| Claude Code | authenticated here | admin of its own organisation |

**Of those nine kvond12 projects, two are higher-ed and may belong here:**
"WilmU: 7106" holds seven documents covering the Chapter I advisor guide, the
student what-goes-where, the course canon, the recap map, the DIP first assignment
template and the DIP advising field map. "Scholarly Writing" holds one, a final
paper rubric. The WilmU set is the only copy of her DIP advising material.

**There are five Claude organisations on the machine.** Two are kvond12's. One is
this account. One, 1fc883da-00b0-488f-9f2a-a1b0787f807c, is unidentified, was at
98 percent of its weekly window on 30 September, and is the only organisation with
its browser extension allowlist enabled. One, cdb42cb9-a0bf-4b2b-8d22-20cb001635c1,
is dormant since 22 August. If you recognise either, say so; it is the open
question blocking every retirement decision.

**The durable repository is kvond/answerable-skills**, cloned at
~/code/answerable-skills, holding 27 skills and an audits folder. It is the
destination for anything that should outlive a chat. Note that hep-scout, which
governs all book manuscript critique, lives only in that repository and is not
one of the seven skills uploaded to kvond12.

## Audit yourself

**1. Account and plan.** Account identity, plan level, model access, usage limits
if visible, Claude Code access if any, Projects, Artifacts, extensions and
connectors, desktop access, and any account setting that affects work.

**2. Project inventory.** Every project in this account. For each: name, purpose,
approximate last use, key documents, project instructions, important chats, whether
it is active, dormant, redundant or important, and whether it holds anything that
exists nowhere else. Pay particular attention to Wilmington University, EdD and
doctoral work, grading, research methods, course design, Answerable Teaching and
the book, academic research, article drafting and literature review.

**3. Document inventory.** Important uploaded and project files. Flag grading
documents, rubrics, grading instructions, feedback frameworks, research notes,
manuscripts, book sections, literature reviews, reusable templates, prompt
documents, and anything that exists only inside Claude.

**4. Grading workflow.** Map how grading actually works: which extension, which
browser profile, whether it depends on this specific account, the prompts and
rubrics used, the recurring steps, where student papers enter, where feedback is
generated, where grades are posted, every manual handoff, the failure points, and
any important prompt that lives only in a chat. Then separate the work into four
kinds: what genuinely requires Katherine's judgment, what is repetitive and
Claude can do, what the extension performs, and what another tool or account
should own.

**5. Chat use patterns.** Do not summarise every conversation. Identify clusters:
grading, higher-ed teaching, doctoral education, research, book work, writing,
administration, personal work that does not belong here, school work that does not
belong here. For each, estimate frequency and importance, say whether it should
remain, and say whether durable content should be extracted.

**6. Durable prompts and workflows.** Find reusable prompts and instruction sets
embedded in chats and projects. For each: purpose, where it lives, whether it is
current or obsolete, whether it should become a durable contract, and its
destination among ~/code/answerable-skills, GitHub, Google Drive, Roam, Todoist,
or staying here.

**7. Book and research role.** Assess whether this account is a good permanent home
for Answerable Teaching synthesis, literature critique, manuscript review, chapter
integration, academic argument testing, Substack and article drafting, research
notes, and annotated literature reviews. Do not assume all of them belong here.
Recommend only those that fit this account's existing state. Compare against
ChatGPT for personal and system oversight, Codex and Desktop Commander for
technical and system work, Perplexity for literature discovery, and Roam as the
canonical research repository.

**8. Misplaced work.** Anything here that should not stay: personal finance,
family planning, household tasks, Red Clay school operations, generic technical
maintenance, duplicate book work better owned elsewhere. For each, say where it
should go and what must be extracted first.

**9. Unique value.** What this account does especially well because of accumulated
context, projects, grading setup, files, extensions, prompts or familiarity.
Distinguish genuine advantage from inertia.

**10. Permanent role.** Give this account one primary domain, one primary role, and
at most three secondary roles. Specify work explicitly prohibited here, execution
jobs, maintenance jobs, browser profile, extension dependencies, and what should be
open by default. Make it memorable enough to recall without a chart.

**11. Compare with kvond12.** Using only the facts supplied above, say what should
stay in UD, what should migrate from kvond12 into UD, what should instead go to a
repository rather than into another Claude account, and what should be abandoned.
The goal is not to move everything across. It is to keep only what belongs in this
domain.

**12. Migration targets.** Four lists: keep in UD Claude; migrate into UD Claude;
move out to a durable repository; retire and do not migrate.

**13. Risks.** What breaks if kvond12 is retired, if browser profiles are cleaned
up, if the grading extension is moved, if prompts are shortened, if projects are
deleted, or if the Claude Code identity changes.

## Output

Produce these sections in order: account summary; project inventory; grading
workflow; chat use patterns; durable prompts and workflows; book and research
role; misplaced work; proposed permanent role; migration map; risks; next ten
actions; unresolved questions.

Name the file ud-claude-deep-audit-2026-10-11.md. If you have Desktop Commander or
another route to the filesystem, write it into ~/code/answerable-skills/audits/
and say so. If you do not, output it as one markdown block for Katherine to save
there herself, and say that you could not write it.

Katherine's standing preferences apply. Prose reads as directions to a person, not
to a computer. Machine strings such as file IDs belong inside the table or box they
serve, never loose in a sentence. Ask one menu question at a time, with a
recommendation, rather than handing back a paragraph of decisions. Do not put
parentheses in any file or folder name you create. Challenge her thinking in
square brackets where the evidence disagrees with the plan.

## Success condition

At the end she should know exactly what lives in this account, why she needs it,
what its permanent job is, what should migrate into it, what should move out of
it, what would break if she simplified too aggressively, and how this account fits
into the rest of the system.

# AI account audit, 11 October 2026

Method: direct inspection of the Mac and of the live browser sessions, through
Desktop Commander and Chrome control. No accounts were changed, no files were
deleted, no scheduled job was altered, and no password, token or cookie is
reproduced here. Anything I could not confirm by inspection is marked
UNVERIFIED instead of guessed.

Two definitions used throughout, because they carry most of the argument:

**Execution owner.** The account that actually performs a recurring job on a
schedule or on demand. It is identified by where the job is configured, not by
where it would make sense to put it.

**Maintenance owner.** The account responsible for improving the prompt, skill
or contract that governs that job over time. It is identified by where the
authoritative text lives and gets edited.

---

## 1. Current account map

| Platform | Account | Browser / profile | Desktop app | Plan and capabilities | Current job | Important state | Keep / migrate / retire | Confidence |
|---|---|---|---|---|---|---|---|---|
| Claude | kvond12@gmail.com | Chrome Profile 4, named "Katherine" | Yes, primary sign-in of Claude Desktop; also Claude Code CLI | Claude Pro, chat capability. Second membership is an individual API org, prepaid, no chat | System of record. Book work, school system design, repo and file work, audits | 9 projects, 110 project documents, 7 account skills, 5 published artifacts, the memory store, Claude Code project history | **Keep**, see section 2 item 1 | High |
| Claude | at least two further accounts, **confirmed to exist** | not signed into any Chrome profile | Yes, in the Claude desktop app only | UNVERIFIED, but each carried real load. See the addendum | One used heavily 11 to 24 September, one used 24 to 30 September | Their own chat history and any projects under them | Identify, then migrate into or out of them | Medium |
| Claude | a UD account at kvond@udel.edu | **not** in Chrome. Both connected Chrome instances resolve to kvond12 | In the desktop app only | UNVERIFIED | Higher-ed grading, and whatever ran 11 to 30 September | Confirmed to exist by usage records, not yet by name. See the addendum | **Keep**, and make it the higher-ed Claude | Medium |
| ChatGPT and Codex | kvond@udel.edu | not in a Chrome profile | Yes, the Codex desktop app | **ChatGPT Plus.** Model gpt-6-sol, reasoning effort low, service tier priority. Token last refreshed 9 October | **The school morning routine.** Both weekday automations run here | Two ACTIVE automations whose prompts hold roughly eight thousand words of school policy that exists nowhere else | **Keep** as school execution owner | High |
| ChatGPT | kvond12@gmail.com | Chrome Profile 4 | No | **Free.** Upgrade prompts shown, Work tab locked | Personal chats. Substitute pay, sheet music, guitar chords, travel, one DNA replication thread | None found. See the correction in the third addendum | **Retire** or keep strictly personal | High |
| Perplexity | kvond12@gmail.com | Chrome, open session | No | Pro, subscription active | Book and manual critique | A project named "Book Answerable Teaching" and sessions asking whether the book is worth publishing and whether the manual suits busy teachers | **Migrate then retire**, see section 2 item 2 | High |
| Desktop Commander | reaches the Mac as an installed plugin | n/a | Yes | Full shell and filesystem on the Mac | Files, repositories, audits, batch work, repairs | Nothing of its own. It is a capability, not a store | **Keep** | High |
| Canva | none found | n/a | n/a | n/a | n/a | n/a | UNVERIFIED, no session or app present | Low |
| Google | kvd@answerableteaching.com | Drive symlink in your home folder | n/a | Workspace | Holds the Biology cycle folders and the slide archive | Your own repository README says this account has limited time remaining and its contents need migrating | **Migrate**, deadline unknown | Medium |
| Google | katherine.s.vonduyke@wilmu.edu | signed into Chrome Profile 4 | n/a | n/a | No AI session found under it | none found | Leave as a Google sign-in only | Medium |

Supporting AI tools present on the machine, none of them account boundaries:
Grammarly, with an extension in two profiles and three background update agents;
Gemini in Chrome, built into the browser in all three profiles; a ChatGPT search
extension in Profile 4; Glasp; DeepL; Elicit; Wispr Flow, which is also a
connected Claude connector; Notion; Zotero; Dedoose.

### Chrome profile layout as it actually is

| Profile folder | Display name | Primary Google account | Also signed in | AI extensions present |
|---|---|---|---|---|
| Default | PROFESSIONAL | kvond@udel.edu | kvond12 | Claude, ChatGPT, Grammarly |
| Profile 4 | Katherine | kvond12@gmail.com | edtpafb, wilmu, redclay | Claude, ChatGPT, ChatGPT search, Grammarly, Glasp |
| Profile 29 | redclay.k12.de.us | katherine.vonduyke@redclay.k12.de.us | kvond12, udel | Claude, plus the unpacked School Workflow Hub companion |

Chrome has created thirty profiles over its life and three survive. The profile
last used was Profile 29. Every one of the three surviving profiles has more
than one Google account signed into it.

---

## 2. Duplication and confusion

**1. The account you plan to retire is the one holding Claude Pro and the whole
system of record.** kvond12@gmail.com is the Claude Pro subscription, the
primary sign-in of the Claude desktop app, the account Claude Code authenticates
as, and the owner of nine projects, one hundred and ten project documents, seven
account skills, five published artifacts and the memory store. Retiring it does
not shed a temporary account. It removes the centre of the system.

Katherine confirmed on 11 October that a separate UD Claude account exists, and
the usage records corroborate her. See the addendum at the end of this document.
The task is therefore a **migration**, not a retirement: nine projects, one
hundred and ten documents, seven skills, five artifacts, the memory store and the
subscription itself all have to move, and section 4 should be read as the plan
for that move rather than as a cleanup.

**2. Book critique runs in two paid accounts.** Your stated convention is that
hep-scout governs all book manuscript critique, even a bare "what do you think?".
The Perplexity Pro account holds a project named "Book Answerable Teaching" and
sessions asking exactly the questions hep-scout is for. Two accounts, two
histories, one job, and only one of them applies your rubric.

**3. Three Google accounts sit inside every Chrome profile.** The school profile
is primary as Red Clay but also carries kvond12 and the UD account. Profile 4
carries four accounts. A Drive write, a Forms read or a document creation can
land under the wrong identity and will not announce that it did. This is the
single largest source of wrong-account work, and it is a browser configuration
problem, not an AI problem.

**4. School work has two owners who can disagree, and currently do.** The Codex
automations under the UD ChatGPT account drive the Hub and the browser companion
each weekday. Claude Code and Desktop Commander own the Hub source and the
repositories. Both touch the same Hub and the same Drive. Right now the local Hub
working tree is twenty nine commits behind the remote while also holding one
unpushed commit and three uncommitted files, which is what divided ownership
looks like on disk.

**5. Skills live in four places.** The repository holds twenty seven and is
authoritative. The Claude account holds seven of those twenty seven as uploaded
account skills. The Codex home holds two more, school-lesson-audit and
school-slides-sweep, which overlap the repository's deck skills and are not
versioned with them. Retired copies remain on disk at ~/answerable and
~/skills_recon. Notably hep-scout, which you treat as mandatory, is in the
repository only and is not one of the seven uploaded to the Claude account.

**6. Two copies of the school browser companion are installed in the school
profile.** One is enabled, one is disabled. Both load from dated session output
folders. See section 8 for why this matters more than it looks.

**7. ~/Documents/Claude is both scratch space and production.** It holds well over
a hundred copies of the hub helper from working sessions, and it also holds the
folder the live extension loads from. Tidying it as scratch would break school
grade entry.

---

## 3. Proposed simple end state

Four identities. Each has one primary job stated in a single sentence, so you can
recall it without this document.

### Claude Pro, kvond12@gmail.com
Think of it as: **the account that owns the rules.**

- Primary domain: the durable system. Prompts, skills, specifications, contracts, audits.
- Primary job: **maintenance owner** for every recurring workflow in this inventory, including the ones another account executes.
- Secondary jobs, closely related: book and manuscript critique under hep-scout; repository, file and batch work through Claude Code and Desktop Commander; higher-ed and DIP advising material.
- Prohibited here: the weekday school morning runs; entering student scores; repetitive browser chores.
- Execution owner for: repository, file, system and audit work.
- Browser and profile: Chrome Profile 4 for the web app, and the Claude desktop app.
- Desktop app: yes, primary.
- Connectors that belong here: Google Drive, Gmail, Google Calendar, Composio, Netlify, Wispr Flow, and the Roam server declared in the desktop configuration.

### ChatGPT Plus, kvond@udel.edu
Think of it as: **the account that runs the mornings.**

- Primary domain: recurring school execution.
- Primary job: **execution owner** for the 6:30 roster and filing run and the 7:30 feedback and print run, weekdays.
- Secondary jobs: on-demand school slide sweeps and lesson audits, through the two Codex skills already installed there.
- Prohibited here: book critique; higher-ed grading; authoring any rule that needs to survive the run. Rules come from the repository.
- Maintenance owner for its prompts: the Claude Pro account, once those prompts are extracted into the repository. Today the prompts maintain themselves inside the automation, which is the problem.
- Browser and profile: it drives Chrome Profile 29 through Desktop Commander.
- Desktop app: yes, the Codex app.
- Connectors that belong here: Google Drive linked to all three of your Google accounts, Gmail, GitHub as kvond, Todoist.

[Challenge: your direction expected UD ChatGPT to take some other durable role and
expected school execution to sit with "school Claude and browser tools". The
machine disagrees. UD ChatGPT already is school execution, and it is the only
paid ChatGPT you have. Moving that work to Claude would mean rewriting roughly
eight thousand words of embedded school policy into skills first. That is worth
doing eventually because the policy belongs in the repository either way, but it
is a project, not a cleanup step.]

### Red Clay Google, Chrome Profile 29
Think of it as: **the school container, not an AI account.**

- Primary job: hold the school sign-ins that Infinite Campus and the Hub companion require.
- Prohibited here: being signed into kvond12 or the UD Google account. Remove both.

### UD Google, Chrome Default, named PROFESSIONAL
Think of it as: **the higher-ed container.**

- Primary job: hold the higher-ed sign-ins and the Claude extension used for grading.
- Prohibited here: school work.
- Confirm first which Claude account that extension acts as. See section 9.

### Retired in this design

ChatGPT Free on kvond12, which holds nothing the Plus account needs. Perplexity
Pro, once the book critique threads are extracted. The
com.kvond.answerable-publish background job, which has never run successfully
since its script went missing. The ~/answerable clone, after its two unpushed
commits are pushed. The kvd@answerableteaching.com Drive, after migration.

---

## 4. kvond12 Claude retirement plan

Katherine confirmed the UD Claude account exists, so this section is now a real
migration plan rather than a hypothetical. Every step is worth doing on its own
merits regardless, because all of it moves knowledge out of a single account and
into versioned storage that any account can read.

### Must be extracted before anything else

**The one hundred and ten project documents.** None of them are in git. By project:

| Project | Documents | What is in them |
|---|---|---|
| Answerable teaching website | 42 | Site source, product data, build scripts, the interactive model pages for photosynthesis, respiration, population and speciation |
| TPT Answerable Teaching | 28 | Reconciled Biology plan, year grid, deck parity and baseline audits, a world-editable-folders alert, supply lists, teacher manual, dated session notes |
| AI HS: Feedbacking and Lesson maker | 21 | Roster score sheet specification, dashboard redesign, concept bank rollout, the Bio v3 system, the deck repoint map, a manifest |
| Answerable Teaching Book | 7 | Current preface draft, writing setup conventions, outline weave, arc decision, newsletter and site operations, Substack intro draft |
| WilmU: 7106 | 7 | Chapter I advisor guide, student what-goes-where, course canon, recap map, DIP first assignment template, DIP advising field map |
| Find Critical Aspect Activities | 3 | Activity discovery, question converter and response sheet builder skills |
| Scholarly Writing | 1 | Final paper rubric |
| Master Agenda for School | 1 | A skill file |
| FINANCES | 0 | nothing |

The WilmU set is the most exposed. It is the only copy of your DIP advising
material and it is the material you said you want to present to candidates and to
build a professorship around.

**The memory store**, which holds your profile, your working preferences and
thirty subject files covering the book, the courses, the Hub, the gradebook
conventions and the Roam system.

**The five published artifacts.** School Workflow Hub Audit, Turn-in Recovery
Runbook, Engine Start-Up, Concept Bank Term Lists, Answerable File Map. The Engine
Start-Up artifact is the thing you asked for at the beginning of work sessions, so
it earns a permanent home.

### Should be migrated rather than extracted

The seven uploaded account skills already exist in the repository, so they need
re-uploading to whichever account survives, not rescuing. The Claude Code project
history across six tracked project folders is reproducible from the repositories
and does not need migrating.

### Should be converted into durable contracts

Three bodies of text currently live only inside a prompt or a conversation and
should become skills or specifications in ~/code/answerable-skills:

1. The two Codex automation prompts, which hold the entire school grading and feedback policy including the dated October 9 and October 10 contract sets.
2. The higher-ed grading procedure, wherever it currently lives.
3. The Perplexity book critique threads, reduced to whatever they add beyond hep-scout, which may be nothing.

### Useful work to spend this account's remaining capacity on

You have most of a Pro month of chat left and essentially all of the coding
capacity. In priority order, the jobs with lasting value:

1. Export all one hundred and ten project documents into the repository, under a per-project folder, and commit.
2. Extract the two automation prompts into skills, and reduce each automation prompt to a short pointer at its skill. This is the single highest-value piece of work available, because it turns eight thousand words of unversioned policy into reviewable text.
3. Push the twenty nine behind, one ahead and three dirty files in the Hub working tree, after you decide which side is authoritative.
4. Push the two unpushed commits in ~/answerable, including the turn-in forms Apps Script.
5. Package the installed school browser companion as a versioned release in the Hub repository, and reinstall the extension from a stable path.
6. Split vt-bio-skill, which your own README flags at 72KB, and create the vt-forensics and vt-anatomy skills the repository references but does not contain.
7. Migrate the kvd@answerableteaching.com Drive contents.
8. Unload the broken nightly publish job and either restore its script or delete the agent.

### Safe to abandon

The FINANCES project, which has no documents. The ChatGPT Free account's personal
projects. The dated agent scratch folders under ~/Documents/Claude, with the sole
and critical exception of the folder the live extension loads from. The retired
skill copies in ~/skills_recon, which your reconciliation notes already confirm
lost nothing.

---

## 5. Migration checklist, safest order

### No risk, documentation only

1. Read this audit and settle the question in section 9.
2. Confirm which Claude account the higher-ed grading extension acts as.
3. Identify the four Claude account identifiers the desktop app has on record.
4. Record the expiry date on kvd@answerableteaching.com.
5. Decide whether the Hub remote or the local working tree is authoritative.

### Low risk, additive migration

6. Export the one hundred and ten project documents into the repository and commit.
7. Export the memory store and the five artifacts into the repository and commit.
8. Push the two unpushed commits in ~/answerable.
9. Push or rebase the Hub working tree once step 5 is settled.
10. Extract the two automation prompts into skills, commit them, and leave the automations untouched for now.
11. Upload hep-scout and any other missing skill to the surviving Claude account.
12. Package the installed browser companion as a tagged release in the Hub repository.

### Requires your approval

13. Reinstall the school browser companion from a stable path, for example a folder under the Hub repository, and remove the two dated-folder installs. This touches the only thing that writes to Infinite Campus, so it wants a weekend and a verification run.
14. Reduce each automation prompt to a pointer at its skill. Changes live weekday behaviour.
15. Remove kvond12 and the UD Google account from Chrome Profile 29, and the school and wilmu accounts from Profile 4. Will sign you out of things.
16. Unload com.kvond.answerable-publish, or restore its missing script.
17. Migrate the kvd@answerableteaching.com Drive contents.
18. Move the Roam token out of the plaintext desktop configuration into an environment variable, as your own connectors reference document already specifies.

### Destructive, last, and not performed here

19. Retire the ChatGPT Free account.
20. Cancel Perplexity Pro, after step 7 of section 4.
21. Delete the dated scratch folders under ~/Documents/Claude, only after step 13 is verified.
22. Retire any Claude account, only after every export above is committed and verified.

---

## 6. Durable workflow inventory

### School morning roster check and submission tidy
- Trigger: weekdays 6:30 local, recurring rule, ACTIVE.
- Inputs: Infinite Campus rosters as canonical; the School Workflow Hub; the live Agenda; registered week folders; Google Forms responses and upload folders.
- Execution owner: ChatGPT Plus, kvond@udel.edu, Codex app, through Desktop Commander and Chrome Profile 29.
- Maintenance owner: today, nobody. The policy lives inside the prompt. Should be the Claude Pro account once extracted.
- Boundaries: no deletion, no sharing changes, no student answer edits, no second Infinite Campus writer, must finish source mutations before 7:00.
- Success: verified checked, filed, unchanged and held counts, with source and destination evidence, and preparation finished before the 7:00 helper.
- Shortest invocation: it fires itself. Manually, open the automation in the Codex app and run it.
- Legacy prompt location: inside the automation definition only.

### School student feedback and print checklist
- Trigger: weekdays 7:30 local, recurring rule, ACTIVE.
- Inputs: each class's latest closed lesson, new revisions without feedback, Agenda Prompt 2, registered lesson and student sources.
- Execution owner: ChatGPT Plus, kvond@udel.edu.
- Maintenance owner: today, nobody. Same problem, larger prompt.
- Boundaries: no scoring, no grade or flag changes, no student messages, no physical printing, teacher-controlled Printed and Handed out marks never inferred.
- Success: individual feedback PDFs filed privately, Biology science writing reports filed separately, the class report updated, the index and the Feedback checklist refreshed, one dated all-class PDF compiled and linked.
- Shortest invocation: it fires itself.
- Legacy prompt location: inside the automation definition only. It also embeds the October 9 and October 10 contract sets, which exist nowhere else.

### Infinite Campus grade entry
- Trigger: 7:00 weekdays, by the browser companion extension.
- Inputs: Hub scores, Infinite Campus section, term, assignment and component bindings.
- Execution owner: the unpacked School Workflow Hub companion extension in Chrome Profile 29.
- Maintenance owner: Claude Code and Desktop Commander, in the Hub repository.
- Boundaries: fill blanks or raise lower scores only, never lower a grade, never clear an uncertain save automatically, read back exact cells.
- Success: verified readback of the written cells.
- Shortest invocation: the extension's own alarm, or its panel in the Hub.
- Legacy location: the Hub repository, plus the installed copy described in section 8.

### Biology and Forensics deck finishing
- Trigger: on demand, per cycle.
- Inputs: Google Slides decks in Drive, the Agenda, the deck skills.
- Execution owner: Claude, through the vt-bio-skill, vt-deck-authoring, vt-fusion-retrofit and vt-post-import skills.
- Maintenance owner: the same account, in ~/code/answerable-skills.
- Boundaries: Drive is the source of truth for decks; the repository ignores binary deck files.
- Success: the deck passes the skill's shipping checks.
- Shortest invocation: name the skill, for example "run cycle 07 through the VT directions".
- Legacy location: repository, authoritative. A second copy of two deck skills sits in ~/.codex/skills and is not versioned with them.

### Monthly school slide sweep and annual lesson audit
- Trigger: on demand or monthly.
- Execution owner: Codex, under the UD ChatGPT account, through its two local skills.
- Maintenance owner: unclear. These two skills are the only ones living in the Codex home rather than the repository.
- Boundaries: a sweep is an audit, not permission to rewrite or publish decks.
- Shortest invocation: name school-slides-sweep or school-lesson-audit in the Codex app.

### Book distill and chapter bank work
- Trigger: on demand, typically end of day.
- Inputs: the Roam graph kvond, #Book captures.
- Execution owner: Claude, through chapter-bank and book-ops.
- Maintenance owner: same, in the repository.
- Boundaries: every page mint passes the create check gate; Roam writes hang mid-session and want a restart rather than a retry.
- Shortest invocation: "book distill".

### Manuscript critique
- Trigger: on demand, including a bare "what do you think?".
- Execution owner: should be Claude under hep-scout. Currently also happening in Perplexity Pro.
- Maintenance owner: the Claude Pro account.
- Note: hep-scout is in the repository but is not one of the seven skills uploaded to the Claude account, so it only applies where the repository is readable.

### Nightly Answerable publish
- Trigger: daily 19:30 and 23:00, background agent loaded.
- Status: **broken.** Exit code 127 on every run. Its script is missing from the folder the agent points at, which now holds only a log full of identical not-found errors.
- Execution owner: nominally the Mac itself.
- Nothing depends on it that I could find.

### Thirteen scheduled run definitions in the kvond/scheduled-runs repository
Named in your own notes as aihs-update, answerable-nightly-distill, author-block,
book-ops-inventory-rebuild, book-ops-monthly-full-sweep, daily-brief-v2,
daily-spanish-lesson, learning-block-agenda, overnight-book-graph-build,
second-brain-distill, sunday-weekly-sweep, tags-pages-sweep and wilmu-update.
No local scheduler reads them. Whether any of them still run anywhere:
UNVERIFIED.

---

## 7. What should move out of chat history

Into **~/code/answerable-skills**, which already has the right shape for all of it:

- The two Codex automation prompts, as skills. Highest value item in this audit.
- The WilmU DIP advising set, seven documents, currently only in a Claude project.
- The AI HS specifications, twenty one documents, including the roster score sheet specification and the deck repoint map.
- The TPT reconciled plan, year grid and dated audits, twenty eight documents.
- The higher-ed grading procedure, once its account is identified.
- The Engine Start-Up artifact, as a reference document rather than a published page.
- The two Codex-home skills, folded in beside their repository siblings.

Into **GitHub**, as repository content rather than working-tree state:

- The Hub working tree's unpushed commit and three modified files.
- The ~/answerable clone's two unpushed commits, including the turn-in forms Apps Script.
- The installed browser companion, as a tagged release.

Into **Google Drive**:

- Nothing new. Drive already holds the decks and the student records and should keep them.

Into **Roam**:

- Nothing new. The book critique findings currently in Perplexity should arrive through the normal chapter-bank route, not as a bulk import.

Into **Todoist**:

- The eight remaining jobs from section 4, so they survive this session.

---

## 8. The finding that needs attention before anything else

The extension that writes grades into Infinite Campus is installed **unpacked**,
and it loads from a dated agent session output folder:

```
id:   kkficpedebnobolfpkpkpfagelofbmde
path: /Users/katherinevonduyke/Documents/Claude/2026-10-07/outputs/hub-helper-0.5.7
hosts: https://school-workflow-hub-611166743877.us-central1.run.app/*
       https://redclayde.infinitecampus.org/*
permissions: storage, alarms
```

The folder is named for version 0.5.7. Its manifest says version 0.5.28, and it
was modified today at 17:41. The name and the contents no longer agree, so the
folder name cannot tell you what is installed. A second unpacked copy at
`/Users/katherinevonduyke/Documents/Claude/2026-10-02/other-x20/outputs/hub-helper-0.5.1`
now contains version 0.5.6 and is disabled, which is the correct state for it.

Three consequences:

1. Any cleanup of ~/Documents/Claude breaks school grade entry, silently, and you would find out on a weekday morning.
2. There is no versioned copy of the build that is actually installed. The repository has the source; the installed artifact is a working folder.
3. The permissions are correctly narrow. Only the Hub and Infinite Campus. That part is well done and worth preserving when you move it.

Separately, the Roam API token is stored in plaintext in the Claude desktop
configuration file. Your own connectors reference document already says that
server should take its token from the environment. It does not. I have not
touched it and have not reproduced it here.

---

## 9. Unresolved questions

Only the ones inspection cannot answer.

1. **What are the two non-kvond12 Claude accounts called?** Their existence is settled. Their email addresses are not stored anywhere on this machine that I can read, so naming them means opening the account switcher in the Claude desktop app, which changes which account the app is signed into. I did not do that without asking. Everything in section 3 about the higher-ed lane depends on the answer.
2. **What is the higher-ed grading extension?** The UD Chrome profile's only AI extensions are Claude, ChatGPT and Grammarly, and nothing named for grading exists in any profile. If the grading work runs through the Claude extension, it currently runs as kvond12, because that is what both connected Chrome instances resolve to.
3. **Does anything still execute the thirteen job definitions in kvond/scheduled-runs?** No local scheduler reads them, and the one macOS job that exists is broken.
4. **Is the Hub remote or the local working tree authoritative?** The local tree is twenty nine commits behind while carrying one unpushed commit and three modified files. Both answers are plausible and they lead to opposite actions.
5. **When does kvd@answerableteaching.com expire?** Your README says time is limited. No date is recorded anywhere I could read.
6. **Is there a Canva account?** No session, no app, no trace.


---

## Addendum, 11 October 2026, after Katherine confirmed a UD Claude account

She reported that a Claude account on kvond@udel.edu exists. I went looking
rather than taking it on trust, and the machine corroborates her.

**What the usage records show.** The Claude desktop app keeps a local record of
plan usage per organisation. It holds three organisations, not one:

| Organisation | Samples | First seen | Last seen | Peak 5 hour window | Peak 7 day |
|---|---|---|---|---|---|
| bf770726-9645-4bdd-a8b3-de9e170dc9a8 | 381 | 11 Sep | 11 Oct, 17:20 | 100% | 90% |
| 1fc883da-00b0-488f-9f2a-a1b0787f807c | 2 | 24 Sep | 30 Sep, 16:58 | 30% | 98% |
| d260f204-a04f-4988-9d93-560e0ffe5a7e | 128 | 11 Sep | 24 Sep, 09:55 | 100% | 42% |

The first is the kvond12 chat organisation. **Neither of the other two belongs to
kvond12**, whose only memberships are that chat organisation and a prepaid
individual API organisation. So at least two further Claude identities have been
used in the desktop app on this computer.

Two details matter. The organisation that stopped on 24 September had been
carrying real load, reaching the ceiling of its five hour window. And the one
sampled only twice sat at 98% of its seven day window when it was seen, meaning it
was being worked hard somewhere the desktop app was not watching. Neither looks
like an idle spare account.

The Claude desktop app also holds four distinct account identifiers, and its
onboarding state pairs organisation 1fc883da with account d01049bf.

**Where the UD Claude is not.** It is not in Chrome. I read the live claude.ai
session in both connected Chrome extension instances, the one Katherine named
SCHOOL and the other one, and both resolve to kvond12@gmail.com on Claude Pro.

**A correction to section 2 item 4.** The Claude extension doing school browser
chores in the Red Clay profile is not a separate school Claude. It acts as
kvond12 Pro, the same account as everything else.

**What this changes.**

The end state in section 3 stands, with one substitution. The higher-ed and book
lane belongs to the UD Claude account, and kvond12 becomes either the account
that is retired or the account that keeps the school and system work. Which way
round depends on where the Pro subscription should live, and that is a billing
decision rather than an architectural one.

The migration in section 4 is now real work with a real deadline, and its order
matters more than before. Export everything to the repository **first**, under
step 6 and step 7 of section 5, because a repository is readable from any Claude
account and a project document is readable from exactly one.

**What I could not finish.** The two organisations have no email address stored
locally. Naming them requires opening the account switcher in the Claude desktop
app, which changes which account the app is signed into and could interrupt a
session. I stopped there rather than do it unasked.

### Second addendum, 11 October 2026, 18:3x — the UD Claude seen directly

Katherine brought the UD Claude window to the front. Read without interacting
with it, Chrome being granted to computer use at read tier only:

- The window is Chrome profile **PROFESSIONAL**, whose Google account is kvond@udel.edu.
- The page is claude.ai, signed in, and greets her as **"Katherine Duyke"**. The kvond12 account greets her as "Katherine von Duyke". The missing "von" is the tell: these are two different Claude accounts, and the UD one carries the display name from her UD Google profile.
- It is running **Opus 5.5**, where this kvond12 session is on Opus 5.
- That profile's claude.ai storage carries organisation **d260f204-a04f-4988-9d93-560e0ffe5a7e**, the one worked hard from 11 to 24 September and then quiet since. Profile 4 has seen that organisation too, so the identification is strong rather than certain.

**Four Claude organisations are now accounted for**, from the desktop app's own
configuration:

| Organisation | Evidence | Reading |
|---|---|---|
| bf770726 | kvond12 chat org, in use today | kvond12 Pro, the current account |
| 6b52845e | kvond12 prepaid API org | not a chat account |
| d260f204 | in the PROFESSIONAL profile; heavy use 11 to 24 Sep | **the UD Claude** |
| 1fc883da | 98% of its weekly window on 30 Sep; the only org with its extension allowlist enabled | a fourth identity, unidentified |
| cdb42cb9 | last touched 22 Aug | dormant, unidentified |

Note the one with the allowlist enabled is **not** kvond12 and **not** the UD
account as identified here. There is a further Claude identity that was being
used hard at the end of September and that has browser extension permissions
granted to it.

**What the desktop app cannot tell us.** It stores organisation identifiers and
never the email addresses behind them. No amount of file reading will name these;
it takes reading the account menu in a signed-in window.

**Correction to carry forward.** Section 3 should read: the UD Claude account,
organisation d260f204, becomes the higher-ed and book lane. kvond12 keeps the
school and system work, or hands it over, depending on where the Pro subscription
should sit. The fourth identity at 1fc883da has to be identified before any
account is retired, because something was running on it eight days before this
audit.

### Third addendum, 11 October 2026, 19:24 — a correction, and where the ChatGPT work really lives

**Correction to section 1.** The first version of this audit attributed four
projects, Health, Book, Wardrobe and Rental, to the kvond12 ChatGPT Free account.
That was wrong. They belong to the **UD ChatGPT Plus account**. The desktop app's
stored sidebar state lists them under account `8deb236d`, and the signed-in
identity in that app resolves to kvond@udel.edu on the plus plan with that same
account ID. The kvond12 ChatGPT holds ordinary personal chats and no projects
that could be found.

This matters in two directions. The Free account is emptier than reported, so
retiring it costs even less. And the Plus account, the one running the school
mornings, is also carrying Health, Wardrobe and Rental, which are home life, and
a Book project that overlaps book work owned elsewhere. That is misplaced work
sitting on the only paid ChatGPT.

**Three wrong surfaces in a row, which is data rather than mishap.** Tonight the
same audit prompt reached, in order, a temporary chat in the kvond12 ChatGPT on
the Free tier, then Perplexity, before arriving at the right app. Perplexity
answered well: it said it could not see the local disk, could not inspect an
account it was not inside, and would not pretend otherwise. The kvond12 ChatGPT
received a terminal transcript and began diagnosing a script.

No surface announced that it was the wrong one, because none of them could know.
This is the cost of the current layout stated in events rather than in principle,
and it is the strongest argument in this audit for reducing the number of places
work can land.

**A method note worth keeping.** The clipboard was used to move a long prompt into
a browser session, which worked, and was then reused for a tool that has a
filesystem, where handing over a path would have been simpler and safer. Prefer
the path when the destination can read files, and the clipboard only when it
cannot.

---

Saved to: `~/code/answerable-skills/audits/ai-account-audit-2026-10-11.md`

# Prompt packet: deep audit of the ChatGPT side

**Which account.** The one that matters is **kvond@udel.edu on ChatGPT Plus**,
the account signed into the Codex desktop app. That is where both weekday school
automations run. The kvond12 ChatGPT is on the Free tier and holds personal
chats; it gets one short section at the end rather than an audit of its own.

**Where to run it.** In the **Codex desktop app**, not chatgpt.com. That session
has a shell, so it can read its own automation definitions, its skills and its
configuration, and can write the result straight into this folder. The browser
can see projects, chats and memories but none of the rest.

**How to use it.** Paste everything below the line into a new task in the Codex
desktop app.

---

You are auditing the ChatGPT and Codex account you are running inside:
kvond@udel.edu on ChatGPT Plus. Audit yourself. Read your own configuration from
disk where you can, rather than reasoning from memory about it.

## Boundaries, and the first one is not routine

**Do not modify, pause, disable, delete or re-prompt either scheduled automation.**
They run Katherine's school mornings on weekdays and their prompts hold school
policy that exists nowhere else. Read them. Change nothing.

Also do not: delete anything, sign out, change the subscription, change
passwords, move or delete files, alter projects, change connectors or plugins, or
publish anything. Do not expose credentials, tokens, cookies or API keys; the
auth file in your own configuration directory contains them, so read identity
claims from it only, never secrets. If something cannot be confirmed, mark it
UNVERIFIED rather than guessing.

## What is already established, 11 October 2026

This came from a direct inspection of the Mac and of the Claude accounts. Treat
it as given, and correct it only if you find hard evidence against it.

**About you.** Signed in as kvond@udel.edu, plan type plus. Model gpt-6-sol,
reasoning effort low, service tier priority. Token last refreshed 9 October.
Memories are on. Roughly sixty project directories are trusted, under
~/Documents/Codex and ~/Documents/Claude.

**Your two automations, both ACTIVE, both weekday heartbeats:**

| ID | Fires | What it does |
|---|---|---|
| morning-roster-check-and-submission-tidy | 06:30 America/New_York, Mon to Fri | Rosters, source matching and filing, before the 07:00 grade helper |
| morning-student-feedback-and-print-checklist | 07:30 America/New_York, Mon to Fri | Individual feedback PDFs, Biology science-writing reports, the class report, the index, the checklist, the dated all-class PDF |

Together their prompts run to roughly eight thousand words and embed the whole
school grading and feedback policy, including dated contract sets from 9 and 10
October. None of that text exists anywhere else.

**Your projects.** You hold four: Health, Book, Wardrobe and Rental. Three of
them are home life and one overlaps book work owned elsewhere, so section 7 should
look hard at them. They were briefly mis-attributed to the kvond12 account; they
are yours.

**Your plugins, enabled:** visualize, documents, pdf, spreadsheets, presentations,
template-creator, codex-app-tools, google-drive, gmail, browser, chrome,
computer-use, unified-computer-use, code-review.

**Your connectors:** Google Drive linked to three accounts, the UD one, the Red
Clay one and kvond12. Gmail. GitHub as kvond. Todoist. Composio. Sites. Pages.

**Your local skills:** school-lesson-audit and school-slides-sweep, in your
configuration directory. Both overlap the deck skills in the repository and are
not versioned with them.

**The rest of the system, so you do not propose duplicating it:**

| Account | Role as it stands |
|---|---|
| Claude, kvond12@gmail.com, Pro | System of record. 9 projects, 110 project documents, 7 skills, 5 artifacts, the memory store, Claude Code |
| Claude, kvond@udel.edu, organisation d260f204 | Higher education and scholarship. WilmU doctoral teaching, graduate grading, book argument testing. Settled today |
| ChatGPT, kvond12@gmail.com, Free | Personal chats only. No projects found |
| Perplexity Pro, kvond12@gmail.com | Book and manual critique. Duplicates the Claude book work |
| Desktop Commander | Files, repositories, audits, batch work, repairs |

**The durable repository** is kvond/answerable-skills, cloned at
~/code/answerable-skills, holding 27 skills, a scripts folder and an audits
folder. Anything that should outlive a chat goes there.

**Two governing distinctions** Katherine uses, and the audit should use them too.
The **execution owner** is the account that actually performs a recurring job,
identified by where the job is configured. The **maintenance owner** is the
account responsible for improving the prompt or contract behind it over time,
identified by where the authoritative text lives. Right now your two automations
have no maintenance owner at all, because the policy lives inside the prompt.

**One correction already made tonight:** the premise that higher-ed grading
depends on a browser extension turned out to be false. Check your own
equivalent assumptions rather than inheriting them.

## Audit yourself

**1. Account and plan.** Identity, plan, model and reasoning defaults, usage
limits if visible, what Codex can reach, memories setting, and any configuration
that affects work. Read your own configuration directory for this.

**2. The two automations, in depth.** For each: full trigger, what it actually
does step by step, which systems it touches, what it is forbidden from doing,
what counts as success, and what breaks if it does not run. Then the important
part: **list every piece of durable policy embedded in its prompt that exists
nowhere else**, grouped so each group could become one skill in the repository.
Do not rewrite the automations. Produce the extraction plan only.

**3. Projects and chats.** Your ChatGPT-side projects and significant chats.
Cluster them: school execution, school design, higher education, book, research,
technical and system work, personal. For each cluster give frequency, importance,
whether it belongs in this account, and whether durable content should be
extracted.

**4. Memories.** What your memory holds, and whether any of it is school policy
or workflow rules that belong in the repository instead.

**5. Skills, plugins and connectors.** What each is for, which are actually used,
which are dormant, and which duplicate something another account already owns.
Say specifically whether school-lesson-audit and school-slides-sweep should move
into the repository beside the deck skills.

**6. Overlap with Claude.** Where you and a Claude account are doing the same
job. Be concrete: name the job, name both owners, and say which should keep it.
Do not assume you should keep it.

**7. Misplaced work.** Anything here that belongs to another account: personal
life, higher-ed and scholarly work, book critique, repository and file work.
For each, where it goes and what must be extracted first.

**8. Unique value.** What this account does well that nothing else does, because
of the automations, the connectors, the Drive access across three Google
accounts, or accumulated school context. Distinguish genuine advantage from
inertia.

**9. Permanent role.** One primary domain, one primary role, at most three
secondary roles. Then: work explicitly prohibited here, execution jobs,
maintenance jobs, which browser profile it drives, and what should be open by
default. Make it memorable without a chart.

**10. Risks.** What breaks if this account is re-signed or retired, if the
automations are edited, if the Claude side is simplified, if the Drive connector
loses one of its three accounts, or if the Codex app is signed into a different
account.

**11. The kvond12 ChatGPT, briefly.** One short section. Does anything in that
Free account need preserving before it is retired, or is it genuinely personal
chats and four personal projects?

**12. One question you may be able to answer that Claude could not.** Two Claude
organisations on this Mac are unidentified and are blocking every retirement
decision. One of them has its browser extension allowlist enabled, which behaves
like an institution-managed account. Do you have any evidence about whether
Wilmington University or Red Clay provision AI accounts to staff, from mail,
Drive, calendar or past chats? If not, say so plainly rather than speculating.

## Output

Sections in this order: account summary; the two automations and the extraction
plan; projects and chats; memories; skills, plugins and connectors; overlap with
Claude; misplaced work; unique value; permanent role; risks; the kvond12 ChatGPT;
next ten actions; unresolved questions.

Write it to `~/code/answerable-skills/audits/chatgpt-deep-audit-2026-10-11.md`
and say that you did. If you cannot reach the filesystem, output it as one
markdown block and say that you could not write it.

Katherine's standing preferences apply. Prose reads as directions to a person,
not to a computer. Machine strings such as automation IDs and file paths belong
inside the table or box they serve, never loose in a sentence. Ask one menu
question at a time, with a recommendation, rather than handing back a paragraph
of decisions. No parentheses in any file or folder name you create. Put
challenges to her thinking in square brackets where the evidence disagrees with
the plan.

## Success condition

She should end up knowing exactly what this account does, what only it can do,
which eight thousand words need rescuing from the automation prompts and in what
shape, what should move to another account or to the repository, and what would
break if she simplified too aggressively.

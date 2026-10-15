# UD Claude deep audit, 11 October 2026

**Provenance.** Produced by the Claude account signed in to the Chrome profile
named PROFESSIONAL, whose Gmail connector authenticates as kvond@udel.edu. It
audited itself from inside, which is the only way that audit could be done: an
account cannot inspect another account, and browser extension pairing follows the
Claude account, so the UD profile's extension is invisible from kvond12.

Run from the prompt packet at `ud-claude-audit-prompt-2026-10-11.md`. The UD
session had no route to this disk, so it returned the audit as text and the file
was written here from the kvond12 session.

**Read it alongside** `ai-account-audit-2026-10-11.md`, which covers the machine,
the browser profiles, the organisation IDs and the other accounts. Where the two
disagree about the machine, that one is the grounded account: this one could not
see the disk. Where they disagree about what lives inside the UD account, this
one is authoritative.

**Cross-checks added after the fact** are in the reconciliation section at the
end of this file. They were not available to the UD session.

---

Audited from inside the account. Everything below is either confirmed by a tool call made during this audit or marked UNVERIFIED. Nothing was deleted, moved, changed or published.


### How to read this


Square brackets mark places where the evidence disagrees with the plan in the brief. Machine strings live in the tables only.

One limit shapes the whole audit: I ran from a chat outside any project, so I can see project memory but not project documents, project instructions, or the chats held inside projects. Anything about project contents is UNVERIFIED until you open each project and look.


## 1. Account summary

| Item | Finding | Status |
|---|---|---|
| Identity | Gmail connector authenticates as kvond@udel.edu; session context reports the same address | Confirmed |
| Name on connected services | Wispr Flow reports "Katherine von Duyke"; the claude.ai greeting name is not visible to me | Greeting UNVERIFIED |
| Organisation ID | Not exposed to any tool I have | UNVERIFIED — match to d260f204-a04f-4988-9d93-560e0ffe5a7e cannot be confirmed from inside |
| Activity window | Newest chat outside projects is 24 Sep 2026; nothing after | Consistent with the 11–24 Sep window in the brief |
| Plan level | Not visible. A 9 Sep chat asked how Max-plan usage rolls over, which shows interest, not ownership | UNVERIFIED |
| Model | Opus 5.5 | Confirmed |
| Claude Code | This audit runs in a Claude Code-based cloud session on this account, so access exists | Confirmed |
| GitHub | No GitHub account linked to this account | Confirmed — this account cannot reach kvond/answerable-skills |
| Scheduled tasks | None | Confirmed — the morning brief is genuinely stopped here |
| Desktop / Cowork | Memory files and both artifacts are stamped as coming from Cowork, so the desktop app has been used on this account | Confirmed it was used; current link not checked |
| Uploaded skills | roam-pullpy, manuscript-ops | Confirmed |
| Published artifacts | 2, both Red Clay high-school material — see table below | Confirmed |
| Memory store | 22 files, including three project scopes | Confirmed |
| Preferred browser setting | Claude in Chrome | Confirmed |
| Browser extensions | Not visible from inside the account | UNVERIFIED |


### Connectors


| Connector | Connected | On in chats |
|---|---|---|
| Gmail | yes | yes |
| Google Calendar | yes | yes |
| Google Drive | yes | yes |
| Wispr Flow | yes | yes |
| Google Docs | yes | no |
| Google Sheets | no | no |
| Google Slides | no | no |
| Microsoft 365 | connection started, not finished | no |


### Artifacts


| Title | Updated | Source | Belongs here? |
|---|---|---|---|
| Answerable Biology Drive Map | 25 Aug 2026 | Cowork | No — Red Clay biology |
| Agenda Link Audit | 24 Aug 2026 | Cowork | No — Red Clay agenda |


[The brief says this account's only known role is higher-ed grading. Its actual footprint is wider: it has been a general working account since at least May, holding book work, system plumbing, Red Clay material and personal tasks alongside WilmU teaching.]


## 2. Project inventory


Three projects are visible through their memory scopes. All three memory scopes were written on 11 Sep 2026, the first day of the heavy-use window, so those projects were probably set up or heavily used that day. There may be other projects without memory; I cannot list them.

| Project | Project ID | Purpose from memory | Last memory write | Documents and instructions | Status | Unique? |
|---|---|---|---|---|---|---|
| WilmU 7106 | 019ecc6d-2648-7210-8c0d-92c467d52248 | Teaching OLI 7106 in the DIP program; the 29-step Develop and Present sequence and the cover letter proposing a role in OLI 7102 | 11 Sep 2026 | UNVERIFIED | Important, likely active this term | The DIP conventions in its memory exist nowhere else I can see |
| Scholarly Writing | 01a02518-24b9-774a-86bf-0912ee705f23 | Grading graduate papers with a seven-section feedback template | 11 Sep 2026 | UNVERIFIED | Important — this is the grading project | The seven-section template lives only in this memory as far as I can tell |
| Answerable Teaching Book | 01a02526-ece0-76db-ada5-07e5c059e821 | Book on agency development; chapter sequence as of Sep 2026; Substack cadence | 11 Sep 2026 | UNVERIFIED | Active in Sep, quiet since | Sep chapter sequence and the Paul and Noelle case plan live in this memory |


[The brief says kvond12 holds "WilmU: 7106", "Scholarly Writing" and a book project, two of which "may belong here". All three already exist here under matching names. Before you migrate anything, compare the document lists side by side. Otherwise you will end up with two divergent copies of your DIP advising material rather than one.]


## 3. Document inventory


What I could confirm, at the level needed to identify dependencies.

| Item | Where it lives | Kind | Exists elsewhere? |
|---|---|---|---|
| Seven-section graduate paper grading template | Scholarly Writing project memory | Grading instructions | Not that I can see. kvond12's Scholarly Writing holds a final paper rubric, which is a different document |
| DIP conventions: vocabulary anchoring, assessment vs indicator vs measurement vs outcomes, step framing | WilmU 7106 project memory | Advising rules | Probably overlaps the kvond12 7106 documents; UNVERIFIED |
| Ten named diagnostic teaching moves for Chapter I | Chat, 27 May 2026, "Feedback on Ilene's paper and DIP chapter 1" | Feedback framework | Summarised in memory; full text only in the chat |
| Differences as the Analytical Entry Point — deck, handout, teaching guide | Chat, 27 May 2026 | Session package | Files were generated in-chat; the Drive location is UNVERIFIED |
| Week 2 7106 deck, edited | Same chat | Teaching material | UNVERIFIED |
| Finishing Map and its Roam TODO version | Chat, 13 Jun 2026 | Book plan | Converted for Roam at the time; whether it was imported is UNVERIFIED |
| Two closing chapters, Decisions and Citations base, book project instructions | Chat, 7 Jun 2026 | Manuscript and prompt documents | The canonical manuscript is in Drive; whether these pieces made it in is UNVERIFIED |
| Three Substack drafts and a list of voice moves | Chat, 23 Aug 2026 | Drafts and a style contract | Only in the chat |
| CV and academic bio rework | Chat, 17 May 2026 | Scholarly identity | You linked the final CV publicly, so it exists outside Claude |
| Project documents in all three projects | Inside the projects | Unknown | UNVERIFIED — open each project's knowledge panel |


## 4. Grading workflow


### What the evidence shows

| Step | What happens | Evidence |
|---|---|---|
| Papers enter | You upload or paste student work into a project or chat; one chat reads a student's Milestone 3 docx from the project knowledge base | 27 May chat |
| Feedback is drafted | Claude produces a commendation with specifics, three top comments with page and line locations, and answers to the student's own questions | 27 May chat |
| Graduate papers are scored | Seven sections: header, rubric table, genre flag that is not scored, quoted commendation, deduction ledger for you, student-facing rewrite, open calls for your judgment | Scholarly Writing memory |
| You correct the reasoning | You push back when the analysis drifts, for example on the fishbone emphasis, and Claude revises | 27 May chat |
| Student questions | Claude drafts replies in your voice, signed Dr. V, with links to APA Style | 10 Sep chat |
| Comments are placed | You paste each comment into the student document at the page and line given | Inferred from the "tell me what page and line" request |
| Grades are posted | No record | UNVERIFIED — the LMS is never named in what I can see |
| Weekly slot | Monday first period is set aside for WilmU attendance and grading | 12 Jun chat |


### The extension question


I found no chat that mentions a grading extension, Chrome, or posting grades through a browser. The account's preferred browser is set to Claude in Chrome, which is consistent with the brief's guess that the Claude extension is the grading tool, but I cannot confirm it.

[Every grading session I can see is chat- or project-based: you bring the paper to Claude. If that is the real pattern, the grading setup depends on the projects and the template, not on an extension, and it can move independently of the browser. Before treating the extension as the anchor, run one grading session and notice whether you actually invoke the extension.]


### Data governance


[A 27 May chat in this account recommended confirming that model training is switched off and checking whether Wilmington offers Claude for Education, because doctoral student writing is likely FERPA-relevant. I find no record that either check happened. More important: the students are Wilmington's, not Delaware's. The account matched to that institution would be the wilmu.edu one. The unidentified organisation that has an extension allowlist enabled behaves like an institution-managed account. It may be a WilmU or Red Clay organisation. That is a hypothesis, not a finding, but it bears directly on where student papers should go.]


### Who owns what

| Kind | Work |
|---|---|
| Your judgment | Final scores; genre-fit calls; which open calls to act on; whether a POP framing is diagnosis or prescription; anything touching a student's standing |
| Repetitive, Claude can do | First-pass seven-section draft; locating evidence for each deduction; page and line placement; APA mechanics; student-facing rewrites; replies to routine questions |
| The extension | UNVERIFIED — at most, reading the paper in the browser and placing comments |
| Another tool | Grammarly for the final proof, already your habit; the LMS for grades; Drive or the repo for the template itself |


### Failure points

The template lives only in project memory. If the project goes, the template goes.
The 7106 feedback framework lives in a May chat that I could only reach because it sits outside a project.
If this account has no paid plan, a grading week can hit the five-hour ceiling, which it did between 11 and 24 September.
Student data protection is unconfirmed.

## 5. Chat use patterns


Covers the roughly twenty chats outside projects, May through September. Chats inside projects are invisible to me, and the heavy September use most likely happened there.

| Cluster | Frequency | Importance | Stay? | Extract? |
|---|---|---|---|---|
| WilmU 7106 teaching, Chapter I feedback, slide packages | Several long sessions, May | High | Yes | Yes — the diagnostic moves and the feedback pattern |
| Grading and student replies, APA | Recurring | High | Yes | Yes — reply conventions |
| Book: finishing map, closing chapters, Substack, pedagogy identification | Several long sessions, May–Aug | High | Decide — see section 7 | Yes — project instructions and voice moves |
| Scholarly identity: CV and bio | Once | Medium | Yes | No, already published |
| System plumbing: morning brief, Roam workflows, Claude Code routines, plan billing | Several, Jun–Sep | Low now; the build is stopped | No | Only the stop decision |
| Red Clay school operations, including a personnel matter, the biology pipeline, schedules and the ClassLink userscript | Several | Medium | No | Move to the school account; carry no student data across |
| Personal: a resume for someone else, family photos | Occasional | Low | No | No |


## 6. Durable prompts and workflows

| Prompt or workflow | Where it lives | Current? | Make it a contract? | Destination |
|---|---|---|---|---|
| Seven-section graduate grading template | Scholarly Writing memory | Current | Yes | answerable-skills as a grading skill, then upload it here |
| DIP conventions and the 29-step Develop and Present sequence | WilmU 7106 memory and documents | Current | Yes | answerable-skills, merged with the kvond12 DIP advising field map |
| Ten diagnostic teaching moves | 27 May chat | Current | Yes | answerable-skills, as part of the 7106 skill |
| Chapter I feedback pattern: one specific positive, three placed comments, answers to the student's questions | 27 May chat | Current | Yes | Same 7106 skill |
| Student reply voice: Dr. V, APA links, concept before mechanics | 10 Sep chat | Current | Fold in | Same 7106 skill |
| Slide visual language: cream band, coral overline, navy Arial | 7106 memory | Current | Fold in | vt-deck-authoring in the repo, if that skill exists there |
| Book project instructions and the Decisions and Citations base | 7 Jun chat | Possibly superseded by the September book memory | Yes | answerable-skills book-ops; canonical text in Roam |
| Substack voice moves | 23 Aug chat | Current | Yes | answerable-skills, beside hep-scout |
| Finishing Map | 13 Jun chat | Superseded by the September chapter sequence | No | Roam only |
| Morning brief SKILL.md v2 | Private daily-brief GitHub repo | Obsolete, stopped 17 Sep | No | Leave archived |
| manuscript-ops and roam-pullpy | Uploaded here | Current | Already contracts | Confirm the repo copy is the source of truth |


## 7. Book and research role

| Function | Fit for this account | Reason |
|---|---|---|
| Academic argument testing | Good | Your best exchanges here are argument-level pushback |
| Literature critique of a draft | Good, if hep-scout is uploaded here | hep-scout governs critique and is not loaded in either account |
| Manuscript review and chapter integration | Conditional | Duplicated with kvond12's book project, book-ops and chapter-bank; it needs one home |
| Substack and article drafting | Good | Scholarly-adjacent; the voice moves came from here |
| Research notes | No | Roam is canonical; Claude should read Roam, not hold notes |
| Annotated literature reviews | No | Perplexity for discovery, Roam for keeping; bring single sources here for critique |
| Personal and system oversight | No | ChatGPT |
| Technical and system work | No | Codex and Desktop Commander |


[The brief frames UD as the scholarly home, but most of the book's operating skills sit in kvond12 and the repo, not here. This account has manuscript-ops only. Making UD the book home means uploading hep-scout and book-ops here from the repo. That is cheap, because the repo is the source, and it is cleaner than keeping two book projects alive.]


## 8. Misplaced work

| Item | Where it is here | Goes to | Extract first |
|---|---|---|---|
| Morning brief and dashboard design | Memory file and June and September chats | Retire | Nothing; the stop decision is already recorded |
| Tiller finance sheet reference | 12 Jun chat | Personal account | Nothing |
| Red Clay biology pipeline | Memory file and May chat | School account | The workflow spec, with no student work |
| School schedule and ClassLink userscript | Memory files | School account | The bell times, if not already on the Master sheet |
| Two Red Clay artifacts | Artifact gallery | School account | Re-create them there if still used, then retire these |
| A Red Clay personnel matter | June chat | Keep out of every AI account once resolved | Nothing; the letter already went to your representative |
| Resume for another person | May chat | Personal | Nothing |
| Family photo organization | Memory file | Personal | Nothing |


Leave every item in place until its destination exists. Removing anything is a later, deliberate step.


## 9. Unique value


### Genuine advantages


The only seven-section grading template I can find.
7106 context that already knows your cohort's patterns and your DIP vocabulary corrections, including "for this purpose", not "on".
Gmail and Drive connectors authenticated to the UD address, so UD mail and files are reachable without switching.
Memory that already describes you as Dr. V, the doctoral educator.


### Inertia, not advantage


The Red Clay and personal material. It is here because the account was open, not because it fits.
The three project names duplicated with kvond12. That is drift, not design.

## 10. Proposed permanent role


One line to remember: UD is the professor's desk — grade, advise, argue.

| Slot | Assignment |
|---|---|
| Primary domain | Higher education and scholarship |
| Primary role | WilmU doctoral teaching: 7106 feedback and graduate paper grading |
| Secondary role 1 | Book argument testing and manuscript review |
| Secondary role 2 | Scholarly and Substack writing |
| Secondary role 3 | Professional identity: CV, bio, proposals to program leadership |
| Prohibited here | Red Clay operations and student data; finances and home life; automation builds and system maintenance |
| Execution jobs | Seven-section grading drafts; Chapter I feedback; student replies; leadership documents |
| Maintenance jobs | Monthly: move any new reusable prompt into the repo. Each term: confirm training is off and the 7106 skill is current |
| Browser profile | PROFESSIONAL |
| Extension dependencies | Claude; Grammarly for the final pass |
| Open by default | WilmU 7106 project, Scholarly Writing project, your WilmU course site |


[If the wilmu.edu address turns out to have its own Claude organisation, the primary role may belong there rather than here. Settle section 13's first open question before you lock this in.]


## 11. Comparison with kvond12

| kvond12 holding | Recommendation |
|---|---|
| Pro subscription | Stays. [If UD has no paid plan, moving the full 7106 workload here will hit the ceiling again.] |
| WilmU: 7106 project, seven documents, the only copy of the DIP advising material | Put the documents in the repo first, then add them to this account's existing 7106 project after comparing |
| Scholarly Writing project, final paper rubric | Put the rubric in the repo beside the seven-section template, then add it to this account's Scholarly Writing project |
| Book project | Retire after extraction, if UD becomes the book home |
| Website, TPT, AI HS, master agenda, finances, critical aspect activities | Stay in kvond12 or go to their own domains; none come here |
| Seven uploaded skills | Repo is the source. Upload here only manuscript-ops, already present, plus book-ops and chapter-bank if UD becomes the book home. The vt- skills and ste stay out |
| Five artifacts | None come here; they read as Red Clay and system material |
| Memory, 30 files | Do not merge. This account's memory already covers the higher-ed subjects |
| Claude Code admin identity | Stays in kvond12; this account has no GitHub link and does not need one for its role |


## 12. Migration map


### Keep in UD Claude


WilmU 7106 project
Scholarly Writing project
Answerable Teaching Book project, if UD becomes the book home
manuscript-ops skill
Gmail, Drive and Calendar connectors


### Migrate into UD Claude


kvond12's seven 7106 documents, after comparison
kvond12's final paper rubric
hep-scout and book-ops from the repo, if UD becomes the book home


### Move out to a durable repository


Seven-section grading template
DIP conventions and the 29-step sequence, merged with the DIP advising field map
Ten diagnostic teaching moves and the Chapter I feedback pattern
Substack voice moves
Book project instructions, reconciled with the September memory


### Retire and do not migrate


Morning brief and dashboard design
The two Red Clay artifacts, once re-created in the school account if still needed
Red Clay, finance and personal memory files, once their destinations exist
kvond12's book project, if UD becomes the book home

## 13. Risks

| If you… | What breaks |
|---|---|
| Retire kvond12 before extracting | The only copy of the DIP advising material is lost; the paid plan goes; Claude Code admin and the repo authentication go with it |
| Clean up browser profiles | If grading really runs through the Claude extension, losing PROFESSIONAL breaks the sign-in pairing. Check before cleaning |
| Move the grading extension | Possibly nothing, if grading is chat-based as the evidence suggests; possibly everything, if it is not. Test one session first |
| Shorten prompts | The seven-section template's separation of instructor and student audiences, and the "flag, don't deduct" genre rule, are the parts that look trimmable and matter most |
| Delete projects | The grading template and the DIP conventions disappear with their project memory |
| Change the Claude Code identity | Nothing here; this account has no GitHub link. The kvond12 side carries that risk |
| Leave things as they are | Two copies each of the 7106, scholarly writing and book projects drift further apart, and student data protection stays unconfirmed |


### Next ten actions

In PROFESSIONAL, open Settings and note this account's organisation ID and plan.
In Settings, Privacy, confirm model training is off.
Check whether the wilmu.edu address has its own Claude organisation; try it against the two unidentified organisation IDs.
Open each of the three projects here and list their documents and instructions.
Compare the 7106 document lists in both accounts and note what exists only in kvond12.
Copy the seven-section template and the kvond12 final paper rubric into answerable-skills as one grading skill.
Copy the DIP conventions, the 29 steps, the diagnostic moves and the advising field map into answerable-skills as one 7106 skill.
Upload those two skills to this account.
Run one real grading session and note whether you ever use the Claude extension.
Decide the book home, then upload hep-scout and book-ops to that account only.

### Unresolved questions

| Question | Blocks |
|---|---|
| Is this account organisation d260f204-a04f-4988-9d93-560e0ffe5a7e? | Confirmation of the outside audit |
| What plan is this account on? | Whether it can carry the full grading load |
| Who owns 1fc883da-00b0-488f-9f2a-a1b0787f807c and cdb42cb9-a0bf-4b2b-8d22-20cb001635c1? Possibly wilmu.edu and redclay.k12.de.us | Every retirement decision, and where WilmU student data should go |
| Does grading actually use the Claude extension? | Whether grading can move independently of the browser profile |
| Which LMS receives grades? | The last step of the workflow map |
| What do the three projects here actually contain? | Duplication decisions |
| Is UD or kvond12 the book's home? | Which skills to upload where |


### Where this file is


I could not write this into ~/code/answerable-skills/audits/. This account has no GitHub link and no route to your Mac. The file was delivered in chat for you to save there.
---

## Reconciliation with the machine audit, added from the kvond12 session

The UD session could not see this computer, so it left several things UNVERIFIED
that the machine audit had already answered, and it produced one finding that
independently confirms a guess made from outside. Both directions are recorded
here.

### The organisation question is now effectively settled

The UD session could not read its own organisation ID and marked the match to
`d260f204-a04f-4988-9d93-560e0ffe5a7e` as unconfirmed. Two independent checks
from this side close most of that gap.

**First, the project IDs match.** Hours before the UD audit ran, a scan of the
PROFESSIONAL profile's claude.ai browser storage recorded a list of identifiers
it held. Two of them are exactly the project IDs the UD session later reported
for itself:

| Project, as the UD session named it | Project ID it reported | Also found in the PROFESSIONAL profile's claude.ai storage |
|---|---|---|
| WilmU 7106 | 019ecc6d-2648-7210-8c0d-92c467d52248 | yes |
| Answerable Teaching Book | 01a02526-ece0-76db-ada5-07e5c059e821 | yes |

Neither side knew what the other would say. The profile that holds those two
project IDs also holds organisation `d260f204`, and holds no other unexplained
organisation.

**Second, the dates coincide.** The machine recorded `d260f204` as last active on
24 September 2026 at 09:55 and silent afterwards. The UD session, with no access
to that record, reported that its newest chat outside any project is 24 September
2026 and that there is nothing after it.

Taken together: the UD Claude is kvond@udel.edu, it lives in the PROFESSIONAL
profile, and it is organisation `d260f204`. The residual doubt is small enough to
act on, and a glance at Settings in that account would retire it entirely.

### What the machine audit can answer that the UD session left open

| The UD session marked UNVERIFIED | What the machine shows |
|---|---|
| Browser extensions in its profile | Exactly four: Claude, ChatGPT, Grammarly, Google Docs Offline. Nothing named for grading |
| Whether the desktop app link is current | The Claude desktop app is not running at all. Its configuration carries four Claude account identifiers and five organisations |
| Its own activity window | Matches `d260f204`, heavy use 11 to 24 September, then silence |

### Where the UD session corrects the brief, and it matters

**Grading is not extension-based.** Every grading session it can see is chat or
project based: the paper is brought to Claude. It found no chat mentioning a
grading extension at all. The machine agrees from the other direction, since no
extension in that profile does anything of the kind.

This overturns the premise both audits were handed, that the UD account must be
kept because a grading extension lives there. The real dependency is the
**seven-section grading template**, which exists only in the Scholarly Writing
project's memory, and the **DIP conventions** in the 7106 project's memory.
Those are the things that would be lost, and neither is a browser extension.
The practical consequence is good news: grading can move between accounts and
browser profiles freely, and what actually needs protecting is two bodies of
text that belong in the repository anyway.

**The project names are duplicated across both accounts.** WilmU 7106, Scholarly
Writing and an Answerable Teaching Book project exist under matching names in
kvond12 and in UD. That is drift rather than design, and it is the strongest
argument in either audit for doing the comparison before any migration.

### A governance point neither audit can settle, raised by the UD session

The students are Wilmington University's. The account grading their papers is a
University of Delaware one. The UD session also found a May recommendation to
confirm that model training is switched off, with no record that the check ever
happened. It then noted that `1fc883da`, the unidentified organisation with its
extension allowlist enabled, behaves like an institution-managed account and may
be a WilmU or a Red Clay organisation.

That is a hypothesis, not a finding, but it is the first plausible account of
what `1fc883da` is, and it raises the stakes on identifying it: if WilmU has its
own Claude organisation, doctoral student writing probably belongs there rather
than in a personal UD account.

### Still open after both audits

1. What plan the UD account is on. It affects whether it can carry the grading load, since `d260f204` hit the ceiling of its five-hour window during the September grading run.
2. Who owns `1fc883da` and `cdb42cb9`. Still the single thing blocking every retirement decision.
3. What the three UD projects actually contain. The UD session ran outside any project and could see project memory but not project documents.
4. Which LMS receives the grades.

---

## Settings check, 15 October 2026

Read from claude.ai Settings in the Chrome browser named "UD CHROME AND CLAUDE"
(Windows), through Claude in Chrome.

| Item | Finding |
|---|---|
| Organisation ID | `d260f204-a04f-4988-9d93-560e0ffe5a7e`. The match is now confirmed, not inferred |
| Plan | Claude Pro (the Account page says the Pro subscription must be cancelled before the account can be deleted) |
| "Help improve our AI models" | Was **on**. Turned **off** at Katherine's instruction; confirmed off after a reload |
| Location metadata | On; left unchanged |

This closes open item 1 (plan) and the organisation question. Still open: who
owns `1fc883da` and `cdb42cb9`, what the three UD projects contain, and which
LMS receives the grades.

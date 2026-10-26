---
name: student-feedback
description: Write students' lesson feedback and science-writing reports for Biology, Forensics and A&P in Katherine's approved formats, and render them as printable PDFs. Holds the canonical feedback prompt (Prompt 2), the rating scale, the class-by-class report layouts, the teacher-only flag rules and the renderer. Slack CURRENT SKILL — Feedback is the first operational reference; this file is its matching GitHub backup and program entrypoint. Use for any feedback or writing report on student work, a catch-up of lessons without feedback, or a question about which format a class uses. Triggers - "feedback", "writing feedback", "feedback on latest work", "catch up feedback", "science writing report", "which feedback format".
---

# Student feedback and science-writing reports

Revision 2026-10-26. Katherine's latest source hierarchy makes the
[Slack CURRENT SKILL — Feedback](https://answerableteaching.slack.com/archives/C0C9E488BAN/p1792976967534889)
the first operational reference. This is its matching consolidated backup.
Agenda Feedback Prompts remains a preserved source and quick reference.
The six sections below consolidate each unique operative requirement from the
existing skill, Prompt 2 v4, Agenda A1:B15 and spreadsheet feedback procedure.
Current corrections and unresolved source conflicts are explicit, not hidden.

Program entrypoints remain [answers.py](scripts/answers.py),
[unique.py](scripts/unique.py), [render.py](scripts/render.py) and the existing
[layout examples](examples/). Use existing private exemplar bindings, never
publish student examples. Report JSON and PDFs stay outside Git checkouts.

```sh
SCRATCH=$(mktemp -d)
python3 skills/student-feedback/scripts/render.py "$SCRATCH/report.json" "$SCRATCH/out.pdf"
```

**1/6 — Scope, evidence, identity and conceptual feedback**

This skill prepares lesson feedback, separate science-writing reports, teacher records and printable packets for Biology, Forensics and Anatomy/A&P. It never changes grades, completion scores, IC, Forms, decks or original student work. Conceptual levels are not numeric IC grades.

**Preflight and reuse**
• Resolve current class/section roster, exact lesson, actual assignment/Form, latest submitted source and genuine earlier submissions. Use Agenda, lesson-name bindings and turn-in evidence, not week number or filename alone. Historical offsets: Forensics intake runs one week ahead from Mock Crime Scene; A&P one week behind from Cell Structure; Biology uses cycles. Verify the actual binding. A&P Cell Structure and continued can be one grade but two lessons.
• Search the verified assignment’s complete permitted intake, including original Form references, upload subfolders, loose/unsorted and earlier/shared locations. Deduplicate file IDs, not distinct submissions/history. Exclude templates, generated reports and test artifacts. An empty lookup, missing link, inaccessible source or unrated report is not missing work. Preserve retired sources and access boundaries.
• Find existing student/lesson/report-type/reviewed-source versions first. Reuse matching verified reports. New filenames/modification dates do not prove new work. Check exact current ownership before any write.
• Print only the supplied roster first name and last initial. Never guess a fuller name. Historical initials may match only within the same section with one unambiguous student. Otherwise exclude the uncertain history and record the reason privately.
• Read actual native Slides/PPTX response evidence, not template text. Distinguish NOTES/DRAFT/BANK, bellringers and tables. Use the existing answer-extraction/comparison helpers when applicable. A blank is blank. No submission, a blank copy and unavailable evidence are different.
• Individual review batches are at most 20 decks; combine and deduplicate all batches before a class-wide comparison or total. Report incomplete coverage rather than pretending a partial batch is the class.

**Read growth history**
Search existing teacher-only Growth record — <class> documents and read applicable rows. For conflicting records of the same student/lesson/aspect, use the newer record after verifying identity/source. No prior record means starting point. Compare explanations, not vocabulary or length alone.

**Critical aspects and levels**
Take aspect names exactly from the deck’s response headings or “Critical aspect” labels. Do not invent, merge or rename aspects. If unlabeled, note that privately and identify the question. What-if evidence can show transfer.
• Beginning: names an idea, with relationship missing or inaccurate.
• Developing: connects some ideas, with mechanism/relationship partly explained.
• Proficient: accurately explains the relationship/mechanism.
• Extending: uses it in a new case, distinguishes similar cases or identifies a limit.
Blank/unreadable = **Evidence unavailable**, never Beginning or zero.

Concepts precede terminology. Rate the relationship, mechanism, distinction, cause or consequence explained—not grammar, length, sophistication or a correct term alone. A clear explanation of a wrong relationship is Beginning.

Rate the revised answer when genuinely present. Compare earlier answers only from a genuine earlier submission or explicit teacher timing evidence. A “first answer” box is not proof of pre-instruction thinking, and filling a blank is completion, not conceptual growth. Describe actual changes: causal link, distinction, correction, mechanism, evidence-to-claim connection, limit, persistent misconception or reduced clarity. Longer/polished wording alone is not growth.

Forensics deliberately uses AI revision coaching. Polish alone is not a flag. If the revised box contains AI feedback rather than the student’s own revision, record that privately and rate the first answer.

---

**2/6 — Teacher-only diagnostic screening and decision boundaries**

Screen before preparing student pages, but do not invent a blanket pre-review hold on routine feedback. Katherine’s latest instruction: finish, file, link and make ordinary feedback/writing print-ready without her pre-review; she reviews after printing. Preserve genuine source/identity/privacy/final-grade safeguards. Parent sending and student-facing authorship allegations are separate.

**Peer-response comparison**
Compare readable answers to the same question across the complete current class set and available same-lesson sections. Ordinary scientific vocabulary is not a flag. For a useful alert, retain privately:
• both students, exact question/aspect/slide and shared wording
• similarity percentage only when actually calculated
• distinctive wording, errors, sentence order or other observable pattern.
Label “POSSIBLE SHARED/COPIED LANGUAGE — TEACHER REVIEW.” Similarity does not prove copying. Never put another student’s name on printed feedback without approved flag wording. Historical approved-message template, only after such approval: “Your response closely matches <first name and last initial>'s response on this question. I need to see your own thinking. Answer the question below in your own words.”

**Possible AI/web/borrowed language**
Compare with established prior writing only when sufficient evidence exists. Consider multiple signals together: major style/complexity/vocabulary change; generic definitions disconnected from the case; sophisticated terms without the relationship; unsupported conceptual jumps; close match to identifiable lesson/web text; radically different revision language; formulaic patterns. Grammar, spelling, brevity, improvement or a single unusual phrase is insufficient.

Prompt 2 v4 historically requests a teacher-only “AI-USE LIKELIHOOD INDICATOR: <0–100>%,” explicitly heuristic, not proof and never sufficient for grading, discipline or accusation. **Methodological issue remains unresolved:** observed text similarity is not verified AI authorship. Do not fabricate precision or present an unsupported probability as fact. Record observable evidence and uncertainty; this is not a new routine-feedback hold. No direct user instruction deleting the historical method has been verified.

The historical student-facing AI-check template remains conditional on explicit teacher approval: “Likely AI-supported response: <percentage>% — this is not proof of AI use. I need to see your own understanding. Answer the question below in your own words.” It must not be used to invent an unsupported percentage. Use a conceptual transfer question to elicit the student’s own understanding where authorized.

Keep pasted AI feedback/URLs, keyboard mash, copied lesson/web language, near-identical answers, shared partner decks, identity/version anomalies and all screening evidence in teacher-only records, never this public channel or ordinary student pages.

**Teacher decisions retained**
Katherine decides interpretation overrides, whether similarity means copying, student-facing authorship wording, any assessment consequences, teaching choices and next lessons. AI may organize evidence, rate against the approved framework, compare legitimate earlier/current work, identify patterns, suggest contrasts/questions and prepare ordinary feedback and summaries. No new numeric grade authority follows. Suggested teaching moves remain suggestions, not scheduled lessons.

---

**3/6 — Student pages and course-specific science-writing formats**

**Lesson feedback content, in order**
1. **Your growth:** a small simple visual. Conceptual plotting codes are Beginning 1, Developing 2, Proficient 3, Extending 4—not grades. Missing evidence is a gap, never zero. Generic Prompt2 requests legitimate historical points; without adequate history use “This is your starting point. Future lessons will show how your explanations develop.”
2. **How you did on this assignment:** usually 2–3 sentences addressed to “you,” identifying an understood relationship and the most important developing aspect. Ideas, not writing polish. Say when evidence is too limited.
3. **One question to think about:** exactly ONE question grounded in the student’s own phrase/claim/misconception and the most important missing distinction. Prefer a meaningful contrast or transfer case. No generic “explain more,” answer giveaway, invented next lesson or activity. Leave generous writing space.
4. **What I understand now that I didn’t before:** “Write this yourself, then hand this page back to me. This is the part I read.” Leave generous full-width space, unfilled.
5. **How I can improve my responses next time:** generous full-width space, unfilled.

Keep wording lean, readable and useful to the course/learner. No generic praise, guessed feelings, standards codes, research jargon or lengthy rubric explanation. Never invent quotes, levels, comparisons or growth. Unless specifically requested, omit full rubric, long quotation lists, all earlier/current pairs, detailed diagnostics, class distributions, similarity calculations, AI indicators, file anomalies and copying investigations. Personal-connection work stays primarily in lesson slides.

**Existing approved-format specification**
• Biology: lesson_onepage (1 page) + writing_bio (2 pages).
• Forensics: lesson_onepage (1 page) + writing_cer (3 pages).
• A&P: lessons_grouped (2 pages), at most THREE critical aspects per lesson + writing_cer (3 pages).
Read the existing private exemplar for the format, not just its filename. Do not publish exemplar links or real examples in Slack.

**Format details**
• lesson_onepage: class kicker, supplied first name/last initial, lesson and submission date, five sections above. The GitHub exemplar specification uses current-level dots per aspect, Evidence unavailable as text/no dot and “A single report does not establish a growth trend,” rather than plotting earlier lessons.
• lessons_grouped: page 1 lesson bands, up to3 aspects per lesson, current level and what the answer shows. Page 2 thinking-change evidence only if genuine earlier work exists (otherwise explicitly no earlier submission), one question, quotes with slide locations and reflection space.
• writing_bio: page 1 reviewed pieces L1/L2…, each area’s prompt/level/lesson/date/code/exact quote/comment and a small chart. Page 2 opens prominently **10 pts summative extra credit**, then latest-lesson challenge title/task, writing lines and discussion question. The label does not authorize posting IC points.
• writing_cer: page 1 four areas with source, level, quote and comment. Page 2 every submitted source S1/S2… in date order, each file once, with a 2×2 chart grid. Page 3 latest-reviewed-lesson why/how question, THREE accurate supplied lesson facts and separate Claim/Evidence/Reasoning writing lines. Practice facts are not student evidence. Returned practice is unrated until actual writing is reviewed.

**Restored exemplar dot colors — October 26, 2026**
Use the established October 21 feedback/writing exemplar colors; color is presentation, not a new rating. Lesson-feedback current-level dots are navy #17384B. Writing graph dots identify the writing strand, NOT achievement level: Vocabulary = blue #087EA4; Conceptual answers = purple #8050A2; Specific evidence = teal #16836D; Reasoning = orange #D36528. The exemplar explicitly pairs Science vocabulary with graph Vocabulary, Constructing an answer with graph Conceptual answers, and Explaining evidence with graph Reasoning; retain the report's established labels rather than renaming them. Apply colors only to a verified matching strand. Do not infer colors for different categories such as Claim or Clarity. Keep the strand labels/key visible; achievement is shown separately by the existing level axis/labels. Do not recolor strand dots by level, change saved scores, re-rate work or invent graph points/history to restore color. Missing or unrated graph evidence remains a gap. Where only existing strand labels can be colored without inventing points, retain the labeled category markers/key and report graph coverage honestly. Check colors in the saved individual PDF and assembled packet; preserve all content and source evidence.

Source: verified October 21 approved-format exemplar and Katherine's October 26 request to restore colors and record the directions. [Current skill clarification](https://answerableteaching.slack.com/archives/C0C9E488BAN/p1793030521927189). Private exemplar/student links stay outside GitHub.

**Separate science-writing judgment**
Four areas: science vocabulary, conceptual explanation, specific evidence, scientific reasoning. Each needs an exact student quote/location, approved level, and 1–2 sentences stating what works and one concrete next move. One chart point per distinct reviewed piece. Unreviewed pieces are gaps; do not re-rate saved work to redraw charts or infer a trend from one point.

**Explicit format conflict**
Generic Prompt2 historical-growth graph instructions and the later GitHub current-dot onepage specification differ. Preserve both source descriptions. Use the already established course exemplar for the actual report being reused/produced, do not fabricate history or silently redesign it. This capture does not assert a newly verified teacher override of every historical graph requirement.

---

**4/6 — Teacher records and class summaries**

**Growth record — teacher only**
Save/update the existing correct private location with the naming pattern:
Growth record — <class> <week> — <assignment> — <date>.
One row per student/aspect:
Student | Section | Week | Lesson | Critical aspect | First level | Current level | First-answer quote | Current quote | Slide | Date.
Quotes≤25 words. Use — for no legitimate earlier answer and retain Evidence unavailable rows. Never print this record for students.

Teacher Notes retain: conceptual interpretation; idea worth chasing; possible discussion question; printed-source copying; peer similarity; AI/web/borrowed-language observations/uncertainty; ambiguous identity; missing/misplaced revision; file/version anomaly; genuinely questionable rating. Authorship concerns stay private unless approved for student-facing wording.

**Class growth summary — teacher only**
Naming pattern: Class growth summary — <class> <week> — <assignment> — <date>.
Keep it quick to use and include all eight sections:
1. Lesson/title, teacher-copy label, class/section, students/decks read/Evidence-unavailable counts. No completion scores.
2. Each aspect’s Beginning/Developing/Proficient/Extending/Evidence-unavailable distribution; each row totals the actual list.
3. One to3 recurring conceptions, each present in more than one student’s work: plain-language idea, n/N, representative short exact quotes/names in the private report, what students discern or conflate.
4. Most important teaching contrast using evidence from both sides: **Why this contrast / Compare / Ask / What not to assume**. Name the insufficiently discerned aspect. Suggest ONE next-lesson opening question/contrast, labeled “Suggested teaching move — teacher decision required,” not scheduled.
5. **An idea worth chasing:** student, short exact quote, aspect, why useful, possible discussion question. Suggestion only.
6. Authorship/understanding review: peer similarity, possible AI/web/borrowed language, printed-source copying and insufficient evidence kept separate. Matching language/observable reasons, no automatic grades or conclusions.
7. **Check these yourself:** only genuinely unresolved duplicate/ownership/revision/mapping/rating/similarity/source-copying/conceptual-jump anomalies.
8. **Every student:** compact row with current level for each aspect and evidence/review note, consistent with the growth record.

Never invent quotes, counts, trends or authorship conclusions. Generalize conflations/misunderstandings and useful follow-up questions for teaching; note epistemic reframing when actually evidenced, not as a required invention.

**Related Agenda Prompt3 — Biology teaching summary (separate teacher-analysis output)**
Keep this distinct from ordinary student feedback and Prompt2 class summary. Reuse saved ratings by stable row key and rate only genuinely unreviewed eligible answers. Explanation and critical-aspect ratings are separate:
• Explanation 1 Names, 2 Connects, 3 Explains how/why, 4 Extends to a new case/limit. If the question did not ask for explanation, “question didn’t ask for an explanation,” not a low rating. Explanation structure can be clear while science is wrong.
• Critical-aspect levels retain the conceptual scale; scientific correctness belongs here.
Use actual revised-answer evidence; blank/copied/code-missing evidence stays a gap, not a low level. No invented quotes, ratings or trends.

Output Teaching summary — Biology — <date>:
Part 1 principals: anonymized StudentA/B labels; explanation≥3 share per lesson/date with rated n under each point; 3–4 explanatory sentences, no trend from 1–2 lessons; 3 well-evidenced earlier/later cases with exact quotes/dates/lessons/levels; unit/aspect table with Proficient-or-Extending n/N and missing distinction/short quote. Preserve existing thresholds Mastered≥75%, Needs reteaching<50%; these are reporting categories, not new grades. Group by verified units or explicitly use lesson order.
Part 2 private teaching records: one page per student with explanation-level/date graph with gaps, 2–3 evidence-based change sentences, strongest/weakest aspects.
Save Summary ratings — Biology — <date>: Row key | Student | Week | Critical aspect | Explanation(or not asked) | Aspect level | Reason≤15 words. Preserve all earlier valid ratings. If Doc graphs unavailable use an authorized .docx with chart images, then numeric chart tables if necessary; if saving unavailable return a private CSV. Report new versus reused counts.

**Unresolved retired-source conflict:** Prompt3 still names the retired Student answers—Biology sheet and old folder wording. Current procedures forbid restoring that sheet. Resolve the existing authorized current evidence binding before that auxiliary report; do not recreate/restore it, invent a replacement or hold routine feedback hostage.

---

**5/6 — Missing-work notes, files, packet and verified completion**

**No-work branch**
Only after genuinely missing work is confirmed under the applicable current rule—not from an empty lookup—use Prompt2’s note:
“I would really like to tell you how your explanations are improving, but I do not have submitted work from this lesson to read yet. Your ideas matter, and I need to see them to give you useful feedback.”
Legitimate prior growth may be shown. Add **MY COMMITMENT FOR NEXT TIME**:
“For the next assignment, I agree to show my thinking and submit my work.”
Leave One step I will take / When I will do it / Help I need or something I want my teacher to know / Student signature / Date.
No invented levels/quotes/growth, no growth-record row for nonexistent work, no grade/deadline change.

For current supportive contracts, use complete fresh intake, roster, taught/due dates, extensions and flags. Exclude Exempt/unassigned/newly joined/future-due/extended work. Located submissions close the corresponding missing-work claim. Combine current missing lessons on one student contract page. Unknown extension status uses “Work not located as of [check date]” and an invitation to show the submission/make a plan, not an invented deadline. Old contracts do not prove present absence. Missing-work analysis stays independent from ready reports.

**File and render**
Use the existing student-feedback renderer and approved report model. Keep input JSON/PDFs in private scratch outside Git. Renderer uses reportlab and enforces scale, ≤ 3 A&P aspects/lesson, four writing areas, one point/source and page counts 1/2/2/3. Its pass does not replace visual review.
Save each report version once in the existing verified private student/class folder:
YYYY-MM-DD — Last, First — <Lesson> — Feedback.pdf
YYYY-MM-DD — Last, First — <Lesson> — Writing.pdf
Use exact roster identity for private filenames. Student pages retain supplied first name/last initial. Reopen saved bytes/text, expected pages, source match, readable graphics/margins/writing space and private destination/access. Filing/indexing failure resumes from saved artifacts, not another assessment. Preserve originals, earlier reports, existing private intake and history.

Student reports use approved PDF formats; Prompt2’s “Student Feedback Doc” wording does not replace them. Growth record and class summary remain teacher-only Docs. Update only exact authorized Submission/Feedback/Writing/index/version cells, preserving layout/history. Record source revision, report ID/version/type, actual submission/review dates and status. No new snapshot workbook or duplicate folder.

**Printable packet is independent**
Evaluate existing saved-report packet assembly even if new generation is held. Use one frozen selection and immutable manifest of report versions/page ranges/PDF ID/hash/build date/omitted scopes. Do not package a file another writer is changing.
Produce or reuse ONE dated private PDF grouped by class/student, with each current student’s latest verified feedback and writing by actual submitted/reviewed chronology—not highest week/file date. Label different lesson/date sources separately. Include actual report content, not links-only. Exclude teacher-only analyses, drafts and proven duplicate representations. Preserve individual files/older packets. Partial coverage must be labeled; one held scope does not block other ready reports.
Reopen complete packet, check page order/bytes/render/private access, publish correct link in the existing checklist and update the existing Hub link when supported. Hub/Gmail/IC health is not a prerequisite for the saved spreadsheet/PDF result.

**Status and final readback**
Yellow means exact saved verified report version not yet included in a verified packet. White means that exact version was included in saved/reopened/checked packet. New version→yellow. Failed/interrupted build never clears yellow. Derive from version/manifest evidence, not cell paint. Blank/white is not proof of feedback.
Preserve Made evidence and teacher-controlled Printed/Handed. Print-ready is not printed or handed out; unknown offline activity is unknown.
IC verification is separate exact student/assignment/component/value/date saved readback by the existing authorized reader/helper. Assignment-level stamps/counts and report/packet scores do not verify an individual cell. Preserve higher retained IC values. This skill never enters grades or creates assignments.

Account for every in-scope student/lesson as new/revised, reused or explicitly held/no-submission/blank/uncertain. Verify aspect names, exact quotes, matching levels, no teacher-only flags on student pages, correct private files and working checklist/packet links. Report new/revised/reused/filed/packaged counts separately and exact remaining scope. No email/parent sending, permission expansion, physical printing or automatic delivery marks. Uncertain model/save outcomes require reconciliation, never blind retries.

---

**6/6 — Related prompts, source precedence and captured conflicts**

**Slack first, GitHub backup**
Katherine’s latest instruction makes this Slack skill the first operational reference. GitHub retains matching versioned backup/programs. Agenda Feedback Prompts remains a preserved source/quick reference, not discarded. Earlier “GitHub always wins/change GitHub first” prose is superseded by that latest hierarchy, not permission to lose prior requirements. Follow explicit current teacher corrections within required safeguards.

Read the general [Hub/IC/Feedback workflow skill](https://answerableteaching.slack.com/archives/C0C9E488BAN/p1792973736205739) rather than duplicating its operational checklist. Routine feedback/writing must finish/file/link/be print-ready without blanket teacher pre-review. Authorship alerts, substantive teaching choices, privacy/identity/source/final-grade safeguards and separately authorized sending remain distinct.

**Other Agenda prompts are preserved but not new authority**
• Prompt0/B7 is a separate deck-labeling procedure: identify actual received questions/response types, preserve all content/order/styles/answers/source/history, exact selectable ASCII labels outside response boxes, same exact ID for genuine NOTES/DRAFT partners, and one matching inventory. Missing code is not evidence a printed question is absent. Do not edit a deck while doing feedback.
• Prompt1/B8 is deterministic completion, not conceptual/writing assessment. Use its deployed current contract, exact identities/assignment/exclusions, found-code denominators and zero-denominator N/A. Required coded blanks stay required; optional is unscored; no correctness/grammar grading. Initial versus final, NOTES/BANK versus DRAFT and six-consecutive-word source-match review rules stay distinct. Copied status is a review signal, not misconduct proof. Preserve exact keep-higher/flags/uncertain-save fences and the sole IC writer. No completion arithmetic changed by this capture.
• The old Photosynthesis exception and old source-readiness text are historical scope, not a reason to reopen a verified closed repair. Check fresh persisted state/evidence. Authorized paper-only Biology lessons do not acquire missing digital revisions or zeros merely because DRAFT is absent. Do not invent codes or bypass holds.
• B6 is Forensics revision coaching, not automatic feedback content: quote one thing the student got right, identify inductive/deductive reasoning if relevant, ask TWO questions probing why the conclusion could be wrong/incomplete/overcertain, name one useful distinction/alternative, stop for the student’s own revised answer. Never rewrite/give the answer. Preserve first answer and actual lesson evidence. Do not impose digital revision coaches on authorized paper-only Biology decks.
• Preserve batching≤20 individual checks with complete combined comparisons, actual roster/identity, complete intake coverage and current source versions. No restore of retired/trashed sources or treating inaccessible evidence as missing.
• Update-together history names Agenda/manual§12/AppendicesB/F/copyable prompts/worked examples and former Skill4/dashboard. Some old copies were not located and current GitHub says Skill4 replaced/no Hub renderer. These alignment/implementation claims need verification; do not fabricate synchronized state or rebuild an obsolete renderer.

**Source coverage, read 2026-10-26**
Agenda Feedback Prompts A1:B15: source/discovery/version rows, Forensics coaching B6, labeling B7, completion B8, full Prompt2v4 B9, Biology teaching-summary B10, integration/name rules B11/B14. Private locators/examples are intentionally not reproduced.
GitHub backups read:
[student-feedback skill](https://github.com/kvond/optimized-system/blob/main/skills/student-feedback/SKILL.md)
[Prompt2v4](https://github.com/kvond/optimized-system/blob/main/skills/student-feedback/reference/prompt-2-feedback-for-students.md)
[Spreadsheet reports/packets](https://github.com/kvond/optimized-system/blob/main/prompts/school-spreadsheet-feedback.md)

**Captured, not implemented:** requirements are consolidated here. GitHub hierarchy/override synchronization is pending the existing documentation batch. Historical graph/exemplar and AI-probability methodological issues are identified above, not silently “resolved.” Retired-source binding and unverified live colour/link/status integrations remain specific independent issues. No new report, grade, packet, parent publication, deployment or full backlog completion is claimed by writing this skill.

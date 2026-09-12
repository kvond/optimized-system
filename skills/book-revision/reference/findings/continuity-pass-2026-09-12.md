# Continuity pass: AnswerableTeachingPrefaceCh5 (Working Copy), 2026-09-12

*Kept verbatim as the second source of the lane work items. It was run against the Doc before Katherine's edits later the same day (the Doc then had 58,500 words; the pass snapshot has 68,000, with a "Revised Taxonomy" section pasted after Chapter 2, the AI chapter relabeled [6A], and The Moves expanded into titled sections). Find strings were valid on the earlier text; the lanes re-verify each one against the current snapshot with `manuscript_check.py --find`. Its item labels (A1–A9, B, C, D, E1–E13, F, G, H) are the ones the lanes and the ledger cite.*

---

Run 2026-09-12 against the live Google Doc (title in Drive: "(4 and 5 next 6 , first 3 chapters feed website)AnswerableTeachingPrefaceCh5 (Working Copy)"). The document is 58,500 words: Preface, Introduction, Chapters 1–5, Chapter [A], Chapter [B], the "Teaching principles" table, Chapter [7], Chapters 8–10, and Chapter [11]. Nothing in the document was changed. This is manuscript-ops Job 1: a mechanical extraction (cross-references, tracked terms, pseudonyms, endnote markers, editorial residue, verbatim overlap between chapters) followed by a full read for the judgment calls.

How to use this: every item names the chapter and section it lives in and gives a Find string you can paste into Ctrl+F in the Doc. Findings are stated as observations. Anything that is a suggestion or a challenge to the argument is in [brackets], per the standing prose rule. Decisions are listed first, because most of the smaller fixes depend on them. Boxes are for ticking off.

A note on the method's limits. The manuscript-ops skill lists Abraham, Aliyah, and "double booking" as tracked terms; none of the three occurs anywhere in this document, so the skill's tracked-term list predates the public pseudonym set and should be refreshed (see the last section). The bundled check_consistency.py was not synced into this session; I rebuilt its extraction as a standard-library script and kept it with the report.

## A. Decisions only you can make

These are ordered by how much downstream text each one governs.

### A1. Chapter numbering in the middle of the book

The document carries at least three incompatible numbering plans for the chapters between Dialogic Teaching and Authorial Agency.

- [ ] Introduction says the AI material is Chapter 6. Find: `I'll get to that in Chapter 6`
- [ ] Chapter 5's last paragraph says the next chapter is the Variation Theory instruction chapter. Find: `The next is about the instruction: how Variation Theory works`
- [ ] The Chapter 5 【NOTE】 says Chapter 6 is the home for the Toxicofera example, but the Toxicofera writing scene is currently the opening of Chapter [A]. Find: `Ch6 is the natural home for Toxicofera` and `what they thought a lizard was doing with venom genes`
- [ ] Chapter [A] opens by saying the previous two chapters described the shared object and the dialogic stance, which assumes a Variation Theory chapter sits between Chapter 5 and Chapter [A]. Find: `The last two chapters described the shared object of attention`
- [ ] Chapter [7] opens by saying the previous chapter ended with a problem Variation Theory alone cannot solve, which assumes the Variation Theory chapter sits immediately before it (it does not; Chapter [B] and the principles table do). Find: `The last chapter ended with a problem Variation Theory alone can't solve`
- [ ] Chapter [11]'s pointers treat "Chapter 6" and "Chapter A" as two different chapters. Find: `[Chapter 6; Chapter A.]`
- [ ] The questions left at the end of Chapter [B] report that the Roam navigation has AI as Chapter 11 and Chapter 6 as "Intellectual Mentorship." Find: `CH 11 AI saving work lands more on teachers`
- [ ] Chapter 8 already treats Noelle's chapter as Chapter 7, and Chapter [7] already says Zara speaks "two chapters from now," which only works if Authorial is 8 and the building chapter is 9. Find: `Chapter 7 showed what democratic agency looks like` and `two chapters from now`
- [ ] "Chapter 11" is claimed by three different bodies of material: Nussbaum's capabilities (Chapter 3, twice: `I take this up in Chapter 11` and `Developed in Chapter 11`), Rogoff and Lave & Wenger in full (Chapter [7]: `Chapter 11 takes them up in full`), and the annotated moves list (the bracketed Chapter [11] heading). Chapter 10's close then points to a further chapter after the moves ("the one after names the apprenticeship"). Find: `The chapter that follows gathers the ways I have found to bring agency up`

Options:

1. AI folds into Chapter 6 with Variation Theory (Chapter 6 = the instruction chapter, with [A] and [B] as its second half). This matches the Introduction's pointer as written, keeps 7–10 as they are labeled, and makes Chapter [A] read as the continuation of the Variation Theory vocabulary it already depends on. Cost: Chapter 6 becomes long, and the Roam navigation's "CH 11 AI" would be retired. [Recommended: it is the plan that the most existing pointers already assume.]
2. Variation Theory = 6, AI = 7 (A and B merged), everything after shifts by one (Room 8, Authorial 9, Building 10, Holding 11, Moves 12, capstone 13). Cost: Chapter 8's "Chapter 7," Chapter [7]'s "two chapters from now," the Chapter 8 and Chapter 10 headings, and all "Chapter 11" claims move.
3. AI moves late, as the Roam navigation has it (after Holding the Tension, before the capstone). Cost: the Introduction's pointer changes, and Chapter [7]'s and Chapter 8's references to writing-during-the-lesson and the pipeline lose their earlier home.

Whichever you choose, the "Chapter 11" claimants (Nussbaum; Rogoff and Lave & Wenger; the moves) need one owner each; under option 1 the natural split is capabilities and apprenticeship in the capstone and the moves list in 11.

### A2. The greenhouse student has three names, and one of them is also your son's

- [ ] Chapter 2, Authorial agency: the greenhouse student is Peter. Find: `a student, Peter, expressed interest in using it` (also the takeaways table, `Peter's greenhouse`, and the Autonomy vs Agency section, `Peter as we will see is a positive example`)
- [ ] Chapter 8, The Marcus/Paul pair: the same student is Paul, and the text says his greenhouse work "appears later in the book," though it already appeared in Chapter 2. Find: `Paul, whose greenhouse work appears later in the book`
- [ ] Chapter 9, Eli's greenhouse: the same student is Eli, in a paragraph that repeats the Chapter 2 paragraph nearly word for word (see E6). Find: `until Eli expressed interest in using it`
- [ ] Chapter 9, The view from above: Peter is your son who transferred into middle school after homeschooling. Find: `When my son Peter transferred into middle school`
- [ ] The handoff note before Chapter 8 lists "Peter" and "Eli" as two different people that Chapter 9 owns, which is consistent with Peter = son and Eli = greenhouse student. Find: `Chapter 9 owns Zara, Peter`

[Recommendation: Eli for the greenhouse student everywhere (Chapter 9 carries the developed version and the "in Eli's terms, a greenhouse" callback), Peter stays the son, and Paul disappears. Chapter 2 then introduces Eli, Chapter 8's pair becomes Marcus/Eli, and Chapter 8's "appears later in the book" becomes a back-reference to Chapter 2.]

### A3. Marcus's scene is told in full twice

Chapter 3 (Traditional schooling) and Chapter 8 (Marcus — the limit case) each tell the whole scene: the question, "I don't care about biology," 4 a.m., stocks, ventures, "fierce drive for mastery," "By any psychological measure Marcus was motivated." The overlap detector found 32 shared eight-word runs between the two passages, the largest overlap in the document.

- [ ] Chapter 3. Find: `Marcus's story is one of the reasons I felt I needed to write this book`
- [ ] Chapter 8. Find: `Marcus is the reason I started suspecting the language of motivation`

[The provenance note says Chapter 8 "owns Marcus as limit case." If that stands, Chapter 3 keeps only what its argument needs (the administrator's "trying to save him," which is the policing point) and points forward; if Chapter 3 keeps the scene because it is the reader's first meeting with Marcus, Chapter 8 opens on the limit-case analysis and recalls the scene in a sentence. Either way, "a different Marcus came into view" should appear once.]

### A4. Authorial agency is defined inside school in Chapter 2 and outside the school frame in Chapter 8

- [ ] Chapter 2: "Authorial agency begins when learners create curricular purposes inside school," "I focus on authorial agency that occurs inside school though it isn't limited there," and "Authorial agency stands out in a school setting; outside one, it is ordinary. Almost everyone authors some portion of their life." Find: `create curricular purposes inside school`
- [ ] Chapter 8: authorial agency is "the capacity and the drive to set one's own learning path entirely ... outside the frame school provides," it "is rare," it "mostly cannot be cultivated from inside a classroom," and it is "the particular form some students, a minority in my experience, have already developed before they arrive." Find: `outside the frame school provides` and `Authorial agency of this kind is rare`

[These are two different concepts wearing one name: Chapter 2's is a form that schools should legitimize and credit (Eli, the greenhouse, the credit structure); Chapter 8's is a limit case that schools cannot host. Chapter 8's own "intellectual authorship" (the capacity underneath the four forms) may be the term that resolves it: ordinary authorship of meaning is the teachable capacity, and authorial agency in Chapter 8's sense is its rare outermost form. If so, Chapter 2's definition and the takeaways table need to say which one they mean, and "outside one, it is ordinary" needs to be reconciled with "rare."]

### A5. Identified regulation is mapped to two different forms

Identified regulation is Deci and Ryan's term for a student endorsing the value of an assigned activity without the activity being intrinsically motivating.

- [ ] Chapter 2, How focusing on motivation unseats knowers: identified regulation is pointed at effortful agency ("see valedictorian research under effortful agency below") and is contrasted with origination ("even genuine internalization is not the same thing as origination"). Find: `see valedictorian research under effortful agency below`
- [ ] Chapter 2, Engaged agency: "In its strictest sense it is Deci and Ryan's identified regulation." Find: `In its strictest sense it is Deci and Ryan's identified regulation`
- [ ] Chapter 8: identified regulation "still has a ceiling. It describes a student who has internalized someone else's goals." Find: `Identified regulation, the most sophisticated version of what schools mean by motivation`

[Engaged agency is defined by origination inside the frame; identified regulation is defined by endorsement of someone else's goal. The Engaged agency sentence equates the two, which undoes the distinction the chapter built earlier in the chapter. One of the three passages has to give.]

### A6. Perception versus response: the book states one position and argues the other in several places

Your stated position (Introduction, and the moves list) is that noticing is not the bottleneck; the response repertoire is.

- [ ] Introduction. Find: `Noticing has never been the bottleneck`
- [ ] Chapter [11], entry 2. Find: `perception is what teachers already have; the response is what they lack`

Passages that frame the taxonomy as a perception aid or make perception the skill the book develops:

- [ ] Chapter 2, after the table: "learn the patterns of agency that make these forms legible to the teacher." Find: `make these forms legible to the teacher`
- [ ] Chapter 2, How focusing on motivation: "vague language doesn't just obscure, it limits perception." Find: `it limits perception`
- [ ] Chapter 2, Genres of agency: "Being able to perceive the forms as they appear in student behaviors, discussions, or writing is what allows a teacher to take appropriate teaching action." Find: `Being able to perceive the forms as they appear`
- [ ] Chapter 4, bridge: "the teacher's perceptual skill, the dialogic orientation, and the curated object are portable conditions." Find: `the teacher's perceptual skill`
- [ ] Chapter [7], What changed first: "That is teacher perception in practice." Find: `That is teacher perception in practice`
- [ ] Chapter 10, A developmental account: "What teachers must learn to see ... That perceptual capacity is not innate. It is developed." Find: `That perceptual capacity is not innate`
- [ ] Chapter [11], opening: "reading the room for agency is a skill, and that it is the one this book is most centrally trying to develop." Find: `reading the room for agency is a skill`
- [ ] Chapter 9 【NOTE】 reports a capstone closing line, "The beginning of change is perception." Find: `The beginning of change is perception`
- [ ] The subtitle itself: Agency, Perception, and the Ethics of Teaching.

[Challenge: a reviewer who knows the teacher-noticing literature will read the Chapter 10 and Chapter [11] sentences as the perception claim the Introduction disowns, and will ask which book this is. The taxonomy can be defended as a map for building response moves (the Introduction's own line: "recognizing which form of agency is alive in a student at any given time and knowing what moves to take"), but then "perception" cannot be the named skill in Chapter 10 and the moves list, and the subtitle's middle term may need to be "response" or "answerability." The alternative is to keep perception and argue explicitly why noticing-research perception is not the perception you mean (channel, not acuity: entry 3's "diagnosis by channel, not by acuity" is already that argument, in one line). Either is defensible; holding both is not.]

### A7. "There is no hierarchy here" against the developmental account

- [ ] Chapter 2, after the table: "There is no hierarchy here." Find: `There is no hierarchy here`
- [ ] Introduction: "cultivate students' agency into increasingly powerful forms." Find: `increasingly powerful forms`
- [ ] Chapter 10: "the more developed forms — engaged, epistemic, democratic, authorial" and "Epistemic, democratic, and authorial agency mark progressively deeper engagements." Find: `the more developed forms` and `progressively deeper engagements`
- [ ] Chapter [7]: adjacent agency as "the zone of proximal development for being a knower" is a developmental ordering by construction.

[The two can coexist if "no hierarchy" is scoped: no hierarchy of worth or of persons (the taxonomy "never classifies the student"), but a developmental order of forms. Chapter 2 says the first half; Chapter 10 needs it to have said the second.]

### A8. Ben's counterfeit tickets: told in Chapter 2, requested as a gap in Chapter 8

- [ ] Chapter 2, Effortful agency, tells the scene (forged tickets funding scarves, jewelry, snacks) as an example of agency emerging in unsanctioned ways under a reward system. Find: `My son Ben and his friends in middle school grew tired`
- [ ] Chapter 8, Ben: "[GAP: the counterfeit-tickets scene ...]" asks for the scene as the authorial case. Find: `Ben is the case that shows authorial agency arising`

[Decide which chapter owns the scene. If Chapter 8 owns it, Chapter 2's effortful section keeps one sentence and a pointer; if Chapter 2 owns it, the Chapter 8 gap closes with a callback and the reclassification (from a reward-system workaround to authorial agency) is stated there, since Chapter 2 currently files Ben under effortful agency's section without naming his form.]

### A9. Lezir and the Toxicofera Tuesday: one moment or two

- [ ] Chapter 5 tells Lezir's real question with no day and no lesson named (the [GAP] asks for both). Find: `I'll call him Lezir`
- [ ] Chapter [A] opens on "a Tuesday in the evolution unit" with the venom-genes writing prompt and does not mention Lezir. Find: `On a Tuesday in the evolution unit`
- [ ] Chapter [B] opens as if the two are the same moment: "Lezir got several minutes that Tuesday." Find: `Lezir got several minutes that Tuesday`
- [ ] Chapter [11], entry 9, plans a "callback to the Toxicofera exchange" for Lezir. Find: `callback to the Toxicofera exchange`

[Chapter [B] has already decided this for you: it needs Lezir's question to be the Toxicofera question. If that is not what happened, Chapter [B]'s opening line has to change.]

## B. Cross-references and pointers to repair

Under this volume's order (cases → taxonomy → school models → manufacture → dialogic), these pointers resolve wrongly or point at something the target does not contain.

- [ ] Chapter 1, last line, points at Chapter 4's question, but Chapter 2 follows. Chapter 1 closes "What in the structure of schooling makes this kind of disconnection nearly inevitable rather than exceptional, especially in high-poverty schools?" That is the question Chapter 4 opens on (nearly verbatim: `What structural pressures in schools make this disconnection nearly inevitable`) and Chapter 3 closes on (`What comes next is the why`). The reader turns the page to the taxonomy. Find: `nearly inevitable rather than exceptional`
- [ ] Chapter 2 promises that Chapter 3 describes The Circle School "more fully"; Chapter 3 never names it. Chapter 3 discusses Sudbury Valley and "the Sudbury-model school I researched" without saying that this is TCS, so the reader cannot connect the two. Find: `The school's approach is described more fully in the next chapter` and `At the Sudbury-model school I researched`
- [ ] Chapter 3 says "We will later look at Patall's work," but Patall's caveat was already given in Chapter 2 (Engaged agency section) and is given again four paragraphs later in Chapter 3. Find: `We will later look at Patall's work`
- [ ] Chapter 3: "the one I opened this book with." The book opens with the Sunday scaries and Toma; Chapter 1 opens with Angie. Find: `the one I opened this book with`
- [ ] Chapter 4, bridge: "the forms of agency this chapter and Chapter 1 have been building toward." The forms were built in Chapter 2. Find: `this chapter and Chapter 1 have been building toward`
- [ ] Chapter 4, "More than one driver," announces five drivers and delivers three. The Carnegie Unit is never mentioned again in the chapter, and "the three competing aims of public education" are Labaree's, discussed in Chapter 3 and absent from Chapter 4's body. The lettered causes (a)–(e) the provenance note mentions were cut; this paragraph is the dangling referent the cut left. Find: `the Carnegie Unit and its downward pressure`
- [ ] Chapter 4, "The bridge to the next chapter," announces the next chapter three times. Find: `The next chapter is about the stance`, `It is the subject of the next chapter`, `Those questions are what the next chapter takes up`
- [ ] Chapter 8: "Paul, whose greenhouse work appears later in the book." It appeared in Chapter 2 (see A2). Find: `appears later in the book`
- [ ] Chapter 9: "Take the bathroom policy that opened this chapter." The chapter opened with Zara in the hallway; the bathroom policy enters in "The view from above." Find: `the bathroom policy that opened this chapter`
- [ ] Chapter 9: "the 'student voice' slogan I set aside in the Introduction." The Introduction lists "voice, choice, ownership" among the fixes the system invokes and discusses Cook-Sather's student voice in note 3; it does not set the slogan aside in the body. Find: `slogan I set aside in the Introduction`
- [ ] Chapter 10 twice cites "Chapter 2" for the school models. The models are Chapter 3 in this volume; the handoff note before Chapter 10 confirms the drafter was working from the old order. Find: `In Chapter 2 I argued that each school model holds one ethic` and `this is where Chapter 2 comes back around`
- [ ] Chapter [11], entry 2, cites "[Chapter 3.]" for the taxonomy and the practice gap. The taxonomy is Chapter 2; the practice gap is the Introduction. Find: `so that next time the name retrieves the response. [Chapter 3.]`
- [ ] Chapter [11] cites "Chapter 6" in entries 5, 6, 9, 11, and 12 for the fiddle sim, the student moves, and the Toxicofera exchange; no Chapter 6 exists in this document, and the Toxicofera scene is in Chapter [A] (see A1, A9).
- [ ] Chapter [11], opening: "I have said from the introduction that reading the room for agency is a skill, and that it is the one this book is most centrally trying to develop." The Introduction says the opposite (see A6). Find: `I have said from the introduction`
- [ ] Chapter [11], entry 1, misremembers John's question. The entry says the institution saw "a good teacher asking a genuinely open question, 'What have we got here?'"; in Chapter 1 John asked "Where is the remainder?", which presupposes his frame and is the point of the scene. Find: `What have we got here`
- [ ] Introduction, note 2: "her repertoire takes up wrong-but-coherent reasoning." "Her" is Lampert, but the sentence has just named Nancy, so it reads as Nancy's repertoire. Find: `her repertoire takes up wrong-but-coherent reasoning`

Pointers that resolve correctly and can be left alone: Introduction → Chapter 2 (taxonomy); Chapter 1 → Chapter 2 and → Chapter 5 (dialogic lens); Chapter 2 → next chapter (school models); Chapter 3 → Chapter 2 (authorial defined); Chapter 4 → Chapter 2 (taxonomy, phases); Chapter 5 → Chapter 2 (effortful, Ito's clock); Chapter [B] → last chapter ([A]); Chapter [7] → equity chapter; Chapter 8 → Chapter 7 (Noelle) and → Chapter 9 (Zara); Chapter 9 → Chapter 7 (Dewey); Chapter [11] → Chapters 1, 5, 7, 9, 10.

## C. Vignette and pseudonym continuity

- [ ] Marcus is used as an exemplar four times in Chapter 2 before the reader meets him in Chapter 3. "students like Marcus, whose learning was obvious everywhere except inside school"; the map entry that ends "Marcus."; "Marcus sometimes slipped into pseudo-agency"; and the takeaways table's "Marcus's 4 a.m. life," which the reader has not yet been shown. Find: `students like Marcus` [One introducing clause at the first mention, or a pointer to Chapter 3, is enough.]
- [ ] Nancy becomes Katherine's own student in the AI chapters. Chapter [A], The order of materials: "I had been supporting epistemic exploration by instinct rather than by design; with Nancy it was accidental." Chapter [B], Security enough to tolerate emergence: "When Nancy says something that doesn't fit the anticipated trajectory, I have enough cognitive room to hear it." Nancy was John's fourth-grader in a research classroom. Find: `with Nancy it was accidental` and `When Nancy says something`
- [ ] Nancy's arrangement is recharacterized in Chapter [A]. Everywhere else her flower is aesthetic/geometric (balance instead of a count); in Chapter [A] it "turned into a comparison between a math problem with a social context and one without," which is the classmates' fairness reframing from Chapter 1, not Nancy's. Find: `a math problem with a social context and one without`
- [ ] The classmates' fairness questions are a "paradigmatic difference" in Chapter 1 and sense-making (inside the frame) in Chapters 3 and 5. Chapter 1: "Nancy was not the only student with a paradigmatic difference with John's intention." Chapters 3 and 5: the classmates "were sense-making"; Nancy "had crossed into meaning-making." Find: `paradigmatic difference` [If the social questions were inside John's frame, Chapter 1's "paradigmatic difference" overstates them; if they were a reframe, they were epistemic bids too and Chapters 3 and 5 understate them.]
- [ ] The Circle School versus "the Sudbury-model school I researched" versus "The Socratic School." Chapter 2 names TCS; Chapter 3 never names it but describes middle schoolers leaving for a year and returning (Chapter 8 tells the same fact about Cindy at TCS, so they are the same school); Chapter 10 introduces "The Socratic School" as a different research site with staff-led parlor talks. Chapter 3 attributes the "absurdist" relabeling of students' ideas to "the Sudbury staff"; Chapter 10 attributes the symphonic/absurdist framing to the Socratic School's parlor talks. Find: `were relabeled` and `The Socratic School held parlor talks` [Verify against the dissertation which site used "absurdist"; a Sudbury-model staff that holds that "staff have no duty to teach" is an odd host for staff-led parlor talks.]
- [ ] "now approaching its fourth decade." The Circle School dates from 1984, which puts it in its fifth decade in 2026 [verify the founding year against the school's own history]. Find: `approaching its fourth decade`
- [ ] Ben appears in four chapters; the characterizations are consistent, the ownership is not (see A8). Chapter 2 (tickets, under Effortful agency), Chapter 4 ("They're spoken at. But they're not spoken to."), Chapter 5 (landforms), Chapter 8 (authorial, with the tickets as a gap).
- [ ] Two sons transfer into public middle school after homeschooling, in different chapters. Chapter 4: "My son Ben entered public middle school after years of homeschooling." Chapter 9: "When my son Peter transferred into middle school after years of homeschooling." Both can be true; a reader will wonder whether they are the same boy. Find: `entered public middle school after years of homeschooling`
- [ ] Zara / Kalima. "Kalima" now survives only in two notes (the principles-table handoff and a Chapter [7] 【NOTE】); the body uses Zara throughout. Confirm and delete the notes. Find: `Kalima`
- [ ] Frieda / Freida. Spelled both ways in Chapter [11] (entry 8 and the closing note). Find: `Frieda` and `Freida`
- [ ] "The wrestler who says he doesn't care" (Chapter 10, What schools are trained to see). No wrestler appears anywhere in the document. Find: `The wrestler`
- [ ] "What the skull station is" (Chapter [B], Pedagogy mitigates structural problems). The skull station is never described in this document; it belongs to the missing Chapter 6. Find: `the skull station`
- [ ] Lezir's scene has no day in Chapter 5 and is "that Tuesday" in Chapter [B] (see A9).
- [ ] Mekhi and Maya are gone (zero occurrences), as the provenance note intended. Malik and Nancy are consistent across chapters.
- [ ] Heidi, Priya, Toma, Mike, Gustov, Karen, Dana, Cindy, Noelle, Brian: consistent wherever they appear.

## D. Coined terms and definitions (canonical-home check)

"Canonical home" is the convention in your working notes that each theoretical claim or coined term has one chapter location, with pointer sentences elsewhere rather than repeated definitions.

- [ ] Agency is defined five times, and the definitions disagree about their own components. Preface and Chapter 2 epigraph: capabilities + decision-making + origination + answerability. Chapter 2, first section: "origination and answerability on an object of knowing." Chapter 2, same section: "Decision-making and capability drop out of this definition." Chapter 2, How focusing on motivation: "I reach for the concept of agency, with its aspects of origination, decision-making, capabilities, and answerability. Agency ... is a developing capacity to act, with meaning and effect" (the two dropped aspects are back, and the definition is now a capacity rather than a move). Chapter 2, Genres of agency: "each exhibits one or more aspects of origination, decision-making, capabilities, and answerability." Chapter 8: "Agency is the developing capacity to act meaningfully and effectively in one's context." Find: `Decision-making and capability drop out of this definition` [One definition in Chapter 2, then pointers. The "drop out" sentence and the four-aspect sentences cannot both stand.]
- [ ] Sense-making versus meaning-making is defined in four places: Chapter 1 in passing (`This opens the door for meaning-making`), Chapter 2 endnote 3, Chapter 3 body (`What Dewey saw is that students need the opportunity for sense-making`), Chapter 5 body (`Sense-making is the learner trying to orient within a phenomenon`). The Nancy-versus-classmates illustration is run twice, in Chapter 3 and Chapter 5, in nearly the same words (see E12).
- [ ] Legibility is defined three times and used outside Scott's sense five times. Definitions: Chapter 2 (`This is what I mean by institutional legibility`), Chapter 3 (`what Scott (1998) called legibility`, with note 1), Chapter 4 (`make populations governable`, with note 2, and with the author named twice in one sentence). Uses that mean "readable by a person" rather than Scott's institutional sense: Chapter 1 `illegible to her teacher`; Chapter 2 `make these forms legible to the teacher`; Chapter [A] `the contest is legible because the material had an opinion` and `A paragraph produced by a chatbot is legible in a particular way`; Chapter 8 note 1 `which forms of participation are legible`. [Your own rule: legibility only in Scott's sense; elsewhere surface, bury, read, go dark.]
- [ ] Time-world / chronotope is introduced three times. The Introduction introduces chronotope in the body as the book's term; Chapter 2 endnote 2 then presents "time-world" as the lay term and chronotope as optional ("for readers who want a technical term"); Chapter 8 endnote 1 introduces it again. Find: `Bakhtin had a word for these factors: chronotope`, `2. Time-world / chronotope`, `Time-world here is Bakhtin's chronotope`
- [ ] Ito's phases are named "lurking, playing, and geeking out" once (Chapter 2, The Map) and "lurking, messing around, geeking out" everywhere else, including endnote 5, which explains the renaming of only the first phase. Find: `lurking, playing, and geeking out`
- [ ] "Ito's 'agency genres,' as she calls them." Ito and colleagues call them genres of participation (friendship-driven and interest-driven, with hanging out, messing around, and geeking out as modes). "Genres of agency" is your term; the sentence gives it to her. Find: `Ito's "agency genres," as she calls them`
- [ ] "Internally persuasive dialogue" throughout Chapter 5 where Bakhtin's term, and Matusov and von Duyke's (2010) subject, is internally persuasive discourse. Six occurrences, none of "discourse." Find: `Internally persuasive dialogue is the difference between`
- [ ] Effortful agency: "coined" by Matusov, von Duyke, and Kayumova (Chapter 2) and "my own term" (Chapter 3 endnote 4). The Chapter 3 note is also anchored to the wrong sentence (the meaning-making sentence, not an effortful-agency sentence). Find: `"Effortful agency" is my own term`
- [ ] Zombification. The body says Llewellyn's zombies are hers and the zombification is yours; endnote 4 credits "Zombification" to Llewellyn and says "agency sickness" was "first described in Llewellyn's The Teenage Liberation Handbook." "Agency sickness" appears nowhere else, and the three-way split that follows (all dead = disengagement, mostly dead = agency sickness, functionally dead = pseudo-agency) does not map onto the three shadow forms (dysfunctional, pseudo, effortful). Find: `mostly dead (agency sickness)`
- [ ] The Dysfunctional agency heading promises "protective and hostile forms"; the body names "disengaged" and "more hostile actions." Protective is never defined. Find: `Dysfunctional agency: protective and hostile forms`
- [ ] The Chapter 2 table has five rows for a seven-form taxonomy (dysfunctional and pseudo-agency are absent), while the text below says seven genres. Find: `The table below organizes the ways I have watched learning show up` [If the table is deliberately "the ways learning shows up," say so in the lead-in; otherwise add the two rows.]
- [ ] Democratic agency is listed among the forms in which "students are regulating themselves within structures largely framed by adults" (Chapter 2, Authorial agency), two paragraphs after it was defined as shared authorship of the rules. Find: `regulating themselves within structures largely framed by adults`
- [ ] Matusov is quoted two ways on the same point. Chapter 2: "Some critics, like Matusov, describe the larger educational arrangement as 'benevolent control'" (no year). Chapter 8: "Teachers in practice function as benevolent dictators, always pushing classroom goals (Matusov, 2021)." Find: `benevolent control` and `benevolent dictators`
- [ ] The missing ingredient has five names. Intellectual mentorship (Preface; Chapter 4, "what I call intellectual mentorship"), intellectual apprenticeship (Chapters 3, 4, 5, and 7), apprenticeship in learning (Chapter 4, three times), dialogue partner (Chapter 4, where the text itself says the names "all name one thing"), and guided participation (Rogoff's term, Chapter 4). Chapter 8 then adds intellectual authorship for the capacity the apprenticeship builds. Find: `all name one thing` [Pick the canonical term and gloss the others as synonyms once; a reader cannot tell whether these are one thing or five.]
- [ ] Three Variation Theory terms are used before they are defined: critical aspects (Chapter 4, `the dialogue that targets the critical aspects`; defined in Chapter [A]), shared object (Chapter 4, `He saw there was no shared object`), and whole-and-part work (Chapter [A], `needs more whole-and-part work`, never defined). Under option 1 in A1 these all precede Chapter 6.
- [ ] Blumenthal's question is asked twice in Chapter 2, with attribution in the Effortful section and without it in the Authorial section, word for word. Find: `when do they get to define themselves through learning`
- [ ] "fit meaning rather than make it" appears in Chapter 1, Chapter 2, and Chapter 8, and only the third instance attributes it (Biesta, 2006). Find: `fit meaning rather than make it`
- [ ] The Chapter 4 epigraph is repeated in the body. "The person carrying the blame is carrying the structure's debt" is the epigraph and closes the Mills paragraph; the voice guide records your ruling that it stays once. Find: `carrying the structure's debt`
- [ ] The Preface contains a paragraph in the third person ("Katherine von Duyke offers a taxonomy of agency and a new ethic of teaching"), which reads as catalog copy pasted into a first-person preface. Find: `Katherine von Duyke offers a taxonomy`

## E. Passages that appear nearly verbatim in two chapters

From the twelve-word and eight-word overlap passes. Some repetition is deliberate return; each pair is listed so you can decide which.

- [ ] E1. Marcus's scene, Chapter 3 ↔ Chapter 8 (see A3).
- [ ] E2. The walkthrough administrators, Introduction ↔ Chapter 4, In my classroom. Twenty-seven shared eight-word runs; the Introduction version is a near copy of the Chapter 4 paragraph ("They'll note whether I'm on pace, but they won't ask what I'm seeing in students' thinking"). Find: `When district administrators come through`
- [ ] E3. Malik's energy-pyramid cards, Chapter 2 ↔ Chapter [A], Match the grade of control. Chapter [A] re-narrates "he reworked the arrangement twice until I said it was complete." Find: `reworked the arrangement twice`
- [ ] E4. "Demanding visible participation before students have had time to lurk", Chapter 4, How engagement unfolds ↔ Chapter [7], What a shared object can't supply. Find: `before students have had time to lurk`
- [ ] E5. The three-form recap sentence, Chapter [7], Democratic agency ↔ Chapter 8, Authorial agency ("Engaged agency is the student's effort to understand from her own position. Epistemic agency is a bid to reshape the frame"). Find: `bid to reshape the frame`
- [ ] E6. The greenhouse paragraph, Chapter 2 ↔ Chapter 9 (see A2). Find: `long forgotten`
- [ ] E7. The motivation / self-directed / identified-regulation passage, Chapter 2, How focusing on motivation ↔ Chapter 8, What the most sophisticated motivation theory. "Motivated to comply, or to create?"; "if a student buys in, we call it a win"; "Students solve problems; they don't pose them." Find: `Motivated to comply, or to create`
- [ ] E8. "When a student's agency doesn't fit the time-world of school, it becomes ... invisible to teachers, uncountable by the system", Chapter 2 ↔ Chapter 8. Find: `uncountable by the system`
- [ ] E9. Agency practiced elsewhere ("in work, sports, caregiving, or creative pursuits"), Chapter 2 ↔ Chapter 8, including "schools can recruit it or punish it." Find: `caregiving, or creative pursuits`
- [ ] E10. "When schools evaluate students primarily through ... they measure the fluency students bring with them" and "A more honest aim asks not whether students can perform", Chapter 4 ↔ Chapter 9, Marcus, finally. Find: `fluency` and `A more honest`
- [ ] E11. The three models each misread early engagement, told three times: Chapter 2, "2 · The three models each misread early engagement"; Chapter 2, "School models misread lurking and messing around"; Chapter 4, "How engagement unfolds, revisited." The provenance note says the Chapter 4 duplicate was compressed to its equity content; the paragraph that begins `Each school model, when engagement breaks down, reaches for its signature tool` is still the full recap.
- [ ] E12. Nancy's classmates were sense-making; Nancy had crossed into meaning-making, Chapter 3 ↔ Chapter 5. Find: `who gets the extra penny`
- [ ] E13. The structural question, Chapter 1 close ↔ Chapter 3 close ↔ Chapter 4 open (see B, first item).

## F. Editorial residue still inside the document

None of this is prose; all of it would be seen by anyone the link is shared with. Listed in document order.

- [ ] Chapter 2, endnote 1: `[  edition/wording.]` placeholder on the "no alibi in Being" citation (the provenance note flags this as awaiting verification).
- [ ] Chapter 2, Paley note: a stray closing quotation mark after "within it."
- [ ] Chapter 3, endnote 2: an aside to the editor, `can be added if the historical claim needs support`.
- [ ] Chapter 3, endnote 7: `[verify translation/edition]` on Kant.
- [ ] Chapter 4: `(Mississippi NAEP reading gains; 2013 literacy legislation)` and `see the research list in the back matter` stand in for citations.
- [ ] Chapter 4: `[cite: Beechick]`.
- [ ] Chapter 4: `[PLACEHOLDER: an example or two of high-poverty families or communities that apprentice their children well — yours to supply.]`
- [ ] Chapter 4, after the bridge: `Endnote fixes still to make in the Working Copy` names two fixes that have not been made: note 3 still ends "no hidden designer is required," and note 4 still refers to the cut item "(c)" and is anchored nowhere in the body.
- [ ] Chapter 4: `Working literature list` with empty year slots for Golann, Martínez & Golann, Demers et al., Meier, and Beechick.
- [ ] Between Chapter 4 and Chapter 5: `Replaces Chapter 5 in the Working Copy. Your 【NOTE】 and [GAP] slots are untouched.`
- [ ] Chapter 5: `【NOTE — DECIDE: The Lezir thread ...】` and `[GAP: the specific question`
- [ ] Chapter 5, endnotes 2, 4, 5: three bracketed edition/page slots (Find: `edition/wording` and `confirm pages`); then `For 6` and the "Discrimination edges" paragraph carried over for a Chapter 6; then `Change notes.`; then `Two chapters drafted from your notes. Chapter numbers are placeholders.`
- [ ] Chapter [A]: five [GAP] slots (Find: `[GAP:`) (the tank-and-fill sim as built; the vocabulary-in-their-own-words page; one copying incident; one first-tier/second-tier pair; one growth-report example).
- [ ] Chapter [B]: `Questions for you.` (five numbered questions, including the Coursemojo naming question and the chapter-number question).
- [ ] Teaching principles table: the placement suggestion above it, `Two rows are yours to confirm` below it, and `Drafted from your field notes, the jobs notes, the Roam Chapter 6 draft, and the older Noelle/Kalima draft.`
- [ ] Chapter [7]: `[GAP: three or four of the actual responsibilities`, `[GAP: one job's training`, `[GAP: what shows up on the board`, and four 【NOTE — FIX】 items (Patall 2024; Seed A and Zara/Kalima; Seed B; Sierens); then `Questions for you.` (four questions); then the Chapters 8 and 9 handoff paragraph.
- [ ] Chapter 8: `【NOTE — DECIDE: Whether to apply the Ch8/Ch9 split】`, `[GAP: the counterfeit-tickets scene`, `【NOTE — FIX: Seed F】`, `【NOTE — FIX: Seeds D and E】`.
- [ ] Chapter 9: `[ADMIN FEAR SENTENCE SLOT`, `【NOTE — FIX: Seed G ... VERIFY the "(Patall, 2024)" citation】`, `【NOTE — VERIFY: Big Picture Learning / Mastery Transcript Consortium URLs; Lewin ...】`, `【NOTE — DECIDE: Keep "Marcus, finally"】`, `【NOTE — DECIDE: The closing line ... also appears in the capstone】`, then the Chapter 10 handoff paragraph.
- [ ] Chapter 10: `【NOTE — WRITE: Opening vignette】`, `【NOTE — VERIFY: The Bhaer and Tom quotes against the dissertation】`, `【NOTE — DECIDE: The "Reading the Room" skeleton】`.
- [ ] Chapter [11]: five [PLACEHOLDER] slots (Find: `[PLACEHOLDER:`) (Malik callback; a bid scene; the Frieda scene; the Toxicofera callback; the town-hall scene) and the closing `Four things this list can't decide for you` paragraph.

## G. Note apparatus and headings (mechanical)

- [ ] Three note-numbering conventions coexist. Superscript markers (Preface, Chapter 1); bracketed numbers (Introduction, Chapters 3, 4, 5); plain numerals in the notes with bracketed markers in the body (Chapter 2). Chapters [A], [B], [7], 9, 10, and [11] have no notes at all (Chapter 8 has one). Heading names also vary: "Preface note," "Endnotes — Introduction," "Notes — Chapter 1," "Endnotes — Chapter 2." [One convention for the whole volume.]
- [ ] Chapter 1 markers appear out of order: 1, 2, 2b, 5, 6, 3, 4. Find: `epistemic gaslighting.⁵`
- [ ] Chapter 3 markers appear out of order and one is reused: 1, 2, 3, 6, 7, 5, 8, 4, 15, 9, 10, 11, 12, 13, 14, 15. Marker [15] is used twice (after the Zhao paragraph and after "produced by a missing support?"); marker [4] sits on the meaning-making sentence but is the effortful-agency note. Find: `is not by itself the cure` and `produced by a missing support`
- [ ] Chapter 4 markers: 1, 2, 5, 3, 6; note [4] is never anchored (see F).
- [ ] Chapter 2 has four unnumbered notes after note 8 (the Paley asterisk note; "Extrinsic rewards"; "Effortful agency"; "Honesty footnote"), and the asterisk marker in the body (`play boss (Paley, 1992)`) is the only asterisk note in the book.
- [ ] Three chapter titles are bold paragraphs rather than headings, so they do not appear in the Doc outline: Chapter [B], Chapter 9, Chapter [11]. Find: `Chapter [B] — What AI Cannot Do`
- [ ] Citations missing a year: `(cf. Corsaro; Lave & Wenger; Holland)`, `(c.f. Marjanovic-Shane, Meacham)` (also "c.f." for "cf."), `(Peter Gray)`, `(cf. Lave and Wenger)`, `(Skiba et al.)`, `Greenberg, 1985` (in text, absent from the Chapter 3 notes), `Meier (1995)` and `Beechick` in the working list. `(Hargadon, 2021.)` has the period inside the parentheses.
- [ ] Agreement slips the voice guide already lists as fix-directly: `shadow forms are manufactured and reinforced by the system and surfaces in the student`; `Even KIPP find they need`; `What structural pressures in schools make this disconnection nearly inevitable rather than exceptional, and is especially prevalent`; `the Suzuki method I used when I  taught my children violin with`; `simplifying them into countable forms` (James Scott named, then cited as Scott, in one sentence); `Mills called this; turning public issues into private troubles` (semicolon for colon); `another form of pedagogy deemed successful`; `Think of Angie, Nancy, and Heidi, all three had something to bring` (comma splice).

## H. Attributions to verify before a scholarly reviewer does

The voice guide asks for this on every pass. Each line says what the text claims and what to check.

- [ ] Ito's "agency genres" (Chapter 2): Ito et al. use "genres of participation." See D.
- [ ] "Marton's line ... we make meaning when we perceive a difference that makes a difference" (Chapter [A], Critical aspects). The phrase is Bateson's (as your own Chapter 5 note 5 says); check whether Marton uses it or whether the sentence should credit both. Find: `Marton's line is the one I keep returning to`
- [ ] Patall (2024) is cited three times (Chapter 2: "offers a detailed account of engaged agency"; Chapter 4 note 6; Chapter 9: the control-belief finding), with a standing VERIFY note in Chapter [7] and Chapter 9. Chapter 2 also attributes "engaged agency" to Patall's account; her construct is agentic engagement / autonomy support. Find: `Patall (2024) offers a detailed account of engaged agency`
- [ ] Patall, Cooper, and Wynn (2010) is cited for choice benefits being conditional on felt competence (Chapter 4, Autonomy without footing). Confirm the competence moderation is in the 2010 classroom study rather than the 2008 meta-analysis. Find: `Patall, Cooper, and Wynn (2010) found`
- [ ] Patall, Kennedy, et al. (2022) is cited for the loop emerging "primarily for high-achieving students" and failing for students "most exposed to stereotype threat" (Chapter [7], Patall's complication). Confirm both moderators are in that paper. Find: `disproportionately the students most exposed to stereotype threat`
- [ ] Patall et al. (2022) is cited for free-lunch students perceiving teachers as more controlling (Chapter 4). Confirm which 2022 paper, since the 【NOTE】 asks to keep Kennedy et al. and Zambrano et al. distinct. Find: `perceived their teachers as less supportive of their autonomy`
- [ ] Mortimer and Scott (2003) are described as carrying Bakhtin's contrast "as two communicative approaches, authoritative and dialogic." Their scheme has two dimensions (interactive/non-interactive and dialogic/authoritative), giving four classes; "two" narrows it. Find: `two communicative approaches`
- [ ] Moore-Anderson's "dances the tension" and the conversation-theory summary (Chapter 5). The book has no year anywhere (the Change notes say so). Find: `dances the tension`
- [ ] Matusov's "benevolent control" / "benevolent dictators (Matusov, 2021)" (see D). Find: `benevolent`
- [ ] Llewellyn's "zombies" and "agency sickness" (Chapter 2, endnote 4). Find: `first described in Llewellyn's`
- [ ] Miracle Max. The film line is "mostly dead is slightly alive" / "there's a big difference between mostly dead and all dead." The quoted "Mostly dead, but not all dead" is not in the film as such. Find: `Mostly dead, but not all dead`
- [ ] Greenberg (1985), "turn-off to curiosity" (Chapter 3). No note entry; confirm the source (The Sudbury Valley School Experience, 1985, or Free at Last, 1987). Find: `turn-off to curiosity`
- [ ] "The free-school wave of the 1960s and 70s, catalyzed by John Holt's Growing Without Schooling newsletter." GWS began in 1977 and catalyzed homeschooling; the free-school wave predates it (Holt's How Children Fail, 1964, is the earlier influence). Find: `catalyzed by John Holt's`
- [ ] The Circle School's age (see C).
- [ ] "The Germantown study." Neuman and Celano's two Philadelphia neighborhoods were Chestnut Hill and the Badlands (Kensington). If "Germantown" is your label for a reason, say so at first use; if it is a memory slip, the name recurs eleven times. Find: `which I will refer to as the Germantown study`
- [ ] Labaree's third goal. The text says social mobility "echoes the Enlightenment aspiration of rational, autonomous, self-actualized adults." Labaree's social mobility goal is the credentialing, consumer goal; the Enlightenment aspiration maps to democratic equality. [Challenge: a Labaree reader will stop here.] Find: `The third goal echoes the Enlightenment aspiration`
- [ ] Lewin, Lippitt, and White (1939): "destroyed property" when the adult left. Confirm the detail against the paper (the recorded behaviors were aggression, scapegoating, and work stoppage). Find: `destroyed property`
- [ ] Habermas's "concentric circles of participation" (Chapter 9). Not a standard Habermas image; confirm or reattribute. Find: `concentric circles of participation`
- [ ] The Oregon Trail anecdote ("Two education professors once observed a nine-year-old boy") has no source. Find: `Two education professors once observed`
- [ ] The museum heart-exhibit study (father and daughter; retention ten years later) has no source. Find: `In museum education, researchers followed a father and daughter`
- [ ] Bakhtin, "no alibi in Being" (Chapter 2 note 1): still awaiting edition and wording.
- [ ] Bhaer and Tom quotations (Chapter 10): the 【NOTE】 asks to check them against the dissertation.
- [ ] Berlin, Sen, Arendt (Chapter 10, Designing for tension) are invoked without citations; fine for a synthesis paragraph if the notes carry them.

## I. Appendix: voice-guide counts per chapter (mechanical only)

Extraction only, no judgment applied; the voice guide's ceilings are about 3–4 em dashes per 1,000 words, no enumerator openers ("First, / Second,"), and none of the hard-ban lexemes. Chapters [A] and [B], the principles table, and Chapter [11] are [C]-provenance drafts.

| Chapter | Words | Em dashes | per 1,000 | Ban-list hits | "First," openers | "meaningful" |
|---|---|---|---|---|---|---|
| Preface | 863 | 10 | 11.6 | 0 | 0 | 0 |
| Introduction | 2,532 | 26 | 10.3 | 1 | 0 | 1 |
| Chapter 1 | 2,793 | 21 | 7.5 | 0 | 0 | 0 |
| Chapter 2 | 9,826 | 15 | 1.5 | 3 | 0 | 0 |
| Chapter 3 | 4,719 | 17 | 3.6 | 0 | 0 | 0 |
| Chapter 4 | 7,224 | 38 | 5.3 | 1 | 0 | 0 |
| Chapter 5 | 5,472 | 21 | 3.8 | 0 | 0 | 0 |
| Chapter [A] | 3,572 | 1 | 0.3 | 0 | 0 | 0 |
| Chapter [B] | 2,630 | 3 | 1.1 | 0 | 3 | 0 |
| Principles table | 1,446 | 0 | 0.0 | 0 | 0 | 0 |
| Chapter [7] | 5,419 | 37 | 6.8 | 0 | 0 | 0 |
| Chapter 8 | 3,102 | 22 | 7.1 | 1 | 2 | 2 |
| Chapter 9 | 4,281 | 14 | 3.3 | 2 | 0 | 1 |
| Chapter 10 | 2,809 | 13 | 4.6 | 1 | 0 | 5 |
| Chapter [11] | 1,723 | 15 | 8.7 | 1 | 0 | 0 |

The Preface and Introduction are the densest in em dashes, which the provenance note says were mechanically copyedited only; Chapter [B]'s three enumerator openers are in "Three cautions."

## J. What this pass did not do, and where the findings can go

No sentence in the Doc was changed. The Doc is the downstream reading copy; Roam is canonical, so every fix above is a Roam edit first and a Doc edit second (or a Doc edit reconciled back).

Citation integrity (Job 3) was not run; there is no sources manifest in this document, and the References page it keeps pointing to does not exist here.

The manuscript-ops skill's tracked-term list (Abraham, Aliyah, double booking) is stale; a refreshed list for the public set would be: Angie, Nancy, John, Toma, Heidi, Marcus, Priya, Malik, Ben, Brian, Peter (son), Eli, Zara, Noelle, Gustov, Lezir, Karen, Dana, Cindy, Mike; and the terms legibility, sense-making/meaning-making, time-world, adjacent agency, intellectual authorship, dialogue partner, critical aspect, shared object.

Routes for the findings, so nothing has to be shuttled by hand: a Roam handoff file (roam_bulk_ops.py format) that files each A–E item as a block under the chapter page it concerns, tagged for the next writing session; Google Doc comments anchored on each Find string, so the items sit beside the text in the Working Copy; a copy of this report in the "Book" Project on claude.ai, so the next session starts from it.

# Feedback Pipeline: retired 2026-10-15

Katherine, Slack #feedback-pipeline, 2026-10-15: the Feedback Pipeline (Workflows A, B, B1, B2)
"has been replaced with the python code and prompts on the agenda".

Replacement: Master Agenda `Agenda 26-27 CLEAN`, tab **Feedback Prompts** (Prompt 00 Embed
Codes, Prompt 1 Completion, Prompt 2 Feedback, Prompt 3 Class summary), with
`scripts/embed_markers.py`, `scripts/mark_slides_api.py` and the Teaching Hub.

Moved here unchanged (history is also in Git):
- `extract_and_grade_rewrites.py`: B1 rewrite scoring, replaced by Prompt 1/2.
- `workflow_b_lint.py`: pre-draft lint for Workflow B emails. Its exact-quote check is worth
  porting as a test on Prompt 2 output.
- `pipeline_lint.py`, `pipeline_invariants.json`: a drift check across retired Drive copies.
  The idea (Agenda prompt cells, Manual §12 and the Prompt Library must agree) is worth porting.
- `skills-formative-pipeline-v2/`: the old pipeline skill.

Still in `scripts/` on purpose: `extract_and_grade.py` is outside this retirement list and remains
unchanged. `deck_lint.py` owns its exclusion tuples independently; there is no synchronization
requirement between the two files.

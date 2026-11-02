# Check and deliver

Read `../SKILL.md` first; its mandatory boundaries still govern. Path bases do not change when detail moves here: own `scripts/` and `reference/` paths are relative to the original skill root; named sibling-skill paths such as `book-revision/scripts/` are relative to the shared `skills/` directory. Manuscript `revision/` and `book-compile/` paths belong to the designated private manuscript repository; data and derived artifacts belong only in authorized private staging. Never interpret them as paths inside this reference directory or publish private artifacts to the public skills repository. These extracted instructions preserve existing rules; they grant no new authority.

## Job 1 — consistency pass (on-demand, e.g. pre-submission)

`python3 scripts/check_consistency.py --in writing/ --out consistency_report.md`

Then read the report and flag the judgment calls: does each cross-reference's claim actually
live where it points; is "double booking" used consistently with its definition; are the
anchor students characterized consistently. Surface findings for the user; never edit the
manuscript — propose changes against the current Doc with exact locations. For a full pass
over the current draft, use the revision skills instead: `book-revision` and its lanes.

## Job 3 — citation integrity (on-demand)

`check_citations.py` is planned, not implemented. Report that limit rather than claiming
the command ran. Use an authorized current source manifest to identify actual citation gaps;
do not invent references or silently normalize uncertain author/year matches.

## Job 4 — deliverables (on-demand)

Use the docx skill to compile `writing/` into a formatted .docx — full manuscript or
per-chapter — with table of contents and front matter, in the editor's required manuscript
format. The format is set once; this is a transform, not a judgment. Compile with
`SKIP_PROVENANCE=1` (or leave `provenance.md` out): no provenance note goes in front of the
manuscript.

# Reference-page migration — restore record (2026-06-26)

Purpose: rollback point for the compact-[[Author, Year]] migration of the Patall (2022) and
Matusov (2011) reference pages. Created because the git source/ snapshot was uncommitted at
migration time (sandbox mount is delete-blocked). To reverse: repoint each block's link TARGET
back to the original full-citation page title shown below, restore the verbatim original string
for the display-changed blocks, and delete the new canonical pages + stubs.

## New canonical pages created
- `[[Patall et al., 2022]]`  (corrected vol 71, 102097 — was 70/102085 on the old page)
- `[[Matusov, 2011]]`

## Old pages being stubbed (titles = restore identifiers)
- Patall full-citation page uid `eH-b0q-WF`: "Patall, E. A., Kennedy, A. A. U., Yates, N., Zambrano, J., Lee, D., & Vite, A. (2022). The relations between urban high school science students' agentic mindset, agentic engagement, and perceived teacher autonomy support and control. Contemporary Educational Psychology, 70, 102085."
- Matusov dup uid `KMcEtA5wW` (smart-quote, underscored)
- Matusov dup uid `DYt4V5mA6` (straight-quote, underscored)
- Matusov dup uid `JTz-OX7__` (no-underscore) — LEFT AS-IS (referenced by a do-not-edit provenance block)

## Patall backlinks (8) — original strings (TARGET → [[Patall et al., 2022]])

[Ch 7 — target-only, display unchanged] WqDvTA-1f
"Patall and colleagues found, in studies of urban high school science students, that the adaptive relationships between agentic mindset and engagement emerged primarily for high-achieving students [(Patall et al., 2022)]([[Patall, E. A., Kennedy, A. A. U., Yates, N., Zambrano, J., Lee, D., & Vite, A. (2022). The relations between urban high school science students' agentic mindset, agentic engagement, and perceived teacher autonomy support and control. Contemporary Educational Psychology, 70, 102085.]]). For lower-achieving students, the reciprocal loop that builds agency over time — more initiative producing more perceived autonomy support from teachers, more autonomy support producing more initiative — was much weaker or absent. And agentic engagement itself requires what Patall calls an agentic mindset: believing in one's own empowerment, experiencing oneself as someone whose contributions can shape the environment (Patall, 2024). Students without prior experience enacting agency don't just lack the behavior. They lack the underlying orientation that makes autonomy-supportive environments usable."

[Ch 11 — target-only, display unchanged] rqm5FFhi0
"...emerged mainly for higher-achieving students and was weak or absent for the rest [(Patall et al., 2022)]([[Patall, E. A., Kennedy, ... 102085.]]). Agentic engagement, in this work, presupposes an agentic mindset..." (full string captured in session; target-only repoint)

[Ch 4 — target-only, display unchanged] Xr5aPrrlV
"...researchers call it agentic engagement, and the evidence is good ... (Reeve, 2013; [Patall, Kennedy, et al., 2022]([[Patall, E. A., Kennedy, ... 102085.]])). I want my students to do this..." (target-only repoint)

[Ch 3b — DISPLAY CHANGE: bare inline full-citation → "(Patall et al., 2022)"] -mi5K-iz7
"And the advantage being measured is not only academic. In one longitudinal study of urban high
school science students, those who qualified for free or reduced-price lunch perceived their teachers
as less supportive of their autonomy and more controlling than their more affluent classmates did
([[Patall, E. A., Kennedy, A. A. U., Yates, N., Zambrano, J., Lee, D., & Vite, A. (2022). The relations between urban high school science students' agentic mindset, agentic engagement, and perceived teacher autonomy support and control. Contemporary Educational Psychology, 70, 102085.]]).
The students with the least cultural capital are not only handed a curriculum built for someone
else; they experience the classroom itself as a more controlled place — which is close to the
opposite of the conditions under which anyone learns to author their own thinking."

[Ch 3b — DISPLAY CHANGE: bare inline full-citation in a cite list → "Patall et al., 2022"] X6bIUKtgH
"...choice and freedom genuinely enhance intrinsic motivation, effort, and performance — when students have the internal resources to make use of them (Patall, Cooper, & Robinson, 2008; Patall, Cooper, & Wynn, 2010; Reeve & Tseng, 2011; Patall & Zambrano, 2019;
[[Patall, E. A., Kennedy, A. A. U., Yates, N., Zambrano, J., Lee, D., & Vite, A. (2022). The relations between urban high school science students' agentic mindset, agentic engagement, and perceived teacher autonomy support and control. Contemporary Educational Psychology, 70, 102085.]];
Patall, 2024). The 2010 study found that the benefits of choice provision are real but conditional..."

[Tag Hub meta-note — repoint] zd-sXIGSS
"In-text-linked so far: [[Patall, E. A., Kennedy, ... 102085.]] — the only REFERENCES source whose in-text cites matched (Ch 2, 4, 7, 11). Most in-text cites point to sources not yet on REFERENCES (orphan citations)."

[REFERENCES collector — bare link, repoint] oPwz1krfI
"[[Patall, E. A., Kennedy, ... 102085.]]"

[🗂️ Literature — bare link + trailing title, repoint] 9OYIXgh3A
"[[Patall, E. A., Kennedy, ... 102085.]] The relations between urban high school science students' agentic mindset, agentic engagement, and perceived teacher autonomy support and control"

## Matusov backlinks (repoint → [[Matusov, 2011]])
[bare link, repoint] Q_RgokYP0 → was [[Matusov, E. (2011). __Irreconcilable differences in Vygotsky's and Bakhtin's approaches to the social and the individual: An educational perspective__. Culture & Psychology, 17(1), 99–119.]] (smart-quote)
[bare link, repoint] nXVTBgHy3 → was [[Matusov, E. (2011). __Irreconcilable differences ... (straight-quote) ... 99–119.]]
[LEFT ALONE] UKrK-cOOk — "In the originals: ... old migrating (do not edit) ..." provenance block, not touched.

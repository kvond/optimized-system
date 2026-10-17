# Full tracked pipeline reconciliation

Compared all 34 tracked files in the retained pipeline clone against tracked answerable-skills files in the isolated current clone. Source commit: `9f767c70c21b74f1beee423b5b5ab51111de8618`; comparison commit: `5544b4e81d284810864b0849c476d742f360210f`. No source content was copied to Git, and no repository was edited.

27 files have exact SHA256 matches in current answerable-skills, including every inspected code/config file. Seven files have unique bytes. The DOCX handout also has no exact extracted-text match among current tracked DOCX files.

| Unique source path | Classification / smallest disposition |
|---|---|
| MANIFEST.md | historical_deployment_index; retain_in_verified_git_bundle |
| README.md | backup_scope_document; retain_in_verified_git_bundle |
| archive/MANIFEST_PRE-MIGRATION_2026-08-07.md | historical_deployment_index; retain_in_verified_git_bundle |
| docs/Final_Prompts_Student_and_Teacher.md | general_lessons_distilled; original_retained_in_bundle |
| docs/Render_App_Change_Spec.md | general_lessons_distilled; live_consumer_unverified |
| docs/What_Good_Thinking_Looks_Like_student_handout.docx | generic_legacy_handout; retain_binary_in_archive_then_review_compact_rubric |
| skills/AI_COACH_PROMPTS_v3.md | general_lessons_distilled; conflict_retained_explicitly |

The complete pipeline Git bundle is already preserved and verified in the existing archive receipt. Thus these seven files are not lost; no new raw copying is required for immediate preservation. Smallest useful next action: examine three unique policy/spec candidates (final prompts, Render change spec, AI coach prompts) and distill only current-compatible reusable rules with source hashes. Keep the original generic handout, deployment manifests and historical README in the archive. Do not activate old completion/gradebook assumptions, retired email paths or unresolved report-authorship decisions.

## Retirement dependencies still present

The active answerable-skills book-revision skill explicitly references legacy Answerable-Teaching snapshots, voice files, rulings and output paths (lines19–23,29,32). Legacy repository deletion would break those source pointers despite code preservation. The retained repo remains the recovery source until pointers are mapped deliberately to canonical Google Docs or reviewed preserved references. No manuscript/pseudonym/case files were copied by this audit.

Answerable SYNC.md references a local sync.sh path. The local publish LaunchAgent remains loaded with a missing-script/exit127 receipt; it has not been disabled. The unique Render change specification names feedback-system-u1br, but a source specification does not prove current live service status or completed changes. Live consumer resolution still requires authorized Render/account access or deployed readback.

The comparison uses a local retained pipeline commit, not a fresh remote fetch. The current core working-tree source policies were read without mutations; no runtime tests or grading actions ran. Detailed hashes, matches, dispositions and dependency references are in continuation-pipeline-assets.json.

The subsequent [sanitized policy summary](https://github.com/kvond/optimized-system/blob/a03453db2408fab4966322fa3dc075ed9b398a91/ai-ops/retirement-preservation/answerable-pipeline-backup/legacy-policy-summary.md) preserves the three unique policy/spec lessons. Original source bodies remain in the verified bundle; historical conflicts were not activated.

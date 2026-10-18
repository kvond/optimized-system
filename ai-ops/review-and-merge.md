# Technical work, review and merge

Katherine's standing authorization, clarified 2026-10-18: complete routine,
reversible technical work within her stated goals through implementation,
testing, independent review and merge. Do not ask her to approve each batch,
issue, draft PR or merge already covered by that authority. She reviews the
results after the fact and may reject a change or request a correction/revert.
For routine technical repository work, this policy supersedes older “never
merge” or Katherine-only PR merge instructions, including skill handoffs.
Permission to release or publish lesson materials remains a separate contract.

## Completion path

1. Keep the change bounded to the stated goal on a `claude/` or `codex/` branch;
   open a draft PR with the problem, resulting behavior and validation evidence.
2. Run the applicable existing checks. An independent agent/session must review
   the actual latest diff, scope and results; the author cannot self-review or
   supply their own acceptance. Record review acceptance against the exact PR
   head SHA. Resolve actionable findings and repeat the affected checks and
   independent review after subsequent changes.
3. Verify all configured applicable CI and required checks pass on that same
   latest SHA, with no unresolved review findings or branch-protection failures.
   If this repository has no PR CI configured, record **no PR CI configured**,
   the exact SHA, applicable local validation commands/results and independent
   review acceptance. Absence of CI is not a passing CI run; it does not require
   inventing a workflow or permanently block an otherwise verified change.
   Never skip or override a configured required check.
4. Mark the PR ready and merge through the ordinary protected PR path. The
   author may execute the merge after independent acceptance. Never push
   directly to main, self-approve, use an administrator bypass, weaken branch
   protections or merge an unchecked later head.
5. Report the concrete result, PR/commit, checks and any unverified live behavior
   to Katherine. A merged fix is not proof of deployment, execution or delivery.

## Rejection and retained history

When Katherine rejects a result, make a targeted correction or revert through
the same testing, independent review and applicable checks. Preserve Git history
and unrelated work; do not reset or rewrite shared history. A code rejection is
not permission to undo student work, grades, delivery records or other live data
automatically. Identify any separately needed live recovery precisely.

## Decisions outside standing technical authority

Escalate a genuinely new teaching or grading policy, student identity judgment,
access/sharing change, billing or paid-scope increase, schedule change,
destructive action, or work outside Katherine's stated goals. Do the authorized
preparation first so the remaining decision is concrete. Routine engineering
choices, tests, fixes and reversible repository maintenance do not need another
permission request.

School writes, external messages, publishing school material and deployments
remain subject to their existing explicit contracts; merging code does not
grant those permissions. Existing standing-authorized jobs and their ownership,
cadence, budgets and verification requirements remain unchanged. This policy
creates no automation, new rubric, schedule, billing authority or data action.

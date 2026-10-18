# Agent instructions

Read these before acting, in this order:
1. `ai-ops/NAMES.md`: canonical names. Write only these.
2. `ai-ops/HANDOFF.md` and `ai-ops/worker-registry/roles-and-schedules.md`.
3. `ai-ops/privacy-rules/` before touching anything with student data.

Rules:
- Decisions live in Slack #decisions. Code, skills, prompts and scheduled jobs change only in this repo.
- Work on a prefixed branch (`claude/...` or `codex/...`) and open a draft PR. Follow [review and merge](ai-ops/review-and-merge.md): routine reversible technical work within Katherine's stated goals has standing authorization through independent review, checks and merge. Never push directly to main.
- Review the other agent's actual latest diff; never self-review. Katherine reviews routine results after the fact and may reject them or request a tested correction/revert. Escalate only the unresolved decisions outside standing authority described in the review-and-merge policy.
- Consent is the ceiling: no publishing, sending, grading into IC, deleting, or changing a canonical file without a standing rule or Katherine's approval.
- At a standstill, give 2-3 alternatives with costs and recommend one. If you lack access, say what access would let you do the step.
- Build only from Katherine's own constructs and measures. No new rubric criteria, scales or tallies.

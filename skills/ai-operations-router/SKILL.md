---
name: ai-operations-router
description: Resolve a workflow's domain, exact operation, current owner and tested executor from the canonical AI operations contracts, then prepare an evidence-gated route or reference-only handoff. Use for cross-account workflow selection, delegation, resumption or automation routing; ordinary work with an already verified owner does not need a new routing exercise. Triggers - "route this workflow", "who owns this workflow", "delegate this workflow", "resume this workflow", "automation routing".
---

# AI Operations Router

Use the canonical checkout's `ai-ops/workflow-contracts/definitions/` catalog and `ai-ops/runtime/workflow_router.py`. The executable router makes a proposal; the existing executor owns leases, state, budgets, adapters and output readback. Installing this skill does not activate a worker or schedule.

Match the **domain and exact operation**, then the workflow ID. School teaching, higher-ed coursework and book work have different contracts even when each involves writing or feedback. Use `resolve_intent` for exact matching. Unknown or ambiguous intent produces one concrete numbered question with canonical options; save it in the existing private task state. `resume_intent` validates an answer and rejects changed scope or catalog; it is pure and does not consume or persist the answer. The coordinator replaces that pending question with the resolved intent and its stable request ID in the same task state before continuing. Repeated delivery resumes that same request, never a new execution. No answer keeps the same pending question while independent work can continue.

For the selected contract, obtain private resolver evidence for the actual account identity, executor binding, exact capability/operation, source revision and coverage, authority, existing owner and receipt state. Contract requirements, tool presence and historical provider labels are not tests. Keep actual account identifiers, student/manuscript content, credential locations and raw receipts outside Git. Never replace unavailable or partial reads with empty successful results.

Call `route_workflow` using the [runtime interface](references/interface.md). It validates current evidence and the [machine-readable routing rules](references/routing-rules.json). Do not relax a failed gate or invent successful checks to obtain `ready`. A blocked decision includes the next check to make; preserve the current owner. Unknown costs cannot win a price comparison. Supply actual cost inputs with their provenance; reported estimates are not savings or incurred spend.

Keep technical implementation in home Codex. UD Claude on the home Mac has independent coding capability, but that does not transfer this workflow's ownership or prove School Claude/school-computer capability. School Claude can receive only tested, bounded browser work through its own exact identity and authority. The school Chrome helper remains the sole IC grade writer. A competing owner or uncertain save/send/readback stops that action; no alternative tool is an automatic retry.

Pass a ready decision to the existing execution bridge only within the original authority. Verify its lease and recheck fresh source, ownership, receipt and capability evidence immediately before the action; `valid_until` is an upper bound, not permission to ignore an intervening change. Each contract dependency must be truthfully satisfied, including any existing lease requirement. Native content and destination readback establish completion; a route decision, configured schedule or successful local test does not.

Use `build_handoff` to retain the canonical source, receipt-backed completed actions, remaining actions, saved output reference, next owner and one next step. The [handoff schema](references/handoff.schema.json) is reference-only and does not send a message or transfer ownership. Root/coordinator reviews any separately authorized owner or schedule cutover.

For runtime validation, run:

```sh
python3 -m unittest discover -s ai-ops/runtime/tests -p 'test_workflow_router.py' -v
```

If this skill is installed separately from its canonical runtime, locate the configured checkout first. Do not recreate the router, copy private bindings into this skill, or substitute a generic model caller.

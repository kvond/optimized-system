# Birthday dates/history deterministic first

Pure `runtime/birthdays.py` reconciles normalized actual calendar occurrence dates against verified exact-occurrence handled history. No connector, AI, contacts, carts, purchases, messages, scheduling or delivery is implemented. Six synthetic tests cover boundaries and missing-source behavior. This is a tested helper, not a live Birthday workflow.

Known existing scope: primary Calendar Routine and Todoist Birthday Books & Gifts. Exact source IDs, expansions, current history representation, eligibility window and destination must be read from the existing main-UD task and its authorized sources before integration. Keep family/profile details private. The overlapping News cart-at-seven-days policy and Birthday no-cart policy are unresolved; this helper does not grant either action or choose a new boundary.

Required adapter inputs:

- Explicit owner scope, aware current datetime, business timezone and lookahead_days0..366. No default window; use actual accepted policy.
- Calendar and history evidence each: source_id, revision, available, complete, observed_at (aware ISO datetime). Both must be complete, available and observed on the current business date without future timestamps.
- Events: event_id and actual expanded occurrence_date (ISO date). No name, birth year or inferred recurrence. The source adapter must resolve all-day/timezone/recurrence semantics; leap-day alternatives require actual source evidence.
- History: event_id, occurrence_date, status (handled/planned/pending), receipt_id, verified, saved_at. Only handled+verified with actual nonfuture receipt closes the exact occurrence; prior-year, pending, planned or unverified history does not.

Window includes today and the last day. Dates before today or after the window are outside-window, not forgotten/closed. Duplicate occurrences or receipts are rejected. Missing/incomplete/stale sources return blocked with NULL items/counts, no no-work conclusion and no fallback to filename/name inference. Prior state must remain intact in a future adapter; the helper has no state writes.

Results are deterministic for same explicit source/policy identity. Fingerprint includes owner scope, source IDs/revisions/current observation, timezone/date/window and exact event/history inputs. Do not treat a matching old fingerprint as permission to skip fresh complete sources. Persist full results only in verified encrypted private storage. `public_summary` excludes event IDs/dates/history; console output has aggregate counts, source-policy hash and status. New/eligible means eligible for already-approved next planning/research only, not authority to message or buy.

Root integration acceptance: exact live prompt policy and authorized source IDs/destination; complete fresh input readback; seed and unchanged test; exact handled receipt test; partial source preservation; saved private result/readback. Then update the existing task in place without owner/cadence/permissions changes. No live source or task integration was performed by this module.

## Live source binding and current CLI

Read-only connector verification found the home-account primary Routine calendar and the same home-account private Birthday Books & Gifts project. Exact account/calendar/project IDs remain in the encrypted binding/input receipt; portable code checks their binding hashes. Broad bounded calendar discovery completed3pages/508events over October13,2025–January12,2027;49active project tasks and10current-year completion activities were read. No contacts/cart/purchase/message mutations occurred.
Raw current source receipt and normalized inputs are0600 inside encrypted `state/ai-ops`; never copy them to Git. Run:

```sh
python3 ai-ops/runtime/birthday_check.py --request-id birthday-check-unique
```

CLI reads only `birthday-current-inputs.json` from verified encrypted state, enforces the fixed task/account/calendar/project bindings and30-day window, calls hash-verified `worker_context.build_context('birthday')` (146words in current test), saves a private result packet and emits aggregate status/counts/hashes/path only. Repeating an identical request ID/input returns identical readback; different input/result with that ID fails closed. Refresh connector evidence and explicit family crosswalk each business day.

Current scoped acceptance: all19canonical existing gift-history records were inspected privately.17have unique exact date/name or explicit alias calendar matches;24expanded occurrences were bound.30unrelated calendar birthday occurrences are excluded without family inference. Two canonical records retain private crosswalk reconciliation holds, both outside the current30-day window. Current eligible count is1, current-window holds0; broad family reconciliation remains partial. Three current-year handled occurrences are supported by explicit sent/confirmed-order evidence; pending/selected and unspecified purchase details do not establish completion. The current saved CLI readback reports these separate statuses with146words of hash-verified context and zeroAI/actions. Earlier blocked artifact remains preserved as dated evidence.

### Every-run refresh/write/read procedure

1. Read the existing exact task policy and encrypted binding IDs. List the bound Routine calendar and verify owner/primary identity; read only that calendar. Page a bounded365-day past/90-day future range without a birthday keyword so misleading or abbreviated titles are not missed. Confirm the last page has no next token. Use actual business-date boundaries/timezone and source-expanded occurrence dates, never stale fixed dates.
2. Verify the bound private Todoist project/account. Page all current project records and the current-year completion activity needed for reconciliation. Source errors/retention gaps remain scoped coverage warnings, not empty history. Preserve the complete current raw source evidence0600 in encrypted receipts with a unique date/request ID and its SHA256.
3. Establish canonical family scope from existing gift-history records or actual prior user confirmation only. Parse their explicit birthday date and calendar aliases. Require unique exact date plus exact name/alias match; no fuzzy identity. Exclude unrelated calendar-only names. Retain unresolved canonical records as scoped_holds with private record reference, reason and current_window true/false/unknown. A past/upcoming date is not a sent gift.
4. Read each canonical record's current-year status and actual supporting receipt/activity. Normalize handled history only from explicit confirmed sent/purchased/ordered evidence for that exact occurrence; planned, pending, selected or “purchase details not recorded” alone cannot close it. Keep date corrections/history reconciliation in the private packet; source records are not changed by this tool.
5. Write `birthday-current-inputs.json` only inside verified encrypted runtime root, mode0600, after storage revalidation. Required top-level fields: task_id, scope, calendar_id, project_id, source_receipt_path, normalization_complete, family_bindings, scoped_holds, events, history, calendar_source, history_source. Bindings carry event_id/history_task_id/source_receipt_id/verified. Events carry event_id/occurrence_date. Source metadata carry source_id/revision(SHA256)/complete/available/observed_at. History schema is above. Hold current_window must be derived from the fresh canonical birthday date against today's30-day window; unknown cannot mean false.
6. Read back input bytes/hash, then invoke `birthday_check.py --request-id <unique actual run ID>`. Save full eligible/reconciliation packet privately; use public counts/hash/status only in portable receipts. Same request ID with differing inputs fails; preserve earlier receipts. Calendar/history source evidence must be fresh this business day. A partial family's known eligible items remain visible, while any current-window unknown prevents an all-clear.

News may reuse verified date/history evidence while retaining its original21/7-day thresholds. The Birthday helper's30-day gate does not replace News policy, authorize ordering, or collapse the tasks.

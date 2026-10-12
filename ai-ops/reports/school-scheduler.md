# Read-only scheduler inventory

October12 follow-up: this original overnight snapshot is retained below. Fresh [schedule verification](school-schedule-verification-2026-10-12.json) confirms both ACTIVE schedules, exact target bindings and unchanged prompt hashes. Current [continuation report](continuation-2026-10-12.md) records observed same-day model metadata and the verified T7/loaded-publisher findings that supersede older unknowns here. None proves a successful school destination write; no job changed.

2026-10-12T01:12:13.235986+00:00

Two ACTIVE weekday Codex heartbeat jobs verified from current persisted TOMLs. ACTIVE proves configuration, not execution.

## Morning roster check and submission tidy
ID: `morning-roster-check-and-submission-tidy`
Schedule: `RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=6;BYMINUTE=30;BYSECOND=0`
Target thread: `01a0fc18-96be-7873-8386-da8a6b110384`
Prompt SHA256: `24abf8f2962839ad7505ce94441385ffde33ea8800f2a247e34c0a14a6aa4820`

## Morning student feedback and print checklist
ID: `morning-student-feedback-and-print-checklist`
Schedule: `RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=7;BYMINUTE=30;BYSECOND=0`
Target thread: `01a0f4ed-2d87-7e62-9056-46f5ac441ef3`
Prompt SHA256: `13daff66e928ab309cf8ae31113d8de9cf8421d15f5d488b821c4347f8cec15d`

**mode:** read-only; no jobs modified

**owner:** local user katherinevonduyke owns TOMLs; Codex heartbeat dispatcher; local target threads

**timezone:** America/New_York in prompts; RRULE lacks TZID

**model_provider:** TOMLs do not pin model. Remote Desktop Commander and authenticated Hub/Chrome named. Actual backend AI provider/model unverified.

**cron:** crontab -l: no user crontab

**launchd:** No school 06:30/07:30 matches in readable user/system plist inventory. com.kvond.answerable-publish runs 19:30 and 23:00 via Answerable-Teaching nightly-publish.sh. Loaded state unverified.

**volumes:** Only Macintosh HD under /Volumes; no external archive mount verified

**retry:** Prompt constraints: bounded safe read retries; uncertain writes stop; lost feedback provider/save response requires readback, no blind retry/rebilling. Internal dispatcher backoff unknown.

**historical_evidence:** Oct9 target-thread summaries: tidy 149 checked, 147 existing private links, zero new links/moves, two holds; grade helper startup receipt failure with zero grades attempted. Feedback zero new verified reports; Oct7 packet held for teacher review/layout correction. Historical chat receipts only, not current destination readbacks.

**unknown:** ['Cloud Scheduler inventory', 'Internal scheduler retry/wake behavior', 'Actual Hub provider/model receipts', 'Fresh source/destination readback']

**memory:** MEMORY.md:118-171 and 178-242 used for prior scheduler context; current TOMLs supersede older conflicting instructions.

**Inputs:** fresh canonical IC roster/flags, exact live Agenda lesson/week bindings, registered Forms/upload/week folders, native student sources, configured private archive/index.

**Outputs:** 06:30 source filing/index/checklist/readiness before separate 07:00 Chrome helper; 07:30 individual private feedback, science-writing reports, teacher reports, checklist/index and dated immutable daily print packet.

Full sanitized exact prompts are retained in the JSON. No jobs were modified; no student identities retained.

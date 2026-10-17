# Job-watch cost work — October 12, 2026

The existing UD Delaware Education Job Watch now has a narrow repeat-work rule, saved through its normal task editor and reopened for exact readback. The entire original prompt remains an unchanged prefix. Its owner, Monitoring/Daily frequency, candidate criteria and destination were retained. Original and saved prompt copies are preserved privately on the encrypted drive; only the generic added rule and hashes are in [the operational change receipt](https://github.com/kvond/optimized-system/blob/d37f28ccd3a75a77698ace812d54e74c6d0ce71a/ai-ops/reports/job-watch-change-2026-10-12.json). The other four personal tasks and both school schedules were not edited. No new task was created or paused.

The rule asks the existing task to compare accessible verified prior listings before detailed suitability analysis, skip unchanged listings, reuse pages fetched within a run, preserve previous fingerprints and treat incomplete reads as availability holds. It does not provide a persistent local cache to the cloud task, suppress the initial model wakeup or prove lower billing. No future task-run receipt or bill saving is claimed.

## Working deterministic gate

`runtime/vacancies.py` implements a separate local public-listing comparison gate. Explicit grants bind employer, source, privacy partition, exact coverage and authentication requirements. Public anonymous reads require a deliberately public grant; protected sources still require authentication. Candidate profiles, employment decisions and applications are outside this gate. A changed candidate criterion requires reassessment by the caller even when listing text is unchanged.

New, materially changed, unchanged and withdrawn IDs are recorded in private SQLite with immutable revision history, request idempotency and atomic completion receipts/readback. A source ID or title alone cannot widen an approved search. Failed, partial, unauthorized, stale or unavailable reads preserve prior listings and return unknown counts; absence does not imply withdrawal without a complete read of the exact approved scope. Private state is created inside the verified encrypted drive, with no internal-disk fallback or model/network calls from the gate.

Eight targeted tests cover these rules, exact-scope separation, concurrent receipt identity, tampering, persistence and explicit public authentication policy. The current [runtime receipt](https://github.com/kvond/optimized-system/blob/d37f28ccd3a75a77698ace812d54e74c6d0ce71a/ai-ops/reports/runtime-cost-results-2026-10-12.json) records full-suite validation.

## Actual bounded-source acceptance

The [Delaware Department of Education employment page](https://education.delaware.gov/about-doe/employment/) directly links its Frontline employer filter. Normal browser rendering showed three openings in that exact location filter; all three descriptions were opened. Full rendered posting text was fingerprinted locally using SHA256, without copying public source bodies or candidate profiles into Git. A plain metadata-only HTTP response lacked those rendered records and was not treated as complete.

The local gate seeded those three source records, then classified all three as unchanged on repeat, with zero model or paid dispatches. An intentionally partial control returned null counts and preserved the prior source state. Exact counts, source URLs, UTC observation and private receipt hash are in [the bounded acceptance receipt](https://github.com/kvond/optimized-system/blob/d37f28ccd3a75a77698ace812d54e74c6d0ce71a/ai-ops/reports/vacancy-gate-acceptance-2026-10-12.json). This covers that employer filter only; it is not full Delaware coverage, three new candidate matches, a live scheduled source adapter or a cloud-to-drive integration.

## Separate weekly scope

Reading the original Weekly Job Scan established a separate candidate and production/media-management search across a different geographic and employer scope. Its resume, tracker, application/outreach history and prompt remain private at the original source. The Wednesday 7:00 a.m. displayed schedule was unchanged. The two jobs were not merged and no shared candidate analysis or employer approval was created. Earlier conditional-sharing suggestions are superseded by this finding; see [the revised audit](https://github.com/kvond/optimized-system/blob/d37f28ccd3a75a77698ace812d54e74c6d0ce71a/ai-ops/reports/cost-cutting-schedules-2026-10-12.md).

Full raw chat backups remain incomplete. The preserved source-Claude manifest was narrowed to mode0600 with its exact checksum unchanged. The support note is a draft only; no message was sent. Subsequent main-account export observations must be read from the current continuation status rather than inferred from the earlier authentication blocker.

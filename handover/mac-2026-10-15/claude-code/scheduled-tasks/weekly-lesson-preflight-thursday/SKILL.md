---
name: weekly-lesson-preflight-thursday
description: Thursday afternoon: run the Teaching Hub week-ahead check and rebuild the Monday packet for the following week, then list only what needs Katherine.
---

Weekly lesson-readiness preflight for Katherine von Duyke's Teaching Hub. This is a short invocation of the Hub's own deterministic check; the Hub does the checking, you only trigger it and report.

TOOLS: Use the "Control Chrome" desktop connector (tools named mcp__Control_Chrome__*; load them with ToolSearch "select:mcp__Control_Chrome__list_tabs,mcp__Control_Chrome__execute_javascript,mcp__Control_Chrome__open_url"). It drives Katherine's already-signed-in school Chrome window. Never type passwords, never sign in, never use answerableteaching.com.

STEPS
1. Find the open Teaching Hub tab: a tab whose URL starts with https://school-workflow-hub-611166743877.us-central1.run.app/v2/ (use mcp__Control_Chrome__list_tabs). If none, open https://school-workflow-hub-611166743877.us-central1.run.app/v2/#today with open_url and find it again. Always pass that tab's tab_id to execute_javascript. If the page is a Google sign-in page, stop and report "The Hub needs you to sign in in the school Chrome window" — do nothing else.
2. Compute NEXT MONDAY in America/New_York (today is Thursday, so it is today + 4 days) as YYYY-MM-DD.
3. In the Hub tab run synchronous same-origin requests (XMLHttpRequest with open(..., false)):
   a. POST /v2/api/weekly-preflight/run with header Content-Type: application/json and body {"start": NEXT_MONDAY, "weeks": 1}. If the reply's "status" is "incomplete", send the same POST once more (it resumes from saved checkpoints). Keep the parsed reply.
   b. POST /v2/api/weekly-preflight/packet with the same body. Keep the reply's "id", "version", "pages", "cached".
   c. Set the Today panel to that week for Katherine: localStorage.setItem('hub2:weekAheadStart', NEXT_MONDAY).
   These are the ONLY writes allowed. Do not call /repair, /deck-repair or /review, do not edit the Agenda, slides, Forms, Drive or Schoology, do not send email, do not change grades.
4. Report (this is the whole output; keep it short, plain language):
   - Week checked (dates) and overall status, plus "last successful check" time.
   - Monday packet link: https://school-workflow-hub-611166743877.us-central1.run.app/v2/api/weekly-preflight/packet.pdf?id=<packet id> (pages, and whether it was rebuilt or unchanged).
   - Only the unresolved exceptions from the run reply ("exceptions" whose status is not "repaired_and_verified"): one line each with class/section · date or week · lesson · slide numbers if any · reason · next action. Group by class. If there are none, say the week is ready.
   - Lessons whose 90-minute flow or VT review shows "not_reviewed" or "needs_re_review" (from each lesson's "reviews"), as one line per lesson: these need a quick review before Monday.
   - Remind that Schoology links are not checked by this run, and that access is checked with the Hub's account only (student access not verified).
If a request fails, report the HTTP status and the error text exactly, and do not retry more than once.
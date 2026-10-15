# Slack optimize router staging receipt — 2026-10-15

## Verified

- Repository: `kvond/optimized-system`, branch `feat/slack-optimize-router`, PR #15.
- Local gateway test suite: 8/8 passing.
- New Slack lanes created: `#higher-ed` and `#research-roam`; existing category structure otherwise preserved.
- Dedicated Cloud Run service: `ai-ops-slack-router` in `graceful-fold-341018`, region `us-east4`.
- Ready revision after source redeploy: `ai-ops-slack-router-00002-j5p`, 100% traffic, private invocation only.
- `/status` returns the gateway health JSON through authenticated Cloud Run proxy.
- `/slack/events` rejects an unsigned event with HTTP 401.
- Dedicated service account: `ai-ops-slack-router@graceful-fold-341018.iam.gserviceaccount.com`.
- Service identity has `roles/datastore.user` in the personal project.
- Existing OpenAI secret version 1 and Anthropic secret version 2 remain in `school-workflow-hub-54879`; the dedicated personal service identity has Secret Accessor on those two secrets only.
- Empty personal-project secret containers exist for `ai-ops-slack-bot-token` and `ai-ops-slack-signing-secret`; no versions/values exist yet.
- Gateway Firestore state stores event/idempotency, classification result/cache and usage/cost receipts; raw Slack intake text is not written into the cache payload.
- Slack application manifest contains the staged Cloud Run Events API URL.
- Slack app management page was opened on Katherine's Mac and the manifest was copied to the Mac clipboard.

## Not yet claimed

- No dedicated Slack app has been installed yet.
- No Slack bot token or signing secret has been created/stored.
- Cloud Run has not been granted public invocation.
- No live `#optimize-me` event has reached this gateway.
- No live OpenAI or Claude classification call has been made by this gateway.
- PR #15 is intentionally unmerged pending end-to-end acceptance.

## Acceptance gate

1. Create/install Slack app from the committed manifest.
2. Add one enabled version to each pre-created Slack secret container without pasting credentials into GitHub/chat.
3. Bind those two personal secrets to the Cloud Run service as `SLACK_BOT_TOKEN` and `SLACK_SIGNING_SECRET`.
4. Add Optimize Router to `#optimize-me`.
5. Verify signed URL challenge and a deterministic real message first (zero model cost).
6. Verify one forced `openai:` ambiguous message and one forced `claude:` ambiguous message; confirm cache/usage receipts and destination posts.
7. Only after those checks, grant `allUsers` Run Invoker to this single service so Slack can reach the endpoint; application authorization remains HMAC + owner/channel checks.
8. Merge PR #15 after acceptance evidence is saved.

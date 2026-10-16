# Slack optimize gateway

`#optimize-me` is the human intake. The gateway routes one message into the existing Slack category map without turning Slack into a second canonical repository.

## Behavior

- Accept only signed Slack Events API requests.
- Accept only human `message.channels` events from Katherine in `#optimize-me`.
- Ignore bot/subtype/app events and plain status output ending in known ChatGPT/Claude connector footers, including connector posts under Katherine's own user ID, to prevent loops. Ordinary human mentions of the agents remain eligible.
- When a message starts with a direct agent mention, provider prefix or request wording but ends in a connector footer, record one held receipt in its source thread. It may be Katherine's request with pasted agent output, so never silently drop it or send the ambiguous text to a model/another channel. Reposting the request separately with a link resolves that ambiguity; duplicate event delivery does not repeat the receipt.
- Hold sensitive/oversize input instead of sending it to a model.
- Use deterministic routing first.
- If routing is genuinely ambiguous, use the smallest provider model: OpenAI `gpt-6-luna` for operational material; Claude `claude-haiku-5-5` for writing/scholar/research material.
- Prefix an intake with `openai:` or `claude:` to force that provider for ambiguous classification.
- Cache classification by router version + normalized input + provider/model.
- Post a receipt in the source thread and a concise categorized note with an original-message link in the destination channel.
- No destructive/external action executor is exposed here. This service captures/routes only.

Current category lanes are encoded in `routing.py`. Planned technical/delegated admin tasks go to `#work-que`; topic-specific school/writing/research work retains its existing lane. Prepared human actions go to `#kathy`, replacing the old `#delegated-kathy` destination. Mentioning Kathy or a channel in a troubleshooting request does not transfer that work to her.

Explicit `Send to #channel: ...` / `Route this to #channel ...` directives (including Slack channel mentions) take priority. Clear `Blocked:`, `Failure:`, `Error:` and `Exception:` reports go to `#exceptions`; `Retirement candidate:` goes to `#decomission` (the workspace's spelling); teaching observations go to `#teaching-reflection`. Durable decisions retain `#decisions`. `Human action:` or an explicit statement that Kathy/Katherine must approve, choose, decide or sign in can route to `#kathy`; the router does not invent an approval request or decide that an agent has exhausted recovery options.

These are routing rules, not execution or completion signals. The separate Slack workers read source threads and verify authority/ownership before doing work.

## Secrets

Never commit credentials. Cloud Run expects:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `SLACK_BOT_TOKEN`
- `SLACK_SIGNING_SECRET`

The OpenAI and Anthropic credentials already exist in Google Secret Manager in `school-workflow-hub-54879`; do not create plaintext copies. Slack credentials are a one-time setup gate for the dedicated **Optimize Router** Slack app.

## State

Set `FIRESTORE_PROJECT` in Cloud Run to use Firestore for event idempotency, classification cache and usage receipts. Without it, local development uses a private SQLite file at `~/.local/share/ai-ops/slack-gateway.sqlite`.

## Cloud target

The intended always-on target is the personal project (`graceful-fold-341018`), not the school workflow service. Reuse cross-project API secrets only after explicit IAM binding; do not move private Slack intake into the school data plane.

## Test

```bash
python3 -m unittest discover -s ai-ops/slack-gateway/tests -v
```

Unclear messages (keyword confidence below 0.78) go to `#needs-rerouting` for Katherine with no model call. A model is called only when a message starts with `[openai]`, `openai:`, `[claude]` or `claude:` (Katherine, 2026-10-16).

Delivery tests use temporary SQLite state, signed HTTP requests, and mocked Slack/provider calls. They cover persisted event deduplication, connector filtering, source links, current destinations, model cache reuse, invalid output and failure without a second provider. They incur no model charges. Passing them does not prove Cloud Run deployment, Firestore concurrency or a live paid provider call; those remain separate acceptance checks after review/merge/deployment. Existing claimed-but-incomplete events still require investigation rather than blind replay after a Slack delivery error.

## One-time Slack installation gate

1. In Slack API app management, choose **Create New App → From a manifest** and paste `slack-app-manifest.yaml`.
2. Install **Optimize Router** to the Answerable Teaching workspace.
3. Store the generated Bot User OAuth Token as `ai-ops-slack-bot-token` and the app Signing Secret as `ai-ops-slack-signing-secret` in Secret Manager in `graceful-fold-341018`. Do not paste either credential into Slack, GitHub, or chat history.
4. Add the bot to `#optimize-me`. After both secrets are bound to Cloud Run and signature verification is tested, make only this Cloud Run service invokable by `allUsers`; application access remains restricted by Slack HMAC signature + owner/channel checks.

The service URL is `https://ai-ops-slack-router-dvypsqfnpq-uk.a.run.app`; the Events API URL is `/slack/events`.

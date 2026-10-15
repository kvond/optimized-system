# Slack optimize gateway

`#optimize-me` is the human intake. The gateway routes one message into the existing Slack category map without turning Slack into a second canonical repository.

## Behavior

- Accept only signed Slack Events API requests.
- Accept only human `message.channels` events from Katherine in `#optimize-me`.
- Ignore bot/subtype events to prevent loops.
- Hold sensitive/oversize input instead of sending it to a model.
- Use deterministic routing first.
- If routing is genuinely ambiguous, use the smallest provider model: OpenAI `gpt-6-luna` for operational material; Claude `claude-haiku-5-5` for writing/scholar/research material.
- Prefix an intake with `openai:` or `claude:` to force that provider for ambiguous classification.
- Cache classification by router version + normalized input + provider/model.
- Post a receipt in the source thread and a concise categorized note in the destination channel.
- No destructive/external action executor is exposed here. This service captures/routes only.

Current category lanes are encoded in `routing.py`. `#higher-ed` and `#research-roam` were added October 15 because they were missing from the existing workspace structure.

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

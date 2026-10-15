from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import time
import urllib.error
import urllib.request
from dataclasses import replace

from flask import Flask, jsonify, request

from providers import ProviderError, call_provider, estimated_cost
from routing import (
    CHANNELS, CHANNEL_NAMES, RouteDecision, cache_key, classifier_prompt,
    default_provider_for, deterministic_route, normalized, provider_override,
    validate_model_decision,
)
from state import State

app = Flask(__name__)
_state = None

OPTIMIZE_CHANNEL = os.environ.get("OPTIMIZE_CHANNEL_ID", CHANNELS["optimize"])
OWNER_USER = os.environ.get("OPTIMIZE_OWNER_USER_ID", "U0C9C9QESRL")
MAX_MESSAGE_CHARS = int(os.environ.get("MAX_MESSAGE_CHARS", "12000"))

SENSITIVE = re.compile(
    r"\b(password|passcode|api key|secret key|ssn|social security|bank account|routing number|"
    r"credit card|medical record|diagnos(?:is|ed)|medication|prescription|student id|iep|504 plan)\b",
    re.I,
)


def state() -> State:
    global _state
    if _state is None:
        _state = State()
    return _state


def verify_slack_signature(body: bytes, timestamp: str | None, signature: str | None, *, now: float | None = None) -> bool:
    secret = os.environ.get("SLACK_SIGNING_SECRET")
    if not secret or not timestamp or not signature:
        return False
    try:
        ts = int(timestamp)
    except ValueError:
        return False
    now = time.time() if now is None else now
    if abs(now - ts) > 300:
        return False
    base = b"v0:" + timestamp.encode() + b":" + body
    expected = "v0=" + hmac.new(secret.encode(), base, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def slack_api(method: str, payload: dict) -> dict:
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise RuntimeError("SLACK_BOT_TOKEN missing")
    req = urllib.request.Request(
        f"https://slack.com/api/{method}",
        data=json.dumps(payload).encode(),
        headers={"authorization": f"Bearer {token}", "content-type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read(1_000_000))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Slack API request failed: {type(exc).__name__}") from None
    if not data.get("ok"):
        raise RuntimeError(f"Slack API error: {data.get('error', 'unknown_error')}")
    return data


def post(channel: str, text: str, *, thread_ts: str | None = None):
    payload = {"channel": channel, "text": text, "unfurl_links": False, "unfurl_media": False}
    if thread_ts:
        payload["thread_ts"] = thread_ts
    return slack_api("chat.postMessage", payload)


def _extract_json(text: str) -> dict:
    value = text.strip()
    value = re.sub(r"^```(?:json)?\s*", "", value, flags=re.I)
    value = re.sub(r"\s*```$", "", value)
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        start, end = value.find("{"), value.rfind("}")
        if start >= 0 and end > start:
            return json.loads(value[start:end + 1])
        raise


def _classify(text: str) -> tuple[RouteDecision, dict | None, float, bool]:
    direct = deterministic_route(text)
    if direct:
        return direct, None, 0.0, False

    provider, model = default_provider_for(text)
    key = cache_key(text, provider, model)
    cached = state().cache_get(key)
    if cached:
        decision = RouteDecision(**cached["decision"])
        return decision, cached.get("usage"), float(cached.get("cost", 0.0)), True

    raw, usage = call_provider(provider, classifier_prompt(text), model)
    value = _extract_json(raw)
    decision = validate_model_decision(value, provider=provider, model=model)
    cost = estimated_cost(model, usage)
    record = {"decision": decision.asdict(), "usage": usage, "cost": cost}
    state().cache_put(key, record)
    state().log_usage(provider, model, cost, usage)
    return decision, usage, cost, False


def _label(decision: RouteDecision) -> str:
    return f"{decision.kind.replace('_',' ').title()} · {decision.area.replace('_',' ').title()}"


def _destination_name(channel_id: str) -> str:
    return CHANNEL_NAMES.get(channel_id, channel_id)


def _process_event(event_id: str, event: dict):
    text = event.get("text")
    channel = event.get("channel")
    user = event.get("user")
    ts = event.get("ts")
    if not isinstance(text, str) or not text.strip() or not isinstance(ts, str):
        state().complete_event(event_id, {"ignored": "empty_or_missing"})
        return
    if channel != OPTIMIZE_CHANNEL or user != OWNER_USER:
        state().complete_event(event_id, {"ignored": "outside_owner_intake"})
        return
    if len(text) > MAX_MESSAGE_CHARS:
        post(channel, "Held: this intake is too large for the Slack router. Put the working file in its canonical home and link it here.", thread_ts=ts)
        state().complete_event(event_id, {"held": "oversize"})
        return
    if SENSITIVE.search(text):
        post(channel, "Held in #optimize-me: sensitive content was not sent to an API or forwarded to another public channel.", thread_ts=ts)
        state().complete_event(event_id, {"held": "sensitive"})
        return

    try:
        decision, usage, cost, reused = _classify(text)
    except (ProviderError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
        # Do not invent a destination or retry another paid provider on uncertainty.
        post(channel, f"Held for routing: {type(exc).__name__}. No fallback provider was called and nothing was forwarded.", thread_ts=ts)
        state().complete_event(event_id, {"held": "classification_failed", "error_type": type(exc).__name__})
        return

    destination_name = _destination_name(decision.destination_id)
    worker = "deterministic" if decision.deterministic else f"{decision.provider}/{decision.model}"
    cache_note = " · cache hit" if reused else ""
    cost_note = "" if decision.deterministic else f" · est. ${cost:.6f}"
    receipt = f"Captured → #{destination_name} · {_label(decision)} · {worker}{cache_note}{cost_note}"
    post(channel, receipt, thread_ts=ts)

    if decision.destination_id != channel:
        forwarded = (
            f"*From #optimize-me · {_label(decision)}*\n"
            f"{decision.summary}\n"
            f"_Source ts: {ts} · Routed by {worker}{cache_note}_"
        )
        post(decision.destination_id, forwarded)

    result = {
        "decision": decision.asdict(), "usage": usage, "cost": cost,
        "cache_hit": reused, "forwarded": decision.destination_id != channel,
    }
    state().complete_event(event_id, result)


@app.get("/healthz")
def healthz():
    return jsonify({"ok": True, "service": "ai-ops-slack-gateway"})


@app.post("/slack/events")
def slack_events():
    body = request.get_data(cache=True)
    if not verify_slack_signature(body, request.headers.get("X-Slack-Request-Timestamp"), request.headers.get("X-Slack-Signature")):
        return jsonify({"ok": False}), 401
    payload = request.get_json(silent=True) or {}
    if payload.get("type") == "url_verification":
        return jsonify({"challenge": payload.get("challenge", "")})
    if payload.get("type") != "event_callback":
        return jsonify({"ok": True})
    event = payload.get("event") or {}
    if event.get("bot_id") or event.get("subtype"):
        return jsonify({"ok": True})
    if event.get("type") != "message":
        return jsonify({"ok": True})
    event_id = payload.get("event_id")
    if not isinstance(event_id, str) or not event_id:
        return jsonify({"ok": False}), 400
    if not state().claim_event(event_id):
        return jsonify({"ok": True, "duplicate": True})
    _process_event(event_id, event)
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))

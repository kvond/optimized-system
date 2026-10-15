from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

# USD per 1M tokens, standard short-context prices checked 2026-10-15.
PRICES = {
    "gpt-6-luna": {"input": 0.05, "cached": 0.005, "output": 0.25},
    "gpt-6.1-sol": {"input": 1.00, "cached": 0.05, "output": 5.00},
    "claude-haiku-5-5": {"input": 0.10, "cached": 0.01, "output": 0.50},
    "claude-sonnet-5-5": {"input": 2.00, "cached": 0.10, "output": 10.00},
    "claude-opus-5-5": {"input": 4.00, "cached": 0.20, "output": 20.00},
}

class ProviderError(RuntimeError):
    pass


def _request(url: str, headers: dict[str, str], payload: dict, timeout: float = 20.0) -> dict:
    data = json.dumps(payload).encode()
    request = urllib.request.Request(url, data=data, headers={**headers, "content-type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read(2_000_000)
    except urllib.error.HTTPError as exc:
        body = exc.read(4000).decode(errors="replace")
        raise ProviderError(f"provider HTTP {exc.code}: {body[:500]}") from None
    except OSError as exc:
        raise ProviderError(f"provider request failed: {type(exc).__name__}") from None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise ProviderError("provider returned invalid JSON") from None


def _openai_text(data: dict) -> str:
    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text" and isinstance(content.get("text"), str):
                parts.append(content["text"])
    if not parts and isinstance(data.get("output_text"), str):
        parts.append(data["output_text"])
    if not parts:
        raise ProviderError("OpenAI response contained no output text")
    return "\n".join(parts)


def call_openai(prompt: str, model: str = "gpt-6-luna") -> tuple[str, dict]:
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ProviderError("OPENAI_API_KEY missing")
    data = _request(
        "https://api.openai.com/v1/responses",
        {"authorization": f"Bearer {key}"},
        {"model": model, "input": prompt, "max_output_tokens": 500},
    )
    usage = data.get("usage") or {}
    detail = usage.get("input_tokens_details") or {}
    return _openai_text(data), {
        "input_tokens": int(usage.get("input_tokens") or 0),
        "cached_tokens": int(detail.get("cached_tokens") or 0),
        "output_tokens": int(usage.get("output_tokens") or 0),
    }


def call_claude(prompt: str, model: str = "claude-haiku-5-5") -> tuple[str, dict]:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise ProviderError("ANTHROPIC_API_KEY missing")
    data = _request(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": key, "anthropic-version": "2023-06-01"},
        {"model": model, "max_tokens": 500, "messages": [{"role": "user", "content": prompt}]},
    )
    parts = [item.get("text", "") for item in data.get("content", []) if item.get("type") == "text"]
    if not any(parts):
        raise ProviderError("Claude response contained no text")
    usage = data.get("usage") or {}
    return "\n".join(parts), {
        "input_tokens": int(usage.get("input_tokens") or 0),
        "cached_tokens": int(usage.get("cache_read_input_tokens") or 0),
        "output_tokens": int(usage.get("output_tokens") or 0),
    }


def call_provider(provider: str, prompt: str, model: str) -> tuple[str, dict]:
    if provider == "openai":
        return call_openai(prompt, model)
    if provider == "claude":
        return call_claude(prompt, model)
    raise ProviderError("unsupported provider")


def estimated_cost(model: str, usage: dict) -> float:
    price = PRICES.get(model)
    if not price:
        return 0.0
    cached = max(0, int(usage.get("cached_tokens") or 0))
    total_input = max(0, int(usage.get("input_tokens") or 0))
    uncached = max(0, total_input - cached)
    output = max(0, int(usage.get("output_tokens") or 0))
    return (uncached * price["input"] + cached * price["cached"] + output * price["output"]) / 1_000_000

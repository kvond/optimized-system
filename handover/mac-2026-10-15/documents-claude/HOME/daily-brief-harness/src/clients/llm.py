"""The only place a model is called. OpenAI-compatible, so the provider is a
config swap: DeepSeek (api.deepseek.com), Moonshot/Kimi (api.moonshot.ai),
or Anthropic's OpenAI-compat endpoint if the voice needs the upgrade.
"""
import os
from openai import OpenAI

def client(cfg):
    return OpenAI(api_key=os.environ["LLM_API_KEY"], base_url=cfg["llm"]["base_url"])

def ask(cfg, system: str, user: str, force_json: bool = False) -> str:
    c = client(cfg)
    kwargs = {}
    if force_json:
        kwargs["response_format"] = {"type": "json_object"}
    resp = c.chat.completions.create(
        model=cfg["llm"]["model"],
        max_tokens=cfg["llm"]["max_tokens"],
        messages=[{"role": "system", "content": system},
                  {"role": "user", "content": user}],
        **kwargs,
    )
    return resp.choices[0].message.content

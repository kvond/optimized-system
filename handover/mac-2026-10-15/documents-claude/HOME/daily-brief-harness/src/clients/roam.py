"""Roam backend API client — plain HTTPS, no MCP, no mid-session hangs.

Token: env ROAM_API_TOKEN (graph-scoped, minted in Roam under
Settings → Graph → API tokens; needs read+edit).
The API 307-redirects api.roamresearch.com to a peer host; requests
preserves method+body on 307/308, so allow_redirects=True is correct.
"""
import os, requests

BASE = "https://api.roamresearch.com/api/graph"

def _headers():
    return {
        "Authorization": f"Bearer {os.environ['ROAM_API_TOKEN']}",
        "Content-Type": "application/json",
        "x-authorization": f"Bearer {os.environ['ROAM_API_TOKEN']}",  # some peers want this casing
    }

def q(graph: str, query: str, args: list | None = None) -> list:
    """Run a datalog query, return :result."""
    body = {"query": query}
    if args:
        body["args"] = args
    r = requests.post(f"{BASE}/{graph}/q", json=body, headers=_headers(), timeout=60)
    r.raise_for_status()
    return r.json().get("result", [])

def pull(graph: str, eid: str, selector: str):
    r = requests.post(f"{BASE}/{graph}/pull", json={"eid": eid, "selector": selector},
                      headers=_headers(), timeout=60)
    r.raise_for_status()
    return r.json().get("result")

def write(graph: str, actions: list):
    """batch-actions write. Idempotence is the caller's job (delete-then-write
    the day's brief block if re-run)."""
    r = requests.post(f"{BASE}/{graph}/write",
                      json={"action": "batch-actions", "actions": actions},
                      headers=_headers(), timeout=120)
    r.raise_for_status()
    return r.json()

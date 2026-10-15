#!/usr/bin/env python3
"""
roam_pull.py  —  Pull the book graph into inventory.json (READ-ONLY on Roam).

This is the only script that touches Roam. Everything downstream (dedup_sweep.py,
on_create_check.py) operates on the inventory.json it produces, so if you would
rather have Cowork's Roam connection produce the inventory, just emit the same
schema (documented at the bottom of this file) and skip this script.

It runs three Datalog queries against the Roam backend `/q` endpoint:
  1. every page  -> (uid, title)
  2. every page->page reference edge -> backlink sets
  3. page block strings -> a short per-page snippet (for the semantic layer)

Auth note: the first call to api.roamresearch.com returns a 308 redirect to a
peer host. `requests` strips the Authorization header across a host change, so we
subclass Session to preserve it (and also send X-Authorization, which survives).

Usage:
  export ROAM_GRAPH=your-graph-name
  export ROAM_API_TOKEN=roam-graph-token-XXXX        # read-scoped is enough
  python3 roam_pull.py --out inventory.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

import requests

ROAM_BASE = "https://api.roamresearch.com/api/graph/{graph}/q"

# Roam daily-note titles, e.g. "April 26th, 2023" — excluded from the vocabulary by default.
DAILY_RE = re.compile(
    r"^(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+\d{1,2}(st|nd|rd|th),\s+\d{4}$"
)

PAGES_Q = "[:find ?uid ?title :where [?p :block/uid ?uid] [?p :node/title ?title]]"
EDGES_Q = (
    "[:find ?src ?dst "
    ":where [?b :block/refs ?d] [?d :node/title ?dst] "
    "[?b :block/page ?pg] [?pg :node/title ?src]]"
)
SNIPPET_Q = (
    "[:find ?title ?string "
    ":where [?p :node/title ?title] [?b :block/page ?p] [?b :block/string ?string]]"
)


class PreserveAuthSession(requests.Session):
    """Keep the Authorization header when Roam 308-redirects to a peer host."""

    def rebuild_auth(self, prepared_request, response):  # noqa: D102
        return  # do not strip


def run_query(session: requests.Session, graph: str, token: str, query: str) -> list:
    url = ROAM_BASE.format(graph=graph)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
        "X-Authorization": f"Bearer {token}",
    }
    resp = session.post(url, headers=headers, data=json.dumps({"query": query}))
    if resp.status_code != 200:
        sys.exit(f"Roam query failed ({resp.status_code}): {resp.text[:500]}")
    payload = resp.json()
    # The /q endpoint returns {"result": [...]}; tolerate a bare list too.
    return payload.get("result", payload) if isinstance(payload, dict) else payload


def build_inventory(graph: str, token: str, *, include_daily: bool, max_snippet: int) -> dict:
    session = PreserveAuthSession()

    pages = run_query(session, graph, token, PAGES_Q)        # [[uid, title], ...]
    edges = run_query(session, graph, token, EDGES_Q)        # [[src, dst], ...]
    snips = run_query(session, graph, token, SNIPPET_Q)      # [[title, string], ...]

    def keep(title: str) -> bool:
        return include_daily or not DAILY_RE.match(title)

    uid_by_title = {t: u for u, t in pages if keep(t)}

    # backlinks[dst] = {pages that reference dst}
    backlinks: dict[str, set[str]] = {t: set() for t in uid_by_title}
    for src, dst in edges:
        if dst in backlinks and src in uid_by_title and src != dst:
            backlinks[dst].add(src)

    # one capped snippet per page, in stable order
    snippet: dict[str, str] = {}
    for title, string in snips:
        if title not in uid_by_title or not string:
            continue
        cur = snippet.get(title, "")
        if len(cur) < max_snippet:
            snippet[title] = (cur + " " + string).strip()[:max_snippet]

    pages_out = [
        {
            "title": t,
            "uid": uid_by_title[t],
            "backlinks": sorted(backlinks[t]),
            "backlink_count": len(backlinks[t]),
            "snippet": snippet.get(t, ""),
        }
        for t in sorted(uid_by_title)
    ]
    return {
        "graph": graph,
        "pulled_at": datetime.now(timezone.utc).isoformat(),
        "page_count": len(pages_out),
        "pages": pages_out,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Pull a Roam graph into inventory.json (read-only).")
    ap.add_argument("--graph", default=os.environ.get("ROAM_GRAPH"))
    ap.add_argument("--token", default=os.environ.get("ROAM_API_TOKEN"))
    ap.add_argument("--out", default="inventory.json")
    ap.add_argument("--include-daily", action="store_true",
                    help="Include daily-note (date) pages. Off by default — they are not vocabulary.")
    ap.add_argument("--max-snippet", type=int, default=400)
    args = ap.parse_args()

    if not args.graph or not args.token:
        sys.exit("Set --graph/--token or ROAM_GRAPH/ROAM_API_TOKEN.")

    inv = build_inventory(args.graph, args.token,
                          include_daily=args.include_daily, max_snippet=args.max_snippet)
    with open(args.out, "w") as f:
        json.dump(inv, f, indent=2, ensure_ascii=False)
    print(f"Wrote {args.out}: {inv['page_count']} pages.")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# inventory.json schema (the contract for everything downstream):
# {
#   "graph": "name", "pulled_at": "ISO-8601", "page_count": N,
#   "pages": [
#     {"title": str, "uid": str,
#      "backlinks": [str, ...],     # pages that link TO this page
#      "backlink_count": int,
#      "snippet": str}              # short text sample, for the semantic layer
#   ]
# }
# ---------------------------------------------------------------------------

#!/usr/bin/env python3
"""
on_create_check.py  —  The recurring guard (Roam-agnostic).

Run this BEFORE minting any new page — a Q: from a critique, a concept from a
writing session, a tag Cowork wants to add. It compares the one proposed title
against the existing set (top-k nearest, not an all-pairs sweep) and returns
`exists`, `review`, or `clear`. Exit code: 0 clear, 2 review, 3 exists.

Layers reused from the sweep: 1 normalized-exact, 2 fuzzy token-set, 3 alias.
Layer 4 (backlink overlap) can't apply to a page that doesn't exist yet, so each
near-neighbor's backlink_count is shown instead as an "establishment" signal.
Layer 5 (semantic) is a Claude follow-up when the result is `review`.

Usage:
  python3 on_create_check.py --title "student agency" --inventory inventory.json
  python3 on_create_check.py --title "Q: does Ch.5 resolve the legibility objection?" \
      --inventory inventory.json --vocab vocabulary.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys

# Reuse the exact same normalization/initialism as the sweep.
from dedup_sweep import normalize, initialism, nospace

try:
    from rapidfuzz import fuzz, process
except ImportError:
    sys.exit("rapidfuzz is required:  pip install rapidfuzz")

STRONG = 92   # at/above this, treat as a likely duplicate -> review
RECALL = 80   # surface anything this similar as a near-neighbor


def check(title: str, inv: dict, aliases: dict, *, strong: int, recall: int) -> dict:
    pages = {p["title"]: p for p in inv["pages"]}
    titles = list(pages)
    ntitle = normalize(title)

    alias_of = {normalize(f): canon for canon, forms in aliases.items() for f in forms}
    nmap = {t: normalize(t) for t in titles}

    # Layer 1 — exact normalized collision
    for t in titles:
        if nmap[t] == ntitle:
            return {"title": title, "status": "exists", "match": t,
                    "reason": "normalized-exact", "candidates": []}

    # Layer 3 — alias / acronym
    if ntitle in alias_of:
        return {"title": title, "status": "exists", "match": alias_of[ntitle],
                "reason": "alias", "candidates": []}
    init = initialism(title)
    nsp_title = nospace(title)
    for t in titles:
        if (init and init == nospace(t)) or (initialism(t) and initialism(t) == nsp_title):
            return {"title": title, "status": "review", "match": t,
                    "reason": "acronym", "candidates": [_cand(pages[t], t, 99.0, "acronym")]}

    # Layer 2 — fuzzy top-k (same Q/concept type only)
    # Question nodes use the Discourse Graph "QUE" type prefix, not "Q:".
    is_q = lambda s: bool(re.match(r"(?i)^que\b", s.strip()))
    pool = [t for t in titles if is_q(t) == is_q(title)]
    near = process.extract(title, pool, scorer=fuzz.token_set_ratio,
                           score_cutoff=recall, limit=5)
    candidates = [_cand(pages[t], t, score, "fuzzy") for t, score, _ in near]
    status = "review" if any(c["score"] >= strong for c in candidates) else "clear"
    return {"title": title, "status": status, "match": None,
            "reason": None, "candidates": candidates}


def _cand(page: dict, t: str, score: float, reason: str) -> dict:
    return {"title": t, "score": round(float(score), 1), "reason": reason,
            "backlink_count": page["backlink_count"]}


def main() -> None:
    ap = argparse.ArgumentParser(description="Check one proposed page title against the graph.")
    ap.add_argument("--title", required=True)
    ap.add_argument("--inventory", default="inventory.json")
    ap.add_argument("--vocab", default=None)
    ap.add_argument("--strong", type=int, default=STRONG)
    ap.add_argument("--recall", type=int, default=RECALL)
    args = ap.parse_args()

    with open(args.inventory) as f:
        inv = json.load(f)
    aliases = {}
    if args.vocab:
        try:
            with open(args.vocab) as f:
                aliases = json.load(f)
        except FileNotFoundError:
            pass

    result = check(args.title, inv, aliases, strong=args.strong, recall=args.recall)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit({"clear": 0, "review": 2, "exists": 3}[result["status"]])


if __name__ == "__main__":
    main()

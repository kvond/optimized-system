#!/usr/bin/env python3
"""
dedup_sweep.py  —  The one-time sweep (Roam-agnostic; operates on inventory.json).

Runs the matching layers cheapest-first over every page title and emits a ranked
list of merge candidates plus a markdown review surface. It NEVER edits the graph.
A false merge silently destroys a distinction you meant to keep — worse than missing
one — so this is tuned for recall, and every candidate is yours to adjudicate.

Layers:
  1  normalized-exact   casefold/trim/diacritics/punct -> key collision
  2  fuzzy string       rapidfuzz token_set_ratio (word-order + subset)
  3  alias / acronym    vocabulary.json aliases + initialism expansion
  4  backlink overlap   Jaccard of backlink neighborhoods (the graph's own evidence)
  5  semantic           NOT done here — residual titles are written out for Claude
                        to cluster with reasons (no blind collapsing, no API dep)

Usage:
  python3 dedup_sweep.py --inventory inventory.json \
      [--vocab vocabulary.json] [--review dedup_review.md] \
      [--candidates dedup_candidates.json] [--semantic semantic_candidates.json] \
      [--fuzz 88]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from itertools import combinations

try:
    from rapidfuzz import fuzz, process
except ImportError:
    sys.exit("rapidfuzz is required:  pip install rapidfuzz")

_PUNCT = re.compile(r"[^\w\s]", re.UNICODE)
_WS = re.compile(r"\s+")


def normalize(title: str) -> str:
    """Casefold, strip diacritics and punctuation, collapse whitespace."""
    t = unicodedata.normalize("NFKD", title)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = _PUNCT.sub(" ", t).casefold()
    return _WS.sub(" ", t).strip()


_STOP = {"and", "or", "of", "the", "for", "to", "in", "on", "with"}


def nospace(title: str) -> str:
    return normalize(title).replace(" ", "")


def initialism(title: str) -> str:
    """First letters of significant words, e.g. 'Anatomy and Physiology' -> 'ap'."""
    words = [w for w in re.split(r"\s+", normalize(title)) if w and w not in _STOP]
    return "".join(w[0] for w in words) if len(words) > 1 else ""


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def recommend(score: float, bl: float, exact: bool, alias: bool) -> tuple[str, str]:
    """Return (action, confidence). Fuzzy-only matches need backlink corroboration:
    token_set_ratio hits 100 on any subset, so a high score alone is not a merge."""
    if exact:
        return "MERGE", "high"
    if alias:
        return "ALIAS", "high"
    if bl >= 0.5:
        return "MERGE", "high"          # similar name AND used interchangeably
    if bl >= 0.2:
        return "REVIEW", "medium"
    return "KEEP_SEPARATE", "low"        # similar name, used differently -> likely distinct


def canonical(p_a: dict, p_b: dict) -> tuple[str, str]:
    """More-established (more backlinks) title wins; tie-break shorter, then alpha."""
    a, b = p_a, p_b
    key = lambda p: (-p["backlink_count"], len(p["title"]), p["title"])
    win, lose = sorted([a, b], key=key)
    return win["title"], lose["title"]


def sweep(inv: dict, aliases: dict[str, list[str]], fuzz_cut: int) -> list[dict]:
    pages = inv["pages"]
    by_title = {p["title"]: p for p in pages}
    titles = list(by_title)
    norm = {t: normalize(t) for t in titles}
    nsp = {t: nospace(t) for t in titles}
    bl = {t: set(by_title[t]["backlinks"]) for t in titles}

    # alias lookup: surface form -> canonical
    alias_of = {}
    for canon, forms in aliases.items():
        for f in forms:
            alias_of[normalize(f)] = canon
    init = {t: initialism(t) for t in titles}

    pairs: dict[frozenset, dict] = {}
    is_q = lambda t: t.strip().lower().startswith("q:")

    def add(a: str, b: str, layer: str, score: float):
        if is_q(a) != is_q(b):   # never pair a question page with a concept page
            return
        k = frozenset((a, b))
        rec = pairs.get(k)
        if rec is None or score > rec["score"]:
            pairs[k] = {"a": a, "b": b, "layer": layer, "score": float(score)}
        pairs[k].setdefault("layers", set()).add(layer)

    # Layer 1 — normalized-exact
    buckets: dict[str, list[str]] = {}
    for t in titles:
        buckets.setdefault(norm[t], []).append(t)
    for group in buckets.values():
        for a, b in combinations(group, 2):
            add(a, b, "exact", 100.0)

    # Layer 2 — fuzzy token-set (process.extract is fast; cap to top matches each)
    for t in titles:
        for other, score, _ in process.extract(
            t, [x for x in titles if x != t],
            scorer=fuzz.token_set_ratio, score_cutoff=fuzz_cut, limit=6
        ):
            add(t, other, "fuzzy", score)

    # Layer 3 — alias / acronym
    for a, b in combinations(titles, 2):
        if alias_of.get(norm[a]) == b or alias_of.get(norm[b]) == a:
            add(a, b, "alias", 100.0)
        elif (init[a] and init[a] == nsp[b]) or (init[b] and init[b] == nsp[a]):
            add(a, b, "acronym", 99.0)

    # Layer 4 — backlink overlap as evidence + finalize recommendation
    out = []
    for rec in pairs.values():
        a, b = rec["a"], rec["b"]
        layers = rec.get("layers", {rec["layer"]})
        blj = jaccard(bl[a], bl[b])
        exact = "exact" in layers
        alias = "alias" in layers or "acronym" in layers
        action, conf = recommend(rec["score"], blj, exact, alias)
        canon, loser = canonical(by_title[a], by_title[b])
        out.append({
            "a": a, "b": b,
            "layers": sorted(layers),
            "score": round(rec["score"], 1),
            "backlink_overlap": round(blj, 3),
            "backlinks": {a: by_title[a]["backlink_count"], b: by_title[b]["backlink_count"]},
            "action": action,
            "confidence": conf,
            "canonical": canon if action in ("MERGE", "ALIAS") else None,
            "loser": loser if action in ("MERGE", "ALIAS") else None,
        })

    rank = {"high": 0, "medium": 1, "low": 2}
    out.sort(key=lambda r: (rank[r["confidence"]], -r["score"]))
    return out


def write_review(path: str, candidates: list[dict], inv: dict) -> None:
    n = len(candidates)
    lines = [
        f"# Dedup review — {inv.get('graph','graph')}  ({inv.get('page_count','?')} pages)",
        f"_{n} candidate pair(s). Nothing has been written. Mark each: keep / merge / alias._",
        "",
    ]
    for i, c in enumerate(candidates, 1):
        rec = (f"**{c['action']}** → canonical `[[{c['canonical']}]]`, fold `[[{c['loser']}]]`"
               if c["canonical"] else f"**{c['action']}**")
        lines += [
            f"## {i}. `[[{c['a']}]]`  ⇄  `[[{c['b']}]]`",
            f"- {rec}  ·  confidence **{c['confidence']}**",
            f"- matched by: {', '.join(c['layers'])}  ·  score {c['score']}  ·  "
            f"backlink overlap {c['backlink_overlap']}",
            f"- backlinks: `{c['a']}` = {c['backlinks'][c['a']]}, "
            f"`{c['b']}` = {c['backlinks'][c['b']]}",
            "- decision: ⬜ keep separate   ⬜ merge   ⬜ alias",
            "",
        ]
    with open(path, "w") as f:
        f.write("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser(description="One-time dedup sweep over inventory.json.")
    ap.add_argument("--inventory", default="inventory.json")
    ap.add_argument("--vocab", default=None, help="vocabulary.json with {canonical: [aliases]}")
    ap.add_argument("--review", default="dedup_review.md")
    ap.add_argument("--candidates", default="dedup_candidates.json")
    ap.add_argument("--semantic", default="semantic_candidates.json")
    ap.add_argument("--fuzz", type=int, default=88, help="token_set_ratio cutoff (0-100)")
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

    candidates = sweep(inv, aliases, args.fuzz)
    write_review(args.review, candidates, inv)
    with open(args.candidates, "w") as f:
        json.dump(candidates, f, indent=2, ensure_ascii=False)

    # Layer 5 hand-off: every non-paired title goes to Claude to cluster semantically.
    paired = {t for c in candidates for t in (c["a"], c["b"])}
    residual = [{"title": p["title"], "snippet": p["snippet"]}
                for p in inv["pages"] if p["title"] not in paired]
    with open(args.semantic, "w") as f:
        json.dump({"instruction": "Cluster these into likely-duplicate groups WITH a reason "
                                   "for each group. Related-but-distinct is NOT a duplicate.",
                   "titles": residual}, f, indent=2, ensure_ascii=False)

    print(f"{len(candidates)} candidate pair(s) -> {args.review}")
    print(f"{len(residual)} residual title(s) -> {args.semantic} (for the semantic pass)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
on_create_check.py — the permanent book-ops mint guard.

Run this before ANY new page is minted (CLM/EVD/QUE, concept, reference, zettel,
disclosure log). It compares one proposed title against the existing set using
the five matching layers, honoring BOTH node syntaxes ("CLM — x" and
"[[CLM]] - x"), and consulting vocabulary.json for aliases, pending forks, and
the never-merge pins. It returns either `clear` (mint it) or a ranked list of
near-neighbors for you to rule on. It never writes to the graph.

    python3 on_create_check.py --title "student agency"
    python3 on_create_check.py --title "CLM — Auctor is the root capacity ..." --json
    python3 on_create_check.py --title "The developmental sequence — ability, agency, autonomy"

Exit codes (for scripting):  0 clear · 2 review (near-neighbors) · 3 blocked
(touches a never-merge pin or an unresolved pending fork).

Layers: 1 normalized-exact · 2 fuzzy token-set · 3 alias/acronym · 4 backlink-
overlap (only if inventory built --with-edges) · 5 semantic is NOT computed here
— residual near-neighbors are emitted for you/the LLM to cluster with reasons.
"""
import argparse, json, os, re, sys, unicodedata

try:
    from rapidfuzz import fuzz  # optional; better token-set ratio
    def _tsr(a, b): return int(fuzz.token_set_ratio(a, b))
except Exception:  # pure-python fallback, no dependency
    import difflib
    def _tsr(a, b):
        ta, tb = set(a.split()), set(b.split())
        if not ta or not tb:
            return 0
        inter = " ".join(sorted(ta & tb))
        sa = (inter + " " + " ".join(sorted(ta - tb))).strip()
        sb = (inter + " " + " ".join(sorted(tb - ta))).strip()
        r = max(difflib.SequenceMatcher(None, sa, sb).ratio(),
                difflib.SequenceMatcher(None, " ".join(sorted(ta)),
                                        " ".join(sorted(tb))).ratio())
        return int(r * 100)

_DASHES = {ord(c): ord("-") for c in "–—―‒−-"}
_PREFIX_RE = re.compile(r'^\s*(?:\[\[)?(CLM|EVD|QUE)(?:\]\])?\s*[-–—:]\s*(.*)$')


def split_node(title):
    """Return (TYPE or None, core-content) — collapses both node syntaxes."""
    t = title.strip()
    m = _PREFIX_RE.match(t)
    if m:
        return m.group(1), m.group(2)
    if t.startswith("@"):
        return "SRC", t[1:]
    return None, t


def normalize(title):
    _, core = split_node(title)
    core = core.strip().strip("[]").strip()
    core = unicodedata.normalize("NFKD", core)
    core = "".join(c for c in core if not unicodedata.combining(c))
    core = core.translate(_DASHES)
    core = core.replace("→", " to ").replace("/", " ")
    core = core.casefold()
    core = re.sub(r"[^\w\s-]", " ", core)     # drops trailing ? etc.
    core = re.sub(r"[-_]", " ", core)
    core = re.sub(r"\s+", " ", core).strip()
    return core


def expand_acronyms(text, acronyms):
    out = text
    for ac, full in acronyms.items():
        out = re.sub(rf"\b{re.escape(ac.casefold())}\b", full.casefold(), out)
    return out


def load(path, default):
    if not path or not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def check(title, inventory, vocab, threshold=88):
    ptype, _ = split_node(title)
    pnorm = normalize(title)
    acronyms = vocab.get("acronyms", {})
    pnorm_ac = expand_acronyms(pnorm, acronyms)

    result = {"proposed": title, "type": ptype, "normalized": pnorm,
              "verdict": "clear", "matches": [], "never_merge": [],
              "pending_fork": []}

    # --- guard: never-merge pins (report related-but-distinct, suppress score)
    for pin in vocab.get("never_merge", []):
        a, b = pin["pair"]
        if pnorm in (normalize(a), normalize(b)):
            other = b if pnorm == normalize(a) else a
            result["never_merge"].append(
                {"related_to": other, "reason": pin.get("reason", "")})

    # --- guard: pending forks (unresolved — must not mint/merge silently)
    for fork in vocab.get("pending_forks", []):
        if any(pnorm == normalize(v) for v in fork["variants"]):
            result["pending_fork"].append(
                {"variants": fork["variants"],
                 "dominant": fork.get("dominant"),
                 "note": fork.get("note", "")})

    # --- layer 3: alias registry (direct canonical resolution)
    for loser, canon in vocab.get("aliases", {}).items():
        if pnorm == normalize(loser):
            result["matches"].append(
                {"title": canon, "layer": "3-alias", "score": 100,
                 "reason": f"registered alias of proposed → canonical '{canon}'"})

    # --- layers 1/2/(4): scan the inventory
    for pg in inventory.get("pages", []):
        cand = pg["title"]
        cnorm = normalize(cand)
        if not cnorm:
            continue
        layer, score, reason = None, 0, ""
        if cnorm == pnorm:
            layer, score = "1-exact", 100
            reason = "normalized-exact collision"
        else:
            s = max(_tsr(pnorm, cnorm),
                    _tsr(pnorm_ac, expand_acronyms(cnorm, acronyms)))
            if s >= threshold:
                layer, score = "2-fuzzy", s
                reason = f"token-set ratio {s}"
        if layer:
            # layer 4: backlink overlap sharpens the signal when edges are present
            overlap = None
            if "backlink_uids" in pg and pg["backlink_uids"]:
                overlap = "edges-present (compare neighborhoods to confirm)"
            result["matches"].append({
                "title": cand, "type": pg.get("type"), "layer": layer,
                "score": score, "backlinks": pg.get("backlinks", 0),
                "children": pg.get("children", 0),
                "stub": pg.get("children", 0) == 0,
                "reason": reason + (f"; {overlap}" if overlap else "")})

    # de-dup matches by title, keep best score
    best = {}
    for m in result["matches"]:
        t = m["title"]
        if t not in best or m["score"] > best[t]["score"]:
            best[t] = m
    result["matches"] = sorted(best.values(), key=lambda m: -m["score"])

    if result["never_merge"] or result["pending_fork"]:
        result["verdict"] = "blocked"
    elif result["matches"]:
        result["verdict"] = "review"
    return result


def render(res):
    v = res["verdict"]
    tag = {"clear": "✅ CLEAR — mint it",
           "review": "🔎 REVIEW — near-neighbors, you decide",
           "blocked": "⛔ BLOCKED — pin/fork, do not mint or merge silently"}[v]
    lines = [f"{tag}", f"  proposed : {res['proposed']}",
             f"  normalized: {res['normalized']}"]
    for nm in res["never_merge"]:
        lines.append(f"  ⛔ never-merge with [[{nm['related_to']}]] — {nm['reason']}")
    for pf in res["pending_fork"]:
        lines.append(f"  ⛔ unresolved fork: {pf['note']}")
    for m in res["matches"]:
        stub = " (STUB, 0 content)" if m.get("stub") else ""
        bl = f", {m.get('backlinks', 0)} refs" if "backlinks" in m else ""
        lines.append(f"  · [{m['layer']} {m['score']}] {m['title']}"
                     f"{stub}{bl} — {m['reason']}")
    if v == "clear":
        lines.append("  (layer 5 semantic is your/the LLM's call — nothing close surfaced)")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--type", help="optional node type hint (CLM/EVD/QUE)")
    ap.add_argument("--inventory", default="inventory.json")
    ap.add_argument("--vocab", default="vocabulary.json")
    ap.add_argument("--threshold", type=int, default=88)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    inventory = load(args.inventory, {"pages": []})
    vocab = load(args.vocab, {})
    res = check(args.title, inventory, vocab, args.threshold)
    print(json.dumps(res, ensure_ascii=False, indent=2) if args.json else render(res))
    return {"clear": 0, "review": 2, "blocked": 3}[res["verdict"]]


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
export_pages.py  —  Roam -> source/ directly over the Roam backend API (READ-ONLY on Roam).

Replaces the context-expensive MCP fetch step of the nightly distill: the freshness
check (which pages are ahead of their backup) and the faithful markdown export both
run here, in one process, with no LLM in the byte path.

What it does:
  --check           Report scope: pages edited since local midnight, pages whose Roam
                    edit-time is newer than their source/ file's last commit, and any
                    manifest problems (entry resolving to 0 or 2+ live pages; live
                    "Answerable Teaching/" pages not in the manifest — exclusion
                    judgment stays with the author/distill, this only reports).
  --export stale    Export exactly the stale/edited set to source/.
  --export all      Export every mapped page (full re-export; use to verify fidelity).
  --export "Answerable Teaching/Chapter 7 — Adjacent Agency" ...
                    Export specific pages by exact title.

Rendering contract (matches the historical MCP export byte-for-byte):
  - depth d  =>  2*d spaces of indent
  - heading blocks: "#"*heading + " " + string   (no bullet)
  - other blocks:   "- " + string
  - multi-line block strings: embedded newlines verbatim, continuation lines NOT indented
  - children ordered by :block/order; nothing else is transformed
  - file ends with exactly one trailing newline (normalized going forward)

Auth: reads .roam-token (JSON: {"graph": "...", "token": "..."}) from the repo root,
overridable with ROAM_GRAPH / ROAM_API_TOKEN. The token file is gitignored — never
commit it. Roam 308-redirects to a peer host; we re-send with headers intact.

Usage (from repo root):
  python3 scripts/export_pages.py --check
  python3 scripts/export_pages.py --export stale
  python3 scripts/export_pages.py --export all --verify   # export + report diffs vs git HEAD
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

REPO = Path(__file__).resolve().parent.parent
NAMESPACE = "Answerable Teaching/"
LOCAL_TZ = ZoneInfo("America/New_York")
API = "https://api.roamresearch.com/api/graph/{graph}/{op}"
PULL_SELECTOR = "[:block/uid :block/string :block/order :block/heading {:block/children ...}]"


# ---------------------------------------------------------------- API plumbing

def _load_auth() -> tuple[str, str]:
    graph = os.environ.get("ROAM_GRAPH")
    token = os.environ.get("ROAM_API_TOKEN")
    tf = REPO / ".roam-token"
    if (not graph or not token) and tf.exists():
        cfg = json.loads(tf.read_text())
        graph = graph or cfg.get("graph")
        token = token or cfg.get("token")
    if not graph or not token:
        sys.exit("No credentials: set ROAM_GRAPH/ROAM_API_TOKEN or create .roam-token "
                 '(JSON: {"graph": "...", "token": "..."}) in the repo root.')
    return graph, token


def _post(url: str, body: dict, token: str, hops: int = 0) -> dict:
    if hops > 3:
        sys.exit("Too many redirects from the Roam API.")
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json",
                 "Authorization": f"Bearer {token}", "X-Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        if e.code in (301, 302, 307, 308):
            return _post(e.headers["Location"], body, token, hops + 1)
        sys.exit(f"Roam API error {e.code}: {e.read()[:400]}")


def roam_q(graph: str, token: str, query: str) -> list:
    out = _post(API.format(graph=graph, op="q"), {"query": query}, token)
    return out.get("result", out) if isinstance(out, dict) else out


def roam_pull(graph: str, token: str, title: str) -> dict:
    eid = f'[:node/title "{title}"]'
    out = _post(API.format(graph=graph, op="pull"),
                {"eid": eid, "selector": PULL_SELECTOR}, token)
    return out.get("result") if isinstance(out, dict) else out


# ---------------------------------------------------------------- manifest

def load_manifest() -> tuple[list[tuple[str, str]], list[re.Pattern]]:
    """SYNC.md -> (table rows [(title-as-written, filename), ...], exclusion regexes)."""
    text = (REPO / "SYNC.md").read_text()
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*(.+?)\s*\|\s*`([^`]+)`\s*\|\s*$", line)
        if m and not m.group(1).startswith("Roam page") and not set(m.group(1)) <= {"-", " "}:
            rows.append((m.group(1), m.group(2)))
    if not rows:
        sys.exit("Could not parse the filename map out of SYNC.md.")
    excl = []
    block = re.search(r"```exclude\n(.*?)```", text, re.S)
    if block:
        excl = [re.compile(p) for p in block.group(1).splitlines() if p.strip()]
    return rows, excl


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def resolve_manifest(rows: list[tuple[str, str]], excl: list[re.Pattern],
                     live_titles: list[str]) -> tuple[dict, list[str]]:
    """Match each manifest row to exactly one live page (case-insensitive; a trailing
    '…' in the row means prefix-match). Returns ({title: file}, warnings)."""
    mapping: dict[str, str] = {}
    warnings: list[str] = []
    live_ns = [t for t in live_titles if t.startswith(NAMESPACE)]
    for entry, fname in rows:
        want = _norm(entry)
        if want.endswith("…"):
            pref = _norm(NAMESPACE) + want[:-1].strip()
            hits = [t for t in live_ns if _norm(t).startswith(pref)]
        else:
            hits = [t for t in live_ns if _norm(t) == _norm(NAMESPACE) + want]
        if len(hits) == 1:
            mapping[hits[0]] = fname
        elif not hits:
            warnings.append(f"MANIFEST: '{entry}' -> {fname} matches NO live page (renamed/deleted?)")
        else:
            warnings.append(f"MANIFEST: '{entry}' -> {fname} matches {len(hits)} pages: {hits}")
    mapped = set(mapping)
    for t in live_ns:
        if t not in mapped and not any(p.search(t) for p in excl):
            warnings.append(f"UNMAPPED: '{t}' is not in the manifest and matches no SYNC.md "
                            f"exclusion pattern — possible backup drift (author's call; not auto-added).")
    return mapping, warnings


# ---------------------------------------------------------------- freshness

def page_edit_times(graph: str, token: str) -> dict[str, int]:
    q = ('[:find ?title (max ?t) :where [?p :node/title ?title] '
         f'[(clojure.string/starts-with? ?title "{NAMESPACE}")] '
         '[?b :block/page ?p] [?b :edit/time ?t]]')
    return {t: int(ms) for t, ms in roam_q(graph, token, q)}


def file_commit_s(fname: str) -> int:
    env = {**os.environ, "GIT_OPTIONAL_LOCKS": "0"}   # never leave index.lock behind (sandbox can't delete it)
    out = subprocess.run(["git", "log", "-1", "--format=%ct", "--", f"source/{fname}"],
                         cwd=REPO, capture_output=True, text=True, env=env)  # read-only git
    return int(out.stdout.strip() or 0)


def build_scope(mapping: dict[str, str], edits: dict[str, int]) -> list[dict]:
    midnight_ms = int(datetime.now(LOCAL_TZ)
                      .replace(hour=0, minute=0, second=0, microsecond=0).timestamp() * 1000)
    rows = []
    for title, fname in sorted(mapping.items(), key=lambda kv: kv[1]):
        ms = edits.get(title, 0)
        cs = file_commit_s(fname)
        rows.append({"title": title, "file": fname,
                     "roam_edit_ms": ms, "file_commit_ms": cs * 1000,
                     "edited_today": ms >= midnight_ms, "stale": ms > cs * 1000})
    return rows


# ---------------------------------------------------------------- rendering

def render_block(b: dict, depth: int, out: list[str]) -> None:
    s = b.get(":block/string")
    if s is not None:
        s = s.replace(" ", " ")   # NBSP -> space (matches the historical MCP export)
        h = b.get(":block/heading")
        prefix = "  " * depth + ("#" * h + " " if h else "- ")
        out.append(prefix + s)
    kids = sorted(b.get(":block/children", []), key=lambda c: c.get(":block/order", 0))
    for k in kids:
        render_block(k, depth + (1 if s is not None else 0), out)


def render_page(tree: dict) -> str:
    out: list[str] = []
    for k in sorted(tree.get(":block/children", []), key=lambda c: c.get(":block/order", 0)):
        render_block(k, 0, out)
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- main

def main() -> None:
    ap = argparse.ArgumentParser(description="Freshness check + faithful export, Roam -> source/.")
    ap.add_argument("--check", action="store_true", help="report scope + manifest warnings, change nothing")
    ap.add_argument("--export", nargs="+", metavar="WHAT",
                    help="'stale' | 'all' | one or more exact page titles")
    ap.add_argument("--verify", action="store_true",
                    help="after export, list files that differ from git HEAD (read-only git diff --stat)")
    ap.add_argument("--json", action="store_true", help="machine-readable --check output")
    args = ap.parse_args()
    if not args.check and not args.export:
        ap.error("nothing to do: pass --check and/or --export")

    graph, token = _load_auth()
    edits = page_edit_times(graph, token)
    rows, excl = load_manifest()
    mapping, warnings = resolve_manifest(rows, excl, list(edits))
    scope = build_scope(mapping, edits)
    todo = [r for r in scope if r["stale"] or r["edited_today"]]

    if args.check:
        if args.json:
            print(json.dumps({"warnings": warnings, "scope": todo, "all": scope}, indent=2))
        else:
            for w in warnings:
                print("⚠", w)
            if not todo:
                print("Nothing to back up — every mapped page is current.")
            for r in todo:
                flag = "edited-today" if r["edited_today"] else "stale-vs-backup"
                print(f"{flag:16} {r['file']:28} {r['title']}")

    if args.export:
        if args.export == ["stale"]:
            targets = todo
        elif args.export == ["all"]:
            targets = scope
        else:
            by_title = {r["title"]: r for r in scope}
            missing = [t for t in args.export if t not in by_title]
            if missing:
                sys.exit(f"Not in manifest/graph: {missing}")
            targets = [by_title[t] for t in args.export]
        for r in targets:
            tree = roam_pull(graph, token, r["title"])
            if not tree:
                sys.exit(f"Pull returned nothing for '{r['title']}'")
            (REPO / "source" / r["file"]).write_text(render_page(tree))
            print(f"exported {r['file']}  <-  {r['title']}")
        if args.verify:
            out = subprocess.run(["git", "diff", "--stat", "--", "source/"],
                                 cwd=REPO, capture_output=True, text=True,
                                 env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
            print(out.stdout or "verify: source/ is identical to git HEAD.")

    if warnings and not args.check:
        for w in warnings:
            print("⚠", w, file=sys.stderr)


if __name__ == "__main__":
    main()

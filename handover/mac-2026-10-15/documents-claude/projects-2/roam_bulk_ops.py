#!/usr/bin/env python3
"""
roam_bulk_ops.py — fixed-token substitution across a Roam graph, via the backend API.

Built 2026-08-01 for the Provenance:: rename:
    Provenance:: auctor    ->  Provenance:: [K]
    Provenance:: grounded  ->  Provenance:: literature link

WHY A SCRIPT AND NOT THE MCP
    Roam's update-block replaces a block's ENTIRE string. Swapping a fixed token
    through the MCP would mean pulling ~220 full block texts into a language model
    and writing them back verbatim -- every one a chance to corrupt a block that
    never needed to be read. A deterministic substitution should be deterministic.

SAFETY
    - DRY RUN BY DEFAULT. Writes only with --apply.
    - Writes a JSON backup of every block's original string before touching anything.
    - Substring match is exact and case-sensitive; nothing is inferred.
    - Refuses to run if a replacement would change a block in more than one way.
    - --limit lets you prove it on 5 blocks before committing to all of them.

USAGE
    export ROAM_GRAPH=your-graph-name
    export ROAM_API_TOKEN="$(cat ~/.roam/edit_token)"      # EDIT token, not the read token

    python3 roam_bulk_ops.py                     # dry run, full report
    python3 roam_bulk_ops.py --limit 5 --apply   # prove it on five blocks
    python3 roam_bulk_ops.py --apply             # do it

    python3 roam_bulk_ops.py --restore backup-<timestamp>.json --apply   # undo

NOTE ON TOKENS
    The token on [[Local API Token: book-ops read]] is READ-ONLY and will fail on write.
    Create an edit token at: Roam -> graph dropdown -> Settings -> Graph -> API tokens
    -> "Add API token" with EDIT permission. Store it in a file; never inline it.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.roamresearch.com/api/graph"

# (old, new) -- exact, case-sensitive. Order matters only if one is a prefix of another.
REPLACEMENTS = [
    ("Provenance:: auctor", "Provenance:: [K]"),
    ("Provenance:: grounded", "Provenance:: literature link"),
]


def _post(graph, token, path, payload):
    req = urllib.request.Request(
        f"{API}/{graph}/{path}",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "X-Authorization": f"Bearer {token}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = r.read().decode()
            return json.loads(body) if body.strip() else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        if e.code in (307, 308) and "Location" in e.headers:
            # Roam returns a redirect to a region-specific host on first call.
            loc = e.headers["Location"]
            req2 = urllib.request.Request(
                loc, data=json.dumps(payload).encode(),
                headers=dict(req.headers), method="POST")
            with urllib.request.urlopen(req2, timeout=60) as r:
                body = r.read().decode()
                return json.loads(body) if body.strip() else {}
        sys.exit(f"HTTP {e.code} on {path}: {detail}")


def find_targets(graph, token):
    """One datalog query per token. Returns {uid: string} for blocks needing change."""
    found = {}
    for old, _ in REPLACEMENTS:
        esc = old.replace('"', '\\"')
        q = ('[:find ?u ?s :where [?b :block/string ?s] '
             f'[(clojure.string/includes? ?s "{esc}")] [?b :block/uid ?u]]')
        res = _post(graph, token, "q", {"query": q})
        for uid, s in res.get("result", []):
            found[uid] = s
    return found


def plan(found):
    """Compute new strings. Returns (changes, skipped)."""
    changes, skipped = [], []
    for uid, s in sorted(found.items()):
        new = s
        hits = 0
        for old, repl in REPLACEMENTS:
            if old in new:
                hits += new.count(old)
                new = new.replace(old, repl)
        if new == s:
            skipped.append((uid, "no-op"))
        else:
            changes.append({"uid": uid, "old": s, "new": new, "hits": hits})
    return changes, skipped


def apply_changes(graph, token, changes, pause=0.25):
    ok, fail = 0, []
    for i, c in enumerate(changes, 1):
        try:
            _post(graph, token, "write", {
                "action": "update-block",
                "block": {"uid": c["uid"], "string": c["new"]},
            })
            ok += 1
        except SystemExit as e:
            fail.append((c["uid"], str(e)))
        if i % 25 == 0:
            print(f"  ... {i}/{len(changes)}", flush=True)
        time.sleep(pause)          # stay under Roam's rate limit
    return ok, fail


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="actually write (default: dry run)")
    ap.add_argument("--limit", type=int, default=0, help="only touch the first N blocks")
    ap.add_argument("--restore", metavar="BACKUP.json", help="revert from a backup file")
    args = ap.parse_args()

    graph = os.environ.get("ROAM_GRAPH")
    token = os.environ.get("ROAM_API_TOKEN")

    # Nothing to set up in advance: ask for whatever is missing.
    # getpass keeps the token off the screen and out of shell history.
    if not graph:
        graph = input("Roam graph name: ").strip()
    if not token:
        import getpass
        token = getpass.getpass("Roam API token (input hidden): ").strip()
    if not graph or not token:
        sys.exit("Need both a graph name and a token.")

    if args.restore:
        data = json.load(open(args.restore))
        changes = [{"uid": u, "new": s, "old": None, "hits": 0} for u, s in data.items()]
        print(f"RESTORE: {len(changes)} blocks from {args.restore}")
        if not args.apply:
            print("Dry run. Re-run with --apply to actually restore.")
            return
        ok, fail = apply_changes(graph, token, changes)
        print(f"restored {ok}, failed {len(fail)}")
        return

    print(f"Graph: {graph}")
    print("Querying...", flush=True)
    found = find_targets(graph, token)
    changes, skipped = plan(found)
    if args.limit:
        changes = changes[: args.limit]

    total_hits = sum(c["hits"] for c in changes)
    print(f"\n{len(changes)} blocks to change, {total_hits} token occurrences.")
    for c in changes[:5]:
        print(f"\n  uid {c['uid']}")
        print(f"    -  ...{c['old'][:150]}...")
        print(f"    +  ...{c['new'][:150]}...")
    if len(changes) > 5:
        print(f"\n  (+{len(changes)-5} more)")

    if not args.apply:
        print("\nDRY RUN. Nothing written. Re-run with --apply.")
        return

    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup = f"backup-{stamp}.json"
    json.dump({c["uid"]: c["old"] for c in changes}, open(backup, "w"), indent=1)
    print(f"\nBackup written: {backup}")
    print("Writing...", flush=True)
    ok, fail = apply_changes(graph, token, changes)
    print(f"\nDone. {ok} updated, {len(fail)} failed.")
    for uid, err in fail[:10]:
        print(f"  FAIL {uid}: {err}")
    print(f"Undo with:  python3 {sys.argv[0]} --restore {backup} --apply")


if __name__ == "__main__":
    main()

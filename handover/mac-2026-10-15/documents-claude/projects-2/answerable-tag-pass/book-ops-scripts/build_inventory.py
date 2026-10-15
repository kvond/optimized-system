#!/usr/bin/env python3
"""
build_inventory.py — pull the Roam book graph into inventory.json, the snapshot
that on_create_check.py and dedup_sweep.py run against.

The schema is the only contract downstream; it does not matter which path
produced it. Two pull paths (SKILL: "either path"):

  1. Direct  — hit Roam's backend API with a read token (no MCP needed):
       ROAM_API_TOKEN=... ROAM_GRAPH=default python3 build_inventory.py --out inventory.json

  2. From MCP — if you'd rather run the three datalog queries through the Roam
     MCP (in Cowork/Claude), dump each result to a JSON file and assemble:
       python3 build_inventory.py --from-mcp ./pulls --out inventory.json
     where ./pulls holds pages.json, backlinks.json, children.json — each the
     raw ":find" result (a list of rows) of the queries printed by --show-queries.

inventory.json schema:
  {
    "graph": "default",
    "generated": "2026-07-02T13:44:00Z",
    "pages": [
      {"uid": "...", "title": "...", "backlinks": 12, "children": 4, "type": "CLM"},
      ...
    ]
  }
type is inferred from the title prefix (CLM/EVD/QUE/@=SRC) or left null.
Pass --with-edges to also record each page's backlink source-uids
(enables on_create_check layer 4, backlink-overlap). Heavier pull.
"""
import argparse, json, os, re, sys, time, urllib.request, urllib.error

# ---- The three datalog queries. Run these through the MCP for path 2, or the
#      script POSTs them for path 1. Keep them here so both paths give one schema.
PAGES_Q = '[:find ?uid ?title :where [?p :node/title ?title] [?p :block/uid ?uid]]'
BACKLINKS_Q = ('[:find ?title (count ?b) :where [?p :node/title ?title] '
               '[?b :block/refs ?p]]')
CHILDREN_Q = ('[:find ?title (count ?c) :where [?p :node/title ?title] '
              '[?c :block/page ?p]]')
EDGES_Q = ('[:find ?title ?buid :where [?p :node/title ?title] '
           '[?b :block/refs ?p] [?b :block/uid ?buid]]')

API_BASE = "https://api.roamresearch.com"


def infer_type(title):
    m = re.match(r'^\s*(?:\[\[)?(CLM|EVD|QUE)(?:\]\])?\s*[-–—:]', title)
    if m:
        return m.group(1)
    if title.startswith("@"):
        return "SRC"
    return None


def _post(url, token, query):
    body = json.dumps({"query": query, "args": []}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("x-authorization", "Bearer " + token)
    return urllib.request.urlopen(req, timeout=60)


def roam_query(token, graph, query, _depth=0):
    """POST a datalog query to Roam's backend API, following its peer redirect."""
    url = f"{API_BASE}/api/graph/{graph}/q"
    try:
        resp = _post(url, token, query)
        return json.loads(resp.read().decode("utf-8")).get("result", [])
    except urllib.error.HTTPError as e:
        # Roam redirects (307/308) to a specific peer host; re-POST there.
        if e.code in (307, 308) and _depth < 5:
            loc = e.headers.get("Location")
            if loc:
                body = json.dumps({"query": query, "args": []}).encode("utf-8")
                req = urllib.request.Request(loc, data=body, method="POST")
                req.add_header("Content-Type", "application/json")
                req.add_header("Authorization", "Bearer " + token)
                req.add_header("x-authorization", "Bearer " + token)
                resp = urllib.request.urlopen(req, timeout=60)
                return json.loads(resp.read().decode("utf-8")).get("result", [])
        raise


def assemble(pages_rows, backlink_rows, children_rows, edge_rows=None):
    backlinks = {t: n for t, n in backlink_rows}
    children = {t: n for t, n in children_rows}
    edges = {}
    if edge_rows:
        for t, buid in edge_rows:
            edges.setdefault(t, set()).add(buid)
    pages = []
    for uid, title in pages_rows:
        rec = {
            "uid": uid,
            "title": title,
            "backlinks": int(backlinks.get(title, 0)),
            "children": int(children.get(title, 0)),
            "type": infer_type(title),
        }
        if edge_rows is not None:
            rec["backlink_uids"] = sorted(edges.get(title, ()))
        pages.append(rec)
    pages.sort(key=lambda r: r["title"].casefold())
    return pages


def load_rows(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main():
    ap = argparse.ArgumentParser(description="Build inventory.json for book-ops.")
    ap.add_argument("--out", default="inventory.json")
    ap.add_argument("--from-mcp", metavar="DIR",
                    help="assemble from pages.json/backlinks.json/children.json in DIR")
    ap.add_argument("--with-edges", action="store_true",
                    help="also record backlink source-uids (layer-4 overlap)")
    ap.add_argument("--show-queries", action="store_true",
                    help="print the datalog queries (for the MCP path) and exit")
    args = ap.parse_args()

    if args.show_queries:
        print("PAGES_Q     ->", PAGES_Q)
        print("BACKLINKS_Q ->", BACKLINKS_Q)
        print("CHILDREN_Q  ->", CHILDREN_Q)
        if args.with_edges:
            print("EDGES_Q     ->", EDGES_Q)
        return 0

    if args.from_mcp:
        d = args.from_mcp
        pages = load_rows(os.path.join(d, "pages.json"))
        backlinks = load_rows(os.path.join(d, "backlinks.json"))
        children = load_rows(os.path.join(d, "children.json"))
        edges = None
        edge_path = os.path.join(d, "edges.json")
        if args.with_edges and os.path.exists(edge_path):
            edges = load_rows(edge_path)
    else:
        token = os.environ.get("ROAM_API_TOKEN")
        graph = os.environ.get("ROAM_GRAPH", "default")
        if not token:
            sys.exit("ERROR: set ROAM_API_TOKEN (or use --from-mcp DIR). "
                     "Token: Roam graph → Settings → Graph → API tokens (read).")
        pages = roam_query(token, graph, PAGES_Q)
        backlinks = roam_query(token, graph, BACKLINKS_Q)
        children = roam_query(token, graph, CHILDREN_Q)
        edges = roam_query(token, graph, EDGES_Q) if args.with_edges else None

    inventory = {
        "graph": os.environ.get("ROAM_GRAPH", "default"),
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pages": assemble(pages, backlinks, children, edges),
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(inventory, fh, ensure_ascii=False, indent=2)
    print(f"wrote {args.out}: {len(inventory['pages'])} pages"
          f"{' (with edges)' if edges is not None else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

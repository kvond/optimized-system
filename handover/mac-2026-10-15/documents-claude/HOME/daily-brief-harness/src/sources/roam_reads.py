"""The eight trigger reads, per SKILL.md LAST-RUN DERIVATION.

Honest-render rules are enforced here: a missing artifact yields
{'last_run': None, 'note': 'last run unknown'}; a scaffold with empty
Status children yields 'never run'. Nothing substitutes today's date.
"""
import re
from ..clients import roam

DATE_RE = re.compile(r"\[\[(\w+ \d+\w*, \d{4}|\d{2}-\d{2}-\d{4})\]\]")

def _page_string_blocks(cfg, page_title):
    q = """[:find ?uid ?s :in $ ?title :where
           [?p :node/title ?title] [?b :block/page ?p]
           [?b :block/uid ?uid] [?b :block/string ?s]]"""
    return roam.q(cfg["roam_graph"], q, [page_title])

def _first_date_in(blocks, containing: str):
    for _uid, s in blocks:
        if containing.lower() in s.lower():
            m = DATE_RE.search(s)
            return m.group(1) if m else None
    return None

def route(cfg):
    blocks = _page_string_blocks(cfg, "daily-route")
    wm = _first_date_in(blocks, "last-processed")
    return {"last_run": wm, "watermark": wm,
            "note": None if wm else "last run unknown — no last-processed line"}

def book_distill(cfg):
    q = """[:find ?title ?s :where
           [?b :block/string ?s] [(clojure.string/includes? ?s "Book Distill")]
           [?b :block/page ?p] [?p :node/title ?title]
           [?p :block/uid ?uid]]"""
    rows = roam.q(cfg["roam_graph"], q)
    daily = [(t, s) for t, s in rows if re.match(r"\w+ \d", t or "")]
    if not daily:
        return {"last_run": None, "note": "never run"}
    t, s = sorted(daily)[-1]
    stage = re.search(r"(\d/4[^·\n]*)", s)
    return {"last_run": t, "stage": stage.group(1).strip() if stage else None}

def live_mints(cfg):
    q = """[:find ?s ?time :where
           [?b :block/refs ?tag] [?tag :node/title "minted-live"]
           [?b :block/string ?s] [?b :create/time ?time]]"""
    rows = roam.q(cfg["roam_graph"], q)
    if not rows:
        return {"count": 0}
    oldest = min(r[1] for r in rows)
    oldest_title = [r[0] for r in rows if r[1] == oldest][0]
    return {"count": len(rows), "oldest_ms": oldest, "oldest_title": oldest_title}

def learning_block(cfg):
    q = """[:find ?title :where
           [?b :block/string ?s] [(clojure.string/includes? ?s "Learning Block")]
           [?b :block/page ?p] [?p :node/title ?title]]"""
    rows = [t[0] for t in roam.q(cfg["roam_graph"], q) if re.match(r"\w+ \d", t[0] or "")]
    lb = _page_string_blocks(cfg, "Learn Block")
    uke = next((s for _u, s in lb if "Stu Fuchs goal::" in s), None)
    return {"last_run": sorted(rows)[-1] if rows else None,
            "uke_goal": uke.split("::", 1)[1].strip() if uke else None,
            "note": None if rows else "never run"}

def block_update(cfg, which):  # 'WilmU Block' | 'AIHS Block'
    blocks = _page_string_blocks(cfg, which)
    if not blocks:
        return {"last_run": None, "note": "the page needs building"}
    processed = _first_date_in(blocks, "Processed")
    status_children = [s for _u, s in blocks if s.strip() in ("—", "-")]
    if status_children or not processed:
        return {"last_run": processed, "note": "never run"
                if processed else "the page needs building"}
    return {"last_run": processed}

def tasks(cfg):
    blocks = _page_string_blocks(cfg, "📋 TASKS")
    header_date = _first_date_in(blocks, "Distilled")
    todo_count = sum(1 for _u, s in blocks if "{{[[TODO]]}}" in s)
    return {"last_run": header_date, "work_items": todo_count,
            "note": None if header_date else "last run unknown"}

def sweep(cfg):
    blocks = _page_string_blocks(cfg, "book-ops state")
    stamp = _first_date_in(blocks, "last-run")
    return {"last_run": stamp,
            "note": None if stamp else
            "last run unknown — book-ops keeps rulings, not a run log"}

def all_triggers(cfg):
    return {
        "route": route(cfg),
        "book-distill": book_distill(cfg),
        "mint-review": live_mints(cfg),
        "learning-block-agenda": learning_block(cfg),
        "wilmu-update": block_update(cfg, "WilmU Block"),
        "aihs-update": block_update(cfg, "AIHS Block"),
        "tasks": tasks(cfg),
        "sweep": sweep(cfg),
    }

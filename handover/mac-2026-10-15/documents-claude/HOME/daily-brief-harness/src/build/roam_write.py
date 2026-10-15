"""One 📅 Daily Brief block on the Roam daily page, assembled as a single
batch-actions call. Daily-page UID is MM-DD-YYYY, used directly as
parent-uid — never searched for. Re-runs are idempotent: an existing
'📅 Daily Brief' block for the day is deleted first.

The first child is the stable link to the hosted page, so the phone-readable
brief is one tap from the graph.
"""
import secrets as _secrets
from ..clients import roam

def _uid():
    return _secrets.token_urlsafe(6)[:9]

def _flatten(parent_uid, nodes, order_start=0, actions=None):
    actions = actions if actions is not None else []
    for i, node in enumerate(nodes, order_start):
        uid = _uid()
        actions.append({"action": "create-block",
                        "location": {"parent-uid": parent_uid, "order": i},
                        "block": {"string": node["string"], "uid": uid}})
        if node.get("children"):
            _flatten(uid, node["children"], 0, actions)
    return actions

def _existing_brief_uid(cfg, page_uid):
    q = """[:find ?uid :in $ ?puid :where
           [?p :block/uid ?puid] [?b :block/parents ?p]
           [?b :block/uid ?uid] [?b :block/string ?s]
           [(clojure.string/includes? ?s "📅 **Daily Brief")]]"""
    rows = roam.q(cfg["roam_graph"], q, [page_uid])
    return rows[0][0] if rows else None

def stamp(cfg, page_uid: str, tree: dict):
    """tree = {'string': header, 'children': [...]} per SKILL.md ROAM OUTPUT."""
    old = _existing_brief_uid(cfg, page_uid)
    actions = []
    if old:
        actions.append({"action": "delete-block", "block": {"uid": old}})
    root_uid = _uid()
    actions.append({"action": "create-block",
                    "location": {"parent-uid": page_uid, "order": 0},
                    "block": {"string": tree["string"], "uid": root_uid}})
    _flatten(root_uid, tree.get("children", []), 0, actions)
    return roam.write(cfg["roam_graph"], actions)

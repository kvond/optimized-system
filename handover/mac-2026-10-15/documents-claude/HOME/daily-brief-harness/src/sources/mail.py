"""Gmail pass. Deterministic gathering; the model only judges.

Two candidate pools:
  1. Inbox threads from the last `lookback_days` — possible NEEDS ATTENTION
     or RESOLVED. A thread whose LAST message is from Katherine is dropped
     here, in code — 'drop it if Katherine already replied' is not a model
     judgment.
  2. Her SENT threads older than `sent_silence_days` with no reply after —
     the silences, phrased later as such.
"""
import base64, os
from datetime import date, timedelta
from ..clients.google_api import gmail

def _headers(msg):
    return {h["name"].lower(): h["value"] for h in msg["payload"].get("headers", [])}

def _snippet_chain(svc, thread_id):
    t = svc.users().threads().get(userId="me", id=thread_id, format="metadata",
                                  metadataHeaders=["From", "To", "Subject", "Date"]).execute()
    msgs = t.get("messages", [])
    chain = []
    for m in msgs:
        h = _headers(m)
        chain.append({
            "from": h.get("from", ""), "date": h.get("date", ""),
            "subject": h.get("subject", ""), "snippet": m.get("snippet", ""),
            "labels": m.get("labelIds", []),
        })
    return chain

def fetch_candidates(cfg, today: date):
    svc = gmail()
    me = svc.users().getProfile(userId="me").execute()["emailAddress"].lower()
    after = (today - timedelta(days=cfg["gmail"]["lookback_days"])).strftime("%Y/%m/%d")

    inbox, silences = [], []

    resp = svc.users().threads().list(userId="me", q=f"in:inbox after:{after}",
                                      maxResults=40).execute()
    for t in resp.get("threads", []):
        chain = _snippet_chain(svc, t["id"])
        if not chain:
            continue
        if me in chain[-1]["from"].lower():
            continue  # she already replied — dropped in code, not by the model
        inbox.append({"thread_id": t["id"], "chain": chain,
                      "link": f"https://mail.google.com/mail/u/0/#all/{t['id']}"})

    sil_after = (today - timedelta(days=14)).strftime("%Y/%m/%d")
    sil_before = (today - timedelta(days=cfg["gmail"]["sent_silence_days"])).strftime("%Y/%m/%d")
    resp = svc.users().threads().list(
        userId="me", q=f"in:sent after:{sil_after} before:{sil_before}",
        maxResults=30).execute()
    for t in resp.get("threads", []):
        chain = _snippet_chain(svc, t["id"])
        if chain and me in chain[-1]["from"].lower():  # last word is hers → unanswered
            silences.append({"thread_id": t["id"], "chain": chain,
                             "link": f"https://mail.google.com/mail/u/0/#all/{t['id']}"})
    return {"inbox": inbox, "silences": silences, "me": me}

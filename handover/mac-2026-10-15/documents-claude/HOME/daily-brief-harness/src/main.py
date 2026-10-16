"""Orchestrator. Deterministic gathering → two model calls → two outputs.

Failure posture: a source that errors degrades to an honest line in the
brief ("Gmail unreachable this morning"), never a crash that leaves no page.
The Roam write failing prints the full block text to the Actions log so it
can be pasted — same contract as the skill.
"""
import json, sys, traceback
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo
import yaml

from .clients.llm import ask
from .sources import agenda, calendar_src, mail, roam_reads
from .build import terrain, html_render, roam_write

ROOT = Path(__file__).resolve().parents[1]

TRIGGER_LABELS = {
    "route": ("🧭 ROUTE", "run daily-route"),
    "book-distill": ("📖 BOOK DISTILL", "run chapter-bank"),
    "mint-review": ("📇 LIVE MINTS", "review queue"),
    "learning-block-agenda": ("🎧 LEARNING BLOCK", "run learning-block"),
    "wilmu-update": ("🎓 WILMU UPDATE", "run block-update (WilmU)"),
    "aihs-update": ("🍎 AIHS UPDATE", "run block-update (AIHS)"),
    "tasks": ("📋 TASKS", "run task-distill"),
    "sweep": ("🧹 SWEEP", "run book-ops · also auto 8 pm"),
}

def load_cfg():
    return yaml.safe_load((ROOT / "config.yaml").read_text())

def _try(label, fn, fallback):
    try:
        return fn(), None
    except Exception as e:
        traceback.print_exc()
        return fallback, f"{label} unreachable this morning ({type(e).__name__})"

def _days_since(cfg, roam_date_str, today):
    """Roam dates arrive as 'August 2nd, 2026' or '08-02-2026'."""
    if not roam_date_str:
        return None
    s = roam_date_str.replace("st,", ",").replace("nd,", ",").replace("rd,", ",").replace("th,", ",")
    for fmt in ("%B %d, %Y", "%m-%d-%Y"):
        try:
            return (today - datetime.strptime(s, fmt).date()).days
        except ValueError:
            continue
    return None

def trigger_line(key, data, cfg, today):
    label, verb = TRIGGER_LABELS[key]
    if key == "mint-review":
        n = data.get("count", 0)
        if not n:
            return label, "0 provisional"
        age = (datetime.now(tz=ZoneInfo(cfg["timezone"])).timestamp() * 1000 - data["oldest_ms"]) / 86_400_000
        return label, f"{n} provisional · oldest {age:.0f}d"
    lr = data.get("last_run")
    d = _days_since(cfg, lr, today)
    stamp = f"last run {lr} · {d}d" if lr and d is not None else \
            (f"last run {lr}" if lr else (data.get("note") or "never run"))
    extras = []
    if key == "route" and data.get("watermark"):
        extras.append(f"watermark {data['watermark']}")
    if key == "book-distill" and data.get("stage"):
        extras.append(data["stage"])
    if key == "learning-block-agenda":
        extras.append("Spanish ×4")
        if data.get("uke_goal"):
            extras.append(f"Uke: {data['uke_goal']}")
    if key == "tasks" and data.get("work_items") is not None:
        extras.append(f"{data['work_items']} work items")
    if data.get("note") and lr:
        extras.append(data["note"])
    return label, " · ".join([f"{verb} · {stamp}"] + extras)

def main():
    cfg = load_cfg()
    tz = ZoneInfo(cfg["timezone"])
    today = datetime.now(tz).date()
    day_label = today.strftime("%A · %B %-d %Y")
    degraded = []

    week_row, err = _try("Master Agenda", lambda: agenda.week_row_for(cfg, today), None)
    if err: degraded.append(err)
    mode = agenda.classify(cfg, today, week_row)

    (today_ev, ahead_ev), err = _try("Calendar", lambda: calendar_src.fetch(cfg, today), ([], []))
    if err: degraded.append(err)
    is_travel = calendar_src.travel_day(today_ev, cfg["timezone"])

    mail_data, err = _try("Gmail", lambda: mail.fetch_candidates(cfg, today),
                          {"inbox": [], "silences": [], "me": ""})
    if err: degraded.append(err)

    trig, err = _try("Roam", lambda: roam_reads.all_triggers(cfg), {})
    if err: degraded.append(err)

    # ── Model call 1: mail triage ────────────────────────────────────
    needs, resolved = [], []
    if mail_data["inbox"] or mail_data["silences"]:
        payload = {"inbox": mail_data["inbox"],
                   "silences": [dict(t, marker="[SILENCE]") for t in mail_data["silences"]]}
        raw = ask(cfg, (ROOT / "prompts" / "mail_triage.md").read_text(),
                  json.dumps(payload, default=str), force_json=True)
        triage = json.loads(raw)
        links = {t["thread_id"]: t["link"]
                 for t in mail_data["inbox"] + mail_data["silences"]}
        for it in triage.get("needs_attention", []):
            it["link"] = links.get(it.get("thread_id"))
            needs.append(it)
        for it in triage.get("resolved", []):
            it["link"] = links.get(it.get("thread_id"))
            resolved.append(it)

    # ── Model call 2: headline, acts, attend-first ───────────────────
    esc = []
    mr = trig.get("mint-review", {})
    if mr.get("count") and mr.get("oldest_ms"):
        age_d = (datetime.now(tz).timestamp() * 1000 - mr["oldest_ms"]) / 86_400_000
        if age_d >= cfg["mint_review"]["age_escalation_days"]:
            esc.append(f"ESCALATED: review live mint '{mr['oldest_title'][:80]}' — {age_d:.0f}d old")
    day_ctx = {
        "date": day_label, "mode": mode, "travel_day": is_travel,
        "bell": cfg["bell"] if mode == "SCHOOL" else None,
        "agenda_row": week_row["raw"] if week_row else None,
        "events": today_ev, "escalations": esc,
        "needs_attention_titles": [n["title"] for n in needs],
        "summer_blocks": ["Deep work", "Gym", "Deep work",
                          "Practice — vocal / Spanish / uke (rotates)"]
                         if mode == "SUMMER" and not is_travel else None,
    }
    raw = ask(cfg, (ROOT / "prompts" / "headline_acts.md").read_text(),
              json.dumps(day_ctx, default=str), force_json=True)
    ha = json.loads(raw)

    svg = terrain.build(today_ev, ha.get("motif"))
    lines = [trigger_line(k, trig.get(k, {}), cfg, today) for k in cfg["emit_order"] if k in TRIGGER_LABELS]

    ahead = []
    for ev in ahead_ev:
        d = datetime.fromisoformat(ev["start"][:19]).strftime("%a %-m/%-d") \
            if not ev["all_day"] else datetime.strptime(ev["start"], "%Y-%m-%d").strftime("%a %-m/%-d")
        t = "" if ev["all_day"] else datetime.fromisoformat(ev["start"]).strftime(" · %-I:%M %p")
        ahead.append((d, f"{ev['title']}{t}"))

    carry = " · ".join(degraded) if degraded else None

    html = html_render.render(day_label, ha["headline"], svg, ha["acts"],
                              needs, resolved, lines, carry, ahead, None)
    site = ROOT / "site"; site.mkdir(exist_ok=True)
    (site / "index.html").write_text(html)
    print(f"HTML written · {len(html)//1024}KB")

    # ── Roam stamp ───────────────────────────────────────────────────
    header = f"📅 **Daily Brief — {today.strftime('%A, %B %-d, %Y')}** · {'travel day' if is_travel else mode}"
    kids = [{"string": f"🔗 [Today's page]({cfg['site_url']})"}]
    if mode == "SCHOOL" and not is_travel:
        kids.append({"string": "⏰ " + " · ".join(f"{k} {v}" for k, v in cfg["bell"].items())})
    if today_ev:
        kids.append({"string": "Today's calendar",
                     "children": [{"string": f"{e['start'][11:16] if not e['all_day'] else 'all day'} — {e['title']}"}
                                  for e in today_ev]})
    if ha.get("attend_first"):
        kids.append({"string": "✅ ATTEND-TO-FIRST",
                     "children": [{"string": f"{i}. {t}"} for i, t in enumerate(ha["attend_first"][:3], 1)]})
    if resolved:
        kids.append({"string": "RESOLVED",
                     "children": [{"string": r["sentence"]} for r in resolved]})
    kids.append({"string": "── TRIGGERS ── (tap when ready; emitting a line writes nothing)",
                 "children": [{"string": f"{lab} → {state}"} for lab, state in lines]})
    if ahead:
        kids.append({"string": "👀 LOOK-AHEAD (next 14d)",
                     "children": [{"string": f"{d} — {w}"} for d, w in ahead]})
    tree = {"string": header, "children": kids}
    page_uid = today.strftime("%m-%d-%Y")
    try:
        roam_write.stamp(cfg, page_uid, tree)
        print("Roam stamp landed on", page_uid)
    except Exception:
        traceback.print_exc()
        print("ROAM WRITE DID NOT LAND — paste this block:\n")
        print(json.dumps(tree, ensure_ascii=False, indent=1))
        sys.exit(0)  # page still deployed; the brief is not a failure

if __name__ == "__main__":
    main()

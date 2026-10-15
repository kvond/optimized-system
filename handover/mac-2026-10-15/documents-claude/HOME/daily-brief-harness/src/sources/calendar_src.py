"""All calendars, today + lookahead. `list_calendars` first, then one
events call per calendar — Appts is separate from Routine and regularly
non-empty; reading only primary is the documented failure mode.
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from ..clients.google_api import gcal

def fetch(cfg, day):
    tz = ZoneInfo(cfg["timezone"])
    start = datetime.combine(day, datetime.min.time(), tz)
    end_today = start + timedelta(days=1)
    end_ahead = start + timedelta(days=cfg["calendar"]["lookahead_days"] + 1)
    svc = gcal()
    cals = svc.calendarList().list().execute().get("items", [])
    today_events, ahead_events = [], []
    for cal in cals:
        resp = svc.events().list(
            calendarId=cal["id"], singleEvents=True, orderBy="startTime",
            timeMin=start.isoformat(), timeMax=end_ahead.isoformat(),
            maxResults=250).execute()
        for ev in resp.get("items", []):
            if ev.get("status") == "cancelled":
                continue
            s = ev["start"].get("dateTime") or ev["start"].get("date")
            e = ev["end"].get("dateTime") or ev["end"].get("date")
            rec = {
                "calendar": cal.get("summaryOverride") or cal.get("summary"),
                "title": ev.get("summary", "(untitled)"),
                "start": s, "end": e,
                "all_day": "date" in ev["start"],
                "self_response": _my_response(ev),
                "link": ev.get("htmlLink"),
            }
            (today_events if s < end_today.isoformat() else ahead_events).append(rec)
    today_events.sort(key=lambda r: r["start"])
    ahead_events.sort(key=lambda r: r["start"])
    return today_events, ahead_events

def _my_response(ev):
    for a in ev.get("attendees", []):
        if a.get("self"):
            return a.get("responseStatus")
    return None

def travel_day(today_events, tz_name) -> bool:
    """One timed block of ≥6h (flight, tour, drive) → travel day, blocks off."""
    for ev in today_events:
        if ev["all_day"]:
            continue
        try:
            s = datetime.fromisoformat(ev["start"]); e = datetime.fromisoformat(ev["end"])
            if (e - s) >= timedelta(hours=6):
                return True
        except ValueError:
            continue
    return False

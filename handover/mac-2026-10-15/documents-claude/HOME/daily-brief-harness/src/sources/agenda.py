"""Master Agenda read: find the week row covering the target date, extract
mode, day type (for Fridays), Bio / A&P topics, Notes-due / DRAFT-due flags.

The grid layout is read defensively: we scan every row for a date range or a
date cell matching the target, rather than assuming fixed columns. First run
prints the matched row so the mapping can be corrected once, in config, if
the v5 grid shifts.
"""
from datetime import date
from ..clients.google_api import sheets

def read_grid(cfg) -> list[list[str]]:
    rng = f"'{cfg['master_agenda_tab']}'!A1:Z400" if cfg["master_agenda_tab"] else "A1:Z400"
    resp = sheets().spreadsheets().values().get(
        spreadsheetId=cfg["master_agenda_sheet_id"], range=rng).execute()
    return resp.get("values", [])

def _cell_mentions_date(cell: str, d: date) -> bool:
    """Match common US formats the agenda uses: 8/12, 08/12, Aug 12."""
    cell = cell.strip().lower()
    forms = {
        f"{d.month}/{d.day}", f"{d.month:02d}/{d.day:02d}",
        d.strftime("%b %-d").lower() if hasattr(d, "strftime") else "",
        d.strftime("%b %d").lower(),
    }
    return any(f and f in cell for f in forms)

def week_row_for(cfg, d: date) -> dict | None:
    """Return {'row': [...], 'row_index': n, 'raw': joined} or None → SUMMER/BREAK."""
    grid = read_grid(cfg)
    for i, row in enumerate(grid):
        for cell in row:
            if isinstance(cell, str) and _cell_mentions_date(cell, d):
                return {"row": row, "row_index": i, "raw": " | ".join(row)}
    return None

def classify(cfg, d: date, week_row: dict | None) -> str:
    """SUMMER | OFF-DAY | SCHOOL. OFF/IN-SERVICE detection is textual."""
    if week_row is None:
        return "SUMMER"
    raw = week_row["raw"].upper()
    if "OFF" in raw.split() or "IN-SERVICE" in raw or "INSERVICE" in raw:
        # Row-level flag; the renderer still shows the raw row so a false OFF is visible.
        return "OFF-DAY"
    return "SCHOOL"

"""Render student feedback PDFs in the four approved layouts.

Input is one JSON report (see ../SKILL.md section 4 and ../examples/). Keep report JSON and
PDFs in a private folder outside any Git checkout; the renderer refuses an output path inside one.
Usage:
    python3 render.py report.json out.pdf
Layouts (report["layout"]):
    lesson_onepage  - one-lesson critical-aspect feedback (Biology, Forensics)
    lessons_grouped - A&P feedback: critical aspects grouped under lesson names (max 3 per lesson)
    writing_bio     - Biology science-writing report, 2 pages, page 2 = extra-credit challenge
    writing_cer     - science-writing report, 3 pages: four areas, source charts, CER practice
"""
import json
import os
import sys

from reportlab.graphics.shapes import Circle, Drawing, Line, String  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_LEFT  # noqa: E402
from reportlab.lib.pagesizes import letter  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import inch  # noqa: E402
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,  # noqa: E402
                                Spacer, Table, TableStyle)

LEVELS = ["Beginning", "Developing", "Proficient", "Extending"]
LEVEL_COLOR = {"Beginning": "#b45309", "Developing": "#7c3aed", "Proficient": "#15803d",
               "Extending": "#1d4ed8", "Evidence unavailable": "#6b7280"}
VALID_LEVELS = set(LEVEL_COLOR)
PAGES = {"lesson_onepage": 1, "lessons_grouped": 2, "writing_bio": 2, "writing_cer": 3}
WRITING_AREAS = 4
NO_COMPARISON = ("No earlier submission of this work is available, so this report describes your "
                 "current answers only.")
INK, MUTED, RULE = colors.HexColor("#1f2d3d"), colors.HexColor("#5b6b7c"), colors.HexColor("#c9d6e3")
AREA_COLORS = ["#0f766e", "#7e22ce", "#047857", "#c2410c"]

base = ParagraphStyle("base", fontName="Helvetica", fontSize=10, leading=13, textColor=INK, alignment=TA_LEFT)
small = ParagraphStyle("small", parent=base, fontSize=8, leading=10, textColor=MUTED)
kicker = ParagraphStyle("kicker", parent=base, fontName="Helvetica-Bold", fontSize=8, textColor=MUTED)
title = ParagraphStyle("title", parent=base, fontName="Helvetica-Bold", fontSize=22, leading=26)
h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8)
h3 = ParagraphStyle("h3", parent=base, fontName="Helvetica-Bold", fontSize=10, leading=13)
quote = ParagraphStyle("quote", parent=base, fontName="Helvetica-Oblique")
big = ParagraphStyle("big", parent=base, fontName="Helvetica-Bold", fontSize=24, leading=28,
                     textColor=colors.HexColor("#1d4ed8"))


def esc(text):
    return (str(text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def level_span(level):
    return '<font color="%s"><b>%s</b></font>' % (LEVEL_COLOR.get(level, "#1f2d3d"), esc(level))


def lines(n, width=7.0):
    t = Table([[""] for _ in range(n)], colWidths=[width * inch], rowHeights=[0.3 * inch] * n)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE)]))
    return t


def footer_fn(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.75 * inch, 0.5 * inch, text)
        canvas.drawRightString(7.75 * inch, 0.5 * inch, str(doc.page))
        canvas.restoreState()
    return draw


def scale_row(level):
    """Four-point dot scale like the lesson model; no dot when evidence is unavailable."""
    W, H = 3.2 * inch, 0.32 * inch
    d = Drawing(W, H)
    x0, x1, y = 12, W - 12, H / 2
    d.add(Line(x0, y, x1, y, strokeColor=RULE, strokeWidth=1))
    for i in range(4):
        x = x0 + (x1 - x0) * i / 3
        d.add(Line(x, y - 4, x, y + 4, strokeColor=RULE, strokeWidth=1))
    if level in LEVELS:
        x = x0 + (x1 - x0) * LEVELS.index(level) / 3
        d.add(Circle(x, y, 4, fillColor=INK, strokeColor=INK))
    return d


def area_chart(points, labels, color, w=3.1, h=1.45):
    """points: list of level names or None per source; lines stop at gaps. Vector drawing."""
    W, H = w * inch, h * inch
    left, bottom, top, right = 58, 16, 6, 6
    d = Drawing(W, H)
    n = max(len(labels), 1)
    pw, ph = W - left - right, H - bottom - top
    def xy(i, lv):
        x = left + (pw * (i + 0.5) / n)
        y = bottom + ph * (lv + 0.5) / 4
        return x, y
    for lv, name in enumerate(LEVELS):
        _, y = xy(0, lv)
        d.add(Line(left, y, W - right, y, strokeColor=colors.HexColor("#e5edf5"), strokeWidth=0.5))
        d.add(String(left - 4, y - 2, name, fontName="Helvetica", fontSize=5.5, textAnchor="end",
                     fillColor=colors.HexColor(LEVEL_COLOR[name])))
    d.add(Line(left, bottom, left, H - top, strokeColor=RULE, strokeWidth=0.6))
    d.add(Line(left, bottom, W - right, bottom, strokeColor=RULE, strokeWidth=0.6))
    for i, lab in enumerate(labels):
        x, _ = xy(i, 0)
        d.add(String(x, bottom - 9, lab, fontName="Helvetica", fontSize=5.5, textAnchor="middle", fillColor=MUTED))
    col = colors.HexColor(color)
    prev = None
    for i, p in enumerate(points):
        if p in LEVELS:
            cur = xy(i, LEVELS.index(p))
            if prev:
                d.add(Line(prev[0], prev[1], cur[0], cur[1], strokeColor=col, strokeWidth=1.2))
            prev = cur
        else:
            prev = None
    for i, p in enumerate(points):
        if p in LEVELS:
            x, y = xy(i, LEVELS.index(p))
            d.add(Circle(x, y, 2.2, fillColor=col, strokeColor=col))
    return d


class ReportError(ValueError):
    """The report data or the rendered page count does not fit the approved layout."""


def doc_for(path):
    return SimpleDocTemplate(path, pagesize=letter, pageCompression=1, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                             topMargin=0.6 * inch, bottomMargin=0.75 * inch)


def build(path, story, foot, layout):
    """Build the PDF and keep it only when it has the layout's page count."""
    doc = doc_for(path)
    doc.build(story, onFirstPage=footer_fn(foot), onLaterPages=footer_fn(foot))
    if doc.page != PAGES[layout]:
        os.remove(path)
        raise ReportError("%s rendered %d pages; the approved layout has %d. Shorten the text."
                          % (layout, doc.page, PAGES[layout]))


def inside_git_checkout(path):
    folder = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.exists(os.path.join(folder, ".git")):
            return True
        parent = os.path.dirname(folder)
        if parent == folder:
            return False
        folder = parent


def check(r):
    """Reject levels outside Katherine's scale and content the layout would drop."""
    layout = r.get("layout")
    if layout not in PAGES:
        raise ReportError("Unknown layout %r." % layout)
    levels = []
    if layout == "lesson_onepage":
        levels = [a["level"] for a in r["aspects"]]
    elif layout == "lessons_grouped":
        for lesson in r["lessons"]:
            if len(lesson["aspects"]) > 3:
                raise ReportError("%s has %d critical aspects; choose at most three."
                                  % (lesson["lesson"], len(lesson["aspects"])))
            levels += [a["level"] for a in lesson["aspects"]]
    else:
        sources = r["work"] if layout == "writing_bio" else r["sources"]
        if layout == "writing_cer" and len(r["areas"]) != WRITING_AREAS:
            raise ReportError("writing_cer needs exactly four writing areas.")
        for a in r["areas"]:
            if len(a["points"]) != len(sources):
                raise ReportError("%s has %d points for %d sources." % (a["area"], len(a["points"]), len(sources)))
            levels += [a["level"]] + [p for p in a["points"] if p is not None]
    bad = sorted(set(levels) - VALID_LEVELS)
    if bad:
        raise ReportError("Levels outside the scale: %s." % ", ".join(bad))


def lesson_onepage(r, path):
    s = [Paragraph(esc(r["kicker"]), kicker), Spacer(1, 10), Paragraph(esc(r["name"]), title),
         Paragraph("%s | %s" % (esc(r["lesson"]), esc(r["date"])), small), Spacer(1, 10),
         Paragraph("1 &nbsp;YOUR GROWTH", h2),
         Paragraph("Your current understanding in this lesson. A single report does not establish a growth trend.", small),
         Spacer(1, 4)]
    head = Table([["", "Beginning      Developing      Proficient      Extending"]], colWidths=[3.7 * inch, 3.3 * inch])
    head.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 6.5), ("TEXTCOLOR", (0, 0), (-1, -1), MUTED),
                              ("ALIGN", (1, 0), (1, 0), "CENTER")]))
    s.append(head)
    rows = []
    for a in r["aspects"]:
        label = esc(a["name"])
        if a["level"] not in LEVELS:
            label += '<br/><font size="7" color="#6b7280">%s</font>' % esc(a["level"])
        rows.append([Paragraph(label, base), scale_row(a["level"])])
    t = Table(rows, colWidths=[3.7 * inch, 3.3 * inch])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    s += [t, Paragraph("2 &nbsp;HOW YOU DID ON THIS ASSIGNMENT", h2), Spacer(1, 2), Paragraph(esc(r["how_you_did"]), base),
          Paragraph("3 &nbsp;ONE QUESTION TO THINK ABOUT", h2), Spacer(1, 2), Paragraph(esc(r["question"]), base),
          Spacer(1, 4), lines(4),
          Paragraph("4 &nbsp;WHAT I UNDERSTAND NOW THAT I DIDN'T BEFORE", h2),
          Paragraph("Write this yourself, then hand this page back to me. This is the part I read.", small), lines(4),
          Paragraph("5 &nbsp;HOW I CAN IMPROVE MY RESPONSES NEXT TIME", h2), lines(3)]
    build(path, s, r.get("footer", "Conceptual feedback is not a grade."), "lesson_onepage")


def lessons_grouped(r, path):
    s = [Paragraph(esc(r["heading"]), ParagraphStyle("hh", parent=h2, fontSize=13, spaceBefore=0)),
         Paragraph(esc(r["name"]), title),
         Paragraph('<font color="#0f766e">%s</font>' % esc(r["subhead"]), base), Spacer(1, 4),
         Paragraph(esc(r["intro"]), base), Spacer(1, 8), Paragraph("Current understanding", h2)]
    for lesson in r["lessons"]:
        rows = [[Paragraph('<font color="white"><b>%s</b></font>' % esc(lesson["lesson"]), base), "", ""],
                [Paragraph("<b>Critical aspect</b>", small), Paragraph("<b>Current evidence</b>", small),
                 Paragraph("<b>What this answer shows</b>", small)]]
        for a in lesson["aspects"]:
            rows.append([Paragraph(esc(a["name"]), base), Paragraph(level_span(a["level"]), base),
                         Paragraph(esc(a["shows"]), base)])
        t = Table(rows, colWidths=[1.9 * inch, 1.1 * inch, 4.0 * inch])
        t.setStyle(TableStyle([("SPAN", (0, 0), (-1, 0)), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e3a5f")),
                               ("LINEBELOW", (0, 1), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        s += [KeepTogether([t]), Spacer(1, 8)]
    s += [PageBreak(), Paragraph(esc(r["name"]), h2), Paragraph(esc(r["page2_label"]), small),
          Paragraph("How my thinking changed", h2), Paragraph(esc(r.get("thinking_changed") or NO_COMPARISON), base),
          Paragraph("One question to think about", h2), Paragraph(esc(r["question"]), base), Spacer(1, 4), lines(3),
          Paragraph("Evidence for my conceptual understanding", h2)]
    for ev in r["evidence"]:
        s += [Paragraph('<font color="#0f766e"><b>%s</b></font>' % esc(ev["label"]), small),
              Paragraph("“%s”" % esc(ev["text"]), quote), Spacer(1, 4)]
    s += [Paragraph("What I understand now that I didn't before", h2),
          Paragraph("Write three things or ideas you understand now. This reflection is for you; it is not a new submission.", small),
          lines(3)]
    foot = r.get("footer", "Student feedback")
    build(path, s, foot, "lessons_grouped")


def writing_bio(r, path):
    labels = [w["short"] for w in r["work"]]
    s = [Paragraph(esc(r["kicker"]), small), Spacer(1, 6), Paragraph(esc(r["name"]), title),
         Paragraph("Writing observations across your submitted work. Your own challenge is on page 2.", small), Spacer(1, 6),
         Paragraph("Work reviewed", h3)]
    for w in r["work"]:
        s.append(Paragraph("%s %s | source %s" % (esc(w["short"]), esc(w["lesson"]), esc(w["date"])), small))
    s += [Paragraph("Different lessons are different tasks. These observations do not establish a growth score.", small),
          Spacer(1, 6)]
    for i, a in enumerate(r["areas"]):
        left = [Paragraph("%s - %s" % (esc(a["prompt"]), level_span(a["level"])), h3),
                Paragraph("%s | %s | %s" % (esc(a["lesson"]), esc(a["date"]), esc(a["code"])), small),
                Paragraph("From your submitted work: “%s”" % esc(a["quote"]), base) if a.get("quote")
                else Paragraph("No answer to quote in this source.", small), Spacer(1, 2),
                Paragraph(esc(a["comment"]), base)]
        right = [Paragraph('<font color="%s"><b>%s</b></font>' % (AREA_COLORS[i], esc(a["area"])), small),
                 Paragraph("%d rated work sample%s." % (sum(p in LEVELS for p in a["points"]),
                                                        "" if sum(p in LEVELS for p in a["points"]) == 1 else "s"), small),
                 area_chart(a["points"], labels, AREA_COLORS[i], w=2.6, h=1.25),
                 Paragraph("Gaps stay unassessed; no level is invented.", small)]
        t = Table([[left, right]], colWidths=[4.25 * inch, 2.75 * inch])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        s.append(t)
    c = r["challenge"]
    s += [PageBreak(), Paragraph(esc(r["kicker"]), small), Spacer(1, 6), Paragraph(esc(r["name"]), title), Spacer(1, 6),
          Paragraph("10 pts summative extra credit", big), Spacer(1, 6), Paragraph("Your writing challenge", h2),
          Paragraph(esc(c["title"]), h3), Paragraph(esc(c["task"]), base), Spacer(1, 6),
          Paragraph("Try your challenge in your own words. Use a specific example or observation, then explain why it "
                    "supports your answer. Bring this page back so we can discuss your thinking.", base),
          Paragraph("My explanation", h2), lines(10), Paragraph("One question I want to discuss", h2), lines(3), Spacer(1, 6),
          Paragraph(esc(r["page2_note"]), small)]
    foot = "Source dates identify the work. Prepared %s." % r["prepared"]
    build(path, s, foot, "writing_bio")


def writing_cer(r, path):
    s = [Paragraph(esc(r["kicker"]), small), Spacer(1, 6), Paragraph(esc(r["name"]), title),
         Paragraph("What your reviewed work shows", h2),
         Paragraph("The colored levels describe each piece of writing. A change between tasks is not a diagnosis of your ability.", small),
         Spacer(1, 6)]
    for a in r["areas"]:
        s += [Paragraph(esc(a["area"]), h2),
              Paragraph("%s - %s" % (esc(a["source"]), level_span(a["level"])), base),
              Paragraph("Your words (%s): “%s”" % (esc(a["where"]), esc(a["quote"])), quote) if a.get("quote")
              else Paragraph("No answer to quote in this source.", small),
              Paragraph(esc(a["comment"]), base)]
    s += [PageBreak(), Paragraph(esc(r["kicker"]), small), Spacer(1, 6), Paragraph(esc(r["name"]), title),
          Paragraph("Submitted sources - four writing areas", h2),
          Paragraph("S = one exact submitted source. First responses and revisions in one file are not separate time points.", small)]
    for src in r["sources"]:
        s.append(Paragraph("%s | %s | %s" % (esc(src["short"]), esc(src["lesson"]), esc(src["date"])), small))
    labels = [src["short"] for src in r["sources"]]
    cells = []
    for i, a in enumerate(r["areas"]):
        cells.append([Paragraph('<font color="%s"><b>%s</b></font>' % (AREA_COLORS[i], esc(a["area"])), small),
                      area_chart(a["points"], labels, AREA_COLORS[i]),
                      Paragraph(esc(r.get("chart_note", "Only sources reviewed for this report are plotted; earlier saved "
                                                        "feedback remains available and was not re-rated here.")), small)])
    grid = Table([[cells[0], cells[1]], [cells[2], cells[3]]], colWidths=[3.5 * inch, 3.5 * inch])
    grid.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 8)]))
    s += [Spacer(1, 6), grid]
    c = r["cer"]
    s += [PageBreak(), Paragraph(esc(r["kicker"]), small), Spacer(1, 6), Paragraph(esc(r["name"]), title),
          Paragraph("CER practice - claim, evidence, reasoning", h2),
          Paragraph("Based on your latest reviewed lesson: %s" % esc(c["lesson"]), small), Spacer(1, 4),
          Paragraph("<b>%s</b>" % esc(c["question"]), base), Spacer(1, 4),
          Paragraph("Use these three given pieces of evidence. They are practice information, not words attributed to you.", small)]
    for i, fact in enumerate(c["facts"], 1):
        s.append(Paragraph("%d. %s" % (i, esc(fact)), base))
    s += [Spacer(1, 6), Paragraph("Claim: Answer the question in one clear sentence.", h3), lines(2),
          Paragraph("Evidence: Use the three facts that support your claim.", h3), lines(3),
          Paragraph("Reasoning: Explain how each fact connects to your claim. Use the science idea and because.", h3), lines(4),
          Paragraph("Write this yourself and hand this page back. Your paper CER is not assessed in this report.", small)]
    foot = "Saved writing observations, not a grade or a completed CER assessment."
    build(path, s, foot, "writing_cer")


LAYOUTS = {"lesson_onepage": lesson_onepage, "lessons_grouped": lessons_grouped,
           "writing_bio": writing_bio, "writing_cer": writing_cer}

def render(report, path):
    """Validate one report and write its PDF; raises ReportError instead of a wrong page."""
    if inside_git_checkout(path):
        raise ReportError("Write reports outside the repository; %s is inside a Git checkout." % path)
    check(report)
    LAYOUTS[report["layout"]](report, path)


if __name__ == "__main__":
    try:
        render(json.load(open(sys.argv[1])), sys.argv[2])
    except ReportError as error:
        sys.exit("render.py: %s" % error)

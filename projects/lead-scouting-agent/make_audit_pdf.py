#!/usr/bin/env python3
"""Build a tailored 2 page website audit PDF for one lead.

Usage:
  python3 make_audit_pdf.py lead.json audits/bright-way.pdf
  base64 -w0 audits/bright-way.pdf      (paste into the Gmail draft attachment)

lead.json fields:
  business, owner (e.g. "Dr. Hasan"), city, website, niche_word (e.g. "patients"),
  summary (1 to 2 sentences),
  findings: [{"problem": "...", "cost": "...", "fix": "..."}]  (2 to 4 items, all seen on the real site)
  redesign: ["bullet", ...]  (what the new site contains, tied to the findings)
Booking link and name are fixed below. No email address is printed on purpose.
"""
import json
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

BOOKING = "https://calendar.app.google/twytvCCqGKoH9fQ68"
PORTFOLIO = "https://abdulwasiu.vibepreview.com"
NAVY = colors.HexColor("#0B2545")
TEAL = colors.HexColor("#13A89E")
GREY = colors.HexColor("#5B6770")
LIGHT = colors.HexColor("#EEF3F7")

H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22, leading=26, textColor=NAVY)
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=NAVY, spaceBefore=10, spaceAfter=4)
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13, textColor=colors.HexColor("#1F2933"))
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8.5, leading=11, textColor=GREY)
CELL = ParagraphStyle("c", parent=BODY, fontSize=9.2, leading=12.5)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold", textColor=NAVY)
WHITE = ParagraphStyle("w", parent=BODY, fontName="Helvetica-Bold", textColor=colors.white, fontSize=10)


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(lead, out):
    doc = SimpleDocTemplate(out, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                            topMargin=11 * mm, bottomMargin=10 * mm,
                            title=f"Website growth audit for {lead['business']}", author="Abdulwasiu")
    s = []
    s.append(Paragraph("WEBSITE GROWTH AUDIT", ParagraphStyle("k", parent=SMALL, textColor=TEAL, fontName="Helvetica-Bold", fontSize=9)))
    s.append(Paragraph(esc(lead["business"]), H1))
    s.append(Paragraph(esc(f"{lead['website']}  |  {lead['city']}  |  Prepared for {lead['owner']}"), SMALL))
    s.append(Spacer(1, 6))
    s.append(Paragraph(esc(lead["summary"]), BODY))

    s.append(Paragraph("What I found on your website", H2))
    rows = [[Paragraph("What I saw", WHITE), Paragraph("What it costs you", WHITE), Paragraph("The fix", WHITE)]]
    for f in lead["findings"]:
        rows.append([Paragraph(esc(f["problem"]), CELL), Paragraph(esc(f["cost"]), CELL), Paragraph(esc(f["fix"]), CELLB)])
    t = Table(rows, colWidths=[58 * mm, 54 * mm, 58 * mm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#D5DDE3")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    s.append(t)

    s.append(Paragraph(f"What your new website will do for {esc(lead['business'])}", H2))
    for b in lead["redesign"]:
        s.append(Paragraph("&bull;&nbsp;&nbsp;" + esc(b), BODY))
        s.append(Spacer(1, 2))

    steps = [
        ("1", "15 minute call", "I show you a preview of your new design. No cost."),
        ("2", "Approve the look", "You pick changes. I build in days, not months."),
        ("3", "Launch and track", "Booking, WhatsApp and forms tested on mobile before go live."),
    ]
    st = Table([[Paragraph(f"<b>{n}</b>", ParagraphStyle("n", parent=BODY, textColor=colors.white, fontSize=14, alignment=1)),
                 Paragraph(f"<b>{esc(a)}</b><br/>{esc(b)}", CELL)] for n, a, b in steps],
               colWidths=[10 * mm, 160 * mm])
    st.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), TEAL), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("LINEBELOW", (0, 0), (-1, -1), 2, colors.white),
                            ("BACKGROUND", (1, 0), (1, -1), LIGHT),
                            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    s.append(Paragraph("How it works", H2))
    s.append(st)

    cta = Table([[Paragraph(f'<font color="white"><b>Book your 15 minute preview call</b></font><br/>'
                            f'<font color="white" size="9"><link href="{BOOKING}">{BOOKING}</link></font><br/>'
                            f'<font color="white" size="9">See my work: <link href="{PORTFOLIO}">{PORTFOLIO}</link></font>',
                            ParagraphStyle("cta", parent=BODY, textColor=colors.white, fontSize=12, leading=17))]],
               colWidths=[170 * mm])
    cta.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY),
                             ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                             ("LEFTPADDING", (0, 0), (-1, -1), 12)]))
    s.append(Spacer(1, 10))
    s.append(KeepTogether([cta, Spacer(1, 4),
                           Paragraph("Abdulwasiu, web designer, Lagos. Built with WordPress/Elementor or Base44 depending on what suits you. "
                                     "Findings are from my own review of your public website.", SMALL)]))
    doc.build(s)


if __name__ == "__main__":
    build(json.load(open(sys.argv[1])), sys.argv[2])

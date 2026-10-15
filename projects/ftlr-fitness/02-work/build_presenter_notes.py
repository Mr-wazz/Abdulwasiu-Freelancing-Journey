from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf")); pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf")); pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))
pdfmetrics.registerFontFamily("C", normal="C", bold="CB", italic="CI", boldItalic="CB")
INK = colors.HexColor("#1D2A24"); SAGE_D = colors.HexColor("#5F8570"); MUTED = colors.HexColor("#5E6D65"); MINT = colors.HexColor("#EEF4F0"); LINE = colors.HexColor("#D8E3DC")
def st(n, **k):
    b = dict(fontName="C", fontSize=10.3, leading=14, textColor=INK); b.update(k); return ParagraphStyle(n, **b)
body = st("b"); h = st("h", fontName="CB", fontSize=12, leading=15, textColor=colors.white); lab = st("l", fontName="CB", fontSize=9, leading=12, textColor=SAGE_D)
OUT = "/home/user/Abdulwasiu-Freelancing-Journey/projects/ftlr-fitness/02-work/FTLR-Presenter-Notes.pdf"
doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=16*mm, bottomMargin=16*mm, title="FTLR Growth Playbook: presenter notes", author="Up Agency")
CW = A4[0] - 36*mm
S = [Paragraph("Presenter notes: FTLR Growth Playbook", st("t", fontName="CB", fontSize=20, leading=24)),
     Paragraph("For your call with Leah. Private, do not send. About 20 minutes. Rule: give value first, ask before you offer, and never mention prices unless she asks.", st("s", textColor=MUTED, fontSize=10.5, leading=14)), Spacer(1, 8)]
slides = [
 ("1  Cover", "Congratulate her. Say: “I prepared a short playbook for your first 90 days. It is yours to keep.”", "Ask: “How is your launch week shaping up?”", "1 min"),
 ("2  Where we are", "Walk the timeline left to right. Everything is done except Apple's approval. Stress that the safety tools in chat and the web member protection are already in place.", "Ask: “Any news from Apple yet?”", "1 min"),
 ("3  What is strong", "Read the five cards quickly. Say her promise out loud: “Start building your best self for the long run.”", "Ask: “Which of these matters most to your members?”", "1 min"),
 ("4  Member journey", "This is the key slide. Six moments, each can be improved. Her biggest gaps are the first (being found) and the last (being recommended).", "Ask: “Where do you feel members drop off today?” Write the answer down.", "2 min"),
 ("5  90 days at a glance", "Four phases, one focus each. Keep it simple. Do not read the bullets.", "Say: “The next slides give the detail. You can do all of this yourself.”", "1 min"),
 ("6  Phases 1 and 2", "Highlight two items: manual release, so she picks launch time, and the Day 0 welcome message.", "Ask: “Who will answer chat reports and the support email?”", "2 min"),
 ("7  Phases 3 and 4", "Highlight the 14 day challenge and the win back message. Mention counting Android requests.", "Ask: “Do you already run challenges or weekly themes?”", "1 min"),
 ("8  App Store listing", "Give her the real copy: subtitle, keywords, promotional text. Explain that screenshots must show the real app. Say the keywords are exactly 100 characters.", "Offer value: “Send me the exact words you want to keep and I will check them for you.”", "2 min"),
 ("9  First 7 days", "Read the Day 0 message. Explain the goal: a first workout within 24 hours. She can send these herself.", "Ask: “Do you send a welcome message today?”", "2 min"),
 ("10  Design direction", "Explain you used only her own words and colors: sage green, “uplifted, not beat down”, strong, powerful, mobile. Say her paywall already follows the style. The login and home use a generic template.", "Ask: “Does this feel like FTLR to you?” Listen carefully.", "2 min"),
 ("11  Concept: home", "Say clearly: this is a concept with illustrations. Real photos and content would go inside. Point to the Start button, weekly ring and the three pillars.", "Ask: “What would you want members to see first?”", "2 min"),
 ("12  Concept: welcome", "Sign in, choose a goal, a note from her. Say: “This is how a member reaches a first workout in minutes.”", "Ask: “Would a note from you in the app feel natural?”", "2 min"),
 ("13  Android", "Explain the 14 day count. Be honest: if nobody asks, wait. This builds trust.", "Ask: “Do members ask for Android today?” Write the number down.", "1 min"),
 ("14  Quick wins", "Tell her these five take minutes and need no help from you.", "Say: “Start with number 1 today.”", "1 min"),
 ("15  Where we can go next", "Only now mention working together. Options only, no prices. Say: “No pressure, choose any piece or none.”", "Ask: “What matters most in the next 30 days?” Then stop talking and listen.", "2 min"),
 ("16  Thank you", "Thank her. Say you will send a short written summary after the call.", "If she wants prices: “I will send a clear written offer on Fiverr so your payment is protected.”", "30 sec"),
]
for t, say, ask, tm in slides:
    head = Table([[Paragraph(t, h), Paragraph(tm, st("tm", fontName="CB", fontSize=10, textColor=colors.white, alignment=2))]], colWidths=[CW - 25*mm, 25*mm])
    head.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SAGE_D), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    box = Table([[Paragraph("SAY", lab), Paragraph(say, body)], [Paragraph("ASK", lab), Paragraph(ask, body)]], colWidths=[14*mm, CW - 14*mm])
    box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), MINT), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    S.append(KeepTogether([head, box, Spacer(1, 7)]))
S += [Paragraph("If she asks about price", st("x", fontName="CB", fontSize=12, textColor=SAGE_D)),
      Paragraph("Do not quote on the call. Say: “Let me confirm what you want first, then I will send a clear written offer with milestones on Fiverr.” That keeps value first and protects your price.", body), Spacer(1, 6),
      Paragraph("After the call", st("x2", fontName="CB", fontSize=12, textColor=SAGE_D)),
      Paragraph("Send her the PDF playbook, thank her, and tell me what she said. I will write the offer and update the notes.", body)]
doc.build(S)

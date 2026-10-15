from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))
pdfmetrics.registerFontFamily("C", normal="C", bold="CB", italic="CI", boldItalic="CB")

NAVY = colors.HexColor("#0F2747")
TEAL = colors.HexColor("#12A594")
SOFT = colors.HexColor("#EAF6F4")
GREY = colors.HexColor("#5B6B7D")
LINE = colors.HexColor("#D9E1E8")
ZEBRA = colors.HexColor("#F6F9FB")
HIGH = colors.HexColor("#D6453D")
MID = colors.HexColor("#E59B12")
LOW = colors.HexColor("#2F7D5B")
BLUE = colors.HexColor("#2C6FD1")

W, H = A4
LM = RM = 18 * mm

def st(name, **kw):
    base = dict(fontName="C", fontSize=10.5, leading=14.5, textColor=colors.HexColor("#1B2733"))
    base.update(kw)
    return ParagraphStyle(name, **base)

body = st("body")
small = st("small", fontSize=9, leading=12.5, textColor=GREY)
h2 = st("h2", fontName="CB", fontSize=13.5, leading=17, textColor=colors.white)
cell = st("cell", fontSize=9.8, leading=13)
cellb = st("cellb", fontName="CB", fontSize=9.8, leading=13)
num = st("num", fontName="CB", fontSize=10, alignment=TA_CENTER, textColor=NAVY)
badge = st("badge", fontName="CB", fontSize=8.6, leading=11, alignment=TA_CENTER, textColor=colors.white)
head = st("head", fontName="CB", fontSize=8.8, leading=11, textColor=GREY)

def on_page(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, H - 5 * mm, W, 5 * mm, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.rect(0, H - 5 * mm, 40 * mm, 5 * mm, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    c.line(LM, 15 * mm, W - RM, 15 * mm)
    c.setFont("C", 8.5)
    c.setFillColor(GREY)
    c.drawString(LM, 10 * mm, "RiseTrack  |  Audit et plan d'amélioration  |  Document confidentiel")
    c.drawRightString(W - RM, 10 * mm, "Page %d" % doc.page)
    c.restoreState()

doc = BaseDocTemplate(
    "/home/user/Abdulwasiu-Freelancing-Journey/projects/amazigh/02-work/RiseTrack-Audit-et-Plan-d-amelioration.pdf",
    pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=16 * mm, bottomMargin=20 * mm,
    title="RiseTrack: Audit et plan d'amélioration", author="Up Agency",
    subject="Plan d'amélioration RiseTrack")
frame = Frame(LM, 20 * mm, W - LM - RM, H - 36 * mm, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=on_page)])

S = []

# Cover band
cover = Table([[
    [Paragraph("RISETRACK", st("k", fontName="CB", fontSize=10.5, textColor=colors.HexColor("#7FE3D5"), leading=13)),
     Spacer(1, 3),
     Paragraph("Audit et plan d'amélioration", st("t", fontName="CB", fontSize=26, leading=30, textColor=colors.white)),
     Spacer(1, 4),
     Paragraph("Une seule mise à jour complète : une base solide, des revenus, une meilleure expérience.",
               st("s", fontSize=12, leading=16, textColor=colors.HexColor("#DCE8F5")))]
]], colWidths=[W - LM - RM])
cover.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), NAVY),
    ("LEFTPADDING", (0, 0), (-1, -1), 16), ("RIGHTPADDING", (0, 0), (-1, -1), 16),
    ("TOPPADDING", (0, 0), (-1, -1), 16), ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
]))
S += [cover]

meta = Table([[
    Paragraph("<b>Préparé pour</b><br/>Amazigh", cell),
    Paragraph("<b>Préparé par</b><br/>Up Agency", cell),
    Paragraph("<b>Date</b><br/>15 octobre 2026", cell),
    Paragraph("<b>Version</b><br/>1.0", cell),
]], colWidths=[(W - LM - RM) / 4.0] * 4)
meta.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), SOFT),
    ("LINEBELOW", (0, 0), (-1, -1), 2, TEAL),
    ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
]))
S += [meta, Spacer(1, 12)]

S += [Paragraph(
    "Ce document rassemble ce que nous avons observé sur RiseTrack et ce qui peut être amélioré. "
    "Tout est regroupé en <b>une seule mise à jour</b>, pour éviter de refaire une version à chaque petit problème. "
    "Pour chaque point, vous voyez <b>pourquoi il compte</b> pour vos utilisateurs et vos revenus.", body), Spacer(1, 8)]

def chip(text, color):
    t = Table([[Paragraph(text, badge)]], colWidths=[24 * mm], rowHeights=[6.2 * mm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                           ("ROUNDEDCORNERS", [3, 3, 3, 3])]))
    return t

legend = Table([[
    Paragraph("<b>Statut</b>", cellb),
    [chip("CONSTATÉ", NAVY)], Paragraph("observé directement dans l'application", small),
    [chip("À VALIDER", BLUE)], Paragraph("identifié à l'analyse, confirmé avec vous avant d'agir", small),
    [chip("PROPOSITION", TEAL)], Paragraph("idée pour faire progresser l'application", small),
]], colWidths=[16 * mm, 25 * mm, 34 * mm, 25 * mm, 38 * mm, 27 * mm, None])
# simpler legend: two rows to avoid overflow
legend = Table([
    [Paragraph("<b>Statut</b>", cellb), chip("CONSTATÉ", NAVY), Paragraph("observé directement dans l'application", small)],
    ["", chip("À VALIDER", BLUE), Paragraph("identifié lors de l'analyse, confirmé avec vous avant toute intervention", small)],
    ["", chip("PROPOSITION", TEAL), Paragraph("idée pour faire progresser l'application", small)],
], colWidths=[18 * mm, 28 * mm, None])
legend.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                            ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
S += [legend, Spacer(1, 12)]

STAT = {"C": ("CONSTATÉ", NAVY), "V": ("À VALIDER", BLUE), "P": ("PROPOSITION", TEAL)}
PRIO = {"H": ("HAUTE", HIGH), "M": ("MOYENNE", MID), "B": ("BASSE", LOW)}

def section(letter, title, rows):
    bar = Table([[Paragraph(letter, st("lt", fontName="CB", fontSize=13.5, leading=17, textColor=colors.white, alignment=TA_CENTER)), Paragraph(title, h2)]], colWidths=[10 * mm, W - LM - RM - 10 * mm])
    bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TEAL), ("BACKGROUND", (0, 0), (0, 0), NAVY),
                             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                             ("LEFTPADDING", (1, 0), (1, 0), 10), ("TOPPADDING", (0, 0), (-1, -1), 6),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    data = [[Paragraph("N°", head), Paragraph("CONSTAT", head), Paragraph("POURQUOI C'EST IMPORTANT", head),
             Paragraph("STATUT", head), Paragraph("PRIORITÉ", head)]]
    for n, what, why, s, p in rows:
        data.append([Paragraph(str(n), num), Paragraph(what, cellb), Paragraph(why, cell),
                     chip(*STAT[s]), chip(*PRIO[p])])
    cw = [10 * mm, 52 * mm, 54 * mm, 28 * mm, 26 * mm]
    t = Table(data, colWidths=cw, repeatRows=1)
    style = [
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, 0), 1, LINE),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5), ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(style))
    return [KeepTogether([bar, t]), Spacer(1, 9)]

S += section("A", "Une base solide", [
    (1, "Bandeau « Edit with Base44 » en bas de l'écran", "Il donne l'image d'une application non finie et réduit la confiance.", "C", "H"),
    (2, "Texte du haut (la date) qui passe sous l'heure de l'iPhone", "C'est le premier écran vu par chaque utilisateur.", "C", "H"),
    (3, "Rappels (notifications) peu fiables sur iPhone", "Sans rappels, les utilisateurs oublient leurs habitudes et partent.", "V", "H"),
    (4, "Habitudes liées à la semaine de leur création", "Un utilisateur qui perd ses habitudes ne revient pas.", "V", "H"),
    (5, "Suppression du compte incomplète", "Apple peut exiger une suppression complète lors d'une prochaine mise à jour.", "V", "H"),
    (6, "Protection des données de chaque utilisateur", "Chacun doit voir uniquement ses propres données : confiance et sécurité.", "V", "H"),
    (7, "Rapidité de chargement", "L'application ralentira quand le nombre d'utilisateurs augmentera.", "V", "M"),
])
S += section("B", "Revenus", [
    (8, "Abonnement Premium avec le vrai paiement Apple : page de prix, essai gratuit, restauration des achats",
     "C'est ce qui transforme les utilisateurs en revenus réguliers.", "P", "H"),
])
S += section("C", "Expérience utilisateur", [
    (9, "Écran d'accueil avec les progrès du jour et de la semaine", "Voir ses progrès donne envie de revenir chaque jour.", "P", "M"),
    (10, "Affichage sur iPad et ordinateur (aujourd'hui une bande étroite)", "Meilleure image de l'application et plus d'appareils compatibles.", "V", "M"),
    (11, "Coach : aujourd'hui des conseils fixes, sans vrai coach IA", "Un vrai coach est une raison forte de s'abonner.", "V", "M"),
    (12, "Langues : mélange de français et d'anglais", "Pour toucher aussi les utilisateurs anglophones.", "V", "M"),
])
S += section("D", "Plus tard", [
    (13, "Version Android (Google Play)", "L'autre moitié du marché mobile.", "P", "B"),
    (14, "Suivi mensuel : mises à jour, corrections, gestion des refus Apple", "Protège l'application dans le temps.", "P", "B"),
])

# Protection note
prot = Table([[Paragraph(
    "<b>Votre approbation Apple est protégée.</b> Tout ce qui touche à la version iPhone sera testé avant l'envoi, "
    "pour ne rien mettre en danger ce que vous avez déjà obtenu.", body)]], colWidths=[W - LM - RM])
prot.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SOFT), ("LINEBEFORE", (0, 0), (0, -1), 4, TEAL),
                          ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 9),
                          ("BOTTOMPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 12)]))

steps = [
    ("1", "Votre liste", "Vous analysez l'application et m'envoyez vos points."),
    ("2", "Clôture de la liste", "Dimanche 18 octobre. Ce qui arrive après ira dans la mise à jour suivante."),
    ("3", "Proposition claire", "Je vous envoie le contenu exact, les étapes et le calendrier."),
    ("4", "Mise à jour unique", "Réalisée par étapes, testée sur iPhone, puis envoyée à Apple."),
]
rows = []
for n, t, d in steps:
    c = Table([[Paragraph(n, st("n", fontName="CB", fontSize=12, alignment=TA_CENTER, textColor=colors.white, leading=14))]],
              colWidths=[8 * mm], rowHeights=[8 * mm])
    c.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ROUNDEDCORNERS", [4, 4, 4, 4])]))
    rows.append([c, Paragraph("<b>%s</b><br/>%s" % (t, d), cell)])
nt = Table(rows, colWidths=[14 * mm, None])
nt.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
bar = Table([[Paragraph("Prochaines étapes", h2)]], colWidths=[W - LM - RM])
bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), NAVY), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                         ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
S += [KeepTogether([prot, Spacer(1, 9), bar, Spacer(1, 2), nt, Spacer(1, 6),
      Paragraph("Merci pour votre confiance. Je reste disponible pour toute question.", st("end", fontName="CI", fontSize=10.5, textColor=GREY))])]

doc.build(S)
print("ok")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf")); pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf")); pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))
pdfmetrics.registerFontFamily("C", normal="C", bold="CB", italic="CI", boldItalic="CB")
NAVY = colors.HexColor("#0F2747"); TEAL = colors.HexColor("#12A594"); SOFT = colors.HexColor("#EAF6F4"); GREY = colors.HexColor("#5B6B7D")
LINE = colors.HexColor("#D9E1E8"); ZEBRA = colors.HexColor("#F6F9FB"); BLUE = colors.HexColor("#2C6FD1"); GOLD = colors.HexColor("#E59B12")
W, H = A4; LM = RM = 18*mm; CW = W - LM - RM
def st(n, **k):
    b = dict(fontName="C", fontSize=10.5, leading=14.5, textColor=colors.HexColor("#1B2733")); b.update(k); return ParagraphStyle(n, **b)
body = st("b"); small = st("s", fontSize=9, leading=12.5, textColor=GREY); cell = st("c", fontSize=9.8, leading=13); cellb = st("cb", fontName="CB", fontSize=9.8, leading=13)
h2 = st("h2", fontName="CB", fontSize=14, leading=18, textColor=colors.white); head = st("hd", fontName="CB", fontSize=8.8, leading=11, textColor=GREY)
h3 = st("h3", fontName="CB", fontSize=11.5, leading=15, textColor=colors.HexColor("#0E8577"))
bul = st("bul", fontSize=10, leading=13.6, leftIndent=11, bulletIndent=0)
def on_page(c, doc):
    c.saveState(); c.setFillColor(NAVY); c.rect(0, H-5*mm, W, 5*mm, stroke=0, fill=1); c.setFillColor(TEAL); c.rect(0, H-5*mm, 40*mm, 5*mm, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.line(LM, 15*mm, W-RM, 15*mm); c.setFont("C", 8.5); c.setFillColor(GREY)
    c.drawString(LM, 10*mm, "RiseTrack  |  Bilan et prix  |  Document confidentiel"); c.drawRightString(W-RM, 10*mm, "Page %d" % doc.page); c.restoreState()
def bar(title, letter, color=TEAL):
    t = Table([[Paragraph(letter, st("l", fontName="CB", fontSize=14, leading=18, textColor=colors.white, alignment=TA_CENTER)), Paragraph(title, h2)]], colWidths=[10*mm, CW-10*mm])
    t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), color), ("BACKGROUND", (0,0), (0,0), NAVY), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (1,0), (1,0), 10), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)])); return t
def box(flow, bg=SOFT, edge=TEAL):
    t = Table([[flow]], colWidths=[CW]); t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), bg), ("LINEBEFORE", (0,0), (0,-1), 4, edge), ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12), ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9)])); return t
def money(n): return "{:,.0f} $".format(n).replace(",", " ")
def table(rows, widths, header, right=(), total=None):
    data = [[Paragraph(h, head if i not in right else st("hr", fontName="CB", fontSize=8.8, leading=11, textColor=GREY, alignment=TA_RIGHT)) for i, h in enumerate(header)]]
    for r in rows: data.append([Paragraph(str(x), (cellb if i == 0 else cell) if i not in right else st("r", fontName="CB", fontSize=9.8, leading=13, alignment=TA_RIGHT)) for i, x in enumerate(r)])
    if total: data.append([Paragraph(str(x), st("t", fontName="CB", fontSize=10.5, leading=13, alignment=TA_RIGHT if i in right else 0)) for i, x in enumerate(total)])
    t = Table(data, colWidths=widths, repeatRows=1)
    s = [("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LINEBELOW", (0,0), (-1,-1), 0.5, LINE), ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5), ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6)]
    for i in range(1, len(data)):
        if i % 2 == 0: s.append(("BACKGROUND", (0,i), (-1,i), ZEBRA))
    if total: s.append(("BACKGROUND", (0, len(data)-1), (-1, len(data)-1), SOFT))
    t.setStyle(TableStyle(s)); return t

A = [("A1", "Bandeau « Edit with Base44 » supprimé et texte du haut de l'écran corrigé sur iPhone", "En ligne dès publication, sans attendre Apple", 100),
     ("A2", "Habitudes qui restent d'une semaine à l'autre et protection contre les doublons", "En ligne dès publication", 150),
     ("A3", "Vérification complète de l'application et correction des bugs importants (jusqu'à 5 heures)", "En ligne dès publication", 250)]
B = [("B1", "Suppression complète du compte (obligatoire pour qu'Apple accepte l'abonnement)", "Dans la mise à jour Apple", 100),
     ("B2", "Abonnement Premium avec le vrai paiement Apple : page de prix, essai gratuit, restauration des achats", "Dans la mise à jour Apple", 1400),
     ("B3", "Notifications : vrais rappels sur iPhone, même quand l'application est fermée", "Dans la mise à jour Apple", 450),
     ("B4", "Logo agrandi pour bien remplir l'icône et l'écran de démarrage", "Dans la mise à jour Apple", 90)]
TA = sum(x[3] for x in A); TB = sum(x[3] for x in B)
S = []
cv = Table([[[Paragraph("RISETRACK", st("k", fontName="CB", fontSize=10.5, leading=13, textColor=colors.HexColor("#7FE3D5"))), Spacer(1,3),
              Paragraph("Bilan et prix", st("t", fontName="CB", fontSize=28, leading=32, textColor=colors.white)), Spacer(1,4),
              Paragraph("Tes priorités : l'essentiel pour une application solide qui génère des revenus. Un prix par élément, et le choix de payer petit à petit.", st("s", fontSize=12, leading=16, textColor=colors.HexColor("#DCE8F5")))]]], colWidths=[CW])
cv.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY), ("LEFTPADDING", (0,0), (-1,-1), 16), ("RIGHTPADDING", (0,0), (-1,-1), 16), ("TOPPADDING", (0,0), (-1,-1), 16), ("BOTTOMPADDING", (0,0), (-1,-1), 16)]))
meta = Table([[Paragraph("<b>Préparé pour</b><br/>Amazigh", cell), Paragraph("<b>Préparé par</b><br/>Up Agency", cell), Paragraph("<b>Date</b><br/>19 octobre 2026", cell), Paragraph("<b>Version</b><br/>1.0", cell)]], colWidths=[CW/4]*4)
meta.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), SOFT), ("LINEBELOW", (0,0), (-1,-1), 2, TEAL), ("LEFTPADDING", (0,0), (-1,-1), 12), ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
S += [cv, meta, Spacer(1, 12)]
S += [Paragraph("Merci pour ta liste et tes priorités. Tu m'as dit que le plus important, c'est <b>l'abonnement Premium, les notifications et les bugs importants</b>, après les petites touches. Voici exactement cela, en deux étapes claires, avec un prix pour chaque élément.", body), Spacer(1, 8)]
S += [bar("Comment c'est organisé", "1"), Spacer(1, 6)]
two = Table([[[Paragraph("Étape A : en ligne tout de suite", h3), Paragraph("Les petites touches et la fiabilité. Ces changements se font côté site : ils sont visibles dans l'application dès que je les publie, <b>sans attendre Apple</b>.", body)],
              [Paragraph("Étape B : une seule mise à jour Apple", h3), Paragraph("L'abonnement, les notifications, la suppression du compte et le logo. Tout est regroupé dans <b>une seule version</b>, donc une seule validation Apple, plus rapide et plus sûre.", body)]]], colWidths=[CW/2, CW/2])
two.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 12)]))
S += [two, Spacer(1, 6), box([Paragraph("<b>Ton approbation Apple est protégée :</b> tout est testé sur iPhone avant l'envoi, avec seulement les autorisations Caméra et Photos, connexion par email et mot de passe, et un abonnement qui suit les règles d'Apple.", body)]), PageBreak()]

S += [bar("Étape A : petites touches et fiabilité", "2"), Spacer(1, 6)]
S += [table([(a, b, c, money(d)) for a, b, c, d in A], [CW*0.07, CW*0.5, CW*0.27, CW*0.16], ["#", "CE QUE TU OBTIENS", "QUAND", "PRIX"], right=(3,), total=("", "Total étape A", "", money(TA))), Spacer(1, 12)]
S += [bar("Étape B : abonnement, notifications et logo", "3"), Spacer(1, 6)]
S += [table([(a, b, c, money(d)) for a, b, c, d in B], [CW*0.07, CW*0.5, CW*0.27, CW*0.16], ["#", "CE QUE TU OBTIENS", "QUAND", "PRIX"], right=(3,), total=("", "Total étape B", "", money(TB))), Spacer(1, 6),
      Paragraph("L'envoi à Apple, les tests sur iPhone et la gestion d'une éventuelle remarque d'Apple sont inclus dans l'étape B.", small), Spacer(1, 10)]
S += [bar("Aperçu : logo agrandi (point B4)", "4"), Spacer(1, 6)]
img = Image("/home/user/Abdulwasiu-Freelancing-Journey/projects/amazigh/02-work/icon-apercu-avant-apres.png", width=95*mm, height=95*mm*380/780)
cap = Table([[img, [Paragraph("<b>À gauche :</b> aujourd'hui, le logo laisse beaucoup de noir autour de lui.<br/><b>À droite :</b> le logo agrandi remplit mieux l'icône, comme les autres applications.", cell), Spacer(1, 4), Paragraph("Aperçu réalisé à partir de ta capture d'écran, la version finale sera nette et en haute qualité.", small)]]], colWidths=[100*mm, CW-100*mm])
cap.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 0)]))
S += [cap, PageBreak()]

S += [bar("Tes options, selon ton budget", "5"), Spacer(1, 6)]
opts = [("DÉPART", "Étape A seulement", "Les petites touches, les habitudes et les bugs importants, en ligne tout de suite.", TA, NAVY),
        ("REVENUS", "A + abonnement", "Étape A, suppression du compte, abonnement Premium et logo. Pour commencer à gagner de l'argent.", TA + 100 + 1400 + 90, TEAL),
        ("ESSENTIEL COMPLET", "A + B", "Tout ce que tu as demandé comme essentiel, avec les notifications.", TA + TB, GOLD)]
cells = []
for n, sub, d, p, col in opts:
    c = Table([[Paragraph(n, st("tn", fontName="CB", fontSize=9.5, leading=12, textColor=colors.white, alignment=TA_CENTER))], [Paragraph(sub, st("ts", fontName="CB", fontSize=10.5, alignment=TA_CENTER))],
               [Paragraph(money(p), st("tp", fontName="CB", fontSize=22, leading=26, alignment=TA_CENTER, textColor=col))], [Paragraph(d, st("td", fontSize=9.5, leading=12.5))]], colWidths=[CW/3 - 6])
    c.setStyle(TableStyle([("BACKGROUND", (0,0), (0,0), col), ("BACKGROUND", (0,1), (0,3), SOFT), ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
    cells.append(c)
g = Table([cells], colWidths=[CW/3]*3); g.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 6)]))
S += [g, Spacer(1, 6), Paragraph("En option, sur n'importe quelle formule : <b>vraie page d'accueil avant la connexion</b> (ton point 1), côté site, <b>250 $</b>.", body), Spacer(1, 10)]
S += [bar("Payer petit à petit", "6"), Spacer(1, 6)]
S += [Paragraph("Tu n'as pas à tout payer d'un coup. Chaque élément se règle séparément, au moment où je le livre, via la plateforme avec paiement protégé.", body), Spacer(1, 4)]
plan = [("Étape A1", money(100), "Je livre, tu valides, tu règles."), ("Étape A2", money(150), "Idem."), ("Étape A3", money(250), "Idem."),
        ("Étape B, début", "à partir de 30 %", "Pour lancer la mise à jour (suppression du compte, logo)."), ("Étape B, abonnement", "40 %", "Quand l'abonnement fonctionne dans la version de test."),
        ("Étape B, envoi à Apple", "30 %", "Quand la mise à jour part chez Apple.")]
S += [table(plan, [CW*0.28, CW*0.2, CW*0.52], ["PAIEMENT", "MONTANT", "QUAND"]), Spacer(1, 10)]
S += [bar("Ce dont j'ai besoin de toi", "7"), Spacer(1, 6)]
for t in ["Ton choix : Départ, Revenus ou Essentiel complet (et la page d'accueil en option ou non).", "Pour l'abonnement : les prix que tu veux (mensuel et annuel), et que l'accord Apple « Paid Apps » soit actif dans ton compte App Store Connect avec tes informations bancaires et fiscales.",
          "Ton accord écrit sur la plateforme avant de commencer. Rien ne démarre sans ton oui."]:
    S.append(Paragraph(t, bul, bulletText="•"))
S += [Spacer(1, 8), box([Paragraph("<b>Ce qui n'est pas inclus</b> (à voir plus tard, quand l'application génère des revenus) : design moderne complet, tracker refait, page Mon parcours simplifiée, cartes de progrès à partager, nouvelles captures d'écran App Store. Tout ce qui s'ajoute après cet accord fait l'objet d'une petite offre séparée.", body)])]
doc = BaseDocTemplate("/home/user/Abdulwasiu-Freelancing-Journey/projects/amazigh/RiseTrack-Bilan-et-Prix.pdf", pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=16*mm, bottomMargin=20*mm, title="RiseTrack: Bilan et prix", author="Up Agency")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(LM, 20*mm, CW, H-36*mm, 0, 0, 0, 0)], onPage=on_page)])
doc.build(S); print(TA, TB, TA+TB, TA+TB+250)

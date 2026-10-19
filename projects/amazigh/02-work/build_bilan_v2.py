import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf")); pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf")); pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))
pdfmetrics.registerFontFamily("C", normal="C", bold="CB", italic="CI", boldItalic="CB")
NAVY = colors.HexColor("#0F2747"); TEAL = colors.HexColor("#12A594"); SOFT = colors.HexColor("#EAF6F4"); GREY = colors.HexColor("#5B6B7D")
LINE = colors.HexColor("#D9E1E8"); ZEBRA = colors.HexColor("#F6F9FB"); GOLD = colors.HexColor("#E59B12"); AMBER = colors.HexColor("#FBF4E6")
W, H = A4; LM = RM = 18*mm; CW = W - LM - RM
BASE = "/home/user/Abdulwasiu-Freelancing-Journey/projects/amazigh/"

def build(lang):
    EN = lang == "en"
    T = lambda fr, en: en if EN else fr
    def money(n): return ("${:,.0f} CAD".format(n)) if EN else ("{:,.0f} $ CAD".format(n).replace(",", " "))
    def st(n, **k):
        b = dict(fontName="C", fontSize=10.5, leading=14.5, textColor=colors.HexColor("#1B2733")); b.update(k); return ParagraphStyle(n, **b)
    body = st("b"); small = st("s", fontSize=9, leading=12.5, textColor=GREY); cell = st("c", fontSize=9.8, leading=13); cellb = st("cb", fontName="CB", fontSize=9.8, leading=13)
    h2 = st("h2", fontName="CB", fontSize=14, leading=18, textColor=colors.white); head = st("hd", fontName="CB", fontSize=8.8, leading=11, textColor=GREY)
    h3 = st("h3", fontName="CB", fontSize=11.5, leading=15, textColor=colors.HexColor("#0E8577")); bul = st("bul", fontSize=10, leading=13.6, leftIndent=11, bulletIndent=0)
    label = T("RiseTrack  |  Bilan et prix  |  Document confidentiel", "RiseTrack  |  Summary and prices  |  ENGLISH COPY FOR ABDULWASIU, NOT FOR THE CLIENT")
    def on_page(c, doc):
        c.saveState(); c.setFillColor(NAVY); c.rect(0, H-5*mm, W, 5*mm, stroke=0, fill=1); c.setFillColor(TEAL if not EN else GOLD); c.rect(0, H-5*mm, 40*mm, 5*mm, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.line(LM, 15*mm, W-RM, 15*mm); c.setFont("C", 8.5); c.setFillColor(GREY)
        c.drawString(LM, 10*mm, label); c.drawRightString(W-RM, 10*mm, "Page %d" % doc.page); c.restoreState()
    def bar(title, letter, color=TEAL):
        t = Table([[Paragraph(letter, st("l", fontName="CB", fontSize=14, leading=18, textColor=colors.white, alignment=TA_CENTER)), Paragraph(title, h2)]], colWidths=[10*mm, CW-10*mm])
        t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), color), ("BACKGROUND", (0,0), (0,0), NAVY), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (1,0), (1,0), 10), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)])); return t
    def box(flow, bg=SOFT, edge=TEAL):
        t = Table([[flow]], colWidths=[CW]); t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), bg), ("LINEBEFORE", (0,0), (0,-1), 4, edge), ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12), ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9)])); return t
    def table(rows, widths, header, right=(), total=None):
        data = [[Paragraph(h, head if i not in right else st("hr", fontName="CB", fontSize=8.8, leading=11, textColor=GREY, alignment=TA_RIGHT)) for i, h in enumerate(header)]]
        for r in rows: data.append([Paragraph(str(x), (cellb if i == 0 else cell) if i not in right else st("r", fontName="CB", fontSize=9.8, leading=13, alignment=TA_RIGHT)) for i, x in enumerate(r)])
        if total: data.append([Paragraph(str(x), st("t", fontName="CB", fontSize=10.5, leading=13, alignment=TA_RIGHT if i in right else 0)) for i, x in enumerate(total)])
        t = Table(data, colWidths=widths, repeatRows=1)
        s = [("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LINEBELOW", (0,0), (-1,-1), 0.5, LINE), ("TOPPADDING", (0,0), (-1,-1), 3.6), ("BOTTOMPADDING", (0,0), (-1,-1), 3.6), ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6)]
        for i in range(1, len(data)):
            if i % 2 == 0: s.append(("BACKGROUND", (0,i), (-1,i), ZEBRA))
        if total: s.append(("BACKGROUND", (0, len(data)-1), (-1, len(data)-1), SOFT))
        t.setStyle(TableStyle(s)); return t

    Aitems = [("A1", T("Bandeau « Edit with Base44 » supprimé et texte du haut de l'écran corrigé sur iPhone", "“Edit with Base44” badge removed and the text at the top of the screen fixed on iPhone"), T("En ligne dès publication, sans attendre Apple", "Live as soon as published, no Apple wait"), 100),
              ("A2", T("Habitudes qui restent d'une semaine à l'autre et protection contre les doublons", "Habits that carry over from one week to the next, and protection against duplicates"), T("En ligne dès publication", "Live as soon as published"), 130),
              ("A3", T("Vérification complète de l'application et correction des bugs importants (jusqu'à 4 heures)", "Full check of the app and fixing of the important bugs (up to 4 hours)"), T("En ligne dès publication", "Live as soon as published"), 200)]
    Bitems = [("B1", T("Suppression complète du compte (obligatoire pour qu'Apple accepte l'abonnement)", "Complete account deletion (required for Apple to accept the subscription)"), T("Dans la mise à jour Apple", "In the Apple update"), 100),
              ("B2", T("Abonnement Premium, version de base : mensuel et annuel avec le vrai paiement Apple, page de prix, restauration des achats", "Premium subscription, base version: monthly and yearly with real Apple payment, price page, restore purchases"), T("Dans la mise à jour Apple", "In the Apple update"), 1000),
              ("B3", T("Essai gratuit et page de prix soignée", "Free trial and a polished price page"), T("Dans la mise à jour Apple", "In the Apple update"), 200),
              ("B4", T("Notifications : vrais rappels sur iPhone, même quand l'application est fermée", "Notifications: real reminders on iPhone, even when the app is closed"), T("Dans la mise à jour Apple", "In the Apple update"), 380),
              ("B5", T("Logo agrandi pour bien remplir l'icône et l'écran de démarrage", "Logo enlarged to properly fill the icon and the launch screen"), T("Dans la mise à jour Apple", "In the Apple update"), 70)]
    TA = sum(x[3] for x in Aitems); TB = sum(x[3] for x in Bitems)
    OPT_REV = TA + 100 + 1000 + 70; OPT_ALL = TA + TB; WELCOME = 200

    S = []
    cv = Table([[[Paragraph("RISETRACK", st("k", fontName="CB", fontSize=10.5, leading=13, textColor=colors.HexColor("#7FE3D5"))), Spacer(1,3),
                  Paragraph(T("Bilan et prix", "Summary and prices"), st("t", fontName="CB", fontSize=28, leading=32, textColor=colors.white)), Spacer(1,4),
                  Paragraph(T("Tes priorités : l'essentiel pour une application solide qui génère des revenus. Un prix par élément, en dollars canadiens (CAD), et le choix de payer petit à petit.",
                              "Your priorities: the essentials for a solid app that earns revenue. A price per item, in Canadian dollars (CAD), and the choice to pay little by little."), st("s", fontSize=12, leading=16, textColor=colors.HexColor("#DCE8F5")))]]], colWidths=[CW])
    cv.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY), ("LEFTPADDING", (0,0), (-1,-1), 16), ("RIGHTPADDING", (0,0), (-1,-1), 16), ("TOPPADDING", (0,0), (-1,-1), 16), ("BOTTOMPADDING", (0,0), (-1,-1), 16)]))
    meta = Table([[Paragraph(T("<b>Préparé pour</b><br/>Amazigh", "<b>Prepared for</b><br/>Amazigh"), cell), Paragraph(T("<b>Préparé par</b><br/>Up Agency", "<b>Prepared by</b><br/>Up Agency"), cell),
                   Paragraph(T("<b>Date</b><br/>19 octobre 2026", "<b>Date</b><br/>October 19, 2026"), cell), Paragraph(T("<b>Devise</b><br/>Dollars canadiens (CAD)", "<b>Currency</b><br/>Canadian dollars (CAD)"), cell)]], colWidths=[CW/4]*4)
    meta.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), SOFT), ("LINEBELOW", (0,0), (-1,-1), 2, TEAL), ("LEFTPADDING", (0,0), (-1,-1), 12), ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
    S += [cv, meta, Spacer(1, 12)]
    S += [Paragraph(T("Merci pour ta liste et tes priorités. Tu m'as dit que le plus important, c'est <b>l'abonnement Premium, les notifications et les bugs importants</b>, après les petites touches. Voici exactement cela, en petites étapes, avec un prix pour chaque élément. <b>Tous les prix sont en dollars canadiens (CAD).</b>",
                      "Thank you for your list and your priorities. You told me the most important things are <b>the Premium subscription, the notifications and the important bugs</b>, after the small touches. Here is exactly that, in small steps, with a price for every item. <b>All prices are in Canadian dollars (CAD).</b>"), body), Spacer(1, 8)]
    S += [bar(T("Comment c'est organisé", "How it is organized"), "1"), Spacer(1, 6)]
    two = Table([[[Paragraph(T("Étape A : en ligne tout de suite", "Step A: live right away"), h3), Paragraph(T("Les petites touches et la fiabilité. Ces changements se font côté site : ils sont visibles dans l'application dès que je les publie, <b>sans attendre Apple</b>.", "The small touches and reliability. These changes are made on the website side: they appear in the app as soon as I publish them, <b>without waiting for Apple</b>."), body)],
                  [Paragraph(T("Étape B : une seule mise à jour Apple", "Step B: one single Apple update"), h3), Paragraph(T("L'abonnement, les notifications, la suppression du compte et le logo. Tout est regroupé dans <b>une seule version</b>, donc une seule validation Apple, plus rapide et plus sûre.", "The subscription, the notifications, the account deletion and the logo. Everything is grouped in <b>one single version</b>, so one single Apple review, faster and safer."), body)]]], colWidths=[CW/2, CW/2])
    two.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 4), ("RIGHTPADDING", (0,0), (-1,-1), 12)]))
    S += [two, Spacer(1, 6), box([Paragraph(T("<b>Ton approbation Apple est protégée :</b> tout est testé sur iPhone avant l'envoi, avec seulement les autorisations Caméra et Photos, connexion par email et mot de passe, et un abonnement qui suit les règles d'Apple.",
                                             "<b>Your Apple approval is protected:</b> everything is tested on iPhone before sending, with only the Camera and Photos permissions, email and password login, and a subscription that follows Apple's rules."), body)]), PageBreak()]

    hdr = [T("#", "#"), T("CE QUE TU OBTIENS", "WHAT YOU GET"), T("QUAND", "WHEN"), T("PRIX", "PRICE")]
    S += [bar(T("Étape A : petites touches et fiabilité", "Step A: small touches and reliability"), "2"), Spacer(1, 6)]
    S += [table([(a, b, c, money(d)) for a, b, c, d in Aitems], [CW*0.07, CW*0.5, CW*0.27, CW*0.16], hdr, right=(3,), total=("", T("Total étape A", "Total step A"), "", money(TA))), Spacer(1, 12)]
    S += [bar(T("Étape B : abonnement, notifications et logo", "Step B: subscription, notifications and logo"), "3"), Spacer(1, 6)]
    S += [table([(a, b, c, money(d)) for a, b, c, d in Bitems], [CW*0.07, CW*0.5, CW*0.27, CW*0.16], hdr, right=(3,), total=("", T("Total étape B", "Total step B"), "", money(TB))), Spacer(1, 6),
          Paragraph(T("L'envoi à Apple, les tests sur iPhone et la gestion d'une éventuelle remarque d'Apple sont inclus dans l'étape B.", "Sending to Apple, testing on iPhone and handling any Apple remark are included in step B."), small), Spacer(1, 10)]
    S += [bar(T("Aperçu : logo agrandi (point B5)", "Preview: enlarged logo (item B5)"), "4"), Spacer(1, 6)]
    img = Image(BASE + "02-work/icon-apercu-avant-apres.png", width=95*mm, height=95*mm*380/780)
    cap = Table([[img, [Paragraph(T("<b>À gauche :</b> aujourd'hui, le logo laisse beaucoup de noir autour de lui.<br/><b>À droite :</b> le logo agrandi remplit mieux l'icône, comme les autres applications.", "<b>Left:</b> today, the logo leaves a lot of black around it.<br/><b>Right:</b> the enlarged logo fills the icon better, like the other apps."), cell), Spacer(1, 4),
                        Paragraph(T("Aperçu réalisé à partir de ta capture d'écran, la version finale sera nette et en haute qualité.", "Preview made from your screenshot, the final version will be sharp and high quality."), small)]]], colWidths=[100*mm, CW-100*mm])
    cap.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 0)]))
    S += [cap, PageBreak()]

    S += [bar(T("Tes options, selon ton budget", "Your options, depending on your budget"), "5"), Spacer(1, 6)]
    opts = [(T("DÉPART", "START"), T("Étape A seulement", "Step A only"), T("Les petites touches, les habitudes et les bugs importants, en ligne tout de suite.", "The small touches, the habits and the important bugs, live right away."), TA, NAVY),
            (T("REVENUS", "REVENUE"), T("A + abonnement", "A + subscription"), T("Étape A, suppression du compte, abonnement Premium de base et logo. Pour commencer à gagner de l'argent.", "Step A, account deletion, base Premium subscription and logo. To start earning money."), OPT_REV, TEAL),
            (T("ESSENTIEL COMPLET", "COMPLETE ESSENTIALS"), "A + B", T("Tout ce que tu as demandé comme essentiel, avec l'essai gratuit et les notifications.", "Everything you asked for as essential, with the free trial and the notifications."), OPT_ALL, GOLD)]
    cells = []
    for n, sub, d, p, col in opts:
        c = Table([[Paragraph(n, st("tn", fontName="CB", fontSize=9.5, leading=12, textColor=colors.white, alignment=TA_CENTER))], [Paragraph(sub, st("ts", fontName="CB", fontSize=10.5, alignment=TA_CENTER))],
                   [Paragraph(money(p), st("tp", fontName="CB", fontSize=19, leading=24, alignment=TA_CENTER, textColor=col))], [Paragraph(d, st("td", fontSize=9.5, leading=12.5))]], colWidths=[CW/3 - 6])
        c.setStyle(TableStyle([("BACKGROUND", (0,0), (0,0), col), ("BACKGROUND", (0,1), (0,3), SOFT), ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
        cells.append(c)
    g = Table([cells], colWidths=[CW/3]*3); g.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 0), ("RIGHTPADDING", (0,0), (-1,-1), 6)]))
    S += [g, Spacer(1, 6), Paragraph(T("En option, sur n'importe quelle formule : <b>vraie page d'accueil avant la connexion</b> (ton point 1), côté site, <b>%s</b>." % money(WELCOME),
                                       "Optional, on any option: <b>a real welcome page before sign in</b> (your point 1), website side, <b>%s</b>." % money(WELCOME)), body), Spacer(1, 10)]
    S += [bar(T("Payer petit à petit", "Paying little by little"), "6"), Spacer(1, 6)]
    S += [Paragraph(T("Tu n'as pas à tout payer d'un coup. Chaque élément se règle séparément, <b>avant que je commence cet élément</b>. Les gros éléments sont coupés en plusieurs paiements. Rien ne démarre sans ton paiement et ton accord écrit dans notre conversation, et tu reçois un reçu à chaque fois.",
                      "You do not have to pay everything at once. Each item is paid separately, <b>before I start that item</b>. The big items are split into several payments. Nothing starts without your payment and your written agreement in our conversation, and you get a receipt every time."), body), Spacer(1, 4)]
    plan = [("A1", money(100), T("Avant de commencer", "Before starting")), ("A2", money(130), T("Avant de commencer", "Before starting")), ("A3", money(200), T("Avant de commencer", "Before starting")),
            ("B1", money(100), T("Avant de commencer", "Before starting")),
            ("B2", money(350) + " + " + money(350) + " + " + money(300), T("Au début, quand l'abonnement fonctionne en version de test, puis à l'envoi à Apple", "At the start, when the subscription works in the test version, then when sent to Apple")),
            ("B3", money(200), T("Avant de commencer", "Before starting")), ("B4", money(190) + " + " + money(190), T("Au début, puis quand les rappels fonctionnent en version de test", "At the start, then when the reminders work in the test version")),
            ("B5", money(70), T("Avant de commencer", "Before starting"))]
    S += [table(plan, [CW*0.1, CW*0.42, CW*0.48], [T("ÉLÉMENT", "ITEM"), T("PAIEMENT", "PAYMENT"), T("QUAND", "WHEN")]), Spacer(1, 6),
          Paragraph(T("Moyen de paiement : celui que nous avons déjà utilisé (Sendwave), ou un autre moyen que nous convenons ensemble.", "Payment method: the one we already used (Sendwave), or another method we agree on together."), small), Spacer(1, 10)]
    S += [bar(T("Ce dont j'ai besoin de toi", "What I need from you"), "7"), Spacer(1, 6)]
    for t in [T("Ton choix : Départ, Revenus ou Essentiel complet (et la page d'accueil en option ou non).", "Your choice: Start, Revenue or Complete essentials (and the welcome page as an option or not)."),
              T("Pour l'abonnement : les prix que tu veux (mensuel et annuel), et que l'accord Apple « Paid Apps » soit actif dans ton compte App Store Connect avec tes informations bancaires et fiscales.", "For the subscription: the prices you want (monthly and yearly), and the Apple “Paid Apps” agreement active in your App Store Connect account with your bank and tax details."),
              T("Ton accord écrit dans notre conversation, et le paiement de l'élément concerné, avant de commencer.", "Your written agreement in our conversation, and payment of the item concerned, before starting.")]:
        S.append(Paragraph(t, bul, bulletText="•"))
    S += [Spacer(1, 8), box([Paragraph(T("<b>Ce qui n'est pas inclus</b> (à voir plus tard, quand l'application génère des revenus) : design moderne complet, tracker refait, page Mon parcours simplifiée, cartes de progrès à partager, nouvelles captures d'écran App Store. Tout ce qui s'ajoute après cet accord fait l'objet d'une petite offre séparée.",
                                         "<b>Not included</b> (to look at later, when the app earns revenue): full modern design, redone tracker, simplified My Journey page, shareable progress cards, new App Store screenshots. Anything added after this agreement gets a small separate offer."), body)])]
    out = BASE + ("RiseTrack-Bilan-et-Prix-v2-EN-copie-pour-Abdulwasiu.pdf" if EN else "RiseTrack-Bilan-et-Prix-v2-FR-CLIENT.pdf")
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=16*mm, bottomMargin=20*mm, title=T("RiseTrack: Bilan et prix", "RiseTrack: Summary and prices"), author="Up Agency")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(LM, 20*mm, CW, H-36*mm, 0, 0, 0, 0)], onPage=on_page)])
    doc.build(S)
    return TA, TB, OPT_REV, OPT_ALL
print(build("fr")); print(build("en"))

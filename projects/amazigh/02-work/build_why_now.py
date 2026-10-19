from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf")); pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf")); pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))
pdfmetrics.registerFontFamily("C", normal="C", bold="CB", italic="CI", boldItalic="CB")
NAVY = colors.HexColor("#0F2747"); TEAL = colors.HexColor("#12A594"); SOFT = colors.HexColor("#EAF6F4"); GREY = colors.HexColor("#5B6B7D")
LINE = colors.HexColor("#D9E1E8"); ZEBRA = colors.HexColor("#F6F9FB"); GOLD = colors.HexColor("#E59B12"); AMBER = colors.HexColor("#FBF4E6")
W, H = A4; LM = RM = 16*mm; CW = W - LM - RM
BASE = "/home/user/Abdulwasiu-Freelancing-Journey/projects/amazigh/"

def build(lang):
    EN = lang == "en"
    T = lambda fr, en: en if EN else fr
    def money(n): return ("${:,.0f}".format(n)) if EN else ("{:,.0f} $".format(n).replace(",", " "))
    def st(n, **k):
        b = dict(fontName="C", fontSize=10.3, leading=14, textColor=colors.HexColor("#1B2733")); b.update(k); return ParagraphStyle(n, **b)
    body = st("b"); small = st("s", fontSize=8.8, leading=12, textColor=GREY); cell = st("c", fontSize=9.6, leading=12.6); cellb = st("cb", fontName="CB", fontSize=9.6, leading=12.6)
    h2 = st("h2", fontName="CB", fontSize=13, leading=17, textColor=colors.white); h3 = st("h3", fontName="CB", fontSize=11.5, leading=15, textColor=colors.HexColor("#0E8577"))
    label = T("RiseTrack  |  Pourquoi maintenant  |  Document confidentiel", "RiseTrack  |  Why now  |  ENGLISH COPY FOR ABDULWASIU, NOT FOR THE CLIENT")
    def on_page(c, doc):
        c.saveState(); c.setFillColor(NAVY); c.rect(0, H-5*mm, W, 5*mm, stroke=0, fill=1); c.setFillColor(TEAL if not EN else GOLD); c.rect(0, H-5*mm, 40*mm, 5*mm, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.line(LM, 14*mm, W-RM, 14*mm); c.setFont("C", 8.5); c.setFillColor(GREY); c.drawString(LM, 9.5*mm, label); c.restoreState()
    def bar(title, color=TEAL):
        t = Table([[Paragraph(title, h2)]], colWidths=[CW]); t.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), color), ("LEFTPADDING", (0,0), (-1,-1), 10), ("TOPPADDING", (0,0), (-1,-1), 5), ("BOTTOMPADDING", (0,0), (-1,-1), 5)])); return t
    S = []
    cv = Table([[[Paragraph("RISETRACK", st("k", fontName="CB", fontSize=10.5, leading=13, textColor=colors.HexColor("#7FE3D5"))), Spacer(1,3),
                  Paragraph(T("Pourquoi maintenant, et comment avancer sans stress", "Why now, and how to move forward without stress"), st("t", fontName="CB", fontSize=18, leading=22, textColor=colors.white)), Spacer(1,3),
                  Paragraph(T("Un budget léger, payé semaine par semaine, avec un résultat visible chaque semaine. Tu choisis simplement ta formule.", "A light budget, paid week by week, with a visible result every week. You simply choose your plan."), st("s", fontSize=10.5, leading=14, textColor=colors.HexColor("#DCE8F5")))]]], colWidths=[CW])
    cv.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY), ("LEFTPADDING", (0,0), (-1,-1), 14), ("RIGHTPADDING", (0,0), (-1,-1), 14), ("TOPPADDING", (0,0), (-1,-1), 9), ("BOTTOMPADDING", (0,0), (-1,-1), 9)]))
    S += [cv, Spacer(1, 7), bar(T("Ce que ça change pour RiseTrack", "What it changes for RiseTrack")), Spacer(1, 6)]
    cards = [(T("Elle gagne enfin de l'argent", "It finally earns money"), T("Sans abonnement, personne ne peut payer. Avec l'abonnement Premium, chaque nouvel utilisateur peut devenir un revenu.", "Without a subscription, nobody can pay. With the Premium subscription, every new user can become revenue.")),
             (T("Les utilisateurs restent", "Users stay"), T("Une application d'habitudes vit de ses rappels. Sans notifications, les gens oublient, puis ils partent.", "A habit app lives on its reminders. Without notifications, people forget, then they leave.")),
             (T("Elle paraît solide", "It looks solid"), T("Un bandeau Base44, des habitudes qui disparaissent ou des bugs donnent une image non finie et coûtent des avis négatifs.", "A Base44 badge, habits that disappear or bugs give an unfinished image and cost bad reviews.")),
             (T("Apple reste content", "Apple stays happy"), T("La suppression complète du compte est exigée par Apple. La faire maintenant évite un refus plus tard.", "Complete account deletion is required by Apple. Doing it now avoids a rejection later."))]
    g = Table([[Paragraph(h, st("ch", fontName="CB", fontSize=10.3, leading=12.5, textColor=NAVY)) for h, d in cards], [Paragraph(d, cell) for h, d in cards]], colWidths=[CW/4]*4)
    g.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), SOFT), ("LINEABOVE", (0,0), (-1,0), 3, TEAL), ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7),
                           ("TOPPADDING", (0,0), (-1,0), 6), ("BOTTOMPADDING", (0,0), (-1,0), 2), ("TOPPADDING", (0,1), (-1,1), 0), ("BOTTOMPADDING", (0,1), (-1,1), 7), ("LINEAFTER", (0,0), (2,-1), 4, colors.white)]))
    S += [g, Spacer(1, 5)]
    S += [Paragraph(T("<b>Le bon moment, c'est maintenant :</b> l'application vient d'être approuvée par Apple. C'est la période où tu peux attirer tes premiers utilisateurs et tes premiers avis. Attendre, c'est laisser passer cet élan.",
                      "<b>The right time is now:</b> the app has just been approved by Apple. This is the period when you can attract your first users and first reviews. Waiting means letting that momentum pass."), body), Spacer(1, 7)]
    S += [bar(T("Un exemple : comment l'investissement se rembourse", "An example: how the investment pays itself back")), Spacer(1, 6)]
    S += [Table([[Paragraph(T("<b>Exemple illustratif, pas une promesse.</b> Imaginons un abonnement à <b>6 $ CAD par mois</b>. Après la commission d'Apple (environ 15 % pour une petite entreprise), il reste environ <b>5,10 $ CAD</b> par mois et par abonné. "
                                "L'option Revenus (<b>1 600 $ CAD</b>) est alors remboursée avec environ <b>26 abonnés pendant un an</b>. Les abonnés suivants sont du bénéfice. Tu choisis le prix de ton abonnement.",
                                "<b>Illustrative example, not a promise.</b> Imagine a subscription at <b>CAD $6 per month</b>. After Apple's commission (about 15 percent for a small business), about <b>CAD $5.10</b> remains per subscriber per month. "
                                "The Revenue option (<b>CAD $1,600</b>) is then paid back with about <b>26 subscribers for one year</b>. Every subscriber after that is profit. You choose the price of your subscription."), body)]], colWidths=[CW])]
    S[-1].setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), AMBER), ("LINEBEFORE", (0,0), (0,-1), 4, GOLD), ("LEFTPADDING", (0,0), (-1,-1), 12), ("RIGHTPADDING", (0,0), (-1,-1), 12), ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 8)]))
    S += [Spacer(1, 7), bar(T("Un budget amical : tu paies semaine par semaine", "A friendly budget: you pay week by week")), Spacer(1, 6)]
    wk = lambda *a: " | ".join(a)
    rows = [(T("1  DÉPART", "1  START"), money(430) + " CAD", T("3 semaines", "3 weeks"),
             T("Sem. 1 : 100 $ (bandeau et haut de l'écran). Sem. 2 : 130 $ (habitudes). Sem. 3 : 200 $ (bugs importants).", "Wk 1: $100 (badge and top of screen). Wk 2: $130 (habits). Wk 3: $200 (important bugs).")),
            (T("2  REVENUS", "2  REVENUE"), money(1600) + " CAD", T("7 semaines", "7 weeks"),
             T("Les 3 premières semaines comme Départ, puis sem. 4 : 170 $ (suppression du compte et logo), sem. 5 : 350 $, sem. 6 : 350 $, sem. 7 : 300 $ (abonnement Premium, par étapes).", "First 3 weeks like Start, then wk 4: $170 (account deletion and logo), wk 5: $350, wk 6: $350, wk 7: $300 (Premium subscription, in stages).")),
            (T("3  ESSENTIEL COMPLET", "3  COMPLETE ESSENTIALS"), money(2180) + " CAD", T("10 semaines", "10 weeks"),
             T("Comme Revenus, puis sem. 8 : 200 $ (essai gratuit et page de prix), sem. 9 : 190 $ et sem. 10 : 190 $ (notifications).", "Like Revenue, then wk 8: $200 (free trial and price page), wk 9: $190 and wk 10: $190 (notifications)."))]
    data = [[Paragraph(h, st("hd", fontName="CB", fontSize=8.6, leading=11, textColor=GREY)) for h in [T("FORMULE", "PLAN"), T("TOTAL", "TOTAL"), T("DURÉE", "DURATION"), T("PAIEMENTS PAR SEMAINE", "WEEKLY PAYMENTS")]]]
    for r in rows: data.append([Paragraph(r[0], cellb), Paragraph(r[1], cellb), Paragraph(r[2], cell), Paragraph(r[3], cell)])
    t = Table(data, colWidths=[CW*0.2, CW*0.15, CW*0.12, CW*0.53])
    t.setStyle(TableStyle([("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LINEBELOW", (0,0), (-1,-1), 0.5, LINE), ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4), ("BACKGROUND", (0,2), (-1,2), ZEBRA)]))
    S += [t, Spacer(1, 4), Paragraph(T("Tous les montants sont en dollars canadiens (CAD). Chaque semaine : tu paies, je livre quelque chose de visible. Si un paiement est trop grand pour une semaine, on le coupe en deux semaines.",
                                      "All amounts are in Canadian dollars (CAD). Every week: you pay, I deliver something visible. If a payment is too big for one week, we split it over two weeks."), small), Spacer(1, 6)]
    S += [bar(T("Sans risque pour toi", "No risk for you")), Spacer(1, 6)]
    for tx in [T("<b>Tu paies avant chaque élément seulement,</b> jamais d'avance sur tout.", "<b>You only pay before each item,</b> never everything in advance."),
               T("<b>Tu peux t'arrêter quand tu veux.</b> Tu ne paies que ce que tu as choisi.", "<b>You can stop whenever you want.</b> You only pay for what you chose."),
               T("<b>Tu vois le résultat chaque semaine</b> avant de décider de continuer.", "<b>You see the result every week</b> before deciding to continue."),
               T("<b>Ton approbation Apple est protégée :</b> tout est testé sur iPhone avant l'envoi.", "<b>Your Apple approval is protected:</b> everything is tested on iPhone before sending.")]:
        S.append(Paragraph(tx, st("bu", fontSize=9.6, leading=12.6, leftIndent=11, bulletIndent=0), bulletText="•"))
    S += [Spacer(1, 5)]
    cta = Table([[Paragraph(T("Choisis simplement : 1, 2 ou 3.", "Simply choose: 1, 2 or 3."), st("cta", fontName="CB", fontSize=15, leading=19, textColor=colors.white, alignment=TA_CENTER))],
                 [Paragraph(T("Je commence dès que le premier paiement est fait. Si ce n'est pas le bon moment, dis-le-moi, aucun souci.", "I start as soon as the first payment is made. If it is not the right time, tell me, no problem."), st("cta2", fontSize=10.5, leading=14, textColor=colors.HexColor("#DCE8F5"), alignment=TA_CENTER))]], colWidths=[CW])
    cta.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY), ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6)]))
    S += [cta]
    out = BASE + ("RiseTrack-Pourquoi-maintenant-FR-CLIENT.pdf" if not EN else "RiseTrack-Why-now-EN-copie-pour-Abdulwasiu.pdf")
    doc = BaseDocTemplate(out, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=14*mm, bottomMargin=18*mm, title="RiseTrack", author="Up Agency")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(LM, 18*mm, CW, H-32*mm, 0, 0, 0, 0)], onPage=on_page)])
    doc.build(S)
build("fr"); build("en")

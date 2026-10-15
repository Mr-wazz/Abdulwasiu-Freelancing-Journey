from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf")); pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf")); pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))
pdfmetrics.registerFontFamily("C", normal="C", bold="CB", italic="CI", boldItalic="CB")
INK = colors.HexColor("#1D2A24"); SAGE = colors.HexColor("#8FB09B"); SAGE_D = colors.HexColor("#5F8570"); TEAL = colors.HexColor("#2F6F7E")
MINT = colors.HexColor("#EEF4F0"); LINE = colors.HexColor("#D8E3DC"); GREY = colors.HexColor("#5E6D65"); ZEBRA = colors.HexColor("#F7FAF8")
GOLD = colors.HexColor("#C98A1B"); RED = colors.HexColor("#B3402F"); AMBER_BG = colors.HexColor("#FBF4E6")
LOGO = "/home/user/ftlr-ios-wrapper/www/logo.png"
W, H = A4; LM = RM = 18 * mm; CW = W - LM - RM
BASE = "/home/user/Abdulwasiu-Freelancing-Journey/projects/ftlr-fitness/"

def st(n, **k):
    b = dict(fontName="C", fontSize=10.5, leading=14.5, textColor=INK); b.update(k); return ParagraphStyle(n, **b)
body = st("body"); small = st("small", fontSize=9, leading=12.5, textColor=GREY)
cell = st("cell", fontSize=9.6, leading=12.8); cellb = st("cellb", fontName="CB", fontSize=9.6, leading=12.8)
h2 = st("h2", fontName="CB", fontSize=14, leading=18, textColor=colors.white); h3 = st("h3", fontName="CB", fontSize=11.5, leading=15, textColor=SAGE_D)
head = st("head", fontName="CB", fontSize=8.6, leading=11, textColor=GREY)
bul = st("bul", fontSize=10, leading=13.6, leftIndent=11, bulletIndent=0)
bulc = st("bulc", fontSize=9.4, leading=12.4, leftIndent=9, bulletIndent=0)

# ---------------- data ----------------
# (phase, name, client_get, client_value, when, price, month, scope, need, hours, touches_app, done_when)
O = [
 ("Launch ready", "App Store listing pack", "Your App Store name, subtitle, keywords and promotional text, written and checked so they are ready to paste.", "Strangers find FTLR and understand it in seconds.", "Right away", 150, "Oct 2026",
  "2 subtitle options, keyword string of exactly 100 characters, promotional text, a check against Apple's rules. Delivered as a one page document.", "Her choice of tone, one approval.", 2, False, "She approves the final words."),
 ("Launch ready", "App Store screenshots (5 designed)", "Five captioned screenshots using your real screens and telling one story.", "Screenshots decide who installs.", "After the listing", 250, "Oct 2026",
  "5 screenshots at Apple's required size with captions, PNG files, story order from the playbook.", "Screens or a quick screen recording of Home, Workouts, Recipes, Ask Your Coach and Chat.", 4, False, "She approves all five images."),
 ("Launch ready", "Launch announcement pack", "Your launch email, community post and pinned chat message, written in your voice.", "Launch day is ready before launch day.", "Before Nov 1", 120, "Oct 2026",
  "1 email, 2 community posts, 1 pinned chat message, with links to be added.", "Launch date, her tone, her list tool.", 2, False, "She approves the copy."),
 ("Launch ready", "Welcome and 7 day message sequence", "Day 0, 1, 3, 7 and 14 messages written and set up.", "A first workout within 24 hours keeps members.", "Launch week", 180, "Nov 2026",
  "5 short messages, set up as scheduled messages or a simple checklist she can send.", "Access to her email or chat tool.", 3, False, "Messages are live or ready to send."),
 ("Launch week", "Ratings prompt at happy moments", "A polite request for a rating after a finished workout, never at a bad time.", "Ratings build trust and ranking.", "After the first 20 members", 200, "Nov 2026",
  "Apple's in app rating prompt in the iPhone app after a member's 3rd finished workout. Shipped in app version 1.1 and tested in TestFlight.", "Her approval of the trigger rule.", 4, True, "Prompt appears correctly in TestFlight."),
 ("Launch week", "Purchase flow polish", "Clearer progress and a faster unlock after someone subscribes.", "Waiting after paying feels risky. Today it can take about 12 seconds.", "After the first real purchases", 180, "Nov 2026",
  "Better progress message, faster hand off to the member area, sandbox purchase test. Shipped in app version 1.1.", "Nothing, only approval.", 3, True, "Sandbox purchase feels quick and clear."),
 ("Build the habit", "Design quick pack", "Three improvements to your sign in and home screen, in your brand.", "A calm, consistent first impression.", "After the launch week review", 350, "Nov 2026",
  "3 agreed design improvements in Base44 (web side), published.", "Her choice of 3 improvements.", 5, False, "Changes are live and approved."),
 ("Build the habit", "Onboarding flow", "A goal choice, a welcome note from you and a first workout button.", "Turns installs into active members.", "After the design quick pack", 450, "Nov 2026",
  "Goal screen, note from Leah, first workout button, in Base44 (web side), tested on iPhone.", "Her welcome text and photo.", 7, False, "New members see the flow and start a workout."),
 ("Build the habit", "Analytics dashboard", "One simple view: members, active members, subscriptions and cancellations.", "You fix the biggest leak first.", "30 days after launch", 400, "Dec 2026",
  "Admin page with key numbers from her data and RevenueCat, plus a short how to read it guide.", "Read access to RevenueCat and her admin login.", 6, False, "Numbers match RevenueCat."),
 ("Build the habit", "Workout reminders (push)", "Gentle reminders that bring members back to train.", "Habits need a nudge.", "After onboarding is live", 550, "Dec 2026",
  "Push notifications in the iPhone app, a simple reminder schedule, tested in TestFlight, submitted as a new app version.", "Apple push key from her Apple account, her reminder wording.", 10, True, "Reminders arrive on a test phone."),
 ("Grow", "Android, step 1: accounts and setup", "Your Google Play account, app record and billing set up.", "Opens the other half of the market.", "When Android demand is confirmed", 250, "Dec 2026",
  "Google Play developer account guidance, app record, billing and RevenueCat set up for Android.", "Google Play developer account (one time fee paid by her).", 3, False, "Play Console is ready for a build."),
 ("Grow", "Android, step 2: build and billing", "The Android app with the same subscriptions as iPhone.", "Same app, same plans.", "After step 1", 400, "Dec 2026",
  "Android build from the same app, Google billing through RevenueCat, internal test build.", "Test phone or testers.", 6, False, "Test purchase works on Android."),
 ("Grow", "Android, step 3: store listing and submission", "Your Google Play listing, screenshots and submission.", "Live on Google Play.", "After step 2", 250, "Jan 2027",
  "Listing, screenshots, privacy details, submission and review questions.", "Approval of the listing.", 4, False, "Submitted, then approved."),
 ("Grow", "Retention automation, step 1: design", "Welcome and win back messages designed for the right moments.", "Quiet members come back.", "After analytics shows drop off", 350, "Jan 2027",
  "Flow map and message copy for welcome, 10 days quiet and win back, in her chosen tool.", "Her choice of tool and tone.", 5, False, "She approves the flows."),
 ("Grow", "Retention automation, step 2: build and test", "Email and text messages set up, tested and running.", "It works on its own.", "After step 1", 400, "Jan 2027",
  "Build in GoHighLevel or her tool, connect to member data, test with 3 test members, go live.", "Tool access and consent wording.", 6, False, "Test members receive the right messages."),
 ("Grow", "Invite a friend system", "A personal invite link with a reward for both people.", "The cheapest growth there is.", "After retention is live", 450, "Jan 2027",
  "Invite link, tracking of who joined, and a reward that follows Apple's rules (for example bonus content, not outside discounts).", "Her choice of reward.", 7, True, "A test invite is tracked end to end."),
]
FEE = 0.20
TOTAL = sum(o[5] for o in O)

def footer_factory(label):
    def on_page(c, doc):
        c.saveState()
        c.setFillColor(INK); c.rect(0, H - 5 * mm, W, 5 * mm, stroke=0, fill=1)
        c.setFillColor(SAGE); c.rect(0, H - 5 * mm, 40 * mm, 5 * mm, stroke=0, fill=1)
        c.setStrokeColor(LINE); c.line(LM, 15 * mm, W - RM, 15 * mm)
        c.setFont("C", 8.5); c.setFillColor(GREY)
        c.drawString(LM, 10 * mm, label); c.drawRightString(W - RM, 10 * mm, "Page %d" % doc.page)
        c.restoreState()
    return on_page

def bar(title, letter=None, color=SAGE_D):
    if letter:
        t = Table([[Paragraph(letter, st("l", fontName="CB", fontSize=14, leading=18, textColor=colors.white, alignment=TA_CENTER)), Paragraph(title, h2)]], colWidths=[10 * mm, CW - 10 * mm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("BACKGROUND", (0, 0), (0, 0), INK), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (1, 0), (1, 0), 10), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    else:
        t = Table([[Paragraph(title, h2)]], colWidths=[CW])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t
def bullets(items, style=bul): return [Paragraph(i, style, bulletText="•") for i in items]
def box(flow, bg=MINT, edge=SAGE_D):
    t = Table([[flow]], colWidths=[CW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("LINEBEFORE", (0, 0), (0, -1), 4, edge), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return t
def table(rows, widths, header=None, bold_first=True, align_right=()):
    data = []
    if header: data.append([Paragraph(h, head) for h in header])
    for r in rows:
        data.append([Paragraph(str(x), cellb if (i == 0 and bold_first) else cell) for i, x in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    s = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE), ("TOPPADDING", (0, 0), (-1, -1), 4.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5), ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    off = 1 if header else 0
    for i in range(off, len(data)):
        if (i - off) % 2 == 1: s.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(s)); return t
def cover(kicker, title, sub, meta):
    cv = Table([[[Paragraph(kicker, st("k", fontName="CB", fontSize=10.5, leading=13, textColor=colors.HexColor("#BFD9C8"))), Spacer(1, 3),
                  Paragraph(title, st("t", fontName="CB", fontSize=26, leading=30, textColor=colors.white)), Spacer(1, 4),
                  Paragraph(sub, st("s", fontSize=12, leading=16, textColor=colors.HexColor("#E3EEE7")))]]], colWidths=[CW])
    cv.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), INK), ("LEFTPADDING", (0, 0), (-1, -1), 16), ("RIGHTPADDING", (0, 0), (-1, -1), 16), ("TOPPADDING", (0, 0), (-1, -1), 16), ("BOTTOMPADDING", (0, 0), (-1, -1), 16)]))
    mt = Table([[Paragraph("<b>%s</b><br/>%s" % m, cell) for m in meta]], colWidths=[CW / len(meta)] * len(meta))
    mt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), MINT), ("LINEBELOW", (0, 0), (-1, -1), 2, SAGE_D), ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return [cv, mt, Spacer(1, 12)]
def money(n): return "${:,.0f}".format(n)

def build(path, label, story):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=16 * mm, bottomMargin=20 * mm, title=label, author="Up Agency")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(LM, 20 * mm, CW, H - 36 * mm, 0, 0, 0, 0)], onPage=footer_factory(label))])
    doc.build(story)

# =====================================================================
#  DOCUMENT 1: INTERNAL (with prices)
# =====================================================================
S = cover("PRIVATE: FOR ABDULWASIU ONLY, DO NOT SEND", "FTLR Fitness: Drip Billing Plan", "How to earn close to $5,000 from one happy client by selling small steps, one at a time. Everything you need to know, in plain words.",
          [("Client", "Leah Stukov, FTLR Fitness"), ("Goal", "About $5,000 gross"), ("Date", "October 15, 2026"), ("Version", "1.0")])
S += [bar("The idea in one minute", "1"), Spacer(1, 6)]
S += [Paragraph("Instead of asking Leah for one big payment, you offer <b>small, separate steps</b> of $120 to $450. Each step has one clear result she can see. "
                "Each yes is easy because the risk is small and she already trusts you. The steps add up to about <b>%s</b>, plus a <b>$199 monthly care plan</b>." % money(TOTAL), body), Spacer(1, 6)]
S += bullets(["<b>Why it works:</b> small yeses build trust. A $150 step feels easy. A $5,000 project makes people pause.",
              "<b>Why it protects you:</b> every step is paid and approved before the next one starts. You never carry unpaid work.",
              "<b>Why it protects her:</b> every step is a Fiverr custom offer with protected payment, so she feels safe.",
              "<b>Your value stays high:</b> each step solves a real problem from the playbook, so you are not nickel and diming, you are guiding."])
S += [Spacer(1, 8)]
nett = TOTAL * (1 - FEE)
S += [box([Paragraph("<b>The numbers.</b> One time steps: <b>%s</b> gross. After Fiverr's fee (about 20 percent, check your own dashboard): about <b>%s</b> net. "
                     "Care plan: $199 per month, about $597 in 3 months. Total with the care plan: about <b>%s</b> gross." % (money(TOTAL), money(nett), money(TOTAL + 597)), body)]), Spacer(1, 6)]
S += [box([Paragraph("<b>Decision for you.</b> If $5,000 means <b>after</b> Fiverr's fee, you need about <b>$6,250</b> gross. Tell me, and I will raise prices or add steps.", body)], bg=AMBER_BG, edge=GOLD), Spacer(1, 10)]

S += [bar("What if she does not buy everything?", "2"), Spacer(1, 6)]
cases = [("She buys only the 4 launch ready steps", sum(o[5] for o in O[:4])), ("Launch ready, launch week, design and onboarding (steps 1 to 8)", sum(o[5] for o in O[:8])),
         ("Everything up to the analytics dashboard (steps 1 to 9)", sum(o[5] for o in O[:9])), ("Everything (all 16 steps)", TOTAL)]
S += [table([(a, money(b), money(b * (1 - FEE))) for a, b in cases], [CW * 0.62, CW * 0.19, CW * 0.19], header=["SCENARIO", "GROSS", "NET AFTER FEE"]), Spacer(1, 6),
      Paragraph("This is why the plan is built in small steps: even a partial yes is real money, and a full yes reaches your target. Add the care plan on top in every case.", body), PageBreak()]

S += [bar("The 16 steps and what each one pays", "3"), Spacer(1, 6)]
rows = []
for i, o in enumerate(O, 1):
    rows.append((str(i), o[1], money(o[5]), money(o[5] * (1 - FEE)), o[6], o[4]))
rows.append(("", "TOTAL", money(TOTAL), money(nett), "", ""))
t = table(rows, [CW * 0.05, CW * 0.36, CW * 0.1, CW * 0.11, CW * 0.12, CW * 0.26], header=["#", "STEP", "PRICE", "NET", "MONTH", "OFFER IT WHEN"])
S += [t, Spacer(1, 10)]
S += [Paragraph("Cash by month (if every step is accepted)", h3)]
months = ["Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027"]
S += [table([(m, money(sum(o[5] for o in O if o[6] == m)), money(sum(o[5] for o in O if o[6] == m) * (1 - FEE))) for m in months], [CW * 0.4, CW * 0.3, CW * 0.3], header=["MONTH", "GROSS", "NET"]), PageBreak()]

S += [bar("How to run each step (your playbook)", "4"), Spacer(1, 6),
      Paragraph("Hours are my estimates. They help you see that each step stays profitable. If a step grows beyond its hours, stop and quote the extra separately.", small), Spacer(1, 6)]
for i, o in enumerate(O, 1):
    hd = Table([[Paragraph("%d. %s" % (i, o[1]), st("ch", fontName="CB", fontSize=10.5, textColor=colors.white)), Paragraph("%s  |  about %dh  |  %s per hour" % (money(o[5]), o[9], money(o[5] / o[9])), st("cr", fontName="CB", fontSize=9.5, textColor=colors.white, alignment=TA_RIGHT))]], colWidths=[CW * 0.55, CW * 0.45])
    hd.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SAGE_D if not o[10] else TEAL), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    cd = Table([[Paragraph("<b>You deliver</b><br/>%s" % o[7], cell), Paragraph("<b>You need from Leah</b><br/>%s" % o[8], cell), Paragraph("<b>Done when</b><br/>%s<br/><br/><b>Touches iPhone app:</b> %s" % (o[11], "YES, ships in an app update" if o[10] else "No"), cell)]],
               colWidths=[CW * 0.44, CW * 0.28, CW * 0.28])
    cd.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), MINT), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    S.append(KeepTogether([hd, cd, Spacer(1, 5)]))
S += [Paragraph("Blue headers are steps that change the iPhone app. Read the next page before you start those.", small), PageBreak()]

S += [bar("Protect the Apple approval (very important)", "5"), Spacer(1, 6)]
S += bullets(["<b>While Apple is reviewing:</b> do only copy, design and web side work. Do not upload a new iPhone build and do not edit things that would pull the app out of review.",
              "<b>Store listing changes</b> (subtitle, keywords, screenshots) can only be applied with a <b>new app version</b>. Promotional text can change anytime. So steps 1 and 2 are written now and applied in version 1.1.",
              "<b>Bundle app changes in version 1.1:</b> ratings prompt (step 5), purchase flow polish (step 6) and the new listing. One Apple review instead of four.",
              "<b>Later app versions:</b> reminders (step 10) and invite a friend (step 16) each need a new version, so bundle them when you can.",
              "<b>Always test in TestFlight</b> before submitting, and keep the demo account working.",
              "<b>Rewards and offers:</b> never add outside payment links or discounts inside the app. Rewards must follow Apple's rules."])
S += [Spacer(1, 10), bar("How to bill each step on Fiverr", "6"), Spacer(1, 6)]
S += bullets(["<b>1. Wait for her yes</b> to the message. Never send an offer she did not ask for.",
              "<b>2. Create a custom offer</b> in your Fiverr chat with Leah (the create offer button in the conversation).",
              "<b>3. Write the scope</b> in three lines: what you deliver, what you need from her, what is not included. Copy it from section 4.",
              "<b>4. Set the price and delivery time</b> from the table, and one or two revisions.",
              "<b>5. Start only after she accepts and pays.</b> The money is held by Fiverr until she approves the delivery.",
              "<b>6. Deliver, ask for approval,</b> then offer the next step. Fiverr releases your earnings after its clearing period (check your account for the exact days).",
              "<b>7. Big items split in steps</b> (Android, retention) are separate offers, so each payment stays small."])
S += [PageBreak()]

S += [bar("Messages to send", "7"), Spacer(1, 6)]
msgs = [
 ("Step 1: listing pack (after your call)", "Leah, thank you for your time today. The playbook gives you the structure. If you would like me to do the listing for you, I can write and check the App Store name, subtitle, keywords and promotional text so it is ready to paste. It is a small fixed job for $150, on Fiverr with payment protected. Shall I send the offer?"),
 ("Step 2: screenshots (after step 1 is approved)", "Leah, your listing words are ready. The next thing that decides who installs is the screenshots. I can design five captioned screenshots using your real screens, telling the story we planned: $250. I will need your screens or a quick screen recording. Want me to send the offer?"),
 ("Step 3: launch announcement pack", "Leah, launch is close. I can write your launch email, community post and pinned chat message in your voice, so launch day is ready: $120. Shall I send it?"),
 ("Step 4: welcome sequence", "Leah, the first week decides if new members stay. I can write and set up your Day 0, 1, 3, 7 and 14 messages: $180. Want me to send the offer?"),
 ("After any delivery (template)", "Leah, here is [WHAT WAS DELIVERED]. How does it look? If you are happy, the next thing that helps most is [NEXT STEP], because [ONE SENTENCE OF VALUE]. It is $[PRICE]. Want me to send the offer, or would you rather wait?"),
 ("If she says not now", "Of course, no pressure. I will keep it on the list and check in after launch week. Congratulations again on the launch."),
 ("If she asks for a discount", "I keep each step small and fixed so it stays easy. If the budget is tight, we can do the most important piece first and add the rest later."),
 ("If she asks for something extra, free", "Happy to help with that. It is outside the step we agreed, so I will send a small separate offer for it, so everything stays clear for both of us."),
]
S += [table(msgs, [CW * 0.28, CW * 0.72], header=["SITUATION", "MESSAGE"]), Spacer(1, 10)]

S += [bar("Risks and how to handle them", "8"), Spacer(1, 6)]
S += [table([("She is very busy", "Keep messages short. One step at a time. Offer one clear next step, never a menu."),
             ("She says yes but is slow to send material", "Do not start until you have what you need. Say so politely. The offer timer starts when you have it."),
             ("Scope grows", "Stop. Quote the extra as a new small offer. Never do it free."),
             ("Fiverr fee surprises you", "The tracker shows gross and net. Decide now if your target is gross or net."),
             ("An Apple rejection arrives", "It is covered by your first order (2 resubmissions). Do not start app changes until it is resolved."),
             ("She asks to pay outside Fiverr", "Say no kindly. Fiverr protects both of you, and it keeps your reviews and record.")], [CW * 0.3, CW * 0.7], header=["RISK", "WHAT TO DO"]), PageBreak()]

S += [bar("Your weekly routine and next 7 days", "9"), Spacer(1, 6)]
S += [Paragraph("Every Monday (15 minutes)", h3)] + bullets(["Open the tracker (FTLR-Revenue-Roadmap.xlsx) and update every status.", "Check what is paid, what is waiting, what is overdue.", "Send <b>one</b> next offer or one friendly check in.", "Ask yourself: did I deliver a visible win this week?"])
S += [Spacer(1, 6), Paragraph("Your next 7 days, in order", h3)] + bullets(["Finish the Apple submission items (video, notes, demo account) and confirm Apple's review is moving.",
      "Have the call with Leah using the presentation and your presenter notes. No prices on the call unless she asks.",
      "After the call, send <b>only step 1</b> (listing pack, $150) as a Fiverr offer.",
      "Deliver it fast and well. Then send step 3 (launch pack) before November 1.",
      "Ask her to accept delivery of the first order and leave the review. Accept her Reddit shoutout after that."])
S += [Spacer(1, 10), box([Paragraph("<b>The one rule behind everything:</b> value first, one small yes at a time, never push. If you keep delivering visible wins, the next yes comes easily.", body)])]
build(BASE + "FTLR-Drip-Billing-Plan-PRIVATE.pdf", "FTLR Fitness | Drip Billing Plan | PRIVATE, do not send", S)

# =====================================================================
#  DOCUMENT 2: CLIENT (no prices)
# =====================================================================
S = []
logo_w = 52 * mm; logo_h = logo_w * 284.0 / 600.0
S += cover("FOR LEAH STUKOV  |  FTLR FITNESS", "Your Growth Roadmap", "Thirteen small steps, taken one at a time, to turn your approved app into active, loyal members. You choose each step and you approve every result.",
           [("Prepared for", "Leah Stukov"), ("Company", "For the Long Run Fitness LLC"), ("Prepared by", "Up Agency"), ("Date", "October 15, 2026")])
S += [Paragraph("Congratulations on getting FTLR Fitness this far. An approved app is the starting line. This roadmap shows what can come next, in the order that makes the most sense, with the result you can expect from each step. "
                "It is a menu, not a commitment. Take what helps and leave the rest.", body), Spacer(1, 10)]
S += [bar("How we work together", "1"), Spacer(1, 6)]
pr = Table([[Paragraph("<b>One step at a time</b><br/>Each step is small, clear and has one visible result.", cell),
             Paragraph("<b>You stay in control</b><br/>Nothing starts without your written yes. Pause or stop any time.", cell),
             Paragraph("<b>You approve every result</b><br/>You see the work before we talk about the next step.", cell),
             Paragraph("<b>Your payment is protected</b><br/>Everything runs through Fiverr, so both of us are safe.", cell)]], colWidths=[CW / 4] * 4)
pr.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), MINT), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9), ("LINEAFTER", (0, 0), (2, -1), 3, colors.white)]))
S += [pr, Spacer(1, 10)]
S += [bar("The roadmap at a glance", "2"), Spacer(1, 6)]
phs = [("LAUNCH READY", "Oct to early Nov", "Be found and be ready on day one"), ("LAUNCH WEEK", "Nov", "Get the first ratings and a smooth first purchase"),
       ("BUILD THE HABIT", "Nov to Dec", "Turn new members into regular members"), ("GROW", "Dec to Jan", "Reach more people and keep them")]
cells = []
for n, w, d in phs:
    c = Table([[Paragraph(n, st("pn", fontName="CB", fontSize=9, leading=11, textColor=colors.white))], [Paragraph("<b>%s</b>" % w, cell)], [Paragraph(d, small)]], colWidths=[CW / 4 - 4])
    c.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), SAGE_D), ("BACKGROUND", (0, 1), (0, 2), MINT), ("LEFTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    cells.append(c)
g = Table([cells], colWidths=[CW / 4] * 4); g.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
S += [g, PageBreak()]

def step_rows(items):
    rows = []
    for n, name, get, val, when in items: rows.append((name, get, val, when))
    return table(rows, [CW * 0.2, CW * 0.31, CW * 0.27, CW * 0.22], header=["STEP", "WHAT YOU GET", "WHAT IT CHANGES", "A GOOD TIME"])
C = {}
S += [bar("Phase 1 and 2: be ready, then launch", "3"), Spacer(1, 6)]
S += [step_rows([(1, "App Store listing pack", O[0][2], O[0][3], "Now. Promotional text can change anytime. Name, subtitle and keywords go live with your next app update."),
                 (2, "Five designed screenshots", O[1][2], O[1][3], "After the listing. Applied with your next app update."),
                 (3, "Launch announcement pack", O[2][2], O[2][3], "Before November 1."),
                 (4, "Welcome and 7 day messages", O[3][2], O[3][3], "Launch week."),
                 (5, "Ratings prompt", O[4][2], O[4][3], "After your first 20 members. Ships in your next app update."),
                 (6, "Purchase flow polish", O[5][2], O[5][3], "After the first real purchases. Ships in your next app update.")]), Spacer(1, 10)]
S += [bar("Phase 3: build the habit", "4"), Spacer(1, 6)]
S += [step_rows([(7, "Design quick pack", O[6][2], O[6][3], "After the launch week review."),
                 (8, "Onboarding flow", O[7][2], O[7][3], "After the design quick pack."),
                 (9, "Analytics dashboard", O[8][2], O[8][3], "About 30 days after launch."),
                 (10, "Workout reminders", O[9][2], O[9][3], "After onboarding is live.")]), PageBreak()]
S += [bar("Phase 4: grow and keep your members", "5"), Spacer(1, 6)]
S += [step_rows([(11, "Android on Google Play (three small steps)", "Your Google Play account and setup, then the Android app with the same subscriptions, then your listing and submission.", "Opens the other half of the market. Same app, same plans.", "When members show demand. We measure first, using the 14 day count in your playbook."),
                 (12, "Retention messages (two small steps)", "Welcome and win back messages designed for the right moments, then built, tested and running on their own.", "Quiet members come back without you chasing them.", "After the analytics dashboard shows where members drop off."),
                 (13, "Invite a friend", O[15][2], O[15][3], "After retention is live. Rewards follow Apple's rules.")]), Spacer(1, 10)]
S += [box([Paragraph("<b>Your launch is protected.</b> Anything that changes the iPhone app is bundled into planned updates, so Apple reviews fewer versions and nothing puts your Nov 1 launch at risk. Web side improvements can go live sooner.", body)]), Spacer(1, 10)]
S += [bar("What each step looks like", "6"), Spacer(1, 6)]
S += [table([("1. You pick a step", "Tell me which one matters most right now."), ("2. You get a clear written scope", "What you receive, what I need from you, and what is not included."),
             ("3. You say yes", "Work starts only after your written approval."), ("4. You review the result", "You approve it, or ask for the agreed revisions."),
             ("5. Next step, only if you want it", "No pressure. We can pause for as long as you like.")], [CW * 0.32, CW * 0.68]), Spacer(1, 10)]
S += [box([Paragraph("<b>What matters most to you in the next 30 days?</b> We start there.", st("big", fontName="CB", fontSize=13, leading=17, textColor=SAGE_D))])]
S += [Spacer(1, 8), Paragraph("Thank you for trusting me with FTLR Fitness. I am glad to be part of it.", st("end", fontName="CI", fontSize=10.5, textColor=GREY))]
build(BASE + "FTLR-Growth-Roadmap-for-Leah.pdf", "FTLR Fitness | Your Growth Roadmap | Prepared for Leah Stukov", S)
print("done", TOTAL)

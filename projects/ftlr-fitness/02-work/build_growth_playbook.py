from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))
pdfmetrics.registerFontFamily("C", normal="C", bold="CB", italic="CI", boldItalic="CB")

INK = colors.HexColor("#1D2A24")
SAGE_D = colors.HexColor("#5F8570")
SAGE = colors.HexColor("#8FB09B")
SOFT = colors.HexColor("#EEF4F0")
GREY = colors.HexColor("#5E6D65")
LINE = colors.HexColor("#D8E3DC")
ZEBRA = colors.HexColor("#F7FAF8")
GOLD = colors.HexColor("#C98A1B")

W, H = A4
LM = RM = 18 * mm
CW = W - LM - RM

def st(name, **kw):
    b = dict(fontName="C", fontSize=10.5, leading=14.5, textColor=INK)
    b.update(kw)
    return ParagraphStyle(name, **b)

body = st("body"); small = st("small", fontSize=9, leading=12.5, textColor=GREY)
cell = st("cell", fontSize=9.8, leading=13); cellb = st("cellb", fontName="CB", fontSize=9.8, leading=13)
h2 = st("h2", fontName="CB", fontSize=14, leading=18, textColor=colors.white)
h3 = st("h3", fontName="CB", fontSize=11.5, leading=15, textColor=SAGE_D)
head = st("head", fontName="CB", fontSize=8.8, leading=11, textColor=GREY)
bul = st("bul", fontSize=10, leading=13.5, leftIndent=11, bulletIndent=0)

def on_page(c, doc):
    c.saveState()
    c.setFillColor(INK); c.rect(0, H - 5 * mm, W, 5 * mm, stroke=0, fill=1)
    c.setFillColor(SAGE); c.rect(0, H - 5 * mm, 40 * mm, 5 * mm, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.line(LM, 15 * mm, W - RM, 15 * mm)
    c.setFont("C", 8.5); c.setFillColor(GREY)
    c.drawString(LM, 10 * mm, "FTLR Fitness  |  Growth Playbook  |  Prepared for Leah Stukov  |  Confidential")
    c.drawRightString(W - RM, 10 * mm, "Page %d" % doc.page)
    c.restoreState()

OUT = "/home/user/Abdulwasiu-Freelancing-Journey/projects/ftlr-fitness/02-work/FTLR-Fitness-Growth-Playbook.pdf"
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=LM, rightMargin=RM, topMargin=16 * mm, bottomMargin=20 * mm,
                      title="FTLR Fitness Growth Playbook", author="Up Agency", subject="First 90 days on the App Store")
doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(LM, 20 * mm, CW, H - 36 * mm, 0, 0, 0, 0)], onPage=on_page)])

def bar(title, color=SAGE_D, letter=None):
    if letter:
        t = Table([[Paragraph(letter, st("l", fontName="CB", fontSize=14, leading=18, textColor=colors.white, alignment=TA_CENTER)), Paragraph(title, h2)]],
                  colWidths=[10 * mm, CW - 10 * mm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("BACKGROUND", (0, 0), (0, 0), INK),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (1, 0), (1, 0), 10),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    else:
        t = Table([[Paragraph(title, h2)]], colWidths=[CW])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), color), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                               ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t

def bullets(items):
    return [Paragraph(i, bul, bulletText="•") for i in items]

def box(flow, bg=SOFT, edge=SAGE_D):
    t = Table([[flow]], colWidths=[CW])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), bg), ("LINEBEFORE", (0, 0), (0, -1), 4, edge),
                           ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                           ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    return t

def table(rows, widths, header=None):
    data = []
    if header: data.append([Paragraph(h, head) for h in header])
    for r in rows:
        data.append([Paragraph(x, cellb if i == 0 else cell) for i, x in enumerate(r)])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    s = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), 0.5, LINE),
         ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
         ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(1 if header else 0, len(data)):
        if (i - (1 if header else 0)) % 2 == 1: s.append(("BACKGROUND", (0, i), (-1, i), ZEBRA))
    t.setStyle(TableStyle(s)); return t

S = []
# ---------- Cover ----------
cover = Table([[[
    Paragraph("FTLR FITNESS", st("k", fontName="CB", fontSize=10.5, leading=13, textColor=colors.HexColor("#BFD9C8"))),
    Spacer(1, 3),
    Paragraph("Growth Playbook", st("t", fontName="CB", fontSize=28, leading=32, textColor=colors.white)),
    Spacer(1, 4),
    Paragraph("Your first 90 days on the App Store: how to turn an approved app into active, paying members.",
              st("s", fontSize=12, leading=16, textColor=colors.HexColor("#E3EEE7")))]]], colWidths=[CW])
cover.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), INK), ("LEFTPADDING", (0, 0), (-1, -1), 16),
                           ("RIGHTPADDING", (0, 0), (-1, -1), 16), ("TOPPADDING", (0, 0), (-1, -1), 16), ("BOTTOMPADDING", (0, 0), (-1, -1), 16)]))
meta = Table([[Paragraph("<b>Prepared for</b><br/>Leah Stukov", cell), Paragraph("<b>Company</b><br/>For the Long Run Fitness LLC", cell),
               Paragraph("<b>Prepared by</b><br/>Up Agency", cell), Paragraph("<b>Date</b><br/>October 15, 2026", cell)]],
             colWidths=[CW * 0.22, CW * 0.34, CW * 0.2, CW * 0.24])
meta.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), SOFT), ("LINEBELOW", (0, 0), (-1, -1), 2, SAGE_D),
                          ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
S += [cover, meta, Spacer(1, 12)]
S += [Paragraph("Leah, congratulations on getting FTLR Fitness this far. An approved app is the starting line, not the finish. "
                "This playbook is yours to keep and use, whether or not we work together again. It covers what already works in your app, "
                "a simple 90 day plan, ready to use listing copy, a first week plan for new members, and a few quick wins you can do yourself this week.", body),
      Spacer(1, 10)]

S += [bar("Where FTLR stands today", letter="1"), Spacer(1, 6)]
two = Table([[
    [Paragraph("What is already strong", h3)] + bullets([
        "<b>A clear promise:</b> “Start building your best self for the long run” speaks to people who want lasting results, not a quick fix.",
        "<b>A full experience in one app:</b> workouts, programs, recipes, Ask Your Coach, community and resources.",
        "<b>Real Apple subscriptions:</b> Monthly and Yearly plans, Restore Purchases, and legal links in place.",
        "<b>Safe community:</b> reporting, blocking and clear rules protect your members and your brand.",
        "<b>Your web members are protected:</b> they can log in without paying twice."]),
    [Paragraph("Where growth is waiting", h3)] + bullets([
        "<b>Discovery:</b> the App Store listing is how strangers find you. Name, subtitle, keywords and screenshots can all work harder.",
        "<b>Activation:</b> a new member should finish a first workout within 24 hours. A short welcome flow makes that likely.",
        "<b>Reviews:</b> a steady flow of ratings builds trust and ranking. It only happens if you ask at the right moment.",
        "<b>Reach:</b> members on Android cannot join yet. Measure the demand before deciding.",
        "<b>Retention:</b> gentle follow ups keep members training month after month."])]],
    colWidths=[CW / 2, CW / 2])
two.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
S += [two, Spacer(1, 10)]

# at a glance
S += [bar("Your 90 days at a glance", letter="2"), Spacer(1, 6)]
phases = [("THIS WEEK", "Get launch ready", "Listing copy, screenshots, announcement drafts"),
          ("LAUNCH WEEK", "Nov 1 and the days after", "Announce, welcome, ask for first ratings"),
          ("DAYS 8 TO 30", "Build the habit", "Weekly rhythm, challenges, review prompts"),
          ("DAYS 31 TO 90", "Grow and retain", "Retention messages, referrals, next features")]
cells = []
for t, h, d in phases:
    c = Table([[Paragraph(t, st("pt", fontName="CB", fontSize=8.8, leading=11, textColor=colors.white))],
               [Paragraph("<b>%s</b>" % h, cell)], [Paragraph(d, small)]], colWidths=[CW / 4 - 4])
    c.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), SAGE_D), ("BACKGROUND", (0, 1), (0, 2), SOFT),
                           ("LEFTPADDING", (0, 0), (-1, -1), 7), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
    cells.append(c)
g = Table([cells], colWidths=[CW / 4] * 4)
g.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
S += [g, PageBreak()]

# ---------- Page 2: roadmap ----------
S += [bar("The 90 day roadmap, step by step", letter="3"), Spacer(1, 8)]
def phase(title, items):
    return KeepTogether([Paragraph(title, h3)] + bullets(items) + [Spacer(1, 8)])
S += [phase("Phase 1: This week, while Apple reviews your app", [
    "Write your App Store listing using the copy suggestions in section 4. Subtitle and keywords can be updated with any app version, promotional text can be changed anytime.",
    "Plan 5 screenshots that tell one story (see section 4). Screenshots must show the real app in use.",
    "Draft your launch announcement: one email to your list, one post for your community, one pinned message in the group chat.",
    "Prepare a short welcome message that every new member will see on day one (see section 5).",
    "Decide who will answer chat reports and keep your contact email monitored. Apple expects quick responses."]),
    phase("Phase 2: Launch week (Nov 1 and the following 7 days)", [
    "Release the app when you are ready. In App Store Connect, choose \u201cManually release this version\u201d so you pick the day and time after Apple approves.",
    "Send the announcement email and post it in your community. Tell members the app is now on the App Store and what they get inside.",
    "Pin a welcome message in the group chat and invite everyone to complete their first workout this week.",
    "Ask happy members for a rating, not everyone. The best moment is right after a finished workout or a milestone.",
    "Keep outside payment links out of the app. In the app, subscriptions go through Apple only."]),
    phase("Phase 3: Days 8 to 30, build the habit", [
    "Run one simple weekly rhythm: a Monday workout focus, a mid week recipe, a Friday check in.",
    "Launch a 14 day challenge inside the community. Challenges give members a reason to open the app daily.",
    "Reply personally to every review. Replies show future members that a real coach is behind the app.",
    "Count how many members ask about Android. Write it down. This number decides whether an Android version is worth it."]),
    phase("Phase 4: Days 31 to 90, grow and retain", [
    "Send win back messages to members who have not trained in 10 days.",
    "Ask your best members to invite one friend. A simple “bring a friend” week costs almost nothing.",
    "Review your numbers once a month: new members, active members, cancellations. Fix the biggest leak first.",
    "Use real member questions from Ask Your Coach to plan the next programs and recipes."])]

# ---------- Page 3: listing ----------
S += [PageBreak(), bar("App Store listing: ready to use copy", letter="4"), Spacer(1, 8)]
S += [Paragraph("These are starting points. Test them, keep what works, and change one thing at a time so you learn from each change.", body), Spacer(1, 6)]
rows = [
    ["App name (max 30)", "FTLR Fitness", "Short, easy to remember, already your brand."],
    ["Subtitle (max 30)", "Strength, power &amp; mobility", "26 characters. Says what you do in plain words."],
    ["Alternative subtitle", "Uplifting strength coaching", "27 characters. Leans on the “uplifted, not beat down” feeling."],
    ["Promotional text (max 170)", "Your current text is strong: keep it. Update it for the launch, for example: “Now on the App Store. Start your first workout today.”",
     "Can be changed anytime without a new app version."],
    ["Keywords (max 100)", "See the line below this table.",
     "Exactly 100 characters. Do not repeat words from your name and subtitle. Avoid other brand names."],
]
S += [table(rows, [CW * 0.2, CW * 0.45, CW * 0.35], header=["ITEM", "SUGGESTION", "WHY"]), Spacer(1, 6),
      box([Paragraph("<b>Keywords, paste exactly:</b><br/><font name='CB' color='#5F8570'>strength,mobility,workouts,coach,recipes,plan,home,longevity,programs,wellness,meal,healthy,training</font>", body)]),
      Spacer(1, 10)]
S += [Paragraph("Screenshot story: five screens, one message", h3)]
shots = [["1", "Hero: “Start building your best self for the long run”", "Your promise first."],
         ["2", "Workouts and programs", "What members do every day."],
         ["3", "Recipes to fit your dietary preferences", "Proves the nutrition side."],
         ["4", "Ask Your Coach", "Your personal touch, your biggest difference."],
         ["5", "Community", "Belonging keeps people coming back."]]
S += [table(shots, [CW * 0.06, CW * 0.54, CW * 0.4], header=["#", "SCREEN", "WHAT IT SAYS"]), Spacer(1, 10)]
S += [box([Paragraph("<b>Money tip: the Apple Small Business Program.</b> If your yearly App Store earnings stay under Apple's limit, you can apply to the "
                      "Apple Small Business Program and pay a lower commission. Search “Apple Small Business Program”, check you qualify, and apply with your Apple developer account. "
                      "It can mean more of each subscription stays with you.", body)]), Spacer(1, 8)]
S += [box([Paragraph("<b>Pricing note.</b> Your app plans are $12.99 per month and $99.99 per year, while your website shows $10 and $100. "
                      "Different prices across platforms are normal and often cover Apple's commission. Whatever you choose, keep the difference simple so members are never confused.", body)],
          bg=colors.HexColor("#FBF4E6"), edge=GOLD)]

# ---------- Page 4: retention ----------
S += [PageBreak(), bar("The first 7 days: turn installs into active members", letter="5"), Spacer(1, 8)]
S += [Paragraph("Most members decide in the first week whether the app becomes part of their routine. A short, human sequence in your voice does the work. "
                "Send these as emails, chat messages or in app notes, whichever you prefer.", body), Spacer(1, 6)]
seq = [["Day 0", "Welcome from Leah", "“Welcome to FTLR. Start with your first workout today, it takes about 15 minutes. I am glad you are here.”", "First workout within 24 hours"],
       ["Day 1", "Nudge, only if no workout yet", "“Your first workout is waiting. Pick any one and tell me how it felt.”", "Remove the fear of starting"],
       ["Day 3", "Check in and a recipe", "“How is your week going? Here is a recipe that fits your preferences.”", "Show the whole app"],
       ["Day 7", "Celebrate week one", "“One week done! Here is what you finished. If FTLR is helping, a quick rating means a lot to me.”", "First rating, at a happy moment"],
       ["Day 14", "Invite to the community", "“Join this week's challenge in the group chat. Ask me anything in Ask Your Coach.”", "Belonging and daily use"]]
S += [table(seq, [CW * 0.09, CW * 0.2, CW * 0.47, CW * 0.24], header=["DAY", "MESSAGE", "EXAMPLE", "GOAL"]), Spacer(1, 10)]
S += [Paragraph("Is Android worth it? Measure first", h3),
      Paragraph("For the next 14 days, add one line to your welcome message: “Which phone do you use?” Count the answers. If a meaningful share of your members use Android, "
                "or several ask for it, an Android version will pay for itself. If almost nobody asks, wait. This simple count protects your budget.", body), Spacer(1, 10)]
S += [Paragraph("Five quick wins for this week", h3)] + bullets([
    "Write and save your launch announcement (email and community post).",
    "Update your promotional text for launch day.",
    "Choose the 5 screenshots from the story above.",
    "Set up the Day 0 welcome message.",
    "Check that your support email is monitored daily."])

# ---------- Page 5: how I can help ----------
S += [PageBreak(), bar("If you would like me to do it for you", letter="6"), Spacer(1, 8)]
S += [Paragraph("Everything above is yours to use freely. If you would rather save the time and have it built and tested for you, here are three clear options. "
                "Each one is a fixed price, delivered in milestones, on Fiverr with payment protected.", body), Spacer(1, 8)]
tiers = [
    ("LAUNCH READY", "$600", SAGE_D, ["Optimized App Store listing: name, subtitle, keywords, promotional text",
                                      "Screenshot storyline with captions, ready for your designer or tool",
                                      "30 day launch plan with written emails and posts",
                                      "Ratings and welcome message setup guidance"]),
    ("LAUNCH + ANDROID", "$1,850", INK, ["Everything in Launch Ready",
                                          "Android version on Google Play: same app, same subscriptions",
                                          "Quick design pack: 3 improvements to the look and flow",
                                          "Store setup and submission handled for you"]),
    ("GROWTH PARTNER", "$3,750", GOLD, ["Everything in Launch + Android",
                                         "Full design refresh in place of the quick pack",
                                         "Automated welcome and retention messages (email and text)",
                                         "Priority support during your first launch month"])]
hdr, prc, lst = [], [], []
for name, price, col, items in tiers:
    hdr.append(Paragraph(name, st("tn", fontName="CB", fontSize=9.5, leading=12, textColor=colors.white, alignment=TA_CENTER)))
    prc.append(Paragraph(price, st("tp", fontName="CB", fontSize=22, leading=26, alignment=TA_CENTER, textColor=col)))
    lst.append([Paragraph(i, st("ti", fontSize=9.4, leading=12.5, leftIndent=9, bulletIndent=0), bulletText="\u2022") for i in items])
tt = Table([hdr, prc, lst], colWidths=[CW / 3] * 3)
sty = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 1), (-1, 2), SOFT),
       ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9),
       ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
       ("LINEAFTER", (0, 0), (1, -1), 4, colors.white)]
for i, (_, _, col, _) in enumerate(tiers):
    sty.append(("BACKGROUND", (i, 0), (i, 0), col))
tt.setStyle(TableStyle(sty))
S += [tt, Spacer(1, 10)]
S += [box([Paragraph("<b>Optional care plan: $199 per month.</b> Keeps your app healthy after launch: Apple and system updates, bug fixes, "
                      "handling of any store review questions, and one hour of changes each month. Cancel anytime.", body)]), Spacer(1, 8)]
S += [Paragraph("How it works", h3)] + bullets([
    "We agree the scope in writing. You approve before anything starts.",
    "I send a Fiverr custom offer with two milestones. Your payment is protected by Fiverr.",
    "You see progress at each milestone and approve the result.",
    "Anything outside the agreed scope is quoted separately, so there are never surprises."])
S += [Spacer(1, 8), Paragraph("There is no pressure. Use the playbook, see how launch week goes, and tell me which option, if any, fits your plans. "
                              "Thank you for trusting me with FTLR Fitness.", st("end", fontName="CI", fontSize=10.5, textColor=GREY))]

doc.build(S)
print("ok")

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import simpleSplit, ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import math

D = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("C", D + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("CB", D + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("CI", D + "Carlito-Italic.ttf"))

SAGE = colors.HexColor("#8FB09B"); SAGE_D = colors.HexColor("#5F8570"); INK = colors.HexColor("#1D2A24")
MUTED = colors.HexColor("#66756D"); LINE = colors.HexColor("#DFE7E2"); BG = colors.HexColor("#F6F9F7")
TEAL = colors.HexColor("#2F6F7E"); MINT = colors.HexColor("#E6F0EA"); GOLD = colors.HexColor("#C98A1B")
WHITE = colors.white; DANGER = colors.HexColor("#B3402F")
LOGO = "/home/user/ftlr-ios-wrapper/www/logo.png"

W, H = 1280.0, 720.0
OUT = "/home/user/Abdulwasiu-Freelancing-Journey/projects/ftlr-fitness/02-work/FTLR-Fitness-Growth-Playbook-Presentation.pdf"
c = canvas.Canvas(OUT, pagesize=(W, H))
c.setTitle("FTLR Fitness Growth Playbook"); c.setAuthor("Up Agency"); c.setSubject("First 90 days on the App Store")
page_no = [0]

def Y(t): return H - t  # top-based y

def rrect(x, t, w, h, r=14, fill=WHITE, stroke=None, lw=1):
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.roundRect(x, Y(t) - h, w, h, r, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
    c.restoreState()

def text(s, x, t, font="C", size=16, color=INK, align="l", lead=None, width=None, maxlines=None):
    """draw (optionally wrapped) text with top at t; returns bottom top-coordinate"""
    c.saveState(); c.setFillColor(color); c.setFont(font, size)
    lead = lead or size * 1.3
    lines = simpleSplit(s, font, size, width) if width else [s]
    if maxlines: lines = lines[:maxlines]
    yy = t + size * 0.92
    for ln in lines:
        if align == "c": c.drawCentredString(x, Y(yy), ln)
        elif align == "r": c.drawRightString(x, Y(yy), ln)
        else: c.drawString(x, Y(yy), ln)
        yy += lead
    c.restoreState()
    return t + lead * len(lines)

def circle(cx, ct, r, fill, stroke=None, lw=2):
    c.saveState()
    if fill is not None: c.setFillColor(fill)
    if stroke is not None: c.setStrokeColor(stroke); c.setLineWidth(lw)
    c.circle(cx, Y(ct), r, stroke=1 if stroke is not None else 0, fill=1 if fill is not None else 0)
    c.restoreState()

def pill(x, t, label, fill=SAGE_D, color=WHITE, size=13, padx=12, h=26):
    w = pdfmetrics.stringWidth(label, "CB", size) + padx * 2
    rrect(x, t, w, h, h / 2, fill=fill)
    text(label, x + w / 2, t + (h - size) / 2 - 1, "CB", size, color, "c")
    return w

def check(cx, ct, r, fill=SAGE_D):
    circle(cx, ct, r, fill)
    c.saveState(); c.setStrokeColor(WHITE); c.setLineWidth(r * 0.22); c.setLineCap(1); c.setLineJoin(1)
    p = c.beginPath(); p.moveTo(cx - r * .42, Y(ct) - r * .02); p.lineTo(cx - r * .1, Y(ct) - r * .34); p.lineTo(cx + r * .44, Y(ct) + r * .32)
    c.drawPath(p, stroke=1, fill=0); c.restoreState()

def new_slide(dark=False, title=None, kicker=None, sub=None):
    if page_no[0] > 0: c.showPage()
    page_no[0] += 1
    c.setFillColor(INK if dark else BG); c.rect(0, 0, W, H, stroke=0, fill=1)
    if not dark:
        c.setFillColor(INK); c.rect(0, H - 8, W, 8, stroke=0, fill=1)
        c.setFillColor(SAGE); c.rect(0, H - 8, 120, 8, stroke=0, fill=1)
        c.setFont("C", 11); c.setFillColor(MUTED)
        c.drawString(60, 24, "FTLR Fitness  |  Growth Playbook  |  Prepared for Leah Stukov")
        c.drawRightString(W - 60, 24, "%d" % page_no[0])
    yy = 48
    if kicker:
        text(kicker.upper(), 60, yy, "CB", 13, SAGE_D if not dark else SAGE); yy += 22
    if title:
        yy = text(title, 60, yy, "CB", 36, WHITE if dark else INK, width=W - 120, lead=42)
    if sub:
        yy = text(sub, 60, yy + 4, "C", 18, colors.HexColor("#CFE0D5") if dark else MUTED, width=W - 140, lead=24)
    return yy + 14

def logo(x, t, w, bg=True):
    ih = w * 284.0 / 600.0
    if bg: rrect(x - 10, t - 10, w + 20, ih + 20, 14, fill=WHITE)
    c.drawImage(ImageReader(LOGO), x, Y(t) - ih, w, ih, mask=None)
    return ih

# ---------------- phone mock ----------------
def phone(x, t, w, draw, shadow=True):
    h = w * 2.05
    if shadow:
        c.saveState(); c.setFillColor(colors.Color(0, 0, 0, alpha=0.10)); c.roundRect(x + 6, Y(t) - h - 8, w, h, w * 0.13, stroke=0, fill=1); c.restoreState()
    rrect(x, t, w, h, w * 0.13, fill=INK)
    ins = w * 0.035
    sx, st_, sw, sh = x + ins, t + ins, w - 2 * ins, h - 2 * ins
    c.saveState()
    p = c.beginPath(); p.roundRect(sx, Y(st_) - sh, sw, sh, w * 0.10); c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(WHITE); c.rect(sx, Y(st_) - sh, sw, sh, stroke=0, fill=1)
    draw(sx, st_, sw, sh)
    # dynamic island
    c.setFillColor(INK); c.roundRect(sx + sw / 2 - sw * 0.14, Y(st_ + sw * 0.045) - sw * 0.07, sw * 0.28, sw * 0.07, sw * 0.035, stroke=0, fill=1)
    c.restoreState()
    return h

def tabbar(sx, st_, sw, sh, active=0, labels=("Home", "Workouts", "Recipes", "Plan", "More")):
    bh = sw * 0.17
    c.setFillColor(WHITE); c.rect(sx, Y(st_ + sh), sw, bh, stroke=0, fill=1)
    c.setStrokeColor(LINE); c.setLineWidth(0.8); c.line(sx, Y(st_ + sh) + bh, sx + sw, Y(st_ + sh) + bh)
    n = len(labels)
    for i, lb in enumerate(labels):
        cx = sx + sw * (i + 0.5) / n
        col = SAGE_D if i == active else MUTED
        circle(cx, st_ + sh - bh * 0.62, sw * 0.022, col)
        text(lb, cx, st_ + sh - bh * 0.42, "CB" if i == active else "C", sw * 0.036, col, "c")

# ---------- concept screens ----------
def screen_home(sx, st_, sw, sh):
    c.setFillColor(BG); c.rect(sx, Y(st_ + sh), sw, sh, stroke=0, fill=1)
    p = sw * 0.06; yy = st_ + sw * 0.13
    text("FOR THE LONG RUN FITNESS", sx + p, yy, "CB", sw * 0.03, SAGE_D); yy += sw * 0.05
    text("Good morning, Sam", sx + p, yy, "CB", sw * 0.082, INK); yy += sw * 0.115
    # hero
    hh = sw * 0.46
    rrect(sx + p, yy, sw - 2 * p, hh, sw * 0.05, fill=TEAL)
    text("TODAY'S FOCUS", sx + p * 2, yy + sw * 0.05, "CB", sw * 0.03, colors.HexColor("#BFE3E9"))
    text("Strength and mobility flow", sx + p * 2, yy + sw * 0.09, "CB", sw * 0.06, WHITE, width=sw * 0.46, lead=sw * 0.07)
    text("22 min  |  Beginner friendly", sx + p * 2, yy + sw * 0.25, "C", sw * 0.036, colors.HexColor("#DCEFF2"))
    pill(sx + p * 2, yy + hh - sw * 0.115, "Start workout", fill=WHITE, color=TEAL, size=sw * 0.04, padx=sw * 0.04, h=sw * 0.075)
    # ring
    rcx, rct, rr = sx + sw - p * 2 - sw * 0.1, yy + sw * 0.17, sw * 0.085
    c.saveState(); c.setLineWidth(sw * 0.02); c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.25)); c.circle(rcx, Y(rct), rr, stroke=1, fill=0)
    c.setStrokeColor(WHITE); c.arc(rcx - rr, Y(rct) - rr, rcx + rr, Y(rct) + rr, 90, -240); c.restoreState()
    text("2/4", rcx, rct - sw * 0.022, "CB", sw * 0.05, WHITE, "c")
    text("this week", rcx, rct + sw * 0.04, "C", sw * 0.026, colors.HexColor("#DCEFF2"), "c")
    yy += hh + sw * 0.05
    # streak + quick tiles
    pill(sx + p, yy, "5 day streak", fill=MINT, color=SAGE_D, size=sw * 0.036, padx=sw * 0.035, h=sw * 0.07)
    yy += sw * 0.1
    tw = (sw - 2 * p - 3 * sw * 0.02) / 4
    for i, lb in enumerate(["Workouts", "Recipes", "Plan", "Coach"]):
        tx = sx + p + i * (tw + sw * 0.02)
        rrect(tx, yy, tw, tw * 1.05, sw * 0.03, fill=WHITE, stroke=LINE)
        circle(tx + tw / 2, yy + tw * 0.38, tw * 0.17, SAGE if i % 2 == 0 else SAGE_D)
        text(lb, tx + tw / 2, yy + tw * 0.68, "CB", sw * 0.033, INK, "c")
    yy += tw * 1.05 + sw * 0.045
    # way card
    rrect(sx + p, yy, sw - 2 * p, sw * 0.26, sw * 0.04, fill=WHITE, stroke=LINE)
    text("This is the FTLR way", sx + p * 1.6, yy + sw * 0.03, "CB", sw * 0.045, INK)
    text("Built for longevity, not just intensity.", sx + p * 1.6, yy + sw * 0.085, "C", sw * 0.035, MUTED)
    px = sx + p * 1.6
    for lb in ["Strong", "Powerful", "Mobile"]:
        px += pill(px, yy + sw * 0.155, lb, fill=SAGE_D, size=sw * 0.034, padx=sw * 0.03, h=sw * 0.06) + sw * 0.02
    tabbar(sx, st_, sw, sh, 0)

def screen_signin(sx, st_, sw, sh):
    c.setFillColor(BG); c.rect(sx, Y(st_ + sh), sw, sh, stroke=0, fill=1)
    p = sw * 0.09; lw_ = sw * 0.5
    ih = lw_ * 284.0 / 600.0
    c.drawImage(ImageReader(LOGO), sx + (sw - lw_) / 2, Y(st_ + sw * 0.2) - ih, lw_, ih)
    yy = st_ + sw * 0.2 + ih + sw * 0.07
    text("Welcome back", sx + sw / 2, yy, "CB", sw * 0.085, INK, "c"); yy += sw * 0.11
    text("Sign in to continue your plan", sx + sw / 2, yy, "C", sw * 0.04, MUTED, "c"); yy += sw * 0.09
    for lb, val in [("Email", "you@example.com"), ("Password", "• • • • • • • •")]:
        text(lb, sx + p, yy, "CB", sw * 0.034, INK); yy += sw * 0.05
        rrect(sx + p, yy, sw - 2 * p, sw * 0.105, sw * 0.03, fill=WHITE, stroke=LINE)
        text(val, sx + p + sw * 0.035, yy + sw * 0.03, "C", sw * 0.04, MUTED); yy += sw * 0.135
    rrect(sx + p, yy, sw - 2 * p, sw * 0.12, sw * 0.035, fill=SAGE_D)
    text("Sign in", sx + sw / 2, yy + sw * 0.034, "CB", sw * 0.048, WHITE, "c"); yy += sw * 0.17
    text("Forgot password?", sx + sw / 2, yy, "CB", sw * 0.036, SAGE_D, "c"); yy += sw * 0.07
    text("New here? Sign up", sx + sw / 2, yy, "C", sw * 0.036, MUTED, "c")

def screen_goal(sx, st_, sw, sh):
    c.setFillColor(BG); c.rect(sx, Y(st_ + sh), sw, sh, stroke=0, fill=1)
    p = sw * 0.08; yy = st_ + sw * 0.16
    for i in range(4):
        rrect(sx + p + i * (sw - 2 * p) / 4, yy, (sw - 2 * p) / 4 - 5, 5, 2.5, fill=SAGE_D if i < 2 else LINE)
    yy += sw * 0.08
    text("STEP 2 OF 4", sx + p, yy, "CB", sw * 0.03, SAGE_D); yy += sw * 0.05
    yy = text("What do you want to build?", sx + p, yy, "CB", sw * 0.08, INK, width=sw - 2 * p, lead=sw * 0.092) + sw * 0.02
    text("Pick all that fit. You can change this later.", sx + p, yy, "C", sw * 0.037, MUTED); yy += sw * 0.09
    for lb, on in [("Build strength", True), ("Improve mobility", True), ("Eat in a way that fits me", False), ("Stay consistent", True)]:
        rrect(sx + p, yy, sw - 2 * p, sw * 0.13, sw * 0.035, fill=MINT if on else WHITE, stroke=SAGE_D if on else LINE, lw=1.6 if on else 1)
        text(lb, sx + p + sw * 0.05, yy + sw * 0.04, "CB", sw * 0.043, INK)
        if on: check(sx + sw - p - sw * 0.06, yy + sw * 0.065, sw * 0.03)
        yy += sw * 0.155
    yy += sw * 0.03
    rrect(sx + p, yy, sw - 2 * p, sw * 0.12, sw * 0.035, fill=SAGE_D)
    text("Continue", sx + sw / 2, yy + sw * 0.034, "CB", sw * 0.048, WHITE, "c")

def screen_welcome(sx, st_, sw, sh):
    c.setFillColor(BG); c.rect(sx, Y(st_ + sh), sw, sh, stroke=0, fill=1)
    p = sw * 0.07; yy = st_ + sw * 0.16
    text("DAY 0", sx + p, yy, "CB", sw * 0.03, SAGE_D); yy += sw * 0.05
    text("A note from Leah", sx + p, yy, "CB", sw * 0.08, INK); yy += sw * 0.11
    rrect(sx + p, yy, sw - 2 * p, sw * 0.5, sw * 0.045, fill=WHITE, stroke=LINE)
    circle(sx + p * 2.2, yy + sw * 0.1, sw * 0.055, SAGE_D)
    text("L", sx + p * 2.2, yy + sw * 0.082, "CB", sw * 0.06, WHITE, "c")
    text("Leah, your coach", sx + p * 2.2 + sw * 0.09, yy + sw * 0.07, "CB", sw * 0.04, INK)
    text("Welcome to FTLR. Start with your first workout today. It takes about 15 minutes, and I am glad you are here.",
         sx + p * 1.5, yy + sw * 0.17, "C", sw * 0.04, INK, width=sw - 2 * p - p, lead=sw * 0.055)
    yy += sw * 0.55
    rrect(sx + p, yy, sw - 2 * p, sw * 0.12, sw * 0.035, fill=SAGE_D)
    text("Start my first workout", sx + sw / 2, yy + sw * 0.034, "CB", sw * 0.046, WHITE, "c"); yy += sw * 0.17
    text("Then explore", sx + p, yy, "CB", sw * 0.036, MUTED); yy += sw * 0.055
    px = sx + p
    for lb in ["Recipes", "Ask Your Coach", "Community"]:
        px += pill(px, yy, lb, fill=MINT, color=SAGE_D, size=sw * 0.033, padx=sw * 0.03, h=sw * 0.06) + sw * 0.015

def screen_shot(caption, sub, accent):
    def f(sx, st_, sw, sh):
        c.setFillColor(accent); c.rect(sx, Y(st_ + sh), sw, sh, stroke=0, fill=1)
        text(caption, sx + sw / 2, st_ + sw * 0.2, "CB", sw * 0.1, WHITE, "c", width=sw * 0.84, lead=sw * 0.115)
        rrect(sx + sw * 0.12, st_ + sw * 0.62, sw * 0.76, sh - sw * 0.7, sw * 0.06, fill=WHITE)
        for i in range(4):
            rrect(sx + sw * 0.18, st_ + sw * 0.72 + i * sw * 0.22, sw * (0.64 if i % 2 == 0 else 0.5), sw * 0.12, sw * 0.03, fill=MINT)
    return f

# =============== SLIDE 1: cover ===============
c.setFillColor(INK); c.rect(0, 0, W, H, stroke=0, fill=1); page_no[0] = 1
c.setFillColor(SAGE); c.rect(0, H - 10, 220, 10, stroke=0, fill=1)
logo(90, 90, 280)
text("GROWTH PLAYBOOK", 80, 262, "CB", 15, SAGE)
text("Your first 90 days on the App Store", 80, 290, "CB", 52, WHITE, width=640, lead=60)
text("How to turn an approved app into active, paying members, plus a design direction for what FTLR can look like next.", 80, 448, "C", 21, colors.HexColor("#CFE0D5"), width=600, lead=29)
text("Prepared for Leah Stukov  |  For the Long Run Fitness LLC", 80, 590, "CB", 16, WHITE)
text("Prepared by Up Agency  |  October 15, 2026", 80, 616, "C", 15, colors.HexColor("#9FB8A8"))
# decorative phones on cover
phone(840, 90, 190, screen_home)
phone(1050, 150, 170, screen_welcome)

# =============== SLIDE 2: journey ===============
yy = new_slide(title="You are almost at the starting line", kicker="Where we are today",
               sub="Everything below is built and working. The next milestone is Apple's approval, then launch on November 1.")
steps = [("Web app live", "Members already use it", True), ("iPhone app built", "Native app wraps your web app", True),
         ("Apple subscriptions", "Monthly and Yearly, with Restore", True), ("Safe community", "Report, block and clear rules", True),
         ("Submitted to Apple", "Notes, video and demo account sent", True), ("Apple approval", "We are waiting here", "now"),
         ("Launch, Nov 1", "You choose the moment", False)]
x0, x1 = 100, W - 100
ty = 330
c.setStrokeColor(LINE); c.setLineWidth(5); c.line(x0, Y(ty), x1, Y(ty))
n = len(steps)
for i, (a, b, st_) in enumerate(steps):
    cx = x0 + (x1 - x0) * i / (n - 1)
    if st_ is True: check(cx, ty, 22)
    elif st_ == "now":
        circle(cx, ty, 28, None, GOLD, 4); circle(cx, ty, 14, GOLD)
    else: circle(cx, ty, 22, WHITE, SAGE, 3)
    text(a, cx, ty + 44, "CB", 17, INK, "c", width=150, lead=20)
    text(b, cx, ty + 92, "C", 14, MUTED, "c", width=150, lead=18)
rrect(60, 520, W - 120, 110, 18, fill=MINT)
text("Why this matters", 90, 540, "CB", 19, SAGE_D)
text("An approved app is the starting line, not the finish. The next 90 days decide how many people find FTLR, finish a first workout, stay, and tell friends. This playbook shows how.",
     90, 570, "C", 18, INK, width=W - 180, lead=25)

# =============== SLIDE 3: strengths ===============
yy = new_slide(title="What is already strong", kicker="Your foundation", sub="Five things most new apps do not have on launch day.")
items = [("A clear promise", "“Start building your best self for the long run” speaks to people who want lasting results, not a quick fix."),
         ("A full experience", "Workouts, programs, recipes, Ask Your Coach, community and resources in one app."),
         ("Real Apple subscriptions", "Monthly and Yearly plans, Restore Purchases, and legal links, as Apple requires."),
         ("A safe community", "Reporting, blocking and clear rules protect your members and your brand."),
         ("Web members protected", "People who already pay on your website can log in without paying twice.")]
cw_, gap = 220, 20; x = 60
for i, (h, d) in enumerate(items):
    xx = 60 + i * (cw_ + gap)
    rrect(xx, yy + 20, cw_, 270, 18, fill=WHITE, stroke=LINE)
    check(xx + 38, yy + 62, 20)
    text(h, xx + 20, yy + 104, "CB", 21, INK, width=cw_ - 40, lead=25)
    text(d, xx + 20, yy + 176, "C", 16, MUTED, width=cw_ - 40, lead=22)

# =============== SLIDE 4: member journey ===============
yy = new_slide(title="A member's journey: where each improvement helps", kicker="The big picture",
               sub="Growth is not one big thing. It is six small moments, and each one can be improved.")
stages = [("Discover", "App Store listing", "Name, subtitle, keywords and screenshots decide who finds you."),
          ("Install", "First impression", "A clean welcome and sign in build trust in seconds."),
          ("First workout", "Within 24 hours", "A short welcome from you gets people started."),
          ("Subscribe", "Clear value", "A simple plans screen with the benefits up front."),
          ("Stay", "Weekly rhythm", "Reminders, challenges and recipes keep the habit."),
          ("Recommend", "Reviews and friends", "Ask at happy moments. Invite a friend.")]
cw_ = 178; gap = 14
for i, (h, s2, d) in enumerate(stages):
    xx = 60 + i * (cw_ + gap)
    col = SAGE_D if i % 2 == 0 else TEAL
    c.saveState(); c.setFillColor(col)
    p = c.beginPath(); p.moveTo(xx, Y(yy + 20)); p.lineTo(xx + cw_ - 16, Y(yy + 20)); p.lineTo(xx + cw_, Y(yy + 62)); p.lineTo(xx + cw_ - 16, Y(yy + 104)); p.lineTo(xx, Y(yy + 104)); p.lineTo(xx + 16, Y(yy + 62)); p.close()
    c.drawPath(p, stroke=0, fill=1); c.restoreState()
    text(h, xx + cw_ / 2, yy + 50, "CB", 20, WHITE, "c")
    rrect(xx, yy + 124, cw_, 200, 16, fill=WHITE, stroke=LINE)
    text(s2.upper(), xx + 16, yy + 144, "CB", 12, col)
    text(d, xx + 16, yy + 176, "C", 16, INK, width=cw_ - 32, lead=22)
text("Today, your biggest gaps are the first and last stages: being found, and being recommended.", 60, 610, "CB", 19, SAGE_D)

# =============== SLIDE 5: 90 days ===============
yy = new_slide(title="Your 90 days at a glance", kicker="The plan", sub="Four phases. One simple focus in each.")
phases = [("PHASE 1", "This week", "Get launch ready", ["Write your listing", "Plan 5 screenshots", "Draft announcements", "Prepare a welcome message"]),
          ("PHASE 2", "Launch week", "Nov 1 and 7 days after", ["Release on your day", "Announce to members", "Pin a welcome in chat", "Ask for first ratings"]),
          ("PHASE 3", "Days 8 to 30", "Build the habit", ["Weekly rhythm", "14 day challenge", "Reply to every review", "Count Android requests"]),
          ("PHASE 4", "Days 31 to 90", "Grow and retain", ["Win back quiet members", "Bring a friend week", "Monthly numbers check", "Plan next programs"])]
cw_ = 270; gap = 20
for i, (a, b, c2, its) in enumerate(phases):
    xx = 60 + i * (cw_ + gap)
    rrect(xx, yy + 10, cw_, 62, 14, fill=SAGE_D if i % 2 == 0 else TEAL)
    text(a, xx + 18, yy + 20, "CB", 12, colors.HexColor("#D9ECE0"))
    text(b, xx + 18, yy + 38, "CB", 21, WHITE)
    rrect(xx, yy + 82, cw_, 300, 14, fill=WHITE, stroke=LINE)
    text(c2, xx + 18, yy + 100, "CB", 19, INK)
    t2 = yy + 150
    for it in its:
        circle(xx + 26, t2 + 10, 5, SAGE)
        t2 = text(it, xx + 42, t2, "C", 17, INK, width=cw_ - 62, lead=22) + 16

# =============== SLIDE 6: phases 1 & 2 ===============
yy = new_slide(title="Phases 1 and 2: get ready, then launch", kicker="Step by step", sub="Do these while Apple reviews your app, and in the first week after.")
col_w = (W - 120 - 30) / 2
blocks = [("Phase 1: This week", ["Write your App Store listing with the copy on slide 8.", "Plan 5 screenshots that tell one story. They must show the real app in use.",
                                  "Draft one email to your list, one community post and one pinned chat message.", "Write the Day 0 welcome message every new member will see.",
                                  "Decide who answers chat reports. Keep your contact email monitored."]),
          ("Phase 2: Launch week", ["Release when you are ready: choose “Manually release this version” in App Store Connect.", "Send the announcement and post it in your community.",
                                    "Pin a welcome in the group chat. Invite everyone to finish a first workout.", "Ask happy members for a rating, right after a finished workout.",
                                    "Keep outside payment links out of the app. In the app, payments go through Apple only."])]
for i, (h, its) in enumerate(blocks):
    xx = 60 + i * (col_w + 30)
    rrect(xx, yy + 10, col_w, 400, 16, fill=WHITE, stroke=LINE)
    rrect(xx, yy + 10, col_w, 50, 16, fill=SAGE_D if i == 0 else TEAL)
    text(h, xx + 20, yy + 22, "CB", 21, WHITE)
    t2 = yy + 80
    for it in its:
        check(xx + 34, t2 + 11, 11, SAGE_D if i == 0 else TEAL)
        t2 = text(it, xx + 58, t2, "C", 17, INK, width=col_w - 84, lead=23) + 18

# =============== SLIDE 7: phases 3 & 4 ===============
yy = new_slide(title="Phases 3 and 4: build the habit, then grow", kicker="Step by step", sub="Small routines that keep members training month after month.")
blocks = [("Phase 3: Days 8 to 30", ["One weekly rhythm: Monday workout focus, mid week recipe, Friday check in.", "A 14 day challenge in the community gives a reason to open the app daily.",
                                     "Reply personally to every review. It shows a real coach is behind the app.", "Count how many members ask about Android. Write the number down."]),
          ("Phase 4: Days 31 to 90", ["Message members who have not trained in 10 days with a warm win back note.", "Run a “bring a friend” week. It costs almost nothing.",
                                      "Once a month, check new members, active members and cancellations. Fix the biggest leak first.", "Use real questions from Ask Your Coach to plan the next programs and recipes."])]
for i, (h, its) in enumerate(blocks):
    xx = 60 + i * (col_w + 30)
    rrect(xx, yy + 10, col_w, 400, 16, fill=WHITE, stroke=LINE)
    rrect(xx, yy + 10, col_w, 50, 16, fill=SAGE_D if i == 0 else TEAL)
    text(h, xx + 20, yy + 22, "CB", 21, WHITE)
    t2 = yy + 80
    for it in its:
        check(xx + 34, t2 + 11, 11, SAGE_D if i == 0 else TEAL)
        t2 = text(it, xx + 58, t2, "C", 17, INK, width=col_w - 84, lead=23) + 20

# =============== SLIDE 8: App Store listing ===============
yy = new_slide(title="Be found: your App Store listing", kicker="Discover", sub="This is how strangers meet FTLR. Test these, keep what works, change one thing at a time.")
# listing card
rrect(60, yy + 10, 470, 420, 18, fill=WHITE, stroke=LINE)
rrect(88, yy + 38, 96, 96, 22, fill=WHITE, stroke=LINE)
c.drawImage(ImageReader(LOGO), 94, Y(yy + 38 + 48 + 22), 84, 84 * 284.0 / 600.0)
text("FTLR Fitness", 204, yy + 46, "CB", 26, INK)
text("Strength, power & mobility", 204, yy + 82, "C", 17, MUTED)
pill(204, yy + 110, "GET", fill=TEAL, size=14, padx=22, h=28)
text("Subtitle: 26 of 30 characters", 88, yy + 168, "CB", 14, SAGE_D)
text("Promotional text, can change anytime:", 88, yy + 200, "CB", 14, SAGE_D)
text("“Now on the App Store. Start your first workout today.”", 88, yy + 222, "CI", 16, INK, width=410, lead=22)
text("Keywords, exactly 100 characters:", 88, yy + 276, "CB", 14, SAGE_D)
text("strength,mobility,workouts,coach,recipes,plan,home,", 88, yy + 298, "CB", 15, INK)
text("longevity,programs,wellness,meal,healthy,training", 88, yy + 318, "CB", 15, INK)
text("Avoid repeating words from the name and subtitle. Avoid other brand names.", 88, yy + 362, "C", 13, MUTED, width=410, lead=18)
# screenshot storyline
text("Five screenshots, one story", 570, yy + 12, "CB", 20, INK)
caps = [("Start building your best self", "Hero", TEAL), ("Workouts and programs", "Daily use", SAGE_D), ("Recipes for your preferences", "Nutrition", SAGE_D),
        ("Ask Your Coach", "Your touch", TEAL), ("Community", "Belonging", SAGE_D)]
pw = 118
for i, (cap, lb, col) in enumerate(caps):
    xx = 570 + i * (pw + 12)
    phone(xx, yy + 48, pw, screen_shot(cap, lb, col), shadow=False)
    text("%d  %s" % (i + 1, lb), xx + pw / 2, yy + 48 + pw * 2.05 + 12, "CB", 13, INK, "c")
text("Screenshots must show the real app in use. These frames show the story order, with your real screens going inside.", 570, yy + 48 + pw * 2.05 + 40, "C", 14, MUTED, width=660, lead=19)

# =============== SLIDE 9: first 7 days ===============
yy = new_slide(title="The first 7 days: from install to habit", kicker="Activation", sub="Most members decide in week one. A short, human sequence in your voice does the work.")
seq = [("Day 0", "Welcome from Leah", "“Start with your first workout today. It takes about 15 minutes. I am glad you are here.”", "First workout in 24 hours"),
       ("Day 1", "Nudge, if no workout yet", "“Your first workout is waiting. Pick any one and tell me how it felt.”", "Remove the fear of starting"),
       ("Day 3", "Check in and a recipe", "“How is your week going? Here is a recipe that fits your preferences.”", "Show the whole app"),
       ("Day 7", "Celebrate week one", "“One week done! If FTLR is helping, a quick rating means a lot to me.”", "First rating, at a happy moment"),
       ("Day 14", "Invite to community", "“Join this week's challenge in the group chat. Ask me anything in Ask Your Coach.”", "Belonging and daily use")]
cw_ = 220; gap = 20
c.setStrokeColor(LINE); c.setLineWidth(4); c.line(80, Y(yy + 38), W - 80, Y(yy + 38))
for i, (d, h, msg, goal) in enumerate(seq):
    xx = 60 + i * (cw_ + gap)
    circle(xx + cw_ / 2, yy + 38, 27, SAGE_D if i % 2 == 0 else TEAL)
    text(d, xx + cw_ / 2, yy + 30, "CB", 14, WHITE, "c")
    text(h, xx + cw_ / 2, yy + 80, "CB", 18, INK, "c", width=cw_, lead=22)
    rrect(xx, yy + 128, cw_, 170, 20, fill=MINT)
    text(msg, xx + 16, yy + 144, "CI", 15, INK, width=cw_ - 32, lead=20)
    text("GOAL", xx + 4, yy + 322, "CB", 12, SAGE_D)
    text(goal, xx + 4, yy + 340, "CB", 16, INK, width=cw_, lead=20)
text("Send these as emails, chat messages or in app notes, whichever you prefer.", 60, 640, "C", 16, MUTED)

# =============== SLIDE 10: design direction ===============
yy = new_slide(title="Design direction: calm, uplifting, unmistakably FTLR", kicker="Look and feel",
               sub="Built only from what you already say and show: sage green, “uplifted instead of beat down”, “strong, powerful, mobile”.")
text("Colors", 60, yy + 10, "CB", 20, INK)
sw_ = [("Sage", "#8FB09B", SAGE, INK), ("Deep sage", "#5F8570", SAGE_D, WHITE), ("Ink", "#1D2A24", INK, WHITE), ("Deep teal", "#2F6F7E", TEAL, WHITE), ("Mist", "#F6F9F7", BG, INK)]
for i, (nm, hx, col, tc) in enumerate(sw_):
    xx = 60 + i * 124
    rrect(xx, yy + 44, 112, 112, 14, fill=col, stroke=LINE)
    text(nm, xx + 12, yy + 108, "CB", 15, tc)
    text(hx, xx + 12, yy + 128, "C", 13, tc)
text("Type", 60, yy + 190, "CB", 20, INK)
rrect(60, yy + 224, 604, 120, 14, fill=WHITE, stroke=LINE)
text("Headlines: bold, tight, confident", 84, yy + 242, "CB", 27, INK)
text("Body: clean and easy to read, in the iPhone system font", 84, yy + 290, "C", 18, MUTED)
text("Brand signature", 60, yy + 372, "CB", 20, INK)
rrect(60, yy + 406, 604, 80, 14, fill=WHITE, stroke=LINE)
rrect(84, yy + 428, 190, 36, 4, fill=SAGE)
text("FTLR", 179, yy + 431, "CB", 24, INK, "c")
text("The sage highlight block is your signature. Keep the logo large and centered.", 296, yy + 428, "C", 15, MUTED, width=348, lead=19)
# principles
rrect(700, yy + 10, W - 760, 476, 18, fill=WHITE, stroke=LINE)
text("Design principles", 728, yy + 30, "CB", 22, INK)
pr = [("Uplifted, not beat down", "Soft greens, generous space, encouraging words. Never harsh."),
      ("Longevity over intensity", "Show progress over weeks and streaks, not only single workouts."),
      ("Strong. Powerful. Mobile.", "Use your three pillars as the way members move around the app."),
      ("One calm system", "Every screen shares the same colors, buttons and spacing, from sign in to the home screen.")]
t2 = yy + 78
for h, d in pr:
    check(740, t2 + 12, 12)
    text(h, 766, t2, "CB", 18, INK)
    t2 = text(d, 766, t2 + 24, "C", 15, MUTED, width=W - 840, lead=20) + 18
text("Today vs direction", 728, t2 + 4, "CB", 17, SAGE_D)
text("Your paywall already follows this style. The login and home screens use a generic template, so there is room to bring the same calm look everywhere.", 728, t2 + 28, "C", 15, INK, width=W - 790, lead=20)

# =============== SLIDE 11: concept home ===============
yy = new_slide(title="Concept: a home screen members come back to", kicker="High fidelity concept",
               sub="A design concept in your colors. Names, workouts and numbers are illustrations, and your real photos and content go inside.")
pw = 236
phone(140, yy - 8, pw, screen_home)
notes = [("Greets and guides", "One clear next step: today's focus, with a single Start button."),
         ("Shows progress", "A weekly ring and streak turn effort into a visible win."),
         ("Quick access", "Workouts, Recipes, Plan and Ask Your Coach one tap away."),
         ("Your philosophy", "“This is the FTLR way” and the three pillars stay in view.")]
t2 = yy + 6
for h, d in notes:
    rrect(500, t2, 700, 100, 16, fill=WHITE, stroke=LINE)
    check(536, t2 + 50, 18)
    text(h, 576, t2 + 18, "CB", 21, INK)
    text(d, 576, t2 + 50, "C", 17, MUTED, width=600, lead=22)
    t2 += 118

# =============== SLIDE 12: concept sign in / onboarding ===============
yy = new_slide(title="Concept: a welcome that gets members to their first workout", kicker="High fidelity concept",
               sub="Sign in, goal and a note from you. Three calm screens in the same style as your paywall.")
pw = 228
for i, (fn, lb, d) in enumerate([(screen_signin, "1  Sign in", "Branded, simple, email and password."),
                                 (screen_goal, "2  Choose a goal", "Personal from the first minute."),
                                 (screen_welcome, "3  A note from Leah", "Your voice, then a first workout.")]):
    cx = 213 + i * 427
    phone(cx - pw / 2, yy - 6, pw, fn)
    text(lb, cx, yy - 6 + pw * 2.05 + 14, "CB", 19, INK, "c")
    text(d, cx, yy - 6 + pw * 2.05 + 40, "C", 15, MUTED, "c", width=340, lead=19)

# =============== SLIDE 13: Android ===============
yy = new_slide(title="Is Android worth it? Measure first", kicker="Reach", sub="A simple 14 day count protects your budget and tells you the truth.")
rrect(60, yy + 10, 420, 330, 18, fill=WHITE, stroke=LINE)
text("Step 1", 84, yy + 32, "CB", 14, SAGE_D)
text("For 14 days, add one line to your welcome message:", 84, yy + 54, "C", 18, INK, width=370, lead=24)
rrect(84, yy + 120, 372, 70, 35, fill=MINT)
text("“Which phone do you use?”", 270, yy + 140, "CB", 22, SAGE_D, "c")
text("Step 2", 84, yy + 224, "CB", 14, SAGE_D)
text("Count the answers, and note every member who asks for Android.", 84, yy + 246, "C", 18, INK, width=370, lead=24)
c.saveState(); c.setFillColor(SAGE_D)
p = c.beginPath(); p.moveTo(500, Y(yy + 130)); p.lineTo(500, Y(yy + 190)); p.lineTo(560, Y(yy + 160)); p.close(); c.drawPath(p, stroke=0, fill=1); c.restoreState()
rrect(580, yy + 10, 640, 150, 18, fill=MINT, stroke=SAGE_D, lw=1.5)
text("Many answer Android, or several ask", 606, yy + 32, "CB", 21, SAGE_D)
text("An Android version will pay for itself. Same app, same subscriptions, on Google Play.", 606, yy + 70, "C", 18, INK, width=590, lead=24)
rrect(580, yy + 180, 640, 150, 18, fill=WHITE, stroke=LINE)
text("Almost nobody asks", 606, yy + 202, "CB", 21, INK)
text("Wait. Spend your effort on the first workout, reviews and retention instead.", 606, yy + 240, "C", 18, MUTED, width=590, lead=24)

# =============== SLIDE 14: quick wins ===============
yy = new_slide(title="Five quick wins you can do this week", kicker="Start today", sub="No tools or help needed. Each one takes minutes.")
wins = [("Write your launch announcement", "One email and one community post."), ("Update your promotional text", "Make it about launch day."),
        ("Choose your 5 screenshots", "Follow the story on slide 8."), ("Set up the Day 0 welcome message", "Your voice, 15 minutes, first workout."),
        ("Check your support email daily", "Apple and members expect quick replies.")]
t2 = yy + 10
for i, (h, d) in enumerate(wins):
    rrect(60, t2, W - 120, 78, 16, fill=WHITE, stroke=LINE)
    circle(104, t2 + 39, 22, SAGE_D); text(str(i + 1), 104, t2 + 26, "CB", 22, WHITE, "c")
    text(h, 148, t2 + 14, "CB", 21, INK); text(d, 148, t2 + 44, "C", 16, MUTED)
    t2 += 92

# =============== SLIDE 15: next ===============
yy = new_slide(title="Where we can go next, together", kicker="Options, no pressure",
               sub="Use the playbook on your own, or choose any piece you would like built and tested for you. We agree the scope in writing before anything starts.")
opts = [("Launch Ready", "Listing copy, screenshot storyline and a 30 day launch plan with written emails and posts."),
        ("Android on Google Play", "The same app and subscriptions for Android members."),
        ("Design refresh", "The look you just saw: home, sign in and welcome, in your brand."),
        ("Retention messages", "Automated welcome and win back emails and texts in your voice."),
        ("Care plan", "Updates, fixes and support so Apple changes never surprise you.")]
cw_ = 224; gap = 15
for i, (h, d) in enumerate(opts):
    xx = 60 + i * (cw_ + gap)
    rrect(xx, yy + 20, cw_, 250, 18, fill=WHITE, stroke=LINE)
    rrect(xx, yy + 20, cw_, 70, 18, fill=SAGE_D if i % 2 == 0 else TEAL)
    text(h, xx + 18, yy + 38, "CB", 21, WHITE, width=cw_ - 36, lead=24)
    text(d, xx + 18, yy + 110, "C", 16, INK, width=cw_ - 36, lead=22)
rrect(60, 580, W - 120, 74, 18, fill=MINT)
text("What matters most to you in the next 30 days? We start there.", W / 2, 604, "CB", 22, SAGE_D, "c")

# =============== SLIDE 16: thanks ===============
c.showPage(); page_no[0] += 1
c.setFillColor(INK); c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(SAGE); c.rect(0, H - 10, 220, 10, stroke=0, fill=1)
logo(80, 150, 260)
text("Thank you, Leah", 80, 330, "CB", 52, WHITE)
text("Congratulations on getting FTLR Fitness this far. I am glad to be part of it.", 80, 400, "C", 22, colors.HexColor("#CFE0D5"), width=620, lead=30)
text("Up Agency", 80, 540, "CB", 18, WHITE)
text("Questions, ideas, or a first priority? Let's talk.", 80, 568, "C", 16, colors.HexColor("#9FB8A8"))
phone(880, 120, 230, screen_home)
c.save()
print("pages", page_no[0])

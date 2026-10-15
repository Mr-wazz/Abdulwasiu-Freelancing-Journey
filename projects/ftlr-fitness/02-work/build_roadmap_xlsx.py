from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter

SAGE_D = "5F8570"; INK = "1D2A24"; MINT = "E6F0EA"; LINEC = "D8E3DC"
hdr_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
hdr_fill = PatternFill("solid", fgColor=SAGE_D)
thin = Side(style="thin", color=LINEC)
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
inp = Font(name="Calibri", color="0000FF", bold=True)   # blue = editable input

wb = Workbook()

# ---------------- Roadmap ----------------
ws = wb.active; ws.title = "Roadmap"
ws["A1"] = "FTLR Fitness: drip billing roadmap (internal, do not send)"
ws["A1"].font = Font(name="Calibri", bold=True, size=16, color=INK)
ws["A2"] = "One small yes at a time. Send ONE Fiverr offer, deliver it, get approval, then offer the next. Blue cells are inputs you can change."
ws["A2"].font = Font(name="Calibri", italic=True, color="5E6D65")
heads = ["#", "Phase", "Offer", "What she gets", "Why now (value to Leah)", "Offer it when", "Month", "Price (USD)",
         "Fiverr fee", "Net to you", "Status", "Date offered", "Notes"]
for i, h in enumerate(heads, 1):
    cl = ws.cell(row=4, column=i, value=h); cl.font = hdr_font; cl.fill = hdr_fill; cl.alignment = Alignment(wrap_text=True, vertical="center"); cl.border = border
rows = [
 ("Launch ready", "App Store listing pack", "Name, subtitle, keywords, promotional text, checked and ready to paste", "Strangers find her app through the listing", "On the call or right after", "Oct 2026", 150),
 ("Launch ready", "App Store screenshots, 5 designed", "Five captioned screenshots using her real screens, telling one story", "Screenshots decide who installs", "After the listing is approved", "Oct 2026", 250),
 ("Launch ready", "Launch announcement pack", "Email, community post and pinned chat message, written in her voice", "Launch day needs words ready", "Before Nov 1", "Oct 2026", 120),
 ("Launch ready", "Welcome and 7 day message sequence", "Day 0, 1, 3, 7 and 14 messages written and set up", "First workout in 24 hours keeps members", "Launch week", "Nov 2026", 180),
 ("Launch week", "Ratings prompt at happy moments", "Asks for a rating after a finished workout, never at a bad time", "Reviews build trust and ranking", "After first 20 members", "Nov 2026", 200),
 ("Launch week", "Purchase flow polish", "Clearer progress and faster unlock after subscribing (today about 12 seconds)", "Waiting after paying feels risky", "After first real purchases", "Nov 2026", 180),
 ("Build the habit", "Design quick pack", "Sign in and home screen: 3 improvements in her brand", "First impression, same calm look everywhere", "After launch week review", "Nov 2026", 350),
 ("Build the habit", "Onboarding flow", "Goal choice, first workout nudge, welcome note from Leah", "Turns installs into active members", "After design quick pack", "Nov 2026", 450),
 ("Build the habit", "Analytics dashboard", "Installs, active members, revenue and cancellations in one view", "Fix the biggest leak first", "30 days after launch", "Dec 2026", 400),
 ("Build the habit", "Workout reminders (push)", "Gentle reminders that bring members back", "Habit needs a nudge", "After onboarding is live", "Dec 2026", 550),
 ("Grow", "Android, step 1: accounts and setup", "Google Play account, app record, billing set up", "Opens the other half of the market", "When Android demand is confirmed", "Dec 2026", 250),
 ("Grow", "Android, step 2: build and billing", "Android app with the same subscriptions", "Same app, same plans", "After step 1", "Dec 2026", 400),
 ("Grow", "Android, step 3: store listing and submission", "Listing, screenshots, review handling", "Live on Google Play", "After step 2", "Jan 2027", 250),
 ("Grow", "Retention automation, step 1", "Welcome and win back flows designed", "Quiet members come back", "After analytics shows drop off", "Jan 2027", 350),
 ("Grow", "Retention automation, step 2", "Email and text setup, testing, go live", "Runs on its own", "After step 1", "Jan 2027", 400),
 ("Grow", "Invite a friend system", "Referral link with a reward for both people", "Cheapest growth there is", "After retention is live", "Jan 2027", 450),
]
r0 = 5
for k, (ph, off, got, why, when, mo, pr) in enumerate(rows):
    r = r0 + k
    vals = [k + 1, ph, off, got, why, when, mo, pr, None, None, "Not offered", None, None]
    for ci, v in enumerate(vals, 1):
        cl = ws.cell(row=r, column=ci, value=v); cl.alignment = wrap; cl.border = border; cl.font = Font(name="Calibri", size=10.5)
    ws.cell(row=r, column=8).font = inp; ws.cell(row=r, column=8).number_format = '"$"#,##0'
    ws.cell(row=r, column=9, value="=H%d*Summary!$B$3" % r).number_format = '"$"#,##0'
    ws.cell(row=r, column=10, value="=H%d-I%d" % (r, r)).number_format = '"$"#,##0'
    ws.cell(row=r, column=12).number_format = "yyyy-mm-dd"
    if k % 2 == 1:
        for ci in range(1, 14): ws.cell(row=r, column=ci).fill = PatternFill("solid", fgColor="F7FAF8")
rl = r0 + len(rows) - 1
tr = rl + 1
ws.cell(row=tr, column=3, value="TOTAL (one time)").font = Font(bold=True)
ws.cell(row=tr, column=8, value="=SUM(H%d:H%d)" % (r0, rl)).number_format = '"$"#,##0'
ws.cell(row=tr, column=9, value="=SUM(I%d:I%d)" % (r0, rl)).number_format = '"$"#,##0'
ws.cell(row=tr, column=10, value="=SUM(J%d:J%d)" % (r0, rl)).number_format = '"$"#,##0'
for ci in (3, 8, 9, 10): ws.cell(row=tr, column=ci).font = Font(bold=True); 
for ci in range(1, 14): ws.cell(row=tr, column=ci).fill = PatternFill("solid", fgColor=MINT); ws.cell(row=tr, column=ci).border = border
widths = [5, 16, 34, 46, 38, 28, 11, 12, 11, 12, 14, 13, 30]
for i, w in enumerate(widths, 1): ws.column_dimensions[get_column_letter(i)].width = w
ws.freeze_panes = "D5"
dv = DataValidation(type="list", formula1='"Not offered,Offered,Accepted,Delivered,Paid,Declined"', allow_blank=False)
ws.add_data_validation(dv); dv.add("K%d:K%d" % (r0, rl))
ws.conditional_formatting.add("K%d:K%d" % (r0, rl), CellIsRule(operator="equal", formula=['"Paid"'], fill=PatternFill("solid", bgColor="B7E1C1", fgColor="B7E1C1")))
ws.conditional_formatting.add("K%d:K%d" % (r0, rl), CellIsRule(operator="equal", formula=['"Offered"'], fill=PatternFill("solid", bgColor="FFE9A8", fgColor="FFE9A8")))
ws.conditional_formatting.add("K%d:K%d" % (r0, rl), CellIsRule(operator="equal", formula=['"Declined"'], fill=PatternFill("solid", bgColor="F4C7C3", fgColor="F4C7C3")))
for r in range(r0, rl + 1): ws.row_dimensions[r].height = 46

# ---------------- Summary ----------------
sm = wb.create_sheet("Summary", 0)
sm["A1"] = "FTLR Fitness: revenue summary"; sm["A1"].font = Font(bold=True, size=16, color=INK)
sm["A3"] = "Fiverr fee rate"; sm["B3"] = 0.20; sm["B3"].number_format = "0%"; sm["B3"].font = inp
sm["C3"] = "Check your own Fiverr dashboard and change this if your fee differs."
sm["A4"] = "Your target (gross)"; sm["B4"] = 5000; sm["B4"].number_format = '"$"#,##0'; sm["B4"].font = inp
sm["A5"] = "Care plan per month"; sm["B5"] = 199; sm["B5"].number_format = '"$"#,##0'; sm["B5"].font = inp
sm["A6"] = "Care plan months in first 90 days"; sm["B6"] = 3; sm["B6"].font = inp
lines = [
 ("Planned one time total (gross)", "=Roadmap!H%d" % tr),
 ("Planned one time total (net after fee)", "=Roadmap!J%d" % tr),
 ("Care plan over the period (gross)", "=B5*B6"),
 ("Planned total including care plan (gross)", "=B7+B9"),
 ("Gap to target (gross, one time only)", "=B4-B7"),
 ("Paid so far (gross)", '=SUMIF(Roadmap!K%d:K%d,"Paid",Roadmap!H%d:H%d)' % (r0, rl, r0, rl)),
 ("Accepted or delivered, not yet paid", '=SUMIF(Roadmap!K%d:K%d,"Accepted",Roadmap!H%d:H%d)+SUMIF(Roadmap!K%d:K%d,"Delivered",Roadmap!H%d:H%d)' % (r0, rl, r0, rl, r0, rl, r0, rl)),
 ("Offered, waiting for her yes", '=SUMIF(Roadmap!K%d:K%d,"Offered",Roadmap!H%d:H%d)' % (r0, rl, r0, rl)),
 ("Progress to target", "=B12/B4"),
]
for i, (lb, f) in enumerate(lines):
    r = 7 + i
    sm.cell(row=r, column=1, value=lb); cl = sm.cell(row=r, column=2, value=f)
    cl.number_format = '"$"#,##0' if lb != "Progress to target" else "0%"
    cl.font = Font(bold=True)
sm["A17"] = "By phase"; sm["A17"].font = Font(bold=True, size=13, color=INK)
phases = ["Launch ready", "Launch week", "Build the habit", "Grow"]
for i, p in enumerate(phases):
    sm.cell(row=18 + i, column=1, value=p)
    cl = sm.cell(row=18 + i, column=2, value='=SUMIF(Roadmap!B%d:B%d,A%d,Roadmap!H%d:H%d)' % (r0, rl, 18 + i, r0, rl)); cl.number_format = '"$"#,##0'
sm["A23"] = "Cash by month (gross, if every item is accepted)"; sm["A23"].font = Font(bold=True, size=13, color=INK)
for i, m in enumerate(["Oct 2026", "Nov 2026", "Dec 2026", "Jan 2027"]):
    sm.cell(row=24 + i, column=1, value=m)
    cl = sm.cell(row=24 + i, column=2, value='=SUMIF(Roadmap!G%d:G%d,A%d,Roadmap!H%d:H%d)' % (r0, rl, 24 + i, r0, rl)); cl.number_format = '"$"#,##0'
sm["A29"] = "Check: months add up to total"; sm["B29"] = '=IF(SUM(B24:B27)=B7,"OK","CHECK")'
sm["A31"] = "Rules"; sm["A31"].font = Font(bold=True, size=13, color=INK)
rules = ["1. One open offer at a time. Deliver, get her approval, then offer the next.",
         "2. Every offer is a Fiverr custom offer. Never take payment outside Fiverr.",
         "3. Start work only after the milestone is funded.",
         "4. Each offer has a written scope. Anything extra is quoted separately.",
         "5. Always lead with value: show a result first, then offer the next step.",
         "6. If she says no or not now, mark Declined or move it later. Never push."]
for i, t in enumerate(rules): sm.cell(row=32 + i, column=1, value=t)
sm.column_dimensions["A"].width = 52; sm.column_dimensions["B"].width = 16; sm.column_dimensions["C"].width = 70
for r in range(3, 16): sm.cell(row=r, column=1).font = Font(bold=(r in (4,)))

# ---------------- Messages ----------------
ms = wb.create_sheet("Messages")
ms["A1"] = "Messages to send (adjust names and numbers)"; ms["A1"].font = Font(bold=True, size=16, color=INK)
msgs = [
 ("Offer 1: Listing pack (after the call)", "Leah, thank you for your time today. The playbook gives you the structure. If you would like me to do the listing for you, I can write and check the App Store name, subtitle, keywords and promotional text so it is ready to paste. It is a small fixed job for $150, delivered in a short time, on Fiverr with payment protected. Shall I send the offer?"),
 ("Offer 2: Screenshots (after offer 1 is delivered)", "Leah, your listing is ready. The next thing that decides who installs is the screenshots. I can design five captioned screenshots using your real screens, telling the story we planned. It is $250 and I will need your screens or a quick screen recording. Want me to send the offer?"),
 ("Offer 3: Launch announcement pack", "Leah, launch is close. I can write your launch email, community post and pinned chat message in your voice so launch day is ready: $120. Shall I send it?"),
 ("Offer 4: Welcome sequence", "Leah, the first week decides if new members stay. I can write and set up your Day 0, 1, 3, 7 and 14 messages: $180. Want me to send the offer?"),
 ("Template: after any delivery", "Leah, here is [WHAT WAS DELIVERED]. How does it look? If you are happy, the next thing that helps most is [NEXT WIN], because [ONE SENTENCE OF VALUE]. It is $[PRICE]. Want me to send the offer, or would you rather wait?"),
 ("If she says not now", "Of course, no pressure. I will keep it on the list and check in after launch week. Congratulations again on the launch."),
 ("If she asks for a discount", "I keep each job small and fixed so it stays easy. If the budget is tight, we can do the most important piece first and add the rest later."),
]
ms["A3"] = "Situation"; ms["B3"] = "Message"
for cl in (ms["A3"], ms["B3"]): cl.font = hdr_font; cl.fill = hdr_fill
for i, (a, b) in enumerate(msgs):
    ms.cell(row=4 + i, column=1, value=a).alignment = wrap; ms.cell(row=4 + i, column=2, value=b).alignment = wrap
    ms.cell(row=4 + i, column=1).font = Font(bold=True); ms.row_dimensions[4 + i].height = 80
    for ci in (1, 2): ms.cell(row=4 + i, column=ci).border = border
ms.column_dimensions["A"].width = 40; ms.column_dimensions["B"].width = 110

OUT = "/home/user/Abdulwasiu-Freelancing-Journey/projects/ftlr-fitness/FTLR-Revenue-Roadmap.xlsx"
wb.save(OUT); print("saved")

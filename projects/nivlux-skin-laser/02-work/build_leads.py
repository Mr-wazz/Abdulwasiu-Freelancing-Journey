"""Build the NivLux B2B referral partner lead list (Excel).
Usage: python3 build_leads.py <leads.json> <out.xlsx>
Input rows: name, phone, segment, brand, housenumber, street, unit, city, zip, website,
hours, instagram, facebook, email, miles, src, (optional) reviews, years, categories.
"""
import json, re, sys, datetime
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

rows = json.load(open(sys.argv[1])); OUT = sys.argv[2]
TODAY = datetime.date.today().isoformat()

BURG, GOLD, CREAM, INK = "7A0E1E", "C9A227", "FBF6EC", "2B1A12"
HDR = Font(bold=True, color="FFFFFF", name="Calibri", size=11)
HFILL = PatternFill("solid", fgColor=BURG)
TFONT = Font(bold=True, size=18, color=BURG, name="Georgia")
H2 = Font(bold=True, size=13, color=BURG, name="Georgia")
WRAP = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="E3D7BF"); BOX = Border(left=thin, right=thin, top=thin, bottom=thin)

SEG = {  # base score, who to ask for, best call time, pitch angle
 "Bridal & Wedding": (32, "Owner or store manager", "Tue to Thu, 11am to 2pm",
   "Brides book laser 6 to 12 months before the wedding. A 'Smooth by the Big Day' perk makes the shop look premium and costs them nothing."),
 "Pilates, Yoga & Barre": (32, "Studio owner or front desk manager", "Mid morning 10am to 12pm, after early classes",
   "Members wear fitted, sleeveless gear and are already investing in their body. An exclusive member perk adds value to their membership for free."),
 "Lash & Brow": (28, "Owner", "Weekdays 10am to 12pm",
   "Their clients pay monthly for beauty upkeep and trust their artist's advice. Cross referral: NivLux sends facial clients back to them."),
 "Nail Salon": (26, "Owner or manager", "Weekdays 10am to 12pm (avoid lunch and after 4pm)",
   "Regular pedicure and manicure clients care about smooth legs and arms. Easy counter flyer with QR code."),
 "Tanning": (26, "Owner or manager", "Weekdays 10am to 1pm",
   "Tanning and spray tan clients want smooth skin before every session. Shaving before a tan is a pain point."),
 "Beauty Salon": (25, "Owner or salon manager", "Tue to Thu, 10am to 12pm",
   "Beauty clients already spend monthly on looking good. A partner perk adds value with no cost or extra work."),
 "Hair Salon": (22, "Salon owner or manager", "Tue to Thu, 10am to 12pm (Mon often closed)",
   "Stylists are trusted advisers to women who spend on themselves. Staff perk: free Hydra Diamond facial for the team."),
 "Day Spa & Massage": (24, "Owner or spa director", "Weekdays 10am to 12pm",
   "Spa clients love self care but the spa has no laser. Partnership fills the gap instead of losing clients to a competitor."),
 "Gym & Fitness": (24, "Owner, general manager or member services lead", "Weekdays 10am to 2pm (avoid 5pm to 7pm rush)",
   "Members who train want to see definition. Men's back and chest package and women's package as a member perk."),
 "Barbershop": (22, "Owner", "Tue to Thu, 10am to 12pm",
   "Men's grooming customers. Men's Smooth & Confident package (back, shoulders, chest) is a natural fit."),
 "Tattoo Studio": (20, "Owner or shop manager", "Weekdays 1pm to 4pm (shops open late)",
   "Clients shave before tattoos and many want hair free skin to show off ink. NivLux also offers tattoo removal by consultation, a two way referral."),
 "Dance & Pole Studio": (22, "Studio owner", "Weekdays 11am to 2pm",
   "Dancers perform in costumes and leotards, smooth skin is a must. Perk for adult students and instructors."),
 "Cosmetics Store": (12, "Store manager", "Weekdays 10am to 12pm",
   "Beauty shoppers. Chains rarely sign local deals, try for a flyer or event spot."),
}
BIGBOX = re.compile(r"planet fitness|24 hour|la fitness|crunch|great clips|supercuts|sport clips|fantastic sams|cost cutters|ulta|sephora|walmart|target|bally|gold's gym|in-shape|in shape|regis|smartstyle|bath & body|sally beauty|massage envy|hand & stone|european wax", re.I)
FRANCH = re.compile(r"club pilates|pure barre|orangetheory|f45|yogasix|corepower|stretchlab|anytime fitness|snap fitness|massage envy|hand & stone|hand and stone|burn boot|title boxing|9round|row house|cyclebar|solidcore|amazing lash|drybar|madison reed|sola salon|salons by jc|my salon suite|bodyfit", re.I)

def score(r):
    base, who, when, angle = SEG[r["segment"]]
    s = base; tag = "Independent"
    if BIGBOX.search(r["name"]) or BIGBOX.search(r.get("brand", "")): s -= 18; tag = "Big chain"
    elif FRANCH.search(r["name"]) or r.get("brand"): s -= 4; tag = "Franchise (local owner)"
    m = r.get("miles") or 99
    s += 10 if m <= 5 else 6 if m <= 10 else 2 if m <= 18 else 0
    if r.get("website"): s += 3
    try:
        rv = int(r.get("reviews") or 0); s += 5 if rv >= 50 else 3 if rv >= 15 else 0
    except ValueError: pass
    pr = "HOT" if s >= 36 else "WARM" if s >= 28 else "STANDARD"
    return s, pr, tag, who, when, angle

for r in rows:
    r["score"], r["priority"], r["type"], r["who"], r["when"], r["angle"] = score(r)
    addr = " ".join(x for x in [r.get("housenumber", ""), r.get("street", "")] if x)
    if r.get("unit"): addr += f", Unit {r['unit']}"
    r["address"] = addr
rows.sort(key=lambda r: (-r["score"], r["miles"]))

wb = Workbook()
# ---------- Start Here ----------
ws = wb.active; ws.title = "Start Here"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3; ws.column_dimensions["B"].width = 34; ws.column_dimensions["C"].width = 90
ws["B2"] = "NivLux Skin & Laser: B2B Referral Partner Lead List"; ws["B2"].font = TFONT
ws["B3"] = f"Greater Sacramento, about 30 miles around 2 Scripps Dr, Suite 203, Sacramento, CA 95825. Built {TODAY}."
ws["B3"].font = Font(italic=True, color="6B5B4B")
cnt = Counter(r["priority"] for r in rows)
info = [
 ("Total leads", len(rows)),
 ("HOT (call first)", cnt["HOT"]), ("WARM", cnt["WARM"]), ("STANDARD", cnt["STANDARD"]),
 ("Goal of every call", "Book a 10 minute meeting or a free partner visit at NivLux, so the owner can try a Hydra Diamond Facial and agree to a partner perk for their clients."),
 ("What we sell through partners", "Women's Smooth Essentials: Brazilian + Underarms + Full Legs + Full Arms, 10 sessions each, $2,999 (single session value about $6,750). Men's Smooth & Confident: Full Back + Shoulders + Chest, 10 sessions each, $2,299 (single session value about $4,950). Each comes with a free Hydra Diamond Facial ($199 value)."),
 ("Why a partner says yes", "Free perk for their customers, free facial for owner and staff, co branded QR flyer, shout out on NivLux Instagram. No cost, no work, makes them look premium."),
 ("Compliance (important)", "Laser hair reduction is a medical service in California. California rules (Business and Professions Code 650) restrict paying cash per patient referral. Offer perks, co marketing and staff treats, not cash per client, until NivLux's medical director confirms what is allowed. Business numbers only. Remove anyone who says do not call."),
 ("How to use the Leads tab", "1. Filter Priority = HOT. 2. Call in the 'Best time to call' window. 3. Fill Call Status, Decision maker, Next step, Follow up date after every call. 4. Interested leads: send the follow up text or email from the Call Script tab the same day."),
 ("Data sources", "OpenStreetMap contributors (ODbL license) and each business's own website, checked " + TODAY + ". Phones can change: if a number is wrong, mark 'Wrong number' and move on."),
]
for i, (k, v) in enumerate(info, start=5):
    ws.cell(i, 2, k).font = Font(bold=True, color=INK); c = ws.cell(i, 3, v); c.alignment = WRAP
    ws.row_dimensions[i].height = 18 if len(str(v)) < 90 else 15 * (len(str(v)) // 85 + 1)
r0 = 5 + len(info) + 1
ws.cell(r0, 2, "Leads by segment").font = H2
for j, (sg, n) in enumerate(Counter(r["segment"] for r in rows).most_common(), start=r0 + 1):
    ws.cell(j, 2, sg); ws.cell(j, 3, n).alignment = Alignment(horizontal="left")

# ---------- Leads ----------
L = wb.create_sheet("Leads")
cols = [("Lead ID", 9), ("Priority", 11), ("Score", 7), ("Segment", 22), ("Business name", 34), ("Phone", 16),
        ("Address", 30), ("City", 15), ("ZIP", 8), ("Miles from NivLux", 10), ("Website", 30), ("Hours", 24),
        ("Business type", 18), ("Ask for", 26), ("Best time to call", 26), ("Why they fit (pitch angle)", 60),
        ("Source", 16), ("Checked", 11),
        ("Call status", 18), ("Attempts", 9), ("Last call date", 13), ("Decision maker name", 22), ("Email collected", 26),
        ("Outcome / next step", 34), ("Follow up date", 13), ("Notes", 40)]
for j, (h, w) in enumerate(cols, 1):
    c = L.cell(1, j, h); c.font = HDR; c.fill = HFILL if j <= 18 else PatternFill("solid", fgColor="8A6D1F")
    c.alignment = Alignment(wrap_text=True, vertical="center"); L.column_dimensions[get_column_letter(j)].width = w
L.row_dimensions[1].height = 32
for i, r in enumerate(rows, start=2):
    vals = [f"NL-{i-1:03d}", r["priority"], r["score"], r["segment"], r["name"], r["phone"], r["address"], r.get("city", ""),
            r.get("zip", ""), r["miles"], r.get("website", ""), r.get("hours", ""), r["type"], r["who"], r["when"], r["angle"],
            r.get("src", ""), TODAY, "Not called", 0]
    for j, v in enumerate(vals, 1):
        c = L.cell(i, j, v); c.border = BOX
        c.alignment = Alignment(vertical="top", wrap_text=(j in (16,)))
    if r.get("website"):
        L.cell(i, 11).hyperlink = r["website"]; L.cell(i, 11).font = Font(color="1F4E9A", underline="single")
    for j in range(21, 27): L.cell(i, j).border = BOX
    L.cell(i, 21).number_format = "yyyy-mm-dd"; L.cell(i, 25).number_format = "yyyy-mm-dd"
n = len(rows) + 1
L.freeze_panes = "F2"; L.auto_filter.ref = f"A1:{get_column_letter(len(cols))}{n}"
dv = DataValidation(type="list", formula1='"Not called,No answer,Voicemail left,Call back later,Gatekeeper: get owner,Interested: send info,Meeting booked,Partner signed,Not interested,Wrong number,Do not call"', allow_blank=True)
L.add_data_validation(dv); dv.add(f"S2:S{n}")
for txt, col in (("HOT", "F8D7DA"), ("WARM", "FFF1C9"), ("STANDARD", "EEF2F5")):
    L.conditional_formatting.add(f"B2:B{n}", FormulaRule(formula=[f'$B2="{txt}"'], fill=PatternFill("solid", fgColor=col), font=Font(bold=True)))
L.conditional_formatting.add(f"A2:Z{n}", FormulaRule(formula=['OR($S2="Meeting booked",$S2="Partner signed")'], fill=PatternFill("solid", fgColor="D8F0DC")))
L.conditional_formatting.add(f"A2:Z{n}", FormulaRule(formula=['OR($S2="Do not call",$S2="Wrong number",$S2="Not interested")'], font=Font(color="999999", strike=True)))

# ---------- Call Script ----------
C = wb.create_sheet("Call Script"); C.sheet_view.showGridLines = False
C.column_dimensions["A"].width = 3; C.column_dimensions["B"].width = 28; C.column_dimensions["C"].width = 100
C["B2"] = "Cold Call Script: Referral Partner Program"; C["B2"].font = TFONT
script = [
 ("1. Opener (10 seconds)", "Hi, this is [Your Name] calling for NivLux Skin & Laser, a nurse led laser and skin clinic on Scripps Drive near Arden Fair. Quick question, are you the owner or the person who handles partnerships?"),
 ("If gatekeeper", "No problem. What is the best name and time to reach the owner? I'll call back then. (Write it in Decision maker name and set a Follow up date.)"),
 ("2. Reason for the call", "We are picking a few [salons / studios / gyms / bridal shops] in [their city] to offer an exclusive perk to their clients, at zero cost to you. Do you have 30 seconds?"),
 ("3. The value", "Your clients get our intro laser hair reduction package plus a free Hydra Diamond Facial, a $199 value. You get a free facial for you and your team, co branded QR flyers for your counter, and a shout out on our Instagram. No cost, no paperwork, and it makes your business look premium."),
 ("4. Segment hook", "Use the 'Why they fit' column. Example for bridal: 'Brides start laser 6 to 12 months before the wedding, so this is a perfect add on for your brides.' Example for gyms: 'Your members train hard to look good, this helps them show it.'"),
 ("5. The ask (the close)", "Can I bring the flyers by and you come try the facial? Would Tuesday or Thursday work better? (Goal: a booked visit or 10 minute call, not a sale on the phone.)"),
 ("Objection: not interested", "Totally fair. Most owners say that until they see it costs nothing. Can I just text you the one page so you have it? What's the best number?"),
 ("Objection: we already work with someone", "Great, that shows your clients care about this. Many partners work with 2 or 3. Our package includes 10 sessions and a free facial, which most clinics don't match. Worth a look?"),
 ("Objection: send me an email", "Happy to. What is the best email? And so I send the right thing, is it more for your clients or for your staff?"),
 ("Objection: what do I get paid?", "We keep it simple: perks for your clients and your team, plus co marketing. Our medical team sets the rules on referral rewards, I'll ask them what else we can offer you. (Never promise cash per client.)"),
 ("Objection: too busy", "I'll be quick. When is a better time this week, morning or afternoon?"),
 ("Voicemail (20 seconds)", "Hi, this is [Your Name] with NivLux Skin & Laser in Sacramento, 916-202-4302. We are offering a free client perk and a free facial for your team, no cost to you. I'll try you again [day], or call me back at 916-202-4302. Thanks!"),
 ("Follow up text (same day)", "Hi [Name], [Your Name] from NivLux Skin & Laser here. As promised: free partner perk for your clients (intro laser package + free $199 Hydra Diamond Facial) and a free facial for your team. Can I drop by flyers this week? nivluxskinlaser.com"),
 ("Follow up email subject", "Free client perk for [Business name] (no cost)"),
 ("Follow up email body", "Hi [Name],\n\nThanks for your time today. Quick recap:\n\nNivLux Skin & Laser (2 Scripps Dr, Suite 203, Sacramento) is inviting a few local [segment] businesses to offer their clients an exclusive perk:\n- Women's Smooth Essentials: Brazilian, underarms, full legs, full arms, 10 sessions each, $2,999\n- Men's Smooth & Confident: back, shoulders, chest, 10 sessions each, $2,299\n- Both include a free Hydra Diamond Facial ($199 value)\n\nFor you and your team: a free facial, co branded QR flyers, and a feature on our Instagram.\n\nWould [day] or [day] work for a quick visit?\n\nWarm regards,\n[Your Name]\nNivLux Skin & Laser | 916-202-4302 | nivluxskinlaser.com"),
 ("Rules", "Call business numbers only, between 9am and 6pm Pacific. Be warm, slow, and friendly (island hospitality). Never give medical advice or promise results: 'Results vary, suitability is decided at the free consultation.' Remove anyone who asks not to be called."),
]
for i, (k, v) in enumerate(script, start=4):
    C.cell(i, 2, k).font = Font(bold=True, color=BURG); C.cell(i, 2).alignment = WRAP
    c = C.cell(i, 3, v); c.alignment = WRAP
    C.row_dimensions[i].height = max(30, 15 * (v.count("\n") + len(v) // 95 + 1))

# ---------- Dashboard ----------
D = wb.create_sheet("Daily Results"); D.sheet_view.showGridLines = False
D.column_dimensions["B"].width = 34; D.column_dimensions["C"].width = 14
D["B2"] = "Call Results (updates automatically)"; D["B2"].font = TFONT
stats = ["Not called", "No answer", "Voicemail left", "Call back later", "Gatekeeper: get owner", "Interested: send info",
         "Meeting booked", "Partner signed", "Not interested", "Wrong number", "Do not call"]
D.cell(4, 2, "Status").font = HDR; D.cell(4, 2).fill = HFILL; D.cell(4, 3, "Count").font = HDR; D.cell(4, 3).fill = HFILL
for i, s in enumerate(stats, start=5):
    D.cell(i, 2, s); D.cell(i, 3, f'=COUNTIF(Leads!$S$2:$S${n},B{i})')
k = 5 + len(stats) + 1
D.cell(k, 2, "Total calls made (attempts)").font = Font(bold=True); D.cell(k, 3, f"=SUM(Leads!$T$2:$T${n})")
D.cell(k + 1, 2, "Contacted (not 'Not called')").font = Font(bold=True); D.cell(k + 1, 3, f'=COUNTA(Leads!$S$2:$S${n})-COUNTIF(Leads!$S$2:$S${n},"Not called")')
D.cell(k + 2, 2, "Meeting rate").font = Font(bold=True)
D.cell(k + 2, 3, f'=IFERROR((C11+C12)/C{k+1},0)'); D.cell(k + 2, 3).number_format = "0.0%"

wb.save(OUT)
print("saved", OUT, len(rows), dict(cnt))

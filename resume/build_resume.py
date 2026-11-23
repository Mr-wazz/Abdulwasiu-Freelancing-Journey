# Builds an ATS-friendly resume: one column, no tables, no images, standard headings, real text bullets.
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAME = "Adam Owolabi"
TITLE = "WordPress Developer | Elementor, WooCommerce, Page Speed & Technical SEO"
CONTACT = "Maryland, United States  |  Upwork: upwork.com/freelancers/~0154ea4ce5dfd795e0"
START = "2024"  # confirmed by Adam 2026-11-23

doc = Document()
for s in doc.sections:
    s.top_margin = s.bottom_margin = Inches(0.6)
    s.left_margin = s.right_margin = Inches(0.75)
st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
st.paragraph_format.space_after = Pt(2)
st.paragraph_format.line_spacing = 1.08
DARK = RGBColor(0x1F, 0x23, 0x33)

def para(text="", bold=False, size=None, color=None, align=None, after=None, before=None, italic=False):
    p = doc.add_paragraph()
    if text:
        r = p.add_run(text); r.bold = bold; r.italic = italic
        if size: r.font.size = Pt(size)
        if color: r.font.color.rgb = color
    if align is not None: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if before is not None: p.paragraph_format.space_before = Pt(before)
    return p

def rule(p):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
    for k, v in (("w:val","single"),("w:sz","6"),("w:space","2"),("w:color","9AA0B4")): bt.set(qn(k), v)
    b.append(bt); pPr.append(b)

def heading(t):
    p = para(t.upper(), bold=True, size=11, color=DARK, before=10, after=4); rule(p)

def job(title, org, dates):
    p = para(before=6, after=1)
    r = p.add_run(title); r.bold = True; r.font.size = Pt(11)
    p.add_run(f"  |  {org}  |  {dates}")

def bullet(t):
    p = doc.add_paragraph(style="List Bullet"); p.paragraph_format.space_after = Pt(1.5)
    p.add_run(t)

para(NAME, bold=True, size=22, color=DARK, align=WD_ALIGN_PARAGRAPH.CENTER, after=0)
para(TITLE, size=11.5, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
para(CONTACT, size=9.5, align=WD_ALIGN_PARAGRAPH.CENTER, after=4)

heading("Professional Summary")
para("WordPress developer who helps businesses get more calls, bookings and sales from their websites. "
     "I build and fix fast, mobile-friendly WordPress, Elementor and WooCommerce sites, improve page speed and "
     "Core Web Vitals, and set up clear calls to action, tracking and secure checkout. 12 live projects across "
     "e-commerce, architecture, media, nonprofit and software, and a 100% Job Success Score on Upwork. "
     "Every job starts with a full backup and ends with testing on phone, tablet and desktop and a handover the client can manage alone.")

heading("Core Skills")
skills = [
 ("WordPress", "WordPress development, Elementor, WPBakery Page Builder, WordPress themes and plugins, Advanced Custom Fields (ACF), Figma to WordPress, landing pages, website redesign"),
 ("E-commerce", "WooCommerce store setup, product catalogs, cart and checkout optimization, Stripe and PayPal integration, shipping and tax rules"),
 ("Performance", "Page speed optimization, Core Web Vitals, Google PageSpeed Insights, caching, image optimization, Cloudflare CDN"),
 ("SEO and Analytics", "Technical SEO, on-page SEO, Google Search Console, Google Analytics 4 (GA4), Google Tag Manager, 301 redirects"),
 ("Security and Support", "WordPress security hardening, malware removal, backups, bug fixes, plugin conflicts, website migration, website maintenance"),
 ("Web", "HTML, CSS, PHP, JavaScript, responsive design, web applications, dashboards"),
]
for k, v in skills:
    p = para(after=1.5); r = p.add_run(k + ": "); r.bold = True; p.add_run(v)

heading("Professional Experience")
job("Freelance WordPress Developer", "Self-employed (Upwork and direct clients), Remote", f"{START} to Present")
for b in [
 "Build and maintain WordPress, Elementor and WooCommerce websites for small businesses, online stores, nonprofits and personal brands, focused on turning visitors into enquiries and sales.",
 "Built Keerah Beauty (keerahbeauty.com), a WooCommerce skincare store with product search, wishlist, customer accounts and one-click add to cart on the homepage.",
 "Developed Beautymart (beautymartng.com), a WooCommerce beauty store with shop-by-category navigation, product pages, cart and checkout.",
 "Built the RED TV media website (itsred.tv) in Elementor with a full-screen show slider, trailers, show pages and an awards section.",
 "Built the Lateefah Okunnu Foundation nonprofit website with a video hero, program and impact pages and a persistent Donate button, set up so staff publish news without a developer.",
 "Developed a B2B marketplace web app for Copackers Recycling (cprsrecycling.com) with order tracking from quote to payment, inspection and logistics, plus purchase order and proforma drafts.",
 "Developed a personal brand website for a public leader (ibo.org.ng) with WPBakery, responsive on phones and tablets.",
 "Run page speed, Core Web Vitals and security work on client sites: caching, image compression, script cleanup, malware cleanup and backups, with before and after reports.",
 "Hold a 100% Job Success Score on Upwork; every job delivered with a full backup first, cross-device testing and a video walkthrough for the client.",
]: bullet(b)

job("WordPress Developer (Contract, Team Project)", "UP Agency, Remote", "2026")
for b in [
 "Part of the development team that built the WordPress website for Norm Architects (normcph.com), a Copenhagen architecture and design studio, with a gallery-led layout and featured project slider.",
 "Part of the development team that built the WordPress website for Space Copenhagen (spacecph.dk), an international interior design studio, with an editorial project grid and site search, loading in under 2 seconds on mobile.",
]: bullet(b)

heading("Selected Web App and Product Projects (Design Team Member)")
para("Worked as part of the web design team on these sites, responsible for fixing site speed and page layout.", after=2)
for b in [
 "Motoro (motoro-app.com): UK car valuation and selling platform with registration lookup, instant valuation, vehicle history check and a dealer portal.",
 "Smorza (smorza.app): product website for a macOS app with interactive demo, download flow, Pro page and blog.",
 "Make AI Influencer (makeaiinfluencer.com): SaaS landing site with product examples, pricing, FAQ and free-trial sign-up flow.",
 "Shanmugavel's Bookstore (shanmugavel-bookuniverse.vercel.app): eBook and audiobook store with time-based reading passes and card and UPI checkout.",
]: bullet(b)

heading("Education")
p = para(after=1); r = p.add_run("Bachelor's Degree in Computer Science"); r.bold = True; p.add_run("  |  University of Maryland  |  2023 to 2026")

heading("Certifications")
for b in [
 "WordPress Website Speed Optimization, Coursera, 2026",
 "Develop and Optimize WordPress Websites, EDUCBA / Coursera, 2026",
 "WordPress 2026: The Complete WordPress Website Course, Udemy, 2026",
 "WordPress Essential Training, LinkedIn Learning, 2024",
]: bullet(b)

doc.core_properties.title = f"{NAME} Resume"
doc.core_properties.author = NAME
doc.save("Adam-Owolabi-WordPress-Developer-Resume.docx")
print("saved")

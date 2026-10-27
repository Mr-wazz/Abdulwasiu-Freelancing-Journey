#!/usr/bin/env python3
"""Find businesses on Google Maps and audit their websites.

Usage:
  export GOOGLE_PLACES_API_KEY=...        (never commit the key)
  python3 scout.py "dental clinic" "Dubai" --limit 20
  python3 scout.py "aesthetic clinic" "Dubai" --limit 20

Appends scored leads to leads/leads.csv. Standard library only.
Scoring follows audit-checklist.md. Items that need a human eye
(design, Play Store app, review replies) are left for manual review.
"""
import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "leads", "leads.csv")
FIELDS = ["business", "niche", "city", "website", "owner_email", "score", "main_problem",
          "offer", "status", "date_contacted", "follow_up_1", "follow_up_2", "reply",
          "call_booked", "notes"]
UA = "Mozilla/5.0 (compatible; LeadAudit/1.0)"
BOOKING_WORDS = ("book now", "book an appointment", "book appointment", "book online",
                 "schedule", "calendly", "setmore", "zocdoc", "appointment form", "request appointment")
CHAT_WORDS = ("wa.me", "api.whatsapp.com", "tawk.to", "livechat", "intercom", "tidio",
              "crisp.chat", "drift.com", "leadconnector", "highlevel")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
JUNK_EMAIL = ("sentry", "example.", "wixpress", "your@", "name@", ".png", ".jpg", "@2x")


def places_search(key, query, limit):
    url = "https://places.googleapis.com/v1/places:searchText"
    mask = ("places.displayName,places.websiteUri,places.rating,places.userRatingCount,"
            "places.formattedAddress,places.nationalPhoneNumber,places.businessStatus,nextPageToken")
    out, token = [], None
    while len(out) < limit:
        body = {"textQuery": query, "pageSize": min(20, limit - len(out))}
        if token:
            body["pageToken"] = token
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "X-Goog-Api-Key": key,
                     "X-Goog-FieldMask": mask})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        out += data.get("places", [])
        token = data.get("nextPageToken")
        if not token:
            break
        time.sleep(1)
    return out[:limit]


def fetch(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        html = r.read(1_500_000).decode("utf-8", "ignore")
        return html, time.time() - t0, r.geturl()


def find_email(html, base):
    found = [e for e in EMAIL_RE.findall(html) if not any(j in e.lower() for j in JUNK_EMAIL)]
    if not found:
        for path in ("/contact", "/contact-us"):
            try:
                h, _, _ = fetch(urllib.parse.urljoin(base, path), timeout=10)
                found = [e for e in EMAIL_RE.findall(h) if not any(j in e.lower() for j in JUNK_EMAIL)]
                if found:
                    break
            except Exception:
                pass
    return found[0] if found else ""


def audit(place):
    """Return (score, problems[], email). Every problem is something we actually observed."""
    site = place.get("websiteUri")
    problems, score = [], 0
    if not site:
        return 60, ["No website listed on Google Maps (customers cannot book online)"], ""
    try:
        html, secs, final = fetch(site)
    except Exception as e:
        return 40, ["Website did not load when checked (%s)" % type(e).__name__], ""
    low = html.lower()
    if secs > 3:
        score += 15
        problems.append("Homepage took %.1f seconds to respond" % secs)
    if 'name="viewport"' not in low:
        score += 15
        problems.append("No mobile viewport tag, so the site likely breaks on phones")
    if not any(w in low for w in BOOKING_WORDS):
        score += 15
        problems.append("No online booking found on the homepage")
    if not any(w in low for w in CHAT_WORDS):
        score += 15
        problems.append("No chat or WhatsApp lead capture found")
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    desc = re.search(r'name=["\']description["\']', low)
    if not title or len(title.group(1).strip()) < 10 or not desc:
        score += 10
        problems.append("Missing or weak page title / meta description")
    if final.startswith("http://"):
        score += 5
        problems.append("Site is not served over HTTPS")
    reviews = place.get("userRatingCount", 0)
    if reviews < 30:
        score += 10
        problems.append("Only %d Google reviews" % reviews)
    return score, problems, find_email(html, final)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("niche")
    ap.add_argument("city")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args()
    key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not key:
        sys.exit("Set GOOGLE_PLACES_API_KEY first (see SETUP.md).")
    places = places_search(key, "%s in %s" % (a.niche, a.city), a.limit)
    existing = set()
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, newline="") as f:
            existing = {r["business"].lower() for r in csv.DictReader(f)}
    new = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    with open(CSV_PATH, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        for p in places:
            name = p.get("displayName", {}).get("text", "")
            if not name or name.lower() in existing or p.get("businessStatus") not in (None, "OPERATIONAL"):
                continue
            score, problems, email = audit(p)
            w.writerow({"business": name, "niche": a.niche, "city": a.city,
                        "website": p.get("websiteUri", ""), "owner_email": email,
                        "score": score, "main_problem": problems[0] if problems else "",
                        "offer": "", "status": "new" if score >= 50 and email else "review",
                        "date_contacted": "", "follow_up_1": "", "follow_up_2": "", "reply": "",
                        "call_booked": "",
                        "notes": "; ".join(problems) + " | audited %s | verify by hand before emailing" % date.today()})
            print("%3d  %-40s %s" % (score, name[:40], email or "(no email found)"))


if __name__ == "__main__":
    main()

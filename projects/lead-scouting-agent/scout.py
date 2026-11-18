#!/usr/bin/env python3
"""Find businesses on Google Maps and audit their websites.

Usage:
  export GOOGLE_PLACES_API_KEY=...        (never commit the key)
  python3 scout.py "dental clinic" "Dubai" --limit 20
  python3 scout.py "aesthetic clinic" "Dubai" --limit 20
Free, no key (OpenStreetMap):
  python3 scout.py dental Dubai --source osm --limit 40
  python3 scout.py aesthetic Dubai --source osm --limit 40

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
import subprocess
import urllib.parse
import urllib.request
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(HERE, "leads", "leads.csv")
FIELDS = ["business", "niche", "city", "website", "owner_email", "score", "main_problem",
          "offer", "status", "date_contacted", "follow_up_1", "follow_up_2", "reply",
          "call_booked", "notes"]
UA = "lead-scout/1.0 (website audit; contact waiiscreativedigital@gmail.com)"
BOOKING_WORDS = ("book now", "book an appointment", "book appointment", "book online",
                 "schedule", "calendly", "setmore", "zocdoc", "appointment form", "request appointment")
CHAT_WORDS = ("wa.me", "api.whatsapp.com", "tawk.to", "livechat", "intercom", "tidio",
              "crisp.chat", "drift.com", "leadconnector", "highlevel")
BLOCK_MARKERS = ("is parked free", "sgcaptcha", "just a moment", "checking the site connection",
                 "domain is for sale", "attention required", "enable javascript and cookies to continue")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
JUNK_EMAIL = ("sentry", "example.", "wixpress", "your@", "name@", ".png", ".jpg", "@2x")


def curl(url, data=None, timeout=15):
    """HTTP via curl: macOS system Python often fails TLS handshakes that curl handles."""
    cmd = ["curl", "-sSL", "-m", str(timeout), "-A", UA, "-H", "Accept: application/json, text/html;q=0.9, */*;q=0.8",
           "-w", "\n%{url_effective}", "--max-filesize", "3000000"]
    if data is not None:
        cmd += ["--data", data]
    t0 = time.time()
    res = subprocess.run(cmd + [url], capture_output=True, timeout=timeout + 5)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.decode("utf-8", "ignore").strip()[:120] or "curl failed")
    body, _, final = res.stdout.decode("utf-8", "ignore").rpartition("\n")
    return body, time.time() - t0, final


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


CITY_BBOX = {"Dubai": "24.75,54.85,25.40,55.60", "Abu Dhabi": "24.20,54.25,24.60,54.80"}
OSM_FILTERS = {
    "dental": ['["amenity"="dentist"]', '["healthcare"="dentist"]'],
    "aesthetic": ['["healthcare"="clinic"]["name"~"aesthetic|derma|cosmetic|laser|skin|beauty",i]',
                  '["shop"="beauty"]["name"~"clinic|aesthetic|derma|laser|medical",i]'],
}


def osm_search(kind, city, limit):
    """Free source, no key. Returns dicts shaped like Places results (no review counts)."""
    parts = "".join("nwr%s;" % f for f in OSM_FILTERS[kind])
    q = "[out:json][timeout:60][bbox:%s];(%s);out tags center 400;" % (CITY_BBOX[city], parts)
    els = None
    for attempt in range(4):  # Overpass is a shared free server: it sometimes answers busy
        body, _, _ = curl("https://overpass-api.de/api/interpreter", data=urllib.parse.urlencode({"data": q}), timeout=90)
        try:
            els = json.loads(body).get("elements", [])
            break
        except ValueError:
            time.sleep(15 * (attempt + 1))
    if els is None:
        sys.exit("OpenStreetMap server busy, try again in a few minutes.")
    out = []
    for e in els:
        t = e.get("tags", {})
        site = t.get("website") or t.get("contact:website") or t.get("url")
        if not t.get("name") or not site:
            continue
        if not site.startswith("http"):
            site = "http://" + site
        out.append({"displayName": {"text": t["name"]}, "websiteUri": site,
                    "email_hint": t.get("email") or t.get("contact:email") or "",
                    "userRatingCount": None})
    return out[:limit]


def fetch(url, timeout=15):
    return curl(url, timeout=timeout)


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
        return None, ["Website did not load when checked (%s)" % e], ""
    low = html.lower()
    if any(m in low for m in BLOCK_MARKERS) or "/lander" in final or len(low) < 1500:
        return None, ["Parked, bot-check or near-empty page: cannot audit honestly"], ""
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
    reviews = place.get("userRatingCount")
    if reviews is not None and reviews < 30:
        score += 10
        problems.append("Only %d Google reviews" % reviews)
    return score, problems, place.get("email_hint") or find_email(html, final)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("niche")
    ap.add_argument("city")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--source", choices=["places", "osm"], default="places",
                    help="osm is free and needs no key; use niche 'dental' or 'aesthetic'")
    a = ap.parse_args()
    if a.source == "osm":
        places = osm_search(a.niche, a.city, a.limit)
    else:
        key = os.environ.get("GOOGLE_PLACES_API_KEY")
        if not key:
            sys.exit("Set GOOGLE_PLACES_API_KEY first, or use --source osm (see SETUP.md).")
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
            if score is None:  # could not load the site: not evidence of a problem, so do not record a lead
                print("skip  %-40s %s" % (name[:40], problems[0]))
                continue
            w.writerow({"business": name, "niche": a.niche, "city": a.city,
                        "website": p.get("websiteUri", ""), "owner_email": email,
                        "score": score, "main_problem": problems[0] if problems else "",
                        "offer": "", "status": "review",  # a human must open the site and confirm every finding first
                        "date_contacted": "", "follow_up_1": "", "follow_up_2": "", "reply": "",
                        "call_booked": "",
                        "notes": "; ".join(problems) + " | audited %s | verify by hand before emailing" % date.today()})
            print("%3d  %-40s %s" % (score, name[:40], email or "(no email found)"))


if __name__ == "__main__":
    main()

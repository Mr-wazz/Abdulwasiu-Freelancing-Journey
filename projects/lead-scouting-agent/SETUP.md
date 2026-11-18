# Setup (beginner steps)

You do not have GHL. You do not need it to start. Use free tools.

1. Booking page: make a free Cal.com account, create a 20 minute "Free Growth Audit Call" event. Copy the link.
2. Sending email: use your Gmail first (drafts only). Later buy a separate domain such as fiverpulse-mail.com and set up a Google Workspace mailbox. Never cold email from your main address.
3. Google Maps data: open console.cloud.google.com, create a project, enable "Places API", create an API key. Keep it secret. Send it to Claude only inside a private environment variable, never in chat or GitHub.
4. Lead tracker: leads/leads.csv now, Google Sheet later.
5. Later (phase 2): GHL or a free CRM like HubSpot Free once you have 5 or more active leads.

What Claude does next once the key exists: run the finder for one niche and city, fill leads.csv, draft the first 20 emails.

---
## Status (2026-10-27)
- First market: Dubai (UAE) dental and aesthetic clinics. Nigeria is out of plan for now.
- Cal.com: event "Free Growth Audit Call" (20 min) created. Link: https://cal.com/oyenola-abdulwasiu-1h3rwi/free-growth-audit-call (open it once to confirm it loads, then use it in templates).
- Google Places key: not created yet. In the Google Cloud console: select the project, enable "Places API (New)", then Credentials > Create API key > restrict it to Places API (New). Billing must be on (Places has a free monthly allowance; set a budget alert).
- Run: `export GOOGLE_PLACES_API_KEY=...` then `python3 scout.py "dental clinic" "Dubai" --limit 20` (and "aesthetic clinic"). It appends to leads/leads.csv.
- The script only records problems it actually observed. Always open each lead's site yourself before any email is sent.

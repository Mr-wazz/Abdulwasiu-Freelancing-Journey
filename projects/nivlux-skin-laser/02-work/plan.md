# Plan: nivlux-skin-laser

## Tasks in order
1. [done] Research NivLux website, services, prices, brand, weak spots.
2. [done] Pick lead strategy: B2B referral partners in Greater Sacramento (gyms, pilates and yoga, salons, nails, lash and brow, spas, barbers, bridal, tattoo, dance).
3. [done] Pull open business data (OpenStreetMap) and phones from business websites. Clean, remove competitors (laser, med spa, wax, tattoo removal), dedupe by phone, score and rank.
4. [done] Excel builder: build_leads.py. Tabs: Start Here, Leads (with tracker and dropdowns), Call Script, Daily Results.
5. [partial] 163 verified leads in v1. Need about 340 more to reach 500 (waiting on Abdulwasiu's decision about the data source).
6. Final QA: spot check 30 numbers, remove duplicates, check chains, check no competitors.
7. Client message with the file + call plan.
8. Start cold calls (HOT first), log results in Leads tab.

## Files
- build_leads.py: builds the Excel from a JSON lead file.
- data/leads-source-osm.json: cleaned source leads.
- NivLux-B2B-Partner-Leads-v1-PARTIAL.xlsx: current file (163 leads).

## What Abdulwasiu must provide
- Decision on the data source for the remaining leads.
- Ask client: partner perk they approve (no cash per referral until medical director confirms), budget for calling, call hours, caller name, booking link to give partners.

## What the client must provide
- Approved partner offer and flyer (or approval to design one).
- Confirmation from the medical director on referral rewards (California B&P Code 650).
- Black Friday package details and end date.

## Test checklist
- [x] Excel opens, filters work, dropdown on Call status
- [x] No laser or med spa competitors in list (name filter)
- [x] No duplicate phone numbers
- [ ] Spot check 30 phone numbers by hand before calling

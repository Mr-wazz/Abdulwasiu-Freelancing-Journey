# Lead Scouting Agent (internal project, not a client)

Goal: a system that finds businesses with a clear problem, audits them, sends a short value message, books a call, and gives Abdulwasiu a summary so he closes the deal.

## Decision: two channels, Google Maps first
| Channel | Fit | Risk | Verdict |
|---|---|---|---|
| Google Maps audit + email | Business owners with real budgets, you can show proof (slow site, no booking, no app) | Low if volume is small and message is honest | START HERE |
| Facebook personal account | Warm, but automated DMs and scraping get accounts banned | High | Semi manual only (see facebook-plan.md) |
| Facebook Page + Messenger inbound | Automatic replies to people who message you | Low | Add in phase 2 |

## The flow
1. FIND: pick a niche and city (example: dentists in Lagos, gyms in Toronto). Pull businesses from Google Maps.
2. AUDIT: check website speed, mobile view, booking, forms, SEO basics, reviews, social links. Score each lead 0 to 100.
3. PICK: only contact leads with a clear problem and a reachable owner email.
4. WRITE: personal email with ONE finding and the money it costs them. No attachments, no hype.
5. SEND: small daily batch (20 to 30), from a separate domain, with an unsubscribe line.
6. FOLLOW UP: day 3 and day 7.
7. BOOK: reply with a calendar link. Free option: Cal.com or Google Calendar booking page.
8. SUMMARY: before each call, a one page brief (business, problem found, offer, price tier, objections).
9. CLOSE: Abdulwasiu takes the call.

## What is automated vs what needs Abdulwasiu
| Step | Who |
|---|---|
| Finding and auditing leads | Claude (needs a Google Places API key, see SETUP.md) |
| Writing emails | Claude |
| Approving the daily batch | Abdulwasiu (2 minutes, protects reputation) |
| Sending | Gmail drafts first, later a sending tool |
| Replies, booking, call summary | Claude drafts, Abdulwasiu sends |
| The call and closing | Abdulwasiu |

## Rules to stay safe
- Honest audits only. Never invent a problem.
- Business emails only. Respect unsubscribe the same day.
- EU and UK leads need extra care (GDPR). Start with Nigeria, US, Canada, UAE, Australia.
- Never mass blast. Quality over volume.

## Files
- SETUP.md: accounts and keys needed
- audit-checklist.md: how every lead is scored
- templates/: first email, follow ups, reply to interest, call summary
- leads/leads.csv: the lead tracker
- facebook-plan.md: safe Facebook plan

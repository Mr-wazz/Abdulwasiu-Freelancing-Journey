# Notes: Amazigh (RiseTrack)

## History
- 4 Sep 2026: Victor Olatunji submitted build 4. Rejected 8 Sep (5.6 Developer Code of Conduct: fake Premium start_trial and activate, many unused permissions)
- 8 Oct 2026: rejection 2, Guideline 4.0 Design (Sign in with Apple asked for name or email again). iPad Air 11 inch (M3), v1.0 (14). Submission ID 7b414429-74b6-47fe-9fed-b3720fd0de2e
- Fixes: Premium removed, Capacitor 7 wrapper, permissions cut, Sign in with Apple OFF, Resolution Center reply, notes updated, resubmitted
- About 13 Oct 2026: Apple approved
- 14 Oct 2026: handover from Claude chat to Claude Code

## Client personality
French, WhatsApp, friendly, replies a day late sometimes, very careful with money, wants step by step, wants subscription back, plans to reinvest app income.

## Problems solved (for future builds)
1. Base44 ZIP download needed Builder plan and GitHub sync
2. Codemagic "No configuration file found": files must be at repo root
3. "No matching profiles": use fetch-signing-files --create with a generated cert key, no ios_signing
4. 401 from Apple API: re-enter App Store Connect key in Codemagic Integrations
5. External TestFlight failure: submit_to_testflight false (Beta App Information and review contact empty)
6. Resubmit button grey: edit notes and save, refresh, Add for Review, or build 15 as backup

## OPEN ITEMS (ask Abdulwasiu)
1. Payment: Amazigh wants to pay by Sendwave to his OPay account. Not confirmed what it covers (approval job or step 2) or whether the Fiverr or Upwork contract is open. Off platform payment can break platform rules and remove escrow protection. His Fiverr account was blocked once. Recommendation: keep payment on the platform. If he chooses off platform anyway: confirm amount and what it covers in writing first. Sendwave needs only: full name as on OPay, OPay account number, bank OPay, country Nigeria, phone number. Never share a password, PIN, OTP or BVN
2. Was the step 2 message sent? Her step 2 budget
3. Was the approval job delivered, accepted, reviewed on platform
4. Ask her to revoke the App Store Connect API key now that the app is published
5. The two earlier Apple rejection messages were not checked for other reasons
6. Approval job price, deposit, unpaid amount not recorded
7. Who is "Samuel Marvelous" in App Store Connect
8. Real live Base44 link (zips contain a placeholder)

## Time log
Not recorded. Start logging.

## 14 Oct 2026: payment received
- Amazigh paid Abdulwasiu via Sendwave (off platform). Amount and what it covers: NOT yet confirmed in writing. Ask Abdulwasiu.
- Risk reminder: off platform payment means no escrow and possible platform rule issues (Fiverr account was blocked once). Mitigation: written confirmation of amount and scope in the chat, keep a screenshot of the Sendwave receipt, do not mention platform rules to the client.
- Amazigh also sent a message with "some things". Content NOT pasted yet. Ask Abdulwasiu to paste it exactly before replying.
- Upsell message (no prices) drafted, to send right after the payment confirmation, while the client is happy.

## 14 Oct 2026 evening (WhatsApp)
- Amazigh PAID via Sendwave (off platform). Amount and what it covers NOT recorded. Client wrote: "bien reçu normalement"
- Client said: app is online but not complete, many details to improve, example: "Edit with Base44" badge at the bottom
- Client said: even if tight financially, kept their word, so "we can trust each other and move forward together". Wants a call: "Texte-moi quand t'es libre, on se parle"
- Abdulwasiu asked for a talk within the hour
- Client screenshot (iPhone, dark mode) shows: "Edit with Base44" badge bottom right, a Base44 side handle on the right edge, the date text "MARDI 13 OCTOBRE" overlapping the iPhone clock at the top (safe area problem), empty state "Aucune habitude pour aujourd'hui"
- All of these are web side. Fix in Base44 and click Publish. No new iPhone build needed. Do not touch Apple settings
- Open: written confirmation of what the Sendwave payment covered. Draft line included in the reply message

## 14 Oct 2026 late: client refuses calls
- Client does not want a call. Everything is by text (WhatsApp). Upsell is a 3 message text sequence, no prices first.
- Plan: M1 reply and 3 findings (value), M2 two phase plan, M3 price only when asked, 2 milestones, protected payment.

## 14 Oct 2026 night: client wants ONE big complete update
- Client (text): they will analyze the app and send their list of improvements. They asked Abdulwasiu to note everything too, to bundle it all in one big complete update with subscriptions and solid foundations from the start, to avoid a new update for every small problem. After that, progress step by step on details.
- Meaning: buying signal for a bundled project. Plan to sell it as ONE fixed price "RiseTrack 2.0" with milestones, funded escrow on the platform, and a frozen scope date.
- Risk: open ended list (scope creep). Rule: scope freezes on a date, anything later goes to 2.1 as a paid add on. One big update also means one bigger Apple review, so test in TestFlight first and keep the Apple rules (see plan.md)
- Internal price recommendation: Standard 2.0 = packages 1 + 3 (2,100) with milestones 30/40/30. Premium = add dashboard (3,000) plus care plan. Start by text with no prices. Give prices only when they ask, with the frozen scope
- Client facing findings list saved at 02-work/audit-for-client-fr.md (no prices)

## 15 Oct 2026: client accepted the list plan
- Client (French): "Parfait on fait ca ! J'attends ta liste et de mon cote aussi je t'enverrai".
- Value first message ready in 02-work/audit-for-client-fr.md (two messages, no prices, impact per point, priority, list freeze date Sunday 18 Oct). Must confirm the "a confirmer" points on a real iPhone before sending.
- Next: client sends their list, freeze on 18 Oct, then write the fixed price offer (Standard: packages 1 and 3) with milestones and platform escrow.

## 15 Oct 2026: audit PDF for the client
- Built a 2 page colored PDF: 02-work/RiseTrack-Audit-et-Plan-d-amelioration.pdf (source script build_audit_pdf.py). French, no prices. Each point has a status (Constate, A valider, Proposition) and a priority. Replaces the two text messages.
- Prepared by "Up Agency" (name the client sees on WhatsApp). Change in the script if needed.
- Before sending: test the A VALIDER items on an iPhone. The PDF is honest about them, but the fewer unconfirmed points the stronger the document.

## 16 Oct 2026: client read the PDF
- Client (French): doing well, at work, saw the RiseTrack PDF, "bien organisé", will read later and add what is missing. Otherwise "on avancera comme prévu".
- Meaning: soft yes to the plan. List freeze date stays Sunday 18 Oct. Offer draft prepared in 01-proposal-quote.md (INTERNAL draft, not sent).
- Rule: do not chase. One short warm reply, then send the offer on 18 Oct.

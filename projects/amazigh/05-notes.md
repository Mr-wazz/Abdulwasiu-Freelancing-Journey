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

## 17 Oct 2026: client sent his list (8 items) and budget rule
- Items: (1) welcome page before login, (2) modern design, (3) tracker check and redesign, (4) simplify Mon parcours, (5) shareable progress cards for Instagram, (6) redo App Store screenshots, (7) logo reframing (looks too zoomed), (8) check whole app for bugs.
- He will first choose priorities, then wants a "bilan" with the total price. Budget is his main worry. He will decide based on the amount whether to go now or wait.
- Plan: no prices yet. Reply with merged list grouped in lots, ask him to rank by numbers, extend freeze to Tue 20 Oct, ask 2 short questions (which screen with Google, where the logo looks zoomed). Internal priced catalog saved in 02-work/priorities-catalog-INTERNAL.md.
- Note: subscription is not in his new list. Keep as a later offer, do not drop it.

## 19 Oct 2026: client chose essentials and gave budget hint
- Screenshot 1: first open is the Base44 sign in page (email and password, "Welcome to RiseTrack"). NO Google button. His earlier line about Google was wrong. Still wants a real welcome page first (option 250).
- Screenshot 2: logo clarification. He now says the icon logo is NOT zoomed enough and wants it bigger, like other apps. (Earlier he said "trop zoome", he meant the opposite.) Preview made at 02-work/icon-apercu-avant-apres.png (from his screenshot, low resolution).
- Priorities: small touches first, then notifications and the Premium subscription, plus important bugs. Wants essentials only.
- Budget: "presque le meme budget que la derniere fois". The amount of the first job was never recorded. ASK Abdulwasiu the number.
- Bilan built (French PDF): projects/amazigh/RiseTrack-Bilan-et-Prix.pdf. Step A (web, live on publish): A1 badge and top of screen 100, A2 habits and duplicates 150, A3 full check and important bugs 250, total 500. Step B (one Apple update): B1 account deletion 100, B2 Apple subscription 1,400, B3 notifications 450, B4 logo 90, total 2,040. Options: Depart 500, Revenus 2,090, Essentiel complet 2,540. Optional welcome page 250. Pay item by item or 30/40/30 on the platform.
- Dependencies for subscription: client's Paid Apps Agreement, bank and tax must be active in his App Store Connect. Ask.
- Do not take payment by Sendwave again. Use platform with escrow.

## 19 Oct 2026: bilan v2 (CAD, smaller steps, no platform)
- Abdulwasiu does not read French. Client pays in CANADIAN DOLLARS. Abdulwasiu cannot collect payment on Fiverr or Upwork right now, so there is no escrow.
- Candid review: the first bilan (2,540 USD) was too heavy for a tight budget client. Re-priced in CAD and re-scoped. New prices (CAD): A1 100, A2 130, A3 200 (4h cap) = 430. B1 100, B2 subscription base 1,000, B3 free trial and price page 200, B4 notifications 380, B5 logo 70 = 1,750. Options: Depart 430, Revenus 1,600, Essentiel complet 2,180. Welcome page option 200.
- Rough USD value at an ASSUMED 0.72 USD per CAD (check the real rate): 430 = about 310, 1,600 = about 1,150, 2,180 = about 1,570.
- Payment rule without escrow: pay each item BEFORE work starts. Items under 200 CAD paid in full first. Big items split: B2 350 + 350 + 300, B4 190 + 190. Written agreement in chat and a payment receipt screenshot each time. Confirm the money has arrived before starting.
- Platform risk: client came from Fiverr. Taking payment outside the platform can break platform rules, and Abdulwasiu's Fiverr was blocked once. His decision. Better: restore payout on Fiverr or Upwork (for example a payout method the account supports) and move back to platform offers when possible.
- Files: FR client PDF projects/amazigh/RiseTrack-Bilan-et-Prix-v2-FR-CLIENT.pdf and EN copy for Abdulwasiu RiseTrack-Bilan-et-Prix-v2-EN-copie-pour-Abdulwasiu.pdf. The old USD version was renamed v1-OLD-USD-do-not-send.

## 19 Oct 2026: bilan v2 sent, persuasion content prepared
- Abdulwasiu sent the bilan v2 (CAD). Prepared a one page "Pourquoi maintenant" (FR for client, EN copy for Abdulwasiu) and 2 messages (main and 2 day follow up).
- Core message: no subscription means no revenue, no notifications means users forget and leave, small details look unfinished right after approval, Apple needs account deletion. Budget friendly: pay weekly, small amounts, result every week, stop anytime. Plans: 1 Depart 430 CAD (3 weeks), 2 Revenus 1,600 CAD (7 weeks), 3 Essentiel complet 2,180 CAD (10 weeks). CTA: answer 1, 2 or 3. Start after first payment of 100 CAD.
- Illustrative payback: 6 CAD per month, about 5.10 net after Apple 15 percent, 1,600 CAD repaid with about 26 subscribers for a year. Marked as example, not a promise.
- Weekly schedule: Depart 100/130/200. Revenus adds wk4 170, wk5 350, wk6 350, wk7 300. Complet adds wk8 200, wk9 190, wk10 190.

## 20 Oct 2026: client says sums are astronomical
- Client (translated): sums too big, first project, does not want to invest without knowing the app will earn. Either he goes little by little and finds solutions himself, or if Abdulwasiu accepts to move forward with him he will be paid significant sums once the app earns.
- Abdulwasiu wants to learn his budget and get started, with a long term view.
- Response: warm message with 3 paths (little by little from about 50 CAD per week, hybrid partnership with written terms, pause) and 3 questions (budget per week or month, user count, subscription price). Guardrails saved in 02-work/partnership-guardrails-INTERNAL.md.
- Rule: no unpaid work on a pure promise. Cash for the first small win, partial deferral only, written agreement, cap, read only revenue access.

## 20 Oct 2026: Abdulwasiu wants one single payment of about 400
- Designed "Pack Solide" single payment 400 CAD (see 01-proposal-quote.md). Honest limit: 400 cannot cover subscription, notifications, deletion or the Apple build (about 34 hours). Those go to the partnership step.
- Collection steps: written yes, Sendwave transfer, receipt screenshot, confirm money arrived, then start. Delivery in 7 days.

## 20 Oct 2026: client says Base44 makes it easy, CAD 300 for everything
- Client (translated): the app is on Base44, changes are done on the platform, not in code. He thought CAD 300 was enough for bugs, subscriptions and notifications. When the app earns money he will offer another amount.
- Abdulwasiu wants to start today and finish today.
- Reality: subscription and notifications are native Apple features. Need his Paid Apps Agreement, RevenueCat, a new Codemagic build, TestFlight test and Apple review (1 to 2 days at best). Cannot finish in a day.
- Decision proposed: CAD 300 buys Pack Stabilite only (A1, A2, bounded A3). Start when money has arrived. Premium and notifications go to a written revenue share. Prompts ready: 02-work/base44-fix-prompts.md

## 20 Oct 2026: client agrees, scope list for CAD 300
- Client (translated): "OK, you do what you need to on your side, then tell me what to download etc. Good luck my brother, let's move forward together."
- Abdulwasiu has access to his Base44 and App Store Connect. Wants a written scope list and a clause: paid when everything except the payment integration is done. Wants RevenueCat to speed up the payment part.
- Plan: stability first (preview, publish on payment), then RevenueCat subscription, then notifications. Needs from Amazigh: Paid Apps Agreement, bank and tax active (only he can do it), subscription products, APNs key. Time to live: 3 to 5 days because of Apple steps.
- Rough effort inside CAD 300: about 30+ hours. Below value. Tie future work to a written revenue share.

## 20 Oct 2026 (later): prices set, client wants to pay at the end
- Client (French): subscription prices are CAD 3.99 per month and CAD 27.99 per year, with a 7 day free trial.
- Client wants to pay the CAD 300 only after all features work AND Apple accepted the new version. Future work: "we will talk when the time comes".
- CONFLICT with the agreed rule (pay before Publish). Not accepted yet. Proposed counter, waiting for Abdulwasiu: CAD 150 before Publish of the web fixes, CAD 150 when Apple approves the new build. Abdulwasiu decides.
- To check in App Store Connect: that CAD 3.99 and 27.99 price points can be set.
- Base44 login not done yet. Time log: 0 hours so far.

## 20 Oct 2026 (session 2): Prompt 1 run in Base44 Preview
- Abdulwasiu logged in to Base44. Ran Prompt 1 in the editor chat. Base44 added safe-area top padding on the Today page only. viewport-fit=cover was already set.
- Badge: Builder plan allows hiding it. It is a switch in Dashboard, Overview, Platform Badge, "Hide Badge". NOT clicked yet: it probably changes the live app at once, so it waits for Abdulwasiu's OK and payment decision.
- Other screens (Tracker, Defis, Parcours, Reglages) not yet checked for safe area.
- Not published. Time today: about 0.3 hours.

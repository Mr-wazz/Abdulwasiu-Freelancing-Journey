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

## 20 Oct 2026 (session 2, part 2)
- PAYMENT DECISION: Abdulwasiu told Amazigh he pays the CAD 300 when the project is done (client terms accepted). No escrow, no money before delivery. Risk: Apple review is outside our control. Keep Publish and "Hide Badge" as separate asks to Abdulwasiu.
- Safe area padding added in Preview to Tracker, Defis, Parcours, Reglages (Today done before). Base44 says build passes. Cannot be seen in a desktop preview (safe area is 0 there): test on a real iPhone.
- Prompts 2 to 4 not started. Time today: about 0.6 hours.

## 20 Oct 2026 (session 2, part 3)
- Abdulwasiu said: do Prompt 2, hide badge, and publish.
- Backup: clicked "Make a copy" in Dashboard menu. No copy appeared in the Base44 app list after about 1 minute. Not confirmed. Base44 Data has "Backup & Restore" tab marked as a paid feature (not used). Tables: Challenge, Habit, HabitLog.
- "Hide Badge" click was BLOCKED by the app's permission system (counted as a production change). Not done. Nothing published. Prompt 2 not started (no confirmed backup of real user data).
- Time today: about 1 hour.

## 20 Oct 2026 (session 2, part 4)
- Abdulwasiu hid the Base44 badge and published himself (safe area on 5 screens went live with it). Not checked on the live app yet.
- Backup: Abdulwasiu exported the 3 tables (Challenge, Habit, HabitLog) as CSV on his laptop. Not in the repo (user data).
- Prompt 2 run in Preview: Base44 removed the week filter in Today Page, Tracker Page and use Report Stats. Habits now show every week until deleted or archived. No data edited. NOT tested with a real habit (preview account has 0 habits). NOT published.
- Next: test with one test habit, Prompt 3 (duplicate logs), Prompt 4 (bug check, 2h cap). Time today: about 1.7 hours.

## 20 Oct 2026 (session 2, part 5)
- Prompt 3 run in Preview (duplicate logs): Base44 now checks the server before creating a log, so a tap updates the existing log. Added backend function cleanupDuplicateHabitLogs and ran it once: found 0 duplicates. IMPORTANT: the Data tab I can see holds only my test rows, so it looks like a separate test database. The cleanup has NOT yet run on live users' data. After Publish, check once.
- Test in Preview: created habit "TEST Abdul", ticked 20 Oct, went to next week (25 to 31 Oct): habit still shown (carry over works). Double tap on 27 Oct made one log only (no duplicate).
- Small existing quirk: after changing week without picking a day, the old day's tick still shows until a day is selected. Not fixed, can go in the bug check.
- Test data still there: habit "TEST Abdul" and 2 HabitLog rows (20 and 27 Oct). Deleting with Move to Trash did not work from my clicks (count stayed 2). To delete by hand in Dashboard, Data.
- NOT published. Time today: about 2.5 hours.

## 20 Oct 2026 (session 2, part 6): bug check done and PUBLISHED
- Prompt 4 (bug check) run in Base44. Found and fixed:
  1. SERIOUS: Habit, HabitLog, Challenge had no access rules. Any signed in user could read, edit, delete others' data. Added owner only rules (read, update, delete).
  2. SERIOUS: "Reset habits" and "Delete account" listed ALL users' data with no user filter, so one user could wipe everyone's habits, logs and challenges. Now scoped to the user's own records.
  3. Tick bug after switching week: fixed (switching week keeps the same weekday).
  4. Duplicate log through the notes feature: fixed.
  Rechecked OK: carry over every week, no duplicate logs.
- Left for later (price in phase 2): Reset habits says "permanently deleted" but archives and clears only the 2,000 most recent logs; support@risetrack.app mailbox unconfirmed; week-start setting ignored (weeks start Sunday); unused week_start field; leftover subscription fields on user records; Apple 5.1.1(v) real account deletion still not done (login stays).
- PUBLISHED by me at Abdulwasiu's request: dialog showed "Your app is live" at risetracker.base44.app (badge hidden earlier by Abdulwasiu). Includes safe area, carry over, duplicates, access rules.
- WATCH: the new owner only rules go live untested with real accounts. If a real user reports empty habits, check Habit, Data, Permissions (records created by another user would be hidden). CSV backup is on Abdulwasiu's laptop. Also run cleanupDuplicateHabitLogs result check on live data.
- Test data "TEST Abdul" (1 habit, 2 logs) still in the database: delete by hand.
- Time today: about 3.5 hours (bug check about 0.5 hour, under the 2 hour cap).

## 20 Oct 2026 (session 2, part 7): Apple setup message and RevenueCat project
- Wrote the message to Amazigh (French with English below): 02-work/message-amazigh-apple-setup.md. Asks for Paid Apps Agreement, bank and tax, then 2 App Store Connect keys and 1 APNs key (.p8 files never in chat). NOT sent yet, Abdulwasiu sends it.
- Abdulwasiu logged in to his RevenueCat (account also has a project "FTLR Fitness", not touched). I created a new project "RiseTrack" (category Health, platform Capacitor). RevenueCat suggested entitlement "RiseTrack Pro" and offering Monthly, Yearly, Lifetime. I skipped them (Lifetime was not agreed). Nothing else configured.
- Next in RevenueCat, blocked until Apple is ready: add the App Store app (bundle ID com.base6996fa161c7db2beb6067c48.app), upload keys (by Amazigh or Abdulwasiu, never me), products monthly CAD 3.99 and yearly CAD 27.99 with 7 day trial, entitlement, offering. Invite Amazigh as collaborator later.
- Time today: about 4.2 hours.

## 20 Oct 2026 (session 2, part 8): OneSignal
- Decision: OneSignal for push notifications (free plan). Abdulwasiu created the account (login email is his own, not Amazigh's).
- I finished its onboarding: Healthcare and Wellness, 1 to 10 employees, Push channel, skipped brand and SDK steps, chose Free plan. OneSignal auto created an app named "Abdulwasiu App". TO DO: rename it to RiseTrack, add iOS platform with the APNs key (from Amazigh), then the SDK in the iPhone wrapper.
- App Store Connect: not logged in yet in the browser. Waiting for Abdulwasiu.
- Time today: about 4.5 hours.

## 20 Oct 2026 (session 2, part 9): App Store Connect read only check
- Abdulwasiu logged in. Read only checks, nothing changed:
  - v1.0 is "Ready for Distribution", approved build is 14. (Closes open item: which build Apple approved.)
  - Users and Access: belharetamazigh7@gmail.com = Amazigh Belharet, Account Holder and Admin. marvel19.04.2004@gmail.com = "Samuel Marvelous" = the login Abdulwasiu uses, role App Manager. (Closes open item: who is Samuel Marvelous.)
  - Consequence: App Manager cannot create API keys or open Business (Paid Apps Agreement, bank, tax). Only Amazigh can. The idea that Abdulwasiu creates the keys is not possible unless Amazigh makes him Admin (his decision, not recommended to ask).
  - The Business page stayed blank or loading for me, consistent with no access.
- Still to do in App Store Connect (App Manager can do it): create subscription group and 2 products as drafts. Waiting for Abdulwasiu's OK.
- Time today: about 5 hours.

## 20 Oct 2026 (session 2, part 10): App Store Connect subscriptions (drafts)
- Created in Amazigh's App Store Connect (as App Manager): subscription group "RiseTrack Premium" (group ID 22496883) and product "RiseTrack Premium Monthly", product ID risetrack_premium_monthly, duration 1 month, status Prepare for Submission.
- Still missing on the monthly product: availability, price CAD 3.99, 7 day free intro offer, display name and description, review screenshot. Yearly product (risetrack_premium_yearly, 1 year, CAD 27.99, 7 day trial) not created yet.
- Apple note: the first subscription group must be submitted together with a NEW app version, so it goes with the new build.
- Tip: Apple's site needs a wide window and is slow and sometimes blank. Narrow pane hides the left menu.
- Time today: about 5.7 hours.

## 20 Oct 2026 (session 2, part 11): yearly product and price
- Created product "RiseTrack Premium Yearly", ID risetrack_premium_yearly, 1 year, Apple ID 6824962485, in group RiseTrack Premium.
- Set yearly price with base country Canada: CAD 27.99 (confirmed in the pricing dialog, Apple auto converts other countries, e.g. US 19.99 USD, EU 22.99 EUR). The page shows a pricing summary, saved status to be verified once at next visit.
- Apple now has an "Availability" block with two options (1 Year Upfront, or Monthly with 12-Month Commitment, needs iOS 26.4+). We use "1 Year Upfront". Availability not set yet.
- STILL TO DO in App Store Connect: monthly price CAD 3.99 (check that 3.99 exists, use See Additional Prices), 7 day free intro offer on both, availability on both, display name and description (French and English) on both, review screenshot of the paywall (needs the Base44 price page first).
- Time today: about 6.4 hours.

## 20 Oct 2026 (session 2, part 12)
- Wrote progress message to Amazigh (FR with EN below): 02-work/message-amazigh-progress-update.md. Not sent yet. Notes: the monthly price and trial are not yet in App Store Connect.
- Apple's page hung again when I tried the monthly price. Retry next session (reload tab first).
- Time today: about 6.6 hours.

## 21 Oct 2026: client reply
- Abdulwasiu sent the progress message with the Paid Apps Agreement steps. Client (French): "Parfait mon ami, des que je rentre je fais ca". So he will do it when he gets home. NOT done yet.
- Clock for the 3 to 5 days has not started. Blocker: Paid Apps Agreement, bank and tax (only Amazigh).
- Do not chase today. One short check next morning if no news. Keys message (2 App Store Connect keys, 1 APNs key) goes AFTER step 1 is done.
- Meanwhile (no client needed): finish monthly price CAD 3.99, trial, names in App Store Connect, price page in Base44, wrapper work.

## 21 Oct 2026 (later): client added bank info
- Client (French): he added his bank information, Apple is processing it. Missing: TPS and TVQ numbers (Canadian GST and Quebec QST) for the tax part. He will confirm the number tomorrow by calling Revenu Quebec.
- Meaning: Paid Apps Agreement not Active yet. The 3 to 5 day clock still has not started. Tax details are his business, we do not give tax advice. We can only say to check the Apple form for a "not registered" option and ask Revenu Quebec or an accountant.
- Next: wait for his news tomorrow. Meanwhile finish App Store Connect products, Base44 price page, wrapper work.

## 21 Oct 2026: monthly price saved in App Store Connect
- Monthly product risetrack_premium_monthly: price set CAD 3.99 (base Canada). Other countries auto: US 2.99 USD, EU 2.99 EUR, AUD 4.99. Saved (confirmed after the Confirm dialog).
- Yearly product: price CAD 27.99 set earlier.
- STILL TO DO on both: Availability (choose all countries, and for yearly use "1 Year Upfront"), 7 day free intro offer, display name and description (French and English), review screenshot.
- Browser tips for Apple's site: in a narrow pane the screenshots lag and pop-up lists do not show. The normal "desktop" size works better, but wait 5 seconds after each click. Reach the product by clicking from the sidebar (Subscriptions, group, product). Direct links often hang.
- Time today (21 Oct): about 0.7 hours. Total about 7.3 hours.

## 21 Oct 2026 (part 2): Premium price page built in Base44 Preview
- Abdulwasiu OK'd. Prompt run in Base44: new Premium page (FR and EN), reached from Settings ("Passer a Premium"). Files created: Premium Page, components/premium/premium Copy, components/premium/Plan Card, lib/purchases. Edited App and Settings Page.
- Shows: 3 placeholder benefits, Monthly CAD 3.99, Yearly CAD 27.99 marked best value (saves CAD 19.89, 42 percent), 7 day trial line, trial button, Restore Purchases, Terms and Privacy links. Buttons call lib/purchases which looks for window.Capacitor.Plugins.Purchases (RevenueCat). In a browser it shows "Purchases are available in the iPhone app".
- Nothing is locked, all features stay free. NOT published. Preview only.
- OPEN DECISION for Abdulwasiu: what does Premium really unlock? Apple (3.1.2 and 2.3) can reject a subscription that sells things that are already free (the placeholder benefits "unlimited habits, advanced stats, smart reminders" are all free today). Options: lock advanced stats and smart reminders behind Premium, or sell "support the app" style tip, or Premium extras (themes, export, challenges). Locked features must be clearly described and must not break approved free use. Decide before the review screenshot and Apple build.
- Time today (21 Oct): about 1.1 hours. Total about 7.7 hours.

## 21 Oct 2026 (part 3): Option A chosen, Premium locks prepared (OFF)
- Decision (Abdulwasiu): Option A. Free: habits, tasks, weekly tracker, basic stats, 1 active challenge. Premium (CAD 3.99 per month, 27.99 per year, 7 day trial): iPhone reminders, advanced stats and trends, unlimited challenges.
- Built in Base44 Preview: lib/purchases has PREMIUM_LOCKS_ENABLED = false, usePremium(), canUse(feature) (always true while flag is false). Gates wired in Reminder Section, Tracker Page (trends chart), Challenges Page (2nd challenge). New component Premium Lock (small lock plus Unlock button to the Premium page). Premium Page benefits updated to the 3 lines (FR and EN), "nothing is locked" line removed.
- With the flag false the app behaves exactly as before. NOT published (Preview only).
- ORDER RULE: flip PREMIUM_LOCKS_ENABLED to true only AFTER Apple approves the new iPhone build with RevenueCat, then Publish (ask Abdulwasiu first). Otherwise free users would see locks with no way to buy.
- NOT yet tested with the flag on. Test next in Preview by flipping the flag, then flip back.
- Time today (21 Oct): about 1.6 hours. Total about 8.2 hours.

## 21 Oct 2026 (part 4): App Store Connect names
- Client has still not sent the tax numbers (TPS and TVQ), he said "until tomorrow" (22 Oct). Main blocker, nothing to do on our side.
- Subscription group "RiseTrack Premium": localization saved, French (Canada), display name "RiseTrack Premium", app name RiseTrack.
- Monthly product: French (Canada) display name "RiseTrack Premium mensuel", description "Rappels, stats avancées et défis illimités" (limits: 35 and 55 characters). Saved and shown on the page.
- STILL TO DO: yearly display name and description (suggest "RiseTrack Premium annuel", same description), English localization on group and both products (optional), Availability on both ("1 Year Upfront" for yearly), 7 day free trial introductory offer on both (look under the + next to Subscription Prices, price must exist first), review screenshot of the Premium page, review notes.
- Tips: use 1280 by 1500 viewport, take a screenshot and click by coordinates, wait 5 to 8 seconds after each click.
- Time today (21 Oct): about 2.4 hours. Total about 9 hours.

## 21 Oct 2026 (part 5): test data deleted
- Asked Base44 to delete only my test data. It listed before deleting: Habit "TEST Abdul" (one exact match) and its 2 HabitLogs (20 and 27 Oct). Totals before: 18 Habit, 2 HabitLog. Deleted those 3 records only. Totals after: 17 Habit, 0 HabitLog. No other record touched. (Open item closed.)
- Note: 17 Habit records remain, 0 logs overall, so this database looks like test or early data, not many real users yet. The Data page header may still show (18) until refreshed.
- Apple's site hung several times again (clicks time out). Still to do in App Store Connect: yearly display name and description, availability on both, 7 day trial on both, review screenshot and notes. Retry when the pane responds.
- Time today (21 Oct): about 2.8 hours. Total about 9.4 hours.

## 21 Oct 2026 (part 6): Apple availability attempt
- Reached the yearly product page and opened "Upfront Billing Availability". The "Select All" link did not respond to my clicks, so availability is NOT set on either product. Nothing was saved. Dialog closed with Escape.
- Manual steps for Abdulwasiu (a few clicks): open each product, Availability, Set Up Availability, tick all regions (or click "All" top right), Save. Then Subscription Prices, + , add the 7 day free introductory offer. Then yearly display name "RiseTrack Premium annuel".
- Time today (21 Oct): about 3.4 hours. Total about 10 hours.

## 21 Oct 2026 (part 7): iPhone wrapper branch and real purchase code
- DECISION to confirm with Abdulwasiu: reminders use LOCAL notifications (@capacitor/local-notifications), not remote push. Same result for the user (daily reminder at the chosen time), no OneSignal setup and no APNs key from Amazigh needed, no server, fewer Apple steps, lower review risk. OneSignal account (free) stays unused for now, remote push (inactivity messages, news) is a possible paid add-on later. The deal item "reminder notifications (native push)" is still met as native notifications on the iPhone.
- Cloned Mr-wazz/risetrack-ios. Created branch feature/premium-and-reminders (main untouched, no pull request). Added @revenuecat/purchases-capacitor 11.3.3 (newer versions need Capacitor 8) and @capacitor/local-notifications 7.x. npm install checked OK. Added docs/NATIVE_BRIDGE.md (web contract and pre-build checklist). Pushed the branch. NOT built (no Codemagic run, no Apple action).
- Base44 Preview: lib/purchases now makes real RevenueCat calls through window.Capacitor.Plugins.Purchases (configure, logIn, getOfferings, purchasePackage, restorePurchases, getCustomerInfo, entitlement "premium"). Empty REVENUECAT_IOS_API_KEY constant to fill later. New lib/reminders (schedule and cancel daily local notifications at the habit reminder time). Wired into Reminder Section, Habit Form Dialog, Today Page, Settings Page. PREMIUM_LOCKS_ENABLED still false. NOT published, not testable in a browser (needs the iPhone build).
- Draft review notes for Apple: 02-work/apple-review-notes-DRAFT.md.
- Still open: Apple availability and 7 day trial clicks (manual), yearly name, Amazigh tax numbers (due 22 Oct), RevenueCat app and keys, real account deletion (Apple 5.1.1(v)).
- Time today (21 Oct): about 4.6 hours. Total about 11.2 hours.

## 21 Oct 2026 (part 8): decisions and real account deletion
- DECISIONS (Abdulwasiu): (1) reminders use local notifications, yes. (2) Real account deletion is INCLUDED in the CAD 300, free.
- Built in Base44 Preview: backend function deleteMyAccount. Identity only from the session token (base44.auth.me()), no user id from the browser, 401 without a valid session. It deletes the caller's Habit, HabitLog and Challenge records (deleteMany filtered by created_by_id) and then the caller's own login with the service role. Settings flow: confirmation (now says account and login permanently deleted), cancel local reminders, call function, sign out with FR and EN confirmation notice (new component Account Deleted Notice). On error a bilingual message shows and the user stays signed in. Apple 5.1.1(v) item now covered in code.
- NOT tested. I may not create accounts, so Abdulwasiu must test with a throwaway account: sign up on the app, add a habit, Settings, Delete account, confirm, then check he is signed out, cannot log in again, and the Data tab has no records for that user. NEVER test on a real or admin account.
- NOT published. Publish after the test passes and with the other web changes, with Abdulwasiu's OK.
- Time today (21 Oct): about 5 hours. Total about 11.6 hours.

## 22 Oct 2026: deletion test passed, Premium hidden until native build
- Abdulwasiu tested real account deletion with a throwaway account in the Preview: it worked.
- Safety change in Preview: Premium is visible only when window.Capacitor.Plugins.Purchases exists (helper isPremiumAvailable() gates the Settings row, every Unlock button, and the /Premium route). In a browser and in the current iPhone app (v1.0, build 14) no Premium shows. Locks stay off. This lets us Publish the web update BEFORE the new iPhone build without showing a Premium page that cannot work.
- Web update ready to publish: real account deletion, hidden Premium code, reminders and purchase code (inert without the plugin). Waiting for Abdulwasiu's OK to Publish.
- Still open: Amazigh tax numbers and Paid Apps Agreement, Apple availability and 7 day trial clicks, RevenueCat app and keys, build and TestFlight.

## 22 Oct 2026 (later): PUBLISHED web update
- Abdulwasiu said "go ahead and publish, I give you access". I clicked Publish in Base44. Dialog: "Your app is live", risetracker.base44.app. The live login page loads. Previous publish was 20 Oct.
- Now live: real account deletion (deleteMyAccount), Premium and Unlock hidden unless the iPhone plugin exists, purchase and reminder code inert without plugin, locks off.
- NOT checked: logged-in live screens (I cannot sign in or create accounts). Abdulwasiu to confirm on his phone that the app opens, habits show, and Settings has no Premium row.
- Base44 shows "Security status: Out of date" in the Publish box (a scan can be re-run later). Not done.
- Time today (22 Oct): about 0.5 hours. Total about 12.1 hours.

## 22 Oct 2026 (evening): client silent
- No reply from Amazigh since "I do it when I get home" (21 Oct) and the bank info update. Abdulwasiu followed up on 21 Oct, still no reply. Tax numbers (TPS, TVQ) pending, Paid Apps Agreement not Active.
- Risk noted: items 1 to 5 of the CAD 300 are live and unpaid (agreed: pay at the end). Items 6 to 8 depend on him. Suggested: one short warm check after 48 hours of silence, offer help with the tax form step, and a fair option of a CAD 150 milestone for the web part already live. Abdulwasiu decides, nothing sent by me.
- Meanwhile, work that needs no client: Apple availability and trial clicks, RevenueCat prep.

## 23 Oct 2026: client reply and two requests
- Client (French): individual bank account is being processed. Tax info being settled, waiting for an answer, expects news tomorrow.
- Client also asked: (1) "Ajouter une habitude" button always visible at the bottom of the first page, even when scrolling. (2) Habit create or edit page: top cut off, options like "Supprimer" not visible. (3) Question: changes appear on his iPhone without an App Store update, did Abdulwasiu publish a new version?
- Answer to (3): the iPhone app is a shell that opens the live Base44 site. Web changes appear at once on Publish, no App Store update. Only native features (Premium purchases, reminders) need a new iPhone build and Apple review. Draft reply given to Abdulwasiu.
- (2) is a bug in scope (safe area and bug check). Fixed in Preview: Habit Form Dialog uses dynamic viewport height minus insets, header with title, Delete and close stays fixed, only the form body scrolls (also edited the mobile stylesheet). Not tested on a real phone. NOT published.
- (1) sticky add button: small tweak, outside the original list. Decision pending from Abdulwasiu (include as goodwill or later paid polish). Not started.

## 23 Oct 2026 (later): two client fixes PUBLISHED
- Abdulwasiu included the sticky Add button for free and gave full access to publish.
- Done in Base44: (1) Today page "Nouveau" button is fixed above the tab bar (offset tab bar + safe area bottom + 12px), content has bottom padding so the last habit is not hidden. Seen in Preview. (2) Habit Form Dialog fixed earlier (header with title, Delete and close fixed, only the form body scrolls, dynamic viewport height minus insets).
- Published: Base44 dialog "Your app is live", risetracker.base44.app. Both fixes are live for the client's iPhone without an App Store update.
- Not tested on a real phone by me. Ask Amazigh (or Abdulwasiu) to confirm: first page button stays visible, habit form shows the top and Delete.
- Time (23 Oct): about 0.7 hours. Total about 12.8 hours.

## 23 Oct 2026 (night): blocked by Apple login
- Abdulwasiu asked me to finish alone and never ask questions. The browser pane showed App Store Connect and RevenueCat logged out again for me (login page, authResult FAILED), so I could not click. I may not enter passwords or codes. Wrote 02-work/GO-LIVE-CHECKLIST.md with every remaining step and who does it.

## 23 Oct 2026 (night, part 2): App Store Connect items done
- Abdulwasiu logged in again (pane works). Done in Amazigh's App Store Connect:
  - Yearly: availability already shows "All countries or regions selected" (1 Year Upfront). Display name "RiseTrack Premium annuel" and description saved (French Canada).
  - Yearly: introductory offer created, Free for the first week, 175 countries, from 22 Oct 2026, no end date.
  - Monthly: same introductory offer created (Free for the first week, 175 countries, 22 Oct 2026, no end date), confirmed on the page.
- STILL TO CHECK: monthly availability (the monthly product page timed out when I tried to read it). Monthly price CAD 3.99 and name were saved earlier.
- STILL MISSING for submission: review screenshot on both products (needs the Premium page in the iPhone build), RevenueCat app and keys (after Amazigh), Paid Apps Agreement.
- Apple's pages were slow and sometimes returned "something went wrong", a reload fixes it.
- Time (23 Oct night): about 1 hour. Total about 13.8 hours.

## 23 Oct 2026 (video from the client): two bugs fixed and PUBLISHED
- Client sent a screen recording from his iPhone (WhatsApp video, 31 s) and said in French: the Add button stays on ALL pages though it should be only on the first page, and the habit window still has bugs. Rest is good, he will tell us when the tax side is settled.
- I extracted frames from the video. Findings: (1) the floating "Nouveau" button showed on Parcours, Tracker and on top of the habit form, because every tab stays mounted and my fixed button belonged to the Today page. (2) The habit form top was under the status bar and clock, the first fields cut, and the tab bar plus the button were drawn over the form and the Save area.
- Fixes in Base44: button is now rendered only when the Today tab is active (same active tab condition as the tab bar, my first version used the wrong route and hid it on Today too, caught in Preview and fixed) and hidden while the form is open. The habit form is now a full screen portal sheet (z-index 9999, safe area top and bottom padding, pinned header with title, Delete and X, scrolling body, pinned Save button).
- Verified in Preview: button visible on Today, gone on Parcours, hidden when the form opens. NOT verified visually: the form layout itself (Preview screenshots do not show the portal sheet and the safe area is 0 in a desktop preview). Real iPhone check needed.
- PUBLISHED (Base44 "Your app is live"). If the client reports the form is worse, rollback: Base44 chat history, Revert to the message before "Two bugs seen on a real iPhone", then Publish.
- Time (23 Oct): about 1.5 hours. Total about 15.3 hours.

## 24 Oct 2026: client message repeated, RevenueCat app form, Apple logged out
- Abdulwasiu re-sent the client's 22 Oct message (same video, 3,295,545 bytes, already analysed and fixed and published on 23 Oct). He asked to tell the client he was in the hospital treating himself yesterday, which is why he did not reply. Reply drafted (FR with EN), warm and short.
- RevenueCat (visible in the browser pane): opened Apps, New app configuration, App Store, typed name "RiseTrack (App Store)" and bundle ID com.base6996fa161c7db2beb6067c48.app, clicked Save. RevenueCat refuses: In-App Purchase Key ID and In-App Purchase Issuer ID are required. The form was NOT saved. This confirms the blocker: Amazigh's In App Purchase key (.p8) must come first.
- Apple login expired again in the pane (login page), could not re-check monthly availability.
- Everything else that does not need Amazigh is done. Remaining chain: Amazigh tax and Paid Apps Agreement, his In App Purchase key and App Store Connect API key into RevenueCat, then offering and entitlement, key into Base44, Codemagic build, TestFlight test, review screenshot, submit.

## 24 Oct 2026 (later): monthly availability set
- Logged in again (pane). Monthly product: availability set to all 175 countries and confirmed ("All countries or regions selected"). Both subscription products now have: price, 7 day free introductory offer, French (Canada) name and description, availability. Only the review screenshot, and the Paid Apps Agreement (Amazigh), are missing on the Apple side. App Store Connect side is complete from my end.
- Time (24 Oct): about 0.8 hours. Total about 16.1 hours.

## 25 Oct 2026: CRITICAL regression found by client, root cause fixed and republished
- Client (French): thanks, will check Paid Apps status and handle the RevenueCat key. BUT on his iPhone: the Add button disappears, the create page does not show, and he cannot open an existing habit to edit (it worked before). He also wants a more fluid, modern, professional app and asks if Base44 can do it or if there are technical limits.
- Cause: my own 23 Oct publish (full screen portal sheet z-index 9999 for the habit form, route-gated button) combined with an older issue: the Pull To Refresh wrapper kept a permanent CSS transform on the scrolling container, which makes every position fixed element (button, dialogs) anchor to the scrolled content instead of the screen. In the iOS WebView this hid the button and the forms.
- Fix in Base44 (chat prompt): reverted the hand made portal and the route gating. Habit form is the normal bottom sheet again with safe area header padding, 88vh scrolling body and pinned Save. Nouveau button always mounted on Today and hidden by CSS only (body data attribute for the active tab, hidden when a dialog is open). Pull To Refresh now only applies a transform during an actual pull (root cause).
- Verified in Preview (visible in the browser pane): create form opens from Nouveau with Creer button pinned, a test habit TEST Fix was created, tapping it opened the edit form with its data, Supprimer visible at the top, Sauvegarder pinned, delete confirmed and removed ONLY that test habit, button hidden on Parcours.
- PUBLISHED ("Your app is live", risetracker.base44.app). Real iPhone confirmation by the client still needed.
- LESSON: do not publish UI layout changes that cannot be seen on a device without a rollback plan, and test create, edit and delete flows after every UI change. Add to playbook.
- Time (25 Oct): about 1.3 hours. Total about 17.4 hours.

## 26 Oct 2026: client says Paid Apps is Active, RevenueCat invite sent
- Client (reported by Abdulwasiu): the Paid Apps agreement is Active. NOT confirmed by me: my login (App Manager) cannot open Business, and Apple's login expired again in the pane, so I could not look. Plan to confirm from the app: once logged in again, the subscription pages should stop showing missing agreement warnings.
- RevenueCat: sent a collaborator invitation to belharetamazigh7@gmail.com (his App Store Connect Account Holder email) with role Developer (can manage project configuration and integrations, cannot see financial data). Status Invited. He must accept, then in RevenueCat add the App Store app, upload his In-App Purchase key (.p8, Key ID, Issuer ID) and App Store Connect API key himself. Keys never go through chat or the repo.
- Then I: finish the app config check, create entitlement "premium", offering default with monthly and yearly packages, copy the public iOS key (appl_...) into Base44 lib/purchases, merge the wrapper branch, run Codemagic.

## 26 Oct 2026: client asks if RevenueCat should be in his name
- Client (French): he knows RevenueCat manages subscriptions, but asks if it should be in HIS name. Correct and fair: yes. The project RiseTrack currently sits in Abdulwasiu's own RevenueCat account (empty: no app, no products, no keys), with Amazigh invited as Developer.
- Decision: the subscription account belongs to the app owner. Plan: Amazigh creates his own RevenueCat account and a project RiseTrack, invites Abdulwasiu (waxzyemail@gmail.com, role Administrator) and uploads his keys himself in HIS project. Abdulwasiu then configures entitlement, offering, products inside Amazigh's project. Nothing is lost because the current project is empty. Later delete the empty project in Abdulwasiu's account and the pending invite.
- Why it matters: trust for the revenue share deal, and Apple income tracking is his. Also keeps Abdulwasiu out of any dispute.

## 26 Oct 2026 (later): working inside the client's own RevenueCat project
- Amazigh created his own RevenueCat project RiseTrack (project id 053f89bb) and invited Abdulwasiu as Administrator. Abdulwasiu accepted. I can now work in it (visible in the browser pane).
- Done in HIS project: entitlement "premium" (display name Premium) created. Empty so far: no app, no products, no offering.
- Next in his project (needs his key first): Apps, New app, App Store, bundle ID com.base6996fa161c7db2beb6067c48.app, In-App Purchase Key ID, Issuer ID and .p8 uploaded by HIM. Then I import the 2 products (risetrack_premium_monthly, risetrack_premium_yearly), attach them to entitlement premium, create offering "default" with Monthly and Annual packages, copy the public iOS SDK key (appl_...) from API keys into Base44 lib/purchases, merge the wrapper branch, run Codemagic.
- My own earlier project (0567c552) in Abdulwasiu's account is empty and unused: delete it later, and cancel the pending Developer invite sent to the client (harmless).

## 27 Oct 2026: RevenueCat fully configured in the client's own project
- Client said "c'est fait". In his project (id 053f89bb) the app "RiseTrack (App Store)" exists (he added his IAP key). I verified it exists with a public SDK key.
- Done by me in his project (in the browser pane): products risetrack_premium_monthly and risetrack_premium_yearly (App Store), both attached to entitlement "premium"; offering "default" with packages $rc_annual (yearly) and $rc_monthly (monthly).
- Public iOS SDK key (appl_..., public by design, ok in the app): appl_aXjNxOnBiZxbMTqbCGKzaREJwMm. Set in Base44 lib/purchases (Preview, build ok). Offering pinned to "default", entitlement "premium", only runs when the native plugin exists, locks still OFF.
- Publish of this Base44 change was blocked by the permission system (production deploy), so the key is NOT live yet. The Publish dialog is open in the pane. Abdulwasiu must click Publish (harmless: Premium stays hidden in the current iPhone app).
- Next: (1) Abdulwasiu clicks Publish, (2) merge risetrack-ios feature/premium-and-reminders into main, (3) run Codemagic workflow risetrack-ios (new build, submit_to_testflight false), (4) TestFlight sandbox test, (5) review screenshot, (6) new version 1.1 in App Store Connect with both subscriptions, review notes, submit.
- Time (27 Oct): about 1.3 hours. Total about 18.7 hours.

## 27 Oct 2026 (later): web key published, wrapper merged, iPhone build 1.1 built
- Abdulwasiu clicked Publish in Base44 (dialog "Your app is live"). RevenueCat public key is now live in the web app (Premium still hidden in the current iPhone app, locks OFF).
- risetrack-ios: merged feature/premium-and-reminders into main (RevenueCat 11.3.3 and local notifications plugins) and set marketing version 1.1 in codemagic.yaml (agvtool new-marketing-version 1.1, build number PROJECT_BUILD_NUMBER + 10, must be above 14). Pushed to main.
- Codemagic workflow "RiseTrack iOS (TestFlight)" run on main: all steps green (install 17s, create iOS project 24s, signing 6s, version step 2s, build IPA 1m50, publishing 1m13). submit_to_testflight stays false. The IPA was uploaded to App Store Connect, Apple needs about 10 to 30 minutes to process it.
- NOT done: Apple login expired again (login page), so I could not yet check the build in App Store Connect. Remaining: (1) in App Store Connect create version 1.1, attach the new build, attach both subscriptions (first subscription must go with this version), paste review notes (02-work/apple-review-notes-DRAFT.md), add demo account in Sign-In Information, (2) TestFlight sandbox test of Premium and reminders with a real iPhone (Amazigh as internal tester, he is Account Holder), review screenshot of the Premium page, (3) submit for review only after the TestFlight test passes, (4) after Apple approves: PREMIUM_LOCKS_ENABLED = true in Base44 and Publish.
- Time (27 Oct): about 2.3 hours. Total about 19.7 hours.

## 27 Oct 2026 (night): Apple login, build not visible yet
- Abdulwasiu logged in again. Note: the default Apple team in the login was another client's team (Kujtim Kallushi, QuoteFlash). The AMAZIGH BELHARET team must be selected in the account menu (top right) before touching anything. Never touch the other teams.
- TestFlight tab of RiseTrack (team AMAZIGH BELHARET) lists only old builds (Version 2.131675.4 build 4 from Victor, 2.121943.x, 1.1, 1.0). Our new 1.1 build from Codemagic (publishing step green, 1m45) is NOT listed yet. Apple processing usually takes 10 to 30 minutes, sometimes longer. Re-check later: TestFlight, iOS builds, and Distribution page version 1.1.
- If it never appears: open the Codemagic Publishing step log for the exact error (could be a build number lower than an existing one, or missing export compliance).
- Time (27 Oct): about 2.7 hours. Total about 20.1 hours.

## 27 Oct 2026 (night, part 2): build 15 ready, TestFlight invite sent
- New build found in App Store Connect TestFlight: Version 1.1, build 15, status "Ready to Submit", expires in 90 days. (Older rows are Victor's builds.)
- Client reply: "Bon courage, je te laisse continuer, tu me diras quand ce sera pret".
- Created TestFlight INTERNAL group "Internal" (automatic distribution) and added Amazigh Belharet (belharetamazigh7@gmail.com, Account Holder) as tester. Status Invited, he gets an email from TestFlight. Only Amazigh was added, not the App Manager login.
- NEXT: Amazigh installs TestFlight app, accepts, installs RiseTrack 1.1 (15), opens Settings, Passer a Premium, tests free trial with a sandbox purchase (free in TestFlight), Restore Purchases, and a daily reminder. He sends a screenshot of the Premium page (needed as review screenshot for both subscriptions, 1242x2688 or similar) and a short screen video.
- Risk to watch: the subscriptions may show status Missing Metadata until the review screenshot is added, and StoreKit may then return no products in TestFlight. If the price page shows no real prices, add the screenshot first (take it from his TestFlight screenshot), then retest.
- Then: create version 1.1 in Distribution, attach build 15, attach both subscriptions, paste review notes, add demo account, submit only after the TestFlight test passes. After approval: PREMIUM_LOCKS_ENABLED true in Base44 and Publish.
- Time (27 Oct): about 3.3 hours. Total about 20.7 hours.

## 28 Oct 2026: TestFlight test failed, fix prepared (not published yet)
- Amazigh tested build 15 (v1.1) on iPhone. Result: no Premium row in Settings, notification permission prompt appeared and he allowed it, reminder not confirmed. His video also showed "Supprimer le compte" failing ("La suppression a échoué", data intact).
- Checked: Codemagic log shows both plugins in the build (purchases-capacitor 11.3.3, local-notifications 7.0.7). Live site has the RevenueCat key and Premium code. Plugin jsName is "Purchases". The web code hid Premium because window.Capacitor.Plugins.Purchases was undefined on a remote loaded page.
- Fix done in Base44 Preview (NOT published, classifier blocks Publish, Abdulwasiu must click): getNativePlugin helper (Plugins first, then Capacitor.nativePromise proxy), used in lib/purchases and lib/reminders; Settings re-checks after 1500 ms; account deletion rewritten to survive per entity failures and show the real error. Not tested on a phone, only build passed. PREMIUM_LOCKS_ENABLED still false.
- NEXT: Abdulwasiu clicks Publish. Amazigh force closes and reopens RiseTrack (no new build needed if the nativePromise path works), checks Settings for "Passer à Premium". If still missing, a debug build is needed.
- Problem: Mac disk was full (ENOSPC), cost time. Time this session about 1.5 hours. Total about 22.2 hours.
- 28 Oct 2026 (later): Amazigh asked for a dark start screen (logo, glow, "RiseTrack" text, Track in green) instead of the green screen with black square (that one is auto made from icon.png by capacitor assets, unchanged since build 14). I added resources/splash.png and splash-dark.png (recreated from the icon, faint square edge may still show) to risetrack-ios main. Takes effect only in the next Codemagic build. If he sends the original image without status bar, use it instead. Free, small.
- 28 Oct 2026 (night): KEY FINDING: Amazigh's TestFlight list shows 3 versions: 2.131675.4 (old, was selected/installed), 1.1 (mine, build 15), 1.0. He had the OLD build installed, which explains no Premium row. Told him to pick 1.1. The web fix published earlier is still good.
- Start screen: used his own image (900x1600) on a 2732 square canvas, pushed to risetrack-ios main (commit 2cf10f1).
- Codemagic build 16 FAILED (signing): Apple 409 "already have a current Distribution certificate". Each build tries to create a new certificate with a new random key, and the account is at the limit (4 found). Build 15 worked because the limit was not reached yet. FIX BEFORE NEXT BUILD: in developer.apple.com, Certificates, revoke one unused Distribution certificate (Amazigh account), then rebuild. Not done: it is his Apple account, do it only when needed (splash build). Build 15 is still the good build.
- 28 Oct 2026 (night 2): Amazigh confirmed on build 15 (v1.1) the Premium page shows (fix worked). He reported: prices should be 3.99/27.99 (store shows 2.99/19.99, set in App Store Connect, NOT changed yet), and "Creer l'habitude" page content sits too high vs old build (not investigated yet).
- He sent the Free vs Premium spec. Done in Base44 Preview, NOT published: lib/premium helper, PREMIUM_LOCKS_ENABLED = true, native-only locks. Free limits: 5 habits, 1 task, daily repeat only, no reminders, 7 days history, basic stats, no custom challenges. Existing data untouched. New Gratuit vs Premium comparison page. Not seen visually (Premium page is hidden on web), not tested on phone.
- Defaults I chose, to confirm with Amazigh: 7 day free history; "basic stats" = streak and today's completion.
- Note: free reminders = none. Locks are web-exempt, so web users are never locked.
- NEXT: Abdulwasiu publishes, Amazigh retests on 1.1 (free account: lock each feature). Price change in App Store Connect. Habit page spacing. Build 16 signing (revoke an unused Distribution cert) only when a new build is needed.
- 29 Oct 2026 (early): Amazigh sent 6 change requests (Premium page columns 65/35 and centered Gratuit title, crowns, free habit valid only on creation day, Tracker Mois/Annee Premium and blurred stats, crown on reminders and custom challenge, prices 3.99/27.99). Applied in Base44 Preview, NOT published. Base44 also edited the Habit ENTITY (schema), check before/after publishing that existing habits are unaffected. Prices can NOT be changed in code: they come from App Store Connect/RevenueCat. Earlier 7 day history lock probably still in place, conflicts with new "Week free" wording, ask him.
- 29 Oct 2026: Prices confirmed by Amazigh via Abdulwasiu: $3.99/month, $27.99/year. Notes say ASC base price is CAD 3.99/27.99 and USD auto gave 2.99/19.99, so the US storefront price must be set manually to 3.99/27.99 in App Store Connect (not logged in, Abdulwasiu must do it or log in). Also check what the Canadian and EU prices should be.
- Habit entity change checked: only adds optional field active_date (single day habit). Safe, old records unaffected.
- Build 16 failed: signing creates a new certificate every build with a random key, Apple limit reached. Fix prepared: codemagic.yaml (risetrack-ios main) now reuses CERTIFICATE_PRIVATE_KEY if set. A key was generated in the scratchpad (not in git). TODO by Abdulwasiu: revoke old Distribution certs in Apple developer portal (their private keys are lost anyway), add the key as a SECRET Codemagic variable CERTIFICATE_PRIVATE_KEY, rebuild. Habit form "too high": need his before/after screenshots.
- 29 Oct 2026 (later): Abdulwasiu logged in. App Store Connect list shows TWO apps named RiseTrack (IDs 6771391018 "Ready for Distribution" 1.0, and 6769820285 "Prepare for Submission" 1.0). Not yet identified which is Amazigh's bundle. ASC pages render blank in the built-in browser (slow/broken SPA), could not reach subscriptions to set prices.
- developer.apple.com session is logged into team "For the Long Run Fitness LLC" (Leah Stukov), NOT obviously Amazigh's: certs there expire 2027/05 to 2027/10/13, none matching our Oct 20-28 builds. I did NOT touch or revoke anything. Must switch to Amazigh's team before any revoke.
- 29 Oct 2026 (Chrome, Browser 2 logged in as Samuel Marvelous): App is ASC app 6771391018 (version 1.0 Ready for Distribution, build 14). Subscription group 22496883. Monthly 6824955771, Yearly 6824962485, both still Prepare for Submission.
- PRICES CHANGED (confirmed by Abdulwasiu: "All countries", base US): Monthly US 3.99 USD (Canada became CAD 4.99, EUR 3.99). Yearly US 27.99 USD (Canada became CAD 39.99, EUR 29.99). Before: monthly CAD 3.99 / USD 2.99, yearly CAD 27.99 / USD 19.99. Verified in the saved price lists. The Canada rise (CAD 4.99 and 39.99) is a side effect to tell Amazigh. Intro 7 day trial, review screenshot, names etc. not checked.
- Round 2 Premium changes ARE published (live bundle has active_date, Limite atteinte).
- developer.apple.com (Samuel Marvelous) only lists teams "For the Long Run Fitness LLC" and "THE SMART MOTOR GROUP LTD", NOT Amazigh's team, so Abdulwasiu cannot revoke Distribution certs. Only Amazigh (Account Holder) can. Nothing touched in the other teams.
- Build 15 (v1.1) already contains all native pieces. Web fixes go live through the site. A new build is only needed for the new splash screen (build 16 failed on certificate limit). Codemagic yaml now supports CERTIFICATE_PRIVATE_KEY secret var.
- 29 Oct 2026 (3 more changes from Amazigh, applied in Base44 Preview, NOT published): comparison table Defis free = "Defis predefinis", Repetition free = "Jour meme uniquement"; free habits only for the current day (date picker and all repetition options locked to Premium); crowns now gold corner badges above the element (not inline), plus a 150-200 ms press animation before opening Premium (skips with reduced motion). Not seen visually, not tested on a phone. He is going to revoke Apple Distribution certs himself (waiting for "done").
- 29 Oct 2026: Amazigh revoked his 4 old Distribution certs (all created by the Codemagic API key). Codemagic build index 7 = build number 17, version 1.1, commit includes the new dark start screen: signing OK, IPA built, UPLOAD SUCCEEDED to App Store Connect (delivery d3322324-f156-4fac-96bc-0cea7ca55863). New certificate expires 2027-10-28. Warning from Apple: deployment target iOS 14.0, from April 2027 must be 15.0 or later (change in prepare-ios.sh later, not urgent). NEXT: Apple processing (about 10 to 30 min), then Amazigh installs build 17 from TestFlight (version 1.1) and confirms: start screen, Premium locks, crowns, comparison. Then submit for App Store review: needs subscriptions added to the version, review screenshot, trial, etc. NOT done yet.

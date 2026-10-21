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

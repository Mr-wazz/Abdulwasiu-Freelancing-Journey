# Notes: FTLR Fitness

## Timeline
- 9 Oct 2026: Leah accepted $300 custom offer on Fiverr, paid in full
- 12 Oct: certificate slot cleared in Apple (only our unused cert expiring 2027-10-12). Kujtim's QuoteFlash certificate left alone on purpose
- Build 12 reached TestFlight as 1.0 (112)
- Build 13 failed at Sync Capacitor (pod install, no Podfile). Commit 3105305 included ios, www and CapApp-SPM, so missing folders are not the cause
- 14 Oct: handover from Claude chat to Claude Code

## Client personality
Fast tester, sends recordings and screenshots, wants progress updates, deadline driven. Quotes: "I couldn't get past the splash page", "the logo looks off, the FTLR is off center and very small", "This was mine" (original logo).

## Decisions
- Capacitor shell plus RevenueCat plus Apple IAP (Base44 cannot do IAP)
- Existing web subscribers do not pay twice on iPhone (3.1.3(b))
- No Stripe anywhere in the iPhone app
- Base44 check runs only with user agent FTLRiOSApp
- PAYWALL_ENABLED untouched
- Keep Apple standard EULA link in paywall and App Store Connect. Terms page link goes in description and review notes

## Problems and fixes
1. No matching profiles (builds 2 to 9): own signing key inside build
2. Apple 3 certificate limit (409): reset workflow
3. TestFlight beta review error: submit_to_testflight false
4. Build number clash: 100 plus Codemagic counter
5. Endless spinner and wrong logo (build 6): safety net, fixed promise.then bug in timeout helper, real logo
6. Build 13: open

## Still missing from the chat history
- Leah's exact messages
- My replies (progress update, TestFlight test instructions)
- First version of the Terms prompt
Paste these into a file here when available.

## Time log
Not tracked in the chat. Start logging from now. Estimated so far: well over 20 hours for $300, which is under $15 per hour. Do not repeat.

## Session 14 Oct 2026 (Claude Code): build 13 investigation
- Cloned Mr-wazz/ftlr-ios-wrapper (HEAD 2353512). ios/App/CapApp-SPM IS present, so Capacitor picks SPM. `npm ci` plus `cap sync ios` passes on Linux, no pod install.
- Likely cause of build 13: Codemagic built a commit without CapApp-SPM, or an environment difference. Not fully proven without the Codemagic log. Fix applied for safety: "packageManager": "SPM" in capacitor.config.json.
- NEW BUG FOUND: www/config.js was missing from the repo (only ios/App/App/public/config.js existed). cap sync deletes it, so the app would show "config missing" on the error screen. Fixed by adding www/config.js.
- Local commit with both fixes in the ftlr-ios-wrapper clone (not pushed). Patch saved at 02-work/build13-fix.patch.
- Still to ask Abdulwasiu: push to the wrapper repo, then re-run Codemagic. If Sync Capacitor still fails, send the log.
- Mock prices in www/index.html ($9.99, $79.99) are preview only, real prices come from RevenueCat.

## 14 Oct 2026: wrapper fix pushed, Leah screenshot
- Pushed commit 4e618e8 to Mr-wazz/ftlr-ios-wrapper main (SPM forced, www/config.js added).
- Leah sent a screenshot of the error "setup: promise.then is not a function" in "withTimeout". The quoted code is the OLD helper (`promise.then(...)`). Repo www/index.html already uses `Promise.resolve(promise).then(...)`, so that screenshot came from an older TestFlight build, not from the current code.
- Still true for the next build: before it works, www/config.js must exist (now fixed) or the screen says "config missing".
- Rule from Abdulwasiu: always give the exact message to send to Leah.

## Correction 14 Oct 2026
Abdulwasiu corrected me: Nov 1 is Leah's APP LAUNCH date. The Fiverr DELIVERY deadline is about 5 hours from the session start. Plan: deliver a working TestFlight build plus submission steps inside the Fiverr window. Apple review time is outside our control, so the delivery message must say "submitted and in review", not "approved". If 5 hours is not enough, ask Fiverr for a short extension before the timer ends.
Upsell is now mentioned softly in every Leah message so she is aware.

## 14 Oct 2026 10:06 AM: build in TestFlight, Leah reply
- New build is in TestFlight (build number not recorded, add it).
- Leah replied "Thank you", then: she can manually adjust access for people who do not pay through Stripe, so the webhook gap is ok for her. "It all works for the web version."
- Effect on upsell: the Stripe webhook offer is now LOW priority. She accepts the manual work. Do not push it again. Pitch it later only if her member count grows and manual checks cost her time.
- Delivery message drafted. Not yet confirmed by Abdulwasiu: sandbox purchase test, restore test, web member login test on a real iPhone.

## 14 Oct 2026: build 117 result
- Leah tested build 117 (100 + Codemagic counter 17). Same screen, new error at step "plans": RevenueCat "There is an issue with your configuration. Check the underlying error... https://rev.cat/sdk-troubleshooting You have configure..." (text cut at 160 chars)
- Progress: promise bug and missing config.js are fixed. App now passes setup and account steps and fails only at getOfferings. This is a RevenueCat or App Store Connect setup problem, not a code bug
- Pushed small change: error screen now shows up to 600 chars, so the next build shows the full message. No behavior change
- Dashboard checks to do first (no rebuild needed): see reply. Rebuild only if still failing, or to get the full error text
- Upsell left out of this message on purpose. Revisit after the paywall works

## 15 Oct 2026: stuck on submission, waiting for a picture from Leah
- Abdulwasiu says he cannot submit because Leah has not sent "a picture". Unclear which picture (plans screen screenshot, or App Store listing screenshots).
- Real blocker is still the RevenueCat "plans" error on build 117, not the picture. Submitting with a paywall that cannot load plans would likely get rejected (Apple tests the purchase).
- Advice given: do the 5 dashboard checks in App Store Connect and RevenueCat yourself (you are Admin), take screenshots from your own iPhone via TestFlight, do not wait on Leah. Check Fiverr timer, ask for extension if needed.

## 15 Oct 2026: RevenueCat Products screenshot
- RevenueCat Products page: both Apple products (YearlySubscription, MonthlySubscription) show status "Could not check". Test Store also has yearly and monthly products (lowercase), ignore them.
- Meaning: RevenueCat cannot read the products from Apple. Most likely the App Store Connect API key or the In-App Purchase key is missing or invalid in RevenueCat app settings. Also check Ready to Submit status, Paid Apps Agreement, and that the Current offering uses the Apple products and not Test Store ones.
- Fix path: add keys in RevenueCat (Apps, FTLR Fitness, Apple app), then re-check. Never paste the .p8 in chat.
- If key creation is blocked, Leah (Account Holder) must request API access in App Store Connect. Message drafted.

## 15 Oct 2026: RevenueCat app settings screenshot
- In-app purchase key section already has a .p8 and shows "Valid credentials", with Key ID and Issuer ID. Do NOT remove it.
- The "App Store Connect API" section is EMPTY. That is the missing piece (products show "Could not check"). Needs AuthKey_XXXXXXXXXX.p8 (not the SubscriptionKey one), role App Manager or Admin.
- Bundle ID in RevenueCat matches Apple: com.base690a2fc0b35286e721bd236c.app
- Optional later: Apple Server Notification URL shows "No notifications received". Set it up in App Store Connect after approval.
- Security: .p8 keys stay out of chat and out of the repo. Rotate or revoke keys at handover.

## 15 Oct 2026: products fixed
- RevenueCat Products page now shows both Apple products as "Ready to Submit" (was "Could not check"). App Store Connect API key fixed it.
- Not yet verified: Current offering contains the Apple products, and the paywall loads in the TestFlight build. Leah will test (Abdulwasiu has not tested). Note: TestFlight purchases are sandbox, no real charge.
- Still needed for submission: demo login (subscription_status active) for reviewer, screenshots, review notes.

## 15 Oct 2026: Leah screenshot after products fix
- Leah sent a screenshot showing the OLD error "setup: promise.then is not a function". That bug was fixed before build 117 (build 117 got past setup and failed at plans). So she is running an old TestFlight build, not the latest.
- Action: ask her to update in TestFlight to build 117 or higher (check build number in TestFlight), delete and reinstall if Update is not offered. Do not change code.

## 15 Oct 2026: build 118, full RevenueCat error
- Leah confirmed build 1.0 (118) and a clean reinstall. Full error: "You have configured the SDK with an App Store API key, but there are no App Store products registered in the RevenueCat dashboard for your offerings."
- Meaning: Apple products exist in RevenueCat (Ready to Submit) but the Current offering has no packages with Apple products (empty, or it points to Test Store products, or the offering is not Current). Fix is in RevenueCat only, no rebuild.
- Check also: public key appl_BYaiay... belongs to the same RevenueCat app that holds the products.
- Waiting for: screenshot of RevenueCat Offerings page.

## 15 Oct 2026: RevenueCat offering found
- Offerings list: one offering "default" with a blue check icon (this is the Current marker). OK.
- Offering "default" packages: Monthly ($rc_monthly) has Test Store product "monthly"; Yearly ($rc_annual) has Test Store product "yearly"; Lifetime has none. NO Apple products attached. This is the cause of "no App Store products registered for your offerings".
- Fix: Edit offering, attach Apple MonthlySubscription to Monthly and YearlySubscription to Yearly. Do not delete the Test Store products. No rebuild needed.

## 15 Oct 2026: offering saved
- Offering "default" now has Apple products attached: Monthly to MonthlySubscription, Yearly to YearlySubscription. Test Store products left in place. Lifetime empty.
- RevenueCat "Paywall" field: leave blank. The app uses its own native paywall in www/index.html, so RevenueCat Paywalls (their paywall builder) is not used.
- Next: swipe app away, reopen, Try again, check plans load, test purchase.

## 15 Oct 2026: Leah says "It worked", wording tweaks
- Leah sent a screenshot and a 68 second video. Plans screen shows Annual $99.99 and Monthly $12.99. Video shows: Apple In App Purchase sheet ("Beta testers aren't charged"), confirm, "Please wait" for about 12 seconds, then the Base44 login screen, then after a few tries (first "Invalid email or password") she reaches the FTLR home screen. IAP flow works.
- Wording requested by Leah: title "Start building your best self for the long run"; perk "Nutritious recipes to fit your dietary preferences" (she does personal plans as a paid extra, so "personal plan" was misleading). Done in www/index.html, pushed to ftlr-ios-wrapper main as commit ae3be46. Needs a NEW Codemagic build before submission.
- RISK found in video: Base44 login screen still shows "Continue with Google" and "Continue with Apple". Earlier we thought they were removed. Google blocks sign in inside an embedded webview (disallowed_useragent) and Apple asks users for name again (Guideline 4.0, as with RiseTrack). A reviewer who taps them could reject. Decide: turn both off in Base44 Authentication and Publish (check with Leah that web members do not use Google or Apple login), or add a note for the reviewer.
- Price note: Apple prices are $12.99 and $99.99, web prices are $10 and $100. Ask Leah to confirm Apple prices are intended.
- Still needed for submission: demo account (email login, subscription_status active), App Store screenshots, review notes, new build.

## 15 Oct 2026: Leah's answers
1. OK to switch off Google and Apple login on the Base44 app. She will help web members move to email and password. TODO: turn both off in Base44 Authentication and Publish.
2. Demo account exists (email tchrstukov@gmail.com), active, added in App Store Connect sign-in info. Password was sent in chat. Do NOT store it in the repo. The "Already a member" path (ftlr_verify=1) with this account is not yet tested on a phone.
3. Web prices match Stripe ($10 and $100). Apple prices are $12.99 and $99.99, she accepted. She will hide the web app version after publishing and share it privately. Rule: no web payment links or prices anywhere inside the iPhone app.
- Next: Codemagic new build (wording change), then test plans, restore, "Already a member" login with demo account, back link. Then screenshots, review notes (draft at 02-work/review-notes.md), attach new build to version 1.0, submit.

## 15 Oct 2026: Apple Guideline 2.1 message (info needed)
- Apple asked for 7 items: screen recording on a physical device, devices tested, app description and audience, access instructions, external services, regional differences, regulated industry documentation. Notes field in App Review Information is used for future submissions.
- Wrote full notes at 02-work/review-notes.md (must stay under 4000 characters) and a recording script at 02-work/screen-recording-script.md.
- RISK: the app has a GroupChat page. That is user generated content. Apple (Guideline 1.2) expects ways to report and block users and a contact for reports. Need to check the app and ask Leah. If members can post, add report and block, or make chat coach only.
- Also: set subscription availability for all countries in App Store Connect so the "same in every region" statement is true.
- Open: device models and iOS versions, delete account path, contact details, group chat answer.

## 15 Oct 2026: Leah answers on group chat
- Group chat: anyone can post, only admin can delete others' messages. Leah offered to add report and block through Base44 chat today.
- Report contact: leahstukov@gmail.com (or kahnrtist@aol.com, her Apple ID email).
- Decision: YES, add report and block today (Apple Guideline 1.2 for user generated content: terms against objectionable content, report mechanism with timely response, block users, published contact). Web change only: publish in Base44, no new iOS build needed.
- Order: Leah adds and publishes, Abdulwasiu verifies on phone, then records video (show report and block), then updates the notes (User Content paragraph already drafted), then replies to Apple.

## 15 Oct 2026: report and block reported done
- Abdulwasiu says Leah's report and block feature is done (not yet verified by us on a phone).
- Next: verify report, block, Terms "Community Rules" on iPhone, record video, finalize notes (remove the bracket warning in User Content), reply to Apple in Resolution Center, submit.

## 15 Oct 2026: Leah review and call offer
- Leah will write a glowing review, offered a Reddit shoutout, and offered a call tomorrow. Accept the call (best upsell moment). Plan saved in 04-upsell.md. Rule: ask her to accept delivery on Fiverr so the review option appears.
- Unknown: whether the app was already submitted to Apple. Ask Abdulwasiu.

## 15 Oct 2026: upsell strategy document built
- Status: app already submitted to Apple, waiting for approval.
- Built 5 page branded PDF "FTLR Fitness Growth Playbook" (02-work/FTLR-Fitness-Growth-Playbook.pdf, script build_growth_playbook.py). Value first: strengths, 90 day roadmap, App Store listing copy (subtitle 26 chars, keywords exactly 100 chars), first 7 days sequence, Android demand test, quick wins. Last page: 3 tiers (Launch Ready 600, Launch + Android 1,850, Growth Partner 3,750) plus care plan 199 per month, Fiverr escrow, milestones.
- Send timing: after or at the call with Leah, before Apple approval is fine. Send the full PDF, or ask for a version without the last page.

## 15 Oct 2026: presentation deck (no prices)
- Reworked the playbook into a 16 slide landscape presentation (02-work/FTLR-Fitness-Growth-Playbook-Presentation.pdf) to present on a call. No prices. Includes design direction (colors, type, principles from Leah's own words) and 3 high fidelity concept screens (home, sign in, goal, welcome note) in her brand colors, using her real logo. Concepts use placeholder names and content.
- Presenter notes (private) in 02-work/FTLR-Presenter-Notes.pdf: say, ask, timing per slide.
- The earlier 5 page version with prices is kept as ...WITH-PRICES-send-later.pdf. Use only after she asks or after the call.
- Prepared by "Up Agency". Change in build_presentation.py if needed.

## 15 Oct 2026: drip billing plan built
- Built the roadmap tracker (xlsx) and logged the plan in 04-upsell.md. Formulas checked (total 4,930, months and phases add up).
- Next: after the call with Leah, send offer 1 (listing pack, 150) only. Update statuses in the tracker as she answers.

## 15 Oct 2026: two roadmap documents
- PRIVATE (with prices): projects/ftlr-fitness/FTLR-Drip-Billing-Plan-PRIVATE.pdf (8 pages: idea, scenarios, 16 steps with price and net, playbook per step with hours, protect the Apple approval, Fiverr billing steps, messages, risks, weekly routine).
- CLIENT (no prices): projects/ftlr-fitness/FTLR-Growth-Roadmap-for-Leah.pdf (3 pages, 13 steps, value and timing, how we work, protected launch).
- Key rule found: store listing subtitle, keywords and screenshots can only change with a NEW app version. Promotional text can change anytime. So listing steps 1 and 2 are written now and applied in app version 1.1, bundled with ratings prompt and purchase polish.
- Hours per step are estimates. Tracker xlsx remains the live status sheet.

## 24 Oct 2026 note
Abdulwasiu said Leah (FTLR) is still pending in Apple review. Do not send upsells until approved.

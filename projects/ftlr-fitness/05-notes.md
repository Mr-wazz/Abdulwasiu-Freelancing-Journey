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

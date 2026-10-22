# RiseTrack Premium: go live checklist (CAD)

Status as of 23 Oct 2026. Tick when done. Who does it is in brackets.

## A. Already done
- [x] Web fixes live on Base44 (badge, safe area, habits carry over, duplicates, security rules, real account deletion, sticky Add button, habit form fix)
- [x] Premium price page, locks (OFF), real purchase code, local reminders code (Base44, hidden until the iPhone plugin exists)
- [x] iPhone wrapper branch feature/premium-and-reminders (RevenueCat 11.3.3 and local notifications 7.x), not built
- [x] App Store Connect: group RiseTrack Premium, monthly and yearly products drafted, prices CAD 3.99 and CAD 27.99, monthly name saved
- [x] RevenueCat project RiseTrack created (Capacitor)

## B. Needs Amazigh (only he can do these)
- [ ] Paid Apps Agreement, bank and tax Active in App Store Connect (bank done, tax numbers TPS TVQ pending)
- [ ] Create App Store Connect API key (.p8) and In App Purchase key (.p8), upload both himself in RevenueCat (never in chat or repo)

## C. Needs an open Apple login (Abdulwasiu logs in, I click)
- [x] Yearly availability (all countries), monthly availability to re-check
- [x] Both products: 7 day free introductory offer (done 23 Oct)
- [x] Yearly: display name and description (done 23 Oct)
- [ ] Both products: review screenshot of the Premium page (take it from the TestFlight build)
- [ ] RevenueCat: add iOS app (bundle ID com.base6996fa161c7db2beb6067c48.app), entitlement "premium", offering "default" with monthly and yearly packages
- [ ] Copy the RevenueCat iOS public key (appl_...) into Base44 lib/purchases (REVENUECAT_IOS_API_KEY)

## D. Build and release (after B and C)
1. Merge feature/premium-and-reminders into main (risetrack-ios)
2. Run Codemagic workflow risetrack-ios (submit_to_testflight stays false)
3. Install on an iPhone through TestFlight internal testing (Amazigh is Account Holder), sandbox purchase test: trial starts, restore works, reminder fires, premium unlocks after locks are ON
4. In App Store Connect: new version 1.1, select the build, attach both subscriptions, paste review notes (02-work/apple-review-notes-DRAFT.md), add demo account in Sign-In Information, submit for review
5. After Apple approves: set PREMIUM_LOCKS_ENABLED = true in Base44, Publish, check live, release

## E. Rules to keep
- Only Camera and Photo Library permissions, email and password login only, submit_to_testflight false
- Price page shows price, period, trial, auto renewal text, Terms and Privacy, Restore Purchases
- Never put .p8 keys, passwords or the demo account password in chat or the repo

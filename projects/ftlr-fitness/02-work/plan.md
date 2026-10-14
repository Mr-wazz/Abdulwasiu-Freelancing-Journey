# Plan: FTLR Fitness

Source of truth for code: GitHub repo Mr-wazz/ftlr-ios-wrapper (branch main). Copies of key files are in this folder.

## Tasks in order
1. Fix build 13 (fails at Sync Capacitor: pod install, no Podfile). Cause NOT confirmed.
   - Check commit 3105305 for deleted or moved files
   - Check ios/App/CapApp-SPM has Package.swift, README.md, Sources
   - Check package.json and package-lock.json unchanged
   - Idea (unverified): add "packageManager": "SPM" in the ios block of capacitor.config.json
2. Re-run Codemagic workflow "FTLR Fitness iOS to TestFlight"
3. Install the build from TestFlight. Check icon, launch screen, plans screen and prices
4. Back up Base44, then test website in a normal browser (must look unchanged)
5. Confirm https://ftlr-fitness.base44.app/Terms opens while logged out
6. Test on 2 iPhones: sandbox purchase, restore, stays unlocked after reopen, web member login, no subscription screen, back link
7. Send Leah the paywall screenshot
8. Review pack, screen recording, App Store submission
9. After approval: Fiverr review, Reddit referral, upsells

## What Abdulwasiu must provide
- Demo login for Apple review (subscription_status active, or admin)
- One real paying web subscriber email (or a test one)
- Apple sandbox tester account
- Leah's iPhone for the screen recording
- GitHub access for Claude Code on the repo
- Check exact Apple prices in App Store Connect (web is $10 and $100)

## Open risks
- Cancelled web users stay active in Base44, so they could enter the iPhone app via the login path
- Terms text says access needs a paid subscription, but web paywall is off. Keep wording consistent with review notes
- Keep Apple standard EULA link in paywall and App Store Connect (safest for 3.1.2)

# Delivery: FTLR Fitness

Status: NOT delivered. Blocked on build 13.

## Built so far
- Capacitor 8 iOS shell (Swift Package Manager), native paywall, restore, lock, "Already a member" path, visible error naming failing step
- RevenueCat (project FTLR Fitness, entitlement premium)
- Both subscriptions in App Store Connect with screenshots, prices, review notes
- Codemagic signing and upload. Build 12 reached TestFlight as 1.0 (112)
- Base44 iOS only edit (Base44 report: NoSubscriptionIOS.jsx plus App.jsx change). Code not yet seen by us
- Icon, splash, logo made from Leah's file

## Key IDs
- Bundle ID: com.base690a2fc0b35286e721bd236c.app
- App Store Connect app ID: 6774250982
- Live app: https://ftlr-fitness.base44.app/
- Privacy: /PrivacyPolicy. Terms: /Terms
- Codemagic integration: FTLR-ASC, secret group ftlr
- RevenueCat public key is in config.js (public, safe)
- No passwords stored here. Logins stay in a password manager

## Handover checklist
- [ ] Build installs from TestFlight
- [ ] Icon, launch screen, plans and prices correct
- [ ] Sandbox purchase works
- [ ] Restore works
- [ ] Stays unlocked after reopen
- [ ] Web member login works, back link works
- [ ] No Stripe visible anywhere in the iPhone app
- [ ] Website unchanged in normal browser
- [ ] Terms opens logged out
- [ ] Review pack and screen recording done
- [ ] Submitted, approved
- [ ] Invite Leah to RevenueCat
- [ ] Fiverr review requested, testimonial collected
- [ ] Reddit referral accepted

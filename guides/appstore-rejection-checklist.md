# App Store Rejection Checklist

Source: "20+ reasons Apple rejects apps" by Lincoln Devine (lincolndevine.com/guides/rejected/), 7 Sep 2026. Rewritten here as a working checklist. Apple rules change: verify against Apple's current App Review Guidelines before relying on a number.

Why it matters: apps built with AI tools or Base44 ship what was asked for, not what Apple requires. Run this on EVERY app before submission (Capacitor, Base44 wrapped, any iOS build). Also use it when handling a rejection.

## How to use
1. Run the audit prompt (bottom) on the build. Fix every FAIL and CAN'T TELL.
2. Do the manual checks by hand (section B).
3. Record results in the client's 03-delivery.md and 05-notes.md.
4. After approval, send the upsell offers (store optimization, launch plan, reviews).

## A. Code checks (the audit prompt covers these)
| # | Rejection reason | Guideline | Fix |
|---|---|---|---|
| 1 | App needs notifications allowed to open | 4.5.4, 5.1.2(i) | App must work fully with notifications denied. Ask at the moment they help. |
| 2 | Camera, location, contacts asked at launch | 5.1.1(ii) | Ask at the feature. Purpose string names the feature ("Take a photo of your receipt to attach it to an expense", not "We use your camera"). |
| 3 | "GPT" or another brand in the app name | 2.3.7, 4.1(c) | Rename. Say what it does, not what it runs on. |
| 5 | Debug or test route in release build | 2.3.1 | Remove, or gate behind dev flags. |
| 6 | Website in a box (thin webview) | 4.2 | Add one real native feature: push, offline mode, camera, share sheet. |
| 7 | Signup but no in app Delete Account | 5.1.1(v) | Delete Account button in settings that deletes account and data. Email or website link is not enough. |
| 8 | Hidden SDKs (analytics, crash, ads) not in Privacy form | 5.1.1 | List every SDK and data flow, fill the App Privacy form from that list. |
| 11 | Google or Facebook login without a private option | 4.8 | Add Sign in with Apple (or equal: only name and email, can hide email, no ad tracking). Not needed if app only has its own email login. |
| 16 | "Coming soon", placeholders, empty tabs | 2.1 | If not built, remove the button. |
| 18 | User posts but no moderation | 1.2 | Need all four: content filter, report button, block button, contact email. Or hold the feature. |
| 19 | Restore Purchases missing or broken | 3.1.1 | Visible button on paywall and settings. RevenueCat makes it one call. Test in sandbox. |
| 21 | Stripe checkout inside app for digital features | 3.1.1 | Use StoreKit or RevenueCat. US storefront may add a link to web checkout (3.1.1(a)). Outside US needs External Purchase Link Entitlement, check country rules. Stripe is fine for physical goods and outside services. |
| 22 | Tracking SDK runs before App Tracking Transparency prompt | 5.1.2 | Ask ATT first, declare tracking in Privacy form, or remove the SDK. |
| 23 | Login wall on app that needs no account | 5.1.1(v) | Remove or make optional. |
| 24 | Templated look, same as many AI apps | 4.3 | Change what reviewer sees first: own onboarding copy, icon, colours, one custom screen. |

## B. Manual checks (by hand, about 10 minutes each, before submitting)
- [ ] 4. Every paywall product exists in App Store Connect with name, description, price, review screenshot, and is attached to THIS version (not Missing Metadata).
- [ ] 9. In app purchase icon is a DIFFERENT image from the app icon.
- [ ] 10. Subscription apps: terms (EULA) link on the last line of the App Store description (Apple standard EULA works). Every app: Privacy Policy URL filled in App Store Connect and linked inside settings.
- [ ] 12. Demo reviewer account works, has real looking data, everything unlocked, backend is ON. Test the morning you submit. Login plus 2 line walkthrough in Notes for Review.
- [ ] 13. Run on a real phone over cellular, cold start at least once. TestFlight to two friends.
- [ ] 14. Every screen checked on iPad simulator, both orientations. Nothing may break.
- [ ] 15. Screenshots retaken from the exact build being submitted, every time.
- [ ] 17. Support link and privacy link are live web pages. Contact page or working email. Privacy policy says what is collected, who sees it, how to request deletion.
- [ ] 20. Screenshots of paid features carry a Premium or Pro tag. One line in the description says what the subscription includes.
- [ ] 25. No Google Play badge, Android frame or "available on" line in App Store screenshots. Make two asset sets.

## C. Audit prompt (paste into the project, run before every submission)
```
Audit this app against the following App Store rejection reasons.
Report each one as PASS, FAIL, or CAN'T TELL with the file and line
that decides it. Don't change any code.

1. Is there any native feature beyond a webview?
2. If users can create an account, can they delete it in the app?
3. List every third-party SDK and what data it collects or sends.
4. If there is a Google, Facebook, or other social login, is there
   also a login that limits data to name and email, lets users hide
   their email, and doesn't track for ads (Sign in with Apple does)?
5. Are there placeholder screens, "coming soon" text, or empty tabs?
6. If users can post content, is there report, block, a filter, and a
   contact email?
7. Is there a Restore Purchases button wired to the store?
8. Is any checkout for digital features happening inside the app
   through Stripe or another non-Apple processor? (A link out to a web
   checkout is a separate case. Note it, don't fail it.)
9. Is any tracking SDK started before the App Tracking Transparency
   request?
10. Is login required on launch? Does the app have account features
    that justify it?
11. Does any screen block the app until a system permission is granted?
12. Are permissions requested at launch instead of at the feature, and
    does every purpose string name the feature it is for?
13. Are there debug, dev, or test-only routes reachable in a release
    build?

Output a table.
```

## D. Money angle for Fiverpulse
- Sell "App Store readiness audit" as its own paid service (suggested $150 to $500 per app, price by value: a rejection costs the client weeks and launch revenue).
- Stripe inside a Base44 or Capacitor iOS app is the most common money problem: it means in app purchase setup (RevenueCat), a paid add on.
- After approval, send the store optimization, launch plan and review collection offers (Rule 3).

# App Store Approval Playbook (iOS apps and in app purchases)

Use this on EVERY project that ships to the Apple App Store.
Built from the FTLR Fitness launch (Base44 web app + Capacitor + RevenueCat + Codemagic), Oct to Nov 2026: rejected once, then approved with subscriptions.

## Rule 0: The client comes first
- This playbook is a guideline, not a blocker. ALWAYS deliver what the client asked for.
- When a request clashes with an Apple rule, do not refuse it. Build it in the approved way, and tell the client in one line what changed and why ("Apple requires X, so I did it like Y, you still get Z").
- Flag risks early (at quote time), not at submission time.
- Apple rules change. When a point is unclear or new, check the current App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/

## Rule 1: Security (never break)
- The client or Abdulwasiu logs in to App Store Connect, Codemagic, RevenueCat, Base44. Claude never types, asks for or stores passwords, codes, OTPs, PINs or .p8 keys.
- If a login or 2FA screen appears: stop and tell the user.
- Demo account password: never in the repo, notes or chat. The user types it into App Review Information.
- Ask to be added as a team member (Admin or App Manager). Never ask for the owner's Apple ID.

## How to run it
At each stage, go through the checklist and report a table:

| Check | Status (PASS / FIX / RISK / N/A) | What to do |

Fix what you can. Give the user exact beginner steps for anything only they can do.

---

## Stage 1: Intake (before quoting)
- [ ] Who is the Account Holder? (Only they can accept agreements. Usually the client.)
- [ ] Our role in the team: Admin is best.
- [ ] Agreements: Program License Agreement accepted (if not, builds fail with 403). Paid Apps Agreement "Active" with bank and tax done (if not, no purchases load).
- [ ] What is sold? Decide the payment rule now:
  - Digital content, features, subscriptions used in the app: MUST use Apple in app purchase (3.1.1).
  - Physical goods or real world services (delivery, gym visit, in person session): may use Stripe or other (3.1.3(e)).
  - One to one live services between two people (live coaching call): may use other payment (3.1.3(d)).
  - Existing web subscribers: can log in and use what they bought, as long as the same thing is ALSO sold by in app purchase in the app (3.1.3(b)).
  - Buy buttons or links to a web checkout for digital content: risky. Rules differ by country (US rules relaxed in 2025). Check current rules before promising.
- [ ] Is it a website wrapped in an app (Capacitor, WebView)? Then plan native value (see 4.2 below). Price this in.
- [ ] Does it have user generated content (chat, posts, comments)? Plan report and block (1.2).
- [ ] Health, fitness, medical, finance, kids, gambling, crypto: extra rules. Add disclaimers and check the section.
- [ ] Timeline: Apple review usually 1 to 3 days, but first launches can take 1 to 2 weeks with a rejection. Say so in the quote.

## Stage 2: Build rules (while building)

### App quality (2.1, 2.3, 4.2)
- [ ] No crashes, no blank screens, no "coming soon", no placeholder text, no broken links.
- [ ] Wrapper apps (4.2 Minimum Functionality): add real app value. Examples: native paywall, offline and error screen with retry, splash and icon, push notifications, native share, keep users inside the app (no jumping to Safari for core features).
- [ ] Works on iPhone AND iPad if iPad is supported (Apple tests on iPad too). If not tested on iPad, set the app to iPhone only.
- [ ] Every screen reviewers can reach must work with the demo account.
- [ ] App name, icon and screenshots match what the app really does (2.3). Never change the client's name, logo or titles without their OK.

### Accounts and privacy (5.1)
- [ ] Privacy Policy URL works, opens without login.
- [ ] If users can create an account: they must be able to DELETE their account inside the app (5.1.1(v)). Not just "email us".
- [ ] If the app offers Google or Facebook login: also offer Sign in with Apple (or another private login option) (4.8).
- [ ] Permission pop ups (camera, photos, location, notifications) have clear purpose text in Info.plist, and are only asked when needed.
- [ ] Tracking users across apps or for ads: App Tracking Transparency prompt required.
- [ ] Privacy manifest (PrivacyInfo.xcprivacy) present when the app or its SDKs use "required reason" APIs.
- [ ] Export compliance: set ITSAppUsesNonExemptEncryption = NO when only standard HTTPS is used (saves a question on every build).

### User generated content (1.2)
- [ ] Terms of use / community rules that forbid abusive content.
- [ ] Report a post or user. Block a user. A way to remove bad content quickly.
- [ ] Published contact for reports (email in Terms or Settings).

### Subscriptions and in app purchases (3.1.1, 3.1.2)
Paywall screen must show, on the SAME screen as the buy button:
- [ ] Name of each plan (Monthly, Annual).
- [ ] Length of each plan.
- [ ] Price per period, clear and the biggest number. If there is a free trial, the price after the trial is just as clear.
- [ ] "Restore Purchases" button that works.
- [ ] Terms of Use (EULA) link that works. Apple standard EULA is fine: https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
- [ ] Privacy Policy link that works.
- [ ] Auto renew line, e.g. "Subscription renews automatically until cancelled. Cancel anytime in Settings."
- [ ] No fake urgency, no hidden close button, no misleading prices.
- [ ] After purchase: unlock right away; stays unlocked after reopening the app; restore works on a new install.
- [ ] Clear error screen if plans cannot load (with retry), never a blank page.

RevenueCat setup:
- [ ] RevenueCat product IDs EXACTLY match App Store Connect product IDs.
- [ ] Products attached to an entitlement (e.g. "premium") and to the CURRENT offering with packages.
- [ ] App in RevenueCat uses the correct bundle ID, and the In App Purchase key is uploaded (client uploads, never in chat).
- [ ] The app uses the PUBLIC Apple SDK key (starts with appl_). Public key in code is fine. Secret keys never.
- [ ] Sandbox purchase tested on TestFlight (buy, restore, reopen).

## Stage 3: App Store Connect setup (before submitting)

### App information and listing
- [ ] App Description ends with Terms (EULA) and Privacy links, in EVERY language (3.1.2). Or set a custom EULA in App Information.
- [ ] Privacy Policy URL field filled. Support URL works.
- [ ] Screenshots: iPhone 6.9 inch (or 6.5 inch). iPad 13 inch if the app supports iPad. Real app screens only.
- [ ] Age rating questionnaire done honestly.
- [ ] App Privacy (nutrition labels) matches what the app and SDKs collect.
- [ ] Pricing and Availability set. Content Rights answered.

### Each subscription
- [ ] Reference name, product ID, duration.
- [ ] Price set (all territories filled).
- [ ] Availability set.
- [ ] Localization: display name + description (e.g. "Monthly Subscription", "automatically billed monthly until cancelled").
- [ ] Review screenshot: the paywall, full size (at least 640 px wide; a full iPhone screenshot like 1206 x 2622 works).
- [ ] Review notes: where the paywall is and how to reach it.

### Each subscription group
- [ ] Group display name localization filled (this is what users see in Settings).

### App Review Information
- [ ] Demo account (user types the password) that has NO active plan, so reviewers see the paywall.
- [ ] Contact name, phone, email.
- [ ] Notes: what the app does, how to log in, where the paywall is, that Terms and Privacy links are on the paywall, where report and block are, where delete account is. Keep under 4,000 characters.
- [ ] Attach or link a short screen recording when the flow is not obvious.

### The build
- [ ] Version number new (e.g. 1.0.1) and build number higher than the last upload.
- [ ] Build processed ("Valid") and attached to the version.
- [ ] Codemagic: run the release workflow, never "reset certificate" by accident (its dialog may preselect it).

## Stage 4: Submission gate (the step that broke FTLR, check it every time)
- [ ] FIRST in app purchases or subscriptions MUST be submitted with a NEW app version. They cannot go alone.
- [ ] Click "Add for Review" on the version and choose the EXISTING draft submission. NEVER "Create New Submission" if subscriptions are already in a draft (that sends the app alone, and it gets approved WITHOUT the plans).
- [ ] Open "Draft Submissions" and confirm it contains ALL of these:
  - the app version (e.g. iOS App 1.0.1)
  - every subscription (e.g. Subscriptions (2))
  - every subscription GROUP (one item per group)
  So FTLR needed 5 items: version + 2 subscriptions + 2 groups.
- [ ] No yellow warning. "Your auto renewable subscription must be submitted with its subscription group" means a group is missing: open the group page, Add for Review, choose the existing draft.
- [ ] Only then click Submit for Review. Status becomes "Waiting for Review".
- [ ] Afterwards check each subscription status: "Waiting for Review" (good). "Missing Metadata" or "Ready to Submit" means it was NOT sent.
- [ ] Need speed? Request an expedited review (Contact Us, App Review) with a real reason (launch date, critical bug).

## Stage 5: After approval (do not say "done" before this)
- [ ] Subscriptions show "Approved". App shows "Ready for Distribution".
- [ ] Delete the app, install it from the App Store, log in: plans load with real prices.
- [ ] If "could not load plans / offerings empty":
  1. Subscriptions not approved (Missing Metadata / Ready to Submit): resubmit with a new version (Stage 4).
  2. Paid Apps Agreement not Active, or bank and tax missing.
  3. Product IDs in RevenueCat do not match.
  4. Wrong RevenueCat key, bundle ID or missing In App Purchase key.
  5. Just approved: wait up to 24 hours for Apple to spread the products.
- [ ] One real purchase (or ask the client to) and a refund if needed. Restore on a second device.
- [ ] Update 03-delivery.md and 05-notes.md. Then upsell (Rule 3).

## Stage 6: If Apple rejects
1. Read the message in App Review (Resolution Center). Note each guideline number.
2. Fix EVERYTHING listed, plus anything in this playbook that is still FIX.
3. Reply in App Review: short, polite, one paragraph per guideline: what was wrong, what changed, where to see it. Attach a screen recording if useful. Never paste passwords.
4. If only metadata changed (description, notes), you can reply and resubmit without a new build. If code changed, upload a new build first.
5. If you think the reviewer is wrong: reply with facts first. Appeal only if that fails.

## Common rejections and the fix
| Guideline | Why | Fix |
|---|---|---|
| 2.1 Performance | Crash, broken feature, cannot log in | Test on iPhone and iPad, give a working demo account |
| 2.1(b) | IAP / subscriptions not submitted | Stage 4 submission gate |
| 2.3 Metadata | Screenshots or text do not match the app | Real screenshots, honest description |
| 3.1.1 Payments | Digital content sold outside IAP | Use in app purchase for digital items |
| 3.1.2(c) | No Terms (EULA) or Privacy link, unclear price | Links in app paywall AND in App Description |
| 4.2 Minimum functionality | Just a website in an app | Add native value (Stage 2) |
| 4.8 Login | Google login without a private login option | Add Sign in with Apple |
| 5.1.1(v) | No in app account deletion | Add Delete Account in Settings |
| 1.2 UGC | Chat or posts without report and block | Add report, block, rules, contact |

## Lessons from FTLR (keep adding)
- The Account Holder had to accept a new Program License Agreement before any build could upload (Codemagic 403).
- Apple approved the app WITHOUT the subscriptions because the version went in a separate submission. Live app showed "We could not load your plans". Fix took a new version (1.0.1).
- Subscription groups must be in the draft too, not only the subscriptions.
- App Store Connect pages can be slow or blank; the data is still there. Reload or check another page.
- Never print or copy the demo password anywhere.

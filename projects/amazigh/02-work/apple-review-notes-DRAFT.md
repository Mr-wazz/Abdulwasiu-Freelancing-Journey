# Draft review notes for Apple (App Review Information, Notes) 

Use when submitting the new version with the subscriptions. English. Currency: CAD. Do not paste passwords here. The demo account is stored outside the repo.

---
RiseTrack is a habit and task tracker. The app is free to use with habits, tasks, the weekly tracker, basic stats and 1 active challenge.

NEW in this version: optional auto-renewable subscription "RiseTrack Premium" (Subscription group "RiseTrack Premium").
- Monthly: CAD 3.99 per month (risetrack_premium_monthly)
- Yearly: CAD 27.99 per year (risetrack_premium_yearly)
- Both include a 7 day free trial for new subscribers.
Premium unlocks: daily reminders on iPhone, advanced stats and trends, and unlimited challenges.

How to find it: open the Settings tab, tap "Go Premium" (Passer à Premium). The price page shows the plans, the free trial terms, "Restore Purchases", and links to the Terms of Use and Privacy Policy.
Purchases use Apple In-App Purchase only. Restore Purchases is on the same page.
Reminders use local notifications on the device. The app asks for notification permission only when the user turns on a reminder.

Account: sign in with email and password. Account deletion is available in Settings. A demo account is provided in the Sign-In Information fields.
The app wraps our web app and uses native iOS plugins for purchases (RevenueCat) and local notifications.
---

TO CHECK BEFORE SENDING (guidelines 3.1.2, 5.1.1(v), 2.1):
- The price page must show price, period, trial length, auto-renewal text, and Terms and Privacy links. Verify in the final build.
- Real account deletion (login removed) is not done yet. Apple expects it. Offer to Amazigh as a paid add-on, or do it before submission.
- Do not mention third party names that are not needed.

# Delivery: Amazigh (RiseTrack)

## Job 1 delivered
- Apple approved v1.0 (around 13 Oct 2026)
- Fixed: fake Premium removed, old React Native shell replaced by Capacitor 7 wrapper, permissions cut to Camera and Photo Library, Sign in with Apple turned off (email and password only), replied to Apple, resubmitted
- Web app changes: useSubscription always premium, subscription files and backend functions deleted, Terms section 3 now "Free Use", Privacy bullet removed

## Not confirmed
- [ ] Order formally delivered and accepted on Fiverr or Upwork
- [ ] Review left by Amazigh
- [x] Payment received via Sendwave (14 Oct 2026). Amount and scope: confirm in writing
- [ ] Which build Apple approved

## Handover checklist
- [ ] Amazigh has her Apple account and App Store Connect access
- [ ] API key (Issuer ID, Key ID, .p8) revoked by her
- [ ] Demo account details stored safely (not in chat)
- [ ] Wrapper repo and Codemagic settings documented
- [ ] Testimonial and review collected

## Known weak spots (from code review, NOT tested on a phone)
1. Delete account only erases habits, logs, challenges, then signs out. Login stays. Apple 5.1.1(v) expects real deletion. Possible rejection on a future update
2. Reminders use browser Notification API with a 10 second timer. Probably does nothing in the iPhone app
3. Habits tied to week_start, vanish next week, no carry over
4. "AI coach" is a fixed bank of French tips, not AI, not translated
5. About 126 inline language switches, hardcoded Back and Retour button
6. Narrow phone column layout (max-w-lg, fixed position). Thin strip on iPad and desktop
7. No home dashboard
8. No row level security rules in data definitions. Settings loads unfiltered lists. Check in Base44 dashboard
9. Every tab stays mounted, each loads up to 5,000 habit logs
10. No uniqueness per habit and date in logs, duplicates possible
11. Empty catch blocks, no crash reporting, analytics or tests, lint errors in 3 files, about 157 leftover Premium and locked references
12. User table still holds Apple receipt and trial fields

## CAD 300 deal checklist (20 Oct 2026)
- [x] 1 Base44 badge hidden and published by Abdulwasiu (20 Oct), live check pending
- [~] 2 Safe area: published 20 Oct on 5 screens, real iPhone test pending
- [x] 3 Habits carry over: published 20 Oct  [x] 4 Duplicate logs: published 20 Oct  [x] 5 Bug check: done, 4 fixes published, see 05-notes
- [ ] 6 RevenueCat Premium (CAD 3.99 per month, CAD 27.99 per year, 7 day trial)  [ ] 7 Notifications  [ ] 8 New build and Apple review
- Payment: CAD 300 paid by the client after the project is done (agreed by Abdulwasiu)

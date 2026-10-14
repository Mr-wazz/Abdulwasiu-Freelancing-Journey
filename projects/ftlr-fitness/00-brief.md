# Brief: FTLR Fitness

## Client
- Business: For the Long Run Fitness LLC. App: FTLR Fitness
- Owner: Leah Stukov (Fiverr: coachleah7). Country: USA. City: not discussed
- Sells: fitness coaching app (workouts, programs, recipes, personal plan, Ask Your Coach, group chat, resources)
- Source: Fiverr. Custom offer accepted 9 Oct 2026 after her earlier developer failed
- Style: tests fast, sends screen recordings and screenshots, chases progress ("Day 3" message)
- Sensitive: she owns App Store Connect (Abdulwasiu is Admin). Her paying web subscribers (Stripe) must not break

## Goal
Add Apple in app subscriptions (paywall plus Restore Purchases) to her Base44 iOS app and get it approved on the App Store before launch on 1 Nov 2026.

## Real problem
Base44 cannot do App Store subscriptions. Apple rejects apps that sell digital subscriptions without Apple in app purchase. Her first developer did not deliver.

## Money and time
- Agreed: $300 custom offer, paid in full on Fiverr. Nothing unpaid
- Includes: 2 resubmissions after an Apple rejection
- Fiverr delivery deadline: 14 Oct 2026, about 5 hours after the 14 Oct session start (hard deadline for Abdulwasiu)
- Leah's app launch date: 1 Nov 2026 (not the delivery deadline)
- Budget she had: not discussed

## Weak spots found (upsell fuel)
- Web paywall OFF (PAYWALL_ENABLED = false). Leah says on purpose. Do not touch
- Stripe webhook only handles checkout.session.completed. Renewals and cancellations ignored, so cancelled web users stay active
- Web app design weak
- Apple review risks: 2.1, 4.2, 3.1.1, 3.1.2, 3.1.3(b)

## Founder note
$300 for this scope is far under the $5,000 target. Lesson for the playbook: quote App Store subscription rescue jobs by the revenue they unlock, not by hours. Recover value through the upsells in 04-upsell.md.

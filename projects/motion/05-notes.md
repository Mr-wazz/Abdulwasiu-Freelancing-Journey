# Notes: Motion (personal project)

## Timeline
- 2026-11-08: Abdulwasiu described the idea. First message was cut off at "number three". Asked the client tag question, then 21 questions with a suggested answer for each.
- 2026-11-08: he said it is personal, team name Motion. Answered logins, sponsor and earnings proof.
- 2026-11-08: team size 9 now, 30 in a year.
- 2026-11-12: he sent 4 NeoLife PDFs, answered currency, goals, device and resale, added the breakdown, payment details and calculator features, and said to start building.
- 2026-11-12: version 1 built and tested. Demo published. Waiting on him for accounts, price list and member list.

## Decisions
- Custom code, not Base44. Reason: full control of the privacy rules, free hosting, and it can be sold later.
- Supabase for database and logins. Reason: free plan fits 30 members, and privacy is enforced in the database, not only in the screens.
- Members join with a private invite link. The first sign up becomes admin. Sign ups without a link wait for approval.
- Members can add their own recruits. The admin approves them.
- Only approved earnings count toward a goal.
- A sponsor can see the goals and earnings of people under them. Bank details, to do lists, breakdown requests and screenshots stay between the member and the admin.
- The leaderboard shows names and % of goal. It never shows Naira amounts.
- "Breakdown" was built as: the member asks for a month, the admin writes how the amount is made up, can record an amount sent and attach a transfer receipt. If he meant something else, this needs a small change.
- "SVB" is not a number per product. It is a % of BV that depends on the month's QPV. The calculator shows it that way.
- Calculator maths follows the NeoLife Compensation Plan for Africa, March 2026: the chart on page 5, and "your % minus their %" from page 9. A line with 4,000 QPV or more is treated as a Director line and left out, because NeoLife pays that through the Leadership Development Bonus.
- Demo data uses made up names, products and rates. No real NeoLife prices were invented.

## Open questions for Abdulwasiu
1. The NeoLife price list (name, PV, BV, distributor price, retail price).
2. What was "number three" in the first message? Is it covered by what he listed later?
3. Is the breakdown feature what he meant?
4. Should members see the whole team tree, or only their own downline (current)?

## Client personality and feedback
- Speaks his ideas in voice note style. Messages can cut off. Confirm what was understood before building.
- Likes to be asked questions first, then wants fast progress.

## Time log
| Date | Task | Hours | Problems |
|---|---|---|---|
| 2026-11-08 | Discovery questions | 0.5 | First message cut off |
| 2026-11-12 | Read NeoLife plan, design data model and privacy rules | 1 | Price list not in the documents |
| 2026-11-12 | Build app, database file, demo mode | 4 | None |
| 2026-11-12 | Tests: bonus maths, 83 database checks, 68 screen checks | 1.5 | Live Supabase could not be tested without an account |
| 2026-11-12 | Setup guide and project notes | 0.5 | None |

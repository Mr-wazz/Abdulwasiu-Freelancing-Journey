---
description: Run the App Store rejection checklist on a client app before submission
argument-hint: <client-name>
---

App Store check for: $ARGUMENTS

1. If no client is given, ask "Which client is this?" and stop.
2. Read `guides/appstore-rejection-checklist.md` and the client's 00-brief.md, 02-work/plan.md and 03-delivery.md.
3. Run the audit prompt (section C) against the app code in `projects/<client>/02-work/`. If the code is not in the repo, tell Abdulwasiu exactly how to get it here.
4. Show the PASS, FAIL, CAN'T TELL table. Fix what is in scope. Flag out of scope work as a paid add on quote (Rule 2B point 9).
5. Walk Abdulwasiu through section B (manual checks) one item at a time, in beginner words, and say which ones he must do himself in App Store Connect.
6. Save results to the client's 03-delivery.md and log time and problems in 05-notes.md.
7. Update `playbook/upsell-learnings.md` if a new rejection reason or fix appears.

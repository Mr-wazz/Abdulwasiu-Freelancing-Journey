---
description: Test a client site before delivery (speed, links, forms, mobile, SEO basics)
argument-hint: <url> [client-slug]
---

Test a site before delivery: $ARGUMENTS

1. If no URL is given, ask which site and which client. Do not guess.
2. Run `node scripts/test-site.js $ARGUMENTS`. With a client slug it saves report.md, desktop.png and mobile.png to `projects/<slug>/02-work/test-report/`.
3. Read the report. For every FAIL, explain in plain beginner words what it means and give the exact fix. If the fix is outside the agreed scope, draft a paid add on quote (Rule 2B point 9).
4. Open the screenshots and check the layout looks right on desktop and mobile.
5. Tell Abdulwasiu what is finished, what failed, and what the script cannot test (payments, logins, automations, email), which he must test by hand.
6. Log the result in 05-notes.md for that client.

# Base44 fix prompts: Pack Stabilite (CAD 300)

Use these in the Base44 editor chat of the RiseTrack app. One prompt at a time. After each: Preview, test on phone width, then Publish. Web changes go live with no Apple review.

Start only after the CAD 300 has ARRIVED. Need from Amazigh: Base44 editor access (invite as collaborator, never his password).

## Prompt 1: Base44 badge and top of screen
"Remove the 'Edit with Base44' or 'Made with Base44' badge from the app if the plan allows it. On mobile, add top padding using env(safe-area-inset-top) so the header and buttons never sit under the iPhone notch or status bar. Add the viewport meta with viewport-fit=cover. Do not change any other screen."

If the badge cannot be removed on his plan: tell him the exact plan option to change in Base44 settings (his decision, his money).

## Prompt 2: Habits that vanish next week
"Habits are saved with a week_start and disappear the next week. Change this so a habit stays active every week until the user deletes or archives it. Keep the old weekly logs. Do not delete any existing user data. Show the same habit list every week."

Before running: ask Base44 to back up or duplicate the app. Test with one old habit.

## Prompt 3: Duplicate logs
"In habit logs, when a user taps a habit for a date that already has a log, update the existing log instead of creating a second one. Add a one time cleanup that removes duplicate logs with the same habit and date, keeping the newest."

## Prompt 4: Bug check (cap 2 hours)
List what you test, in this order, and stop at 2 hours:
1. Sign up, log in, log out
2. Add, tick, edit, delete a habit
3. Switch week, switch language
4. Stats and challenges screens
5. Delete account (note: only erases data today, full deletion is in phase 2)
6. Settings screen (loads unfiltered lists, check data access rules)
Write each bug found: fixed, or listed for phase 2 with price.

## Not in the CAD 300 (phase 2, written agreement first)
Premium subscription, free trial and price page, push notifications, real account deletion, new Apple build. Needs his Paid Apps Agreement, bank and tax active in App Store Connect.

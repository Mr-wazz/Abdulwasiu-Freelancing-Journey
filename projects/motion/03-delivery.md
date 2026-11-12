# Delivery: Motion (personal project)

## What was built
Version 1 of the Motion Team Portal, in `02-work/portal/`.

For the leader (admin):
- Dashboard: team size, who has a downline, who does not, team earnings, every member's goal progress
- Team: the sponsor tree, search, filters, add and edit members, invite links
- Inbox: earnings to approve or reject, breakdown requests with bank details, new members to approve
- Products: the price list, with paste from a spreadsheet
- Team setup: team name, value of one point, task ideas

For each member:
- Home: goal progress, today's to do list, leaderboard
- Goals: monthly goal broken into weeks and days, to do list with suggestions
- Earnings: report with a screenshot, see approved, waiting and rejected
- Calculator: NeoLife Sales Volume Bonus for their own points and their team's points
- Breakdown: ask the leader for a month's breakdown
- Bank details: where the breakdown is sent
- My team: their own downline, add a recruit for approval
- Incentives: progress toward the three NeoLife Nigeria events

## Where things are
- App code: `02-work/portal/src/`
- Database setup file: `02-work/portal/supabase/schema.sql`
- Setup steps for a beginner: `02-work/portal/SETUP.md`
- Demo with sample data: the Motion Team Portal artifact link given in chat on 12 Nov 2026

## Logins and access
No real accounts exist yet. When Abdulwasiu sets up Supabase:
- The first account created in the portal becomes the admin. Create it right after running the setup file.
- Supabase and Vercel logins stay with Abdulwasiu. Do not paste passwords or the Supabase service key into this repo.
- The two values the app needs (project URL and anon key) go into Vercel, not into the repo.

## Handover checklist
- [x] Everything that can be tested without real accounts is tested
- [ ] Supabase project created and setup file run
- [ ] App deployed on Vercel
- [ ] First sign up done, Abdulwasiu is admin
- [ ] Price list loaded
- [ ] 9 members added, invite links sent
- [ ] Short walkthrough sent to the team

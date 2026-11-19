# Plan: Motion (personal project)

## Tasks in order
1. Read the NeoLife documents. Done.
2. Build the portal app in `02-work/portal/`. Done.
3. Write the database setup file with privacy rules. Done.
4. Test the bonus maths, the privacy rules and every screen. Done. See the test checklist.
5. Publish a demo with sample data so Abdulwasiu can try it. Done.
6. Abdulwasiu creates the free Supabase and Vercel accounts. Steps in `portal/SETUP.md`. Waiting.
7. Abdulwasiu sends the NeoLife price list. Load it into Products. Waiting.
8. Add the 9 members with their sponsors, send invite links on WhatsApp. Waiting.
9. One week of real use, then fix what the team finds.

## How it is built
- Web app: React and TypeScript, built with Vite. Works in the phone browser and on desktop.
- Database, logins and screenshot storage: Supabase.
- Hosting: Vercel.
- Demo mode: the same app running on sample data inside the browser, with no server.

## What Abdulwasiu must provide
- A free Supabase account and a free Vercel account (SETUP.md has the steps)
- The NeoLife price list: product name, code, PV, BV, distributor price, retail price
- The 9 members: full name, phone, who sponsored them, rank, date joined
- A logo and brand colors for Motion, if he has them. The portal has its own simple mark for now.

## Test checklist
- [x] Bonus maths: 15 automatic tests. The results match the examples on pages 5, 7 and 9 of the NeoLife plan.
- [x] Privacy rules: 83 automatic checks on a real Postgres database (`portal/tests/sql/run.sh`)
- [x] Screens: 68 click through checks on a phone sized screen, as a member and as the leader (`portal/scripts/e2e.mjs`)
- [x] Forms: goal, to do, earning with screenshot, bank details, breakdown, add member, product paste
- [x] Mobile view: no sideways scrolling on any page at 390px. Desktop layout at 1280px.
- [x] Light and dark theme
- [ ] Real sign up, invite link, password reset and screenshot upload against Supabase. Cannot be tested until the Supabase project exists.
- [ ] Payments: not part of this project

# Behance Growth (internal project, not a client)

Goal: turn Behance into a steady source of creative design and creative development clients. Target projects of $1,500 and up, with $5,000+ packages for full brand plus build work.

## Status (14 Nov 2026)
- Behance Pro free trial started 14 Nov. Ends 22 Nov 2026, then NGN 17,200 per month. Decide by 21 Nov.
- Gmail check: no job alerts or client messages from Behance so far. Only newsletters. 6 followers and 1 comment since Aug 2025.
- Claude in Chrome: not reachable from the cloud session. Needs a Claude session running on the MacBook (see "Connect Chrome" below).
- Profile: https://www.behance.net/Oyenolaabdulwasiu (audited 14 Nov, see audit.md).

## The flow (Claude does the work, Abdulwasiu approves)
1. AUDIT: Claude opens the profile in Chrome, checks headline, about, services, projects, covers, tags, pricing, availability.
2. FIX: Claude writes all copy (see profile-copy.md). Abdulwasiu approves, Claude pastes it in.
3. FIND: Claude opens Behance Jobs and Freelance projects every day, filters by the rules below.
4. WRITE: Claude writes one tailored proposal per job (see proposal-template.md).
5. APPROVE: Abdulwasiu reads the batch (2 minutes).
6. SEND: Claude fills the form in Chrome. Send only after approval. Max 5 to 10 a day, human pace.
7. TRACK: every proposal logged in proposals-log.csv. Follow up on day 3 where Behance allows messages.

## Job filter (my preferences)
- Services: brand identity, logo, UI and UX, web design, website build (WordPress, Elementor, Webflow, custom), landing pages and funnels, mobile app design and build (Capacitor, App Store, Play Store).
- Minimum budget: $500. Focus on jobs over $1,500 (these go first in every daily batch).
- Skip: contests, spec work, "free test task", budgets under $500, vague posts with no business goal.
- Prefer: business owners and startups with a clear goal (launch, rebrand, more bookings, app store launch).

## Safety rules
- No unattended bot sending. Every proposal approved by Abdulwasiu first.
- Small daily volume, no copy paste spam. Each proposal mentions something specific from the post.
- Only show client work we have permission to show (ask Amazigh and Leah first).

## Connect Chrome (beginner steps)
1. On the MacBook, update the Claude desktop app (Claude menu, Check for updates).
2. Make sure the Claude in Chrome extension is installed and signed in with the same account.
3. In the Claude desktop app, open Claude Code and start a NEW local session in the fiverpulse folder (not a cloud session).
4. Or in Terminal: cd into the project folder, then run `claude --chrome`.
5. Ask that session: "Open my Behance profile in Chrome and audit it using projects/behance-growth".

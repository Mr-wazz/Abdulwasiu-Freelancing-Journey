# Plan: Amazigh (RiseTrack) before any step 2 work

Do NOT start building until the Fiverr or Upwork order is funded.

## Step A: protect and verify (free, internal)
1. In App Store Connect (app ID 6771391018) confirm: version 1.0 status is live, which build was approved. Ignore the second empty RiseTrack record.
2. Test on a real iPhone: delete account, reminders, does a habit vanish next week, Base44 data access rules.
3. Ask Amazigh to revoke the App Store Connect API key (Issuer ID, Key ID, .p8).

## Step B: sell step 2
1. Send value message (no prices). See 04-upsell.md
2. Agree scope to her budget, fund escrow, then build

## Rules for every future Apple update
- No hidden or locked features
- Only Camera and Photo Library permissions
- Email and password login only (unless Sign in with Apple is added properly with every other social login)
- submit_to_testflight stays false
- Subscription must use real Apple In App Purchase, with restore purchase, and review notes must explain it
- Web changes go live when Abdulwasiu clicks Publish in Base44. No new iPhone build needed for web changes

## What Abdulwasiu must provide
- Demo account details for Apple (never paste the password in chat)
- The real live Base44 link (APP_URL in Codemagic and repo)
- Approval job price and payment status
- Whether the step 2 message was sent, and her budget

## Technical reference
Bundle ID: com.base6996fa161c7db2beb6067c48.app
Apple Team ID: 6TL5QTTHLX
App Store Connect app ID: 6771391018
Wrapper repo: github.com/Mr-wazz/risetrack-ios (files at repo root)
Wrapper: Capacitor 7, loads live Base44 site, permissions Camera and Photo Library only
Codemagic workflow: risetrack-ios, mac_mini_m2, node 20, build number = PROJECT_BUILD_NUMBER + 10, submit_to_testflight false
Base44: Builder plan, email and password login only, all social logins OFF
Audit and pricing doc: https://claude.ai/code/artifact/7a017d86-1912-4471-b3d2-9c1bdec20dbb

# Claude Code Plugins: what is installed and how to use it

Installed at project scope (see .claude/settings.json). They load automatically in every new session.

| Plugin | What it does for Fiverpulse | How to use it |
|---|---|---|
| superpowers | Plans before building, tests, reviews. Good for GHL, Capacitor and WordPress builds | Just describe the feature. It brainstorms, writes a plan, builds, reviews. |
| claude-code-setup | Scans the repo and recommends hooks, skills, sub-agents, MCP servers | Say: "recommend Claude Code automations for this project" |
| claude-security | Security scan of code, branches or PRs. Nothing is auto-applied | Before delivering any app or site: "scan this project for vulnerabilities" |
| caveman | Short answers, fewer tokens. Code stays exact | Keep it OFF for client messages. Say "normal mode" when drafting anything a client will read. |

## NOT installed: OmniRoute
It sends your prompts through a local gateway to hundreds of third party providers, including free ones that may log data. Client briefs, logins and contracts live in this repo. Do not use it with client work. If you want it for personal experiments, install it on your own laptop only: `npm install -g omniroute`.

## Automations (built, run on their own)
1. New client folder: start your message with `NEW CLIENT: <name>` and the folder is created for you. No command to remember. (`/new-client <name>` also works.)
2. Secret warning: if Claude is about to save a password, token or key into a file, it stops and asks you first. Write where a login is kept, never the login itself.

## Still to build
- Playwright MCP, to test client sites (links, forms, mobile view) before delivery.

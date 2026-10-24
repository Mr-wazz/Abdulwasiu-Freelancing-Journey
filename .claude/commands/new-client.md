---
description: Create the 6 part project folder for a new client (Rule 1)
argument-hint: <client name>
---

Create a project folder for a new client.

Client name: $ARGUMENTS

Steps:
1. If the client name above is empty, ask "Which client is this?" and stop. Do not guess.
2. Run `scripts/new-client.sh "$ARGUMENTS"`. It creates `/projects/<client-name>/` with 00-brief.md, 01-proposal-quote.md, 02-work/plan.md, 03-delivery.md, 04-upsell.md and 05-notes.md. It refuses to overwrite an existing folder.
3. If the user gave any details in this chat (business, budget, deadline, what they want), fill them into 00-brief.md. Do not invent facts.
4. Read playbook/upsell-learnings.md. Tell Abdulwasiu the folder is ready and name the 3 things you still need from him to write the quote.
5. Start every reply with the client name.

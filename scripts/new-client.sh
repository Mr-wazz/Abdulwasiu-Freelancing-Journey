#!/usr/bin/env bash
# Creates the Rule 1 folder for a new client. Usage: scripts/new-client.sh "Client Name"
set -euo pipefail

name="${1:-}"
if [ -z "$name" ]; then
  echo "Usage: scripts/new-client.sh \"Client Name\"" >&2
  exit 1
fi

slug=$(printf '%s' "$name" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')
if [ -z "$slug" ]; then
  echo "Client name has no usable letters or numbers." >&2
  exit 1
fi

root="$(cd "$(dirname "$0")/.." && pwd)"
dir="$root/projects/$slug"
if [ -e "$dir" ]; then
  echo "Already exists: projects/$slug. Nothing changed." >&2
  exit 1
fi

mkdir -p "$dir/02-work"
today=$(date +%Y-%m-%d)

cat > "$dir/00-brief.md" <<T
# Brief: $name

## Client
- Business:
- Owner:
- Country and city:
- Source (Fiverr, Upwork, Maps, direct):
- Style and personality:

## Goal
What they want, in their words.

## Real problem
The business problem behind the request, and the money it costs them.

## Budget and deadline
- Budget:
- Currency:
- Deadline:
- Language (note: French clients need French message plus English translation):
T

cat > "$dir/01-proposal-quote.md" <<T
# Proposal and Quote: $name

Currency: (say which one)

## Scope
What is included. What is NOT included.

## Tiers (price by value, not hours)
| Tier | What they get | Price |
|---|---|---|
| Basic | | |
| Standard | | |
| Premium | | |

## Phases
1.
2.

## Payment terms

## Retainer proposal (before project closes)
T

cat > "$dir/02-work/plan.md" <<T
# Plan: $name

## Tasks in order
1.

## What Abdulwasiu must provide (logins, content, images)
-

## What the client must provide
-

## Test checklist
- [ ] Links
- [ ] Forms
- [ ] Mobile view
- [ ] Automations
- [ ] Payments
T

cat > "$dir/03-delivery.md" <<T
# Delivery: $name

## What was built

## Logins and access
Do not paste real passwords into a public repo. Say where they are stored.

## Handover checklist
- [ ] Everything tested
- [ ] Client trained or walkthrough sent
- [ ] Access transferred
- [ ] Testimonial and review requested
- [ ] Retainer proposed
T

cat > "$dir/04-upsell.md" <<T
# Upsells: $name

Timing: when the client is happy (milestone or delivery).
Frame: "Here is what will help you earn more".

## Offers (at least 3)

### 1.
- Problem it solves:
- Money or time saved:
- Price:
- Message to send:

### 2.

### 3.

## Status
| Offer | Sent | Reply |
|---|---|---|
T

cat > "$dir/05-notes.md" <<T
# Notes: $name

## Timeline
- $today: project folder created

## Decisions

## Client personality and feedback

## Time log
| Date | Task | Hours | Problems |
|---|---|---|---|
T

echo "Created projects/$slug"
ls -R "$dir"

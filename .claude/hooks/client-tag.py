#!/usr/bin/env python3
"""UserPromptSubmit hook: a first line starting with 'NEW CLIENT: <name>' creates the project folder automatically."""
import json
import os
import re
import subprocess
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

root = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
first = (data.get("prompt") or "").strip().split("\n", 1)[0]
m = re.match(r"(?i)^\s*NEW\s+CLIENT\s*:\s*(.+?)\s*$", first)
if not m:
    sys.exit(0)

name = m.group(1)
r = subprocess.run([os.path.join(root, "scripts", "new-client.sh"), name], capture_output=True, text=True)
if r.returncode == 0:
    note = f"Hook already ran scripts/new-client.sh: {r.stdout.splitlines()[0]}. Do not run it again. Fill 00-brief.md from the message and continue per CLAUDE.md."
else:
    note = f"Hook tried to create the folder for '{name}' and said: {r.stderr.strip()}. Tell Abdulwasiu in one line."
print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": note}}))

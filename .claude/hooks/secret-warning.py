#!/usr/bin/env python3
"""PreToolUse hook: ask for confirmation before a Write/Edit puts a likely secret in a file."""
import json
import re
import sys

PATTERNS = [
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "a private key"),
    (r"\bAKIA[0-9A-Z]{16}\b", "an AWS key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}", "a GitHub token"),
    (r"\bsk-[A-Za-z0-9_-]{20,}", "an API key"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}", "a Slack token"),
    (r"(?i)\b(pass(?:word|wd)?|pwd|secret|token|api[_ -]?key|pin)\b[\w ]{0,12}[:=]\s*[`\"']?([^\s`\"'<>()\[\]]{6,})", "a password, token or key"),
]
PLACEHOLDER = re.compile(r"(?i)^(x+|\*+|\.+|none|n/?a|tbd|todo|redacted|changeme|your.*|example.*|stored|see|in|via|ask|sent|shared|pending|not)$")

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = data.get("tool_input") or {}
path = tool_input.get("file_path", "")
text = tool_input.get("content") or tool_input.get("new_string") or ""

found = None
for pattern, label in PATTERNS:
    for m in re.finditer(pattern, text):
        value = m.group(m.lastindex) if m.lastindex and m.lastindex > 1 else m.group(0)
        if label == "a password, token or key" and PLACEHOLDER.match(value):
            continue
        found = label
        break
    if found:
        break

if found:
    reason = (
        f"Secret check: this edit to {path or 'a file'} looks like it contains {found}. "
        "This repo is shared on GitHub. Store real logins in a password manager and write only where they are kept. "
        "Approve only if this is a fake or test value."
    )
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}))

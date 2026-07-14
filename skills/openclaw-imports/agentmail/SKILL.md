---
name: agentmail
description: Send and receive emails using AgentMail
env:
  - AGENTMAIL_API_KEY
---

# AgentMail Skill

Use curl commands against the AgentMail API, or Python's `urllib` when the API key has special characters that bash mangles.

## API Key

Lives in `~/.openclaw/.env`:
```
AGENTMAIL_API_KEY=your...rce it with `source ~/.openclaw/.env` before curl commands,
or read it directly in Python. See `references/setup.md` for full auth details.

## API Base URL

```
https://api.agentmail.to/v0
```

## Authentication

```
Authorization: Bearer $AGENT...L_KEY
```

The API key lives in `~/.openclaw/.env` — source that file before using the variable.
See `references/setup.md` for key location, auth gotchas, and verification steps.

## Common Operations

### List inboxes

```bash
source ~/.openclaw/.env
curl -s -H "Authorization: Bearer $AGENT...EY" \
  https://api.agentmail.to/v0/inboxes
```

### Send an email

```bash
source ~/.openclaw/.env
curl -s -X POST \
  -H "Authorization: Bearer $AGENT...EY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["recipient@example.com"],
    "subject": "Hello from OpenClaw",
    "text": "This email was sent by my AI assistant."
  }' \
  https://api.agentmail.to/v0/inboxes/{inbox_id}/messages/send
```

### Send HTML email

AgentMail supports the `html` field for formatted emails. Use this when markdown rendering matters (tables, bold, headers).

```python
import json, urllib.request
payload = json.dumps({
    "to": ["recipient@example.com"],
    "subject": "HTML Email",
    "text": "Plain text fallback",
    "html": "<h1>Hello</h1><p>This is <b>HTML</b></p>"
}).encode()
```

### List messages in an inbox

```bash
source ~/.openclaw/.env
curl -s -H "Authorization: Bearer $AGENT...EY" \
  https://api.agentmail.to/v0/inboxes/{inbox_id}/messages
```

### Reply to a message

```bash
source ~/.openclaw/.env
curl -s -X POST \
  -H "Authorization: Bearer $AGENT...EY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thanks for your email!"}' \
  https://api.agentmail.to/v0/inboxes/{inbox_id}/messages/{message_id}/reply
```

## Python Send (for special chars in API key)

```python
import os, json, urllib.request
key = os.environ.get('AGENTMAIL_API_KEY')
payload = json.dumps({
    "to": ["recipient@example.com"],
    "subject": "Subject",
    "text": "Body"
}).encode()
req = urllib.request.Request(
    'https://api.agentmail.to/v0/inboxes/smith-agent@agentmail.to/messages/send',
    data=payload,
    headers={
        'Authorization': f'Bearer {key}',
        'Content-Type': 'application/json'
    },
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    print(resp.read().decode())
```

## Pitfalls

- The `text` field does NOT render markdown — use `html` field for formatted content
- Email clients (Outlook, Gmail) strip external CSS — always use inline styles in HTML emails
- Always include both `text` (plain fallback) and `html` fields in payload

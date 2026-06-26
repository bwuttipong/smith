# Sending Email via AgentMail (Python/urllib)

The AgentMail curl examples work for simple cases, but **when the API key contains special characters** (e.g. `$`, `{`, `}`, `!`), curl string interpolation in bash will mangle or fail to send the `Authorization` header with the correct value.

In those cases, use Python's built-in `urllib` instead — it handles special characters in strings correctly because Python never passes them through a shell.

## Prerequisite

The API key lives in `~/.openclaw/.env`:
```
AGENTMAIL_API_KEY=yourkeyhere
```

Source it before using, or read it from Python:
```python
import os
# Read from the env file
with open(os.path.expanduser('~/.openclaw/.env')) as f:
    for line in f:
        line = line.strip()
        if line.startswith('AGENTMAIL_API_KEY='):
            key = line.split('=', 1)[1].strip('"').strip("'")
            break
```

## Send an Email

```python
import json, urllib.request

payload = json.dumps({
    "to": ["recipient@example.com"],
    "subject": "Your Subject",
    "text": "Your email body"
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

with urllib.request.urlopen(req, timeout=10) as resp:
    result = json.loads(resp.read().decode())
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

## List Inbox Messages

```python
req = urllib.request.Request(
    'https://api.agentmail.to/v0/inboxes/smith-agent@agentmail.to/messages',
    headers={'Authorization': f'Bearer {key}'}
)
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read().decode())
for msg in data.get('messages', []):
    print(f"from: {msg.get('from', {}).get('email', '?')}")
    print(f"subject: {msg.get('subject', '?')}")
    print(f"preview: {msg.get('text', '')[:200]}")
```

## API Details

- **Base URL**: `https://api.agentmail.to/v0`
- **Auth**: Bearer token in `Authorization` header (NOT query param — `/v0` uses Bearer)
- **Inbox ID**: `smith-agent@agentmail.to`
- **Send endpoint**: `POST /v0/inboxes/{inbox_id}/messages/send`
- **List endpoint**: `GET /v0/inboxes/{inbox_id}/messages`
- **Reply endpoint**: `POST /v0/inboxes/{inbox_id}/messages/{message_id}/reply`

## Troubleshooting

| Symptom | Likely cause |
|---------|-------------|
| `"Forbidden"` | API key has special chars that bash mangled — use Python/urllib instead |
| `"Unauthorized"` | Wrong auth method — must use Bearer header, not `?api_key=` query param |
| `"Route not found"` | Using `/v1/` endpoints — this inbox uses the `/v0/` API |

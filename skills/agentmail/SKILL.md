---
name: agentmail
description: Send and receive emails using AgentMail
env:
  - AGENTMAIL_API_KEY
---

# AgentMail Skill

Use the `exec` tool to run curl commands against the AgentMail API.

## API Base URL

```
https://api.agentmail.to/v0
```

## Authentication

Include your API key in the Authorization header:

```
Authorization: Bearer $AGENTMAIL_API_KEY
```

## Common Operations

### List inboxes

```bash
curl -s -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  https://api.agentmail.to/v0/inboxes
```

### Create an inbox

```bash
curl -s -X POST -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"display_name": "My Agent"}' \
  https://api.agentmail.to/v0/inboxes
```

### Send an email

```bash
curl -s -X POST -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": ["recipient@example.com"],
    "subject": "Hello from OpenClaw",
    "text": "This email was sent by my AI assistant."
  }' \
  https://api.agentmail.to/v0/inboxes/{inbox_id}/messages/send
```

### List messages in an inbox

```bash
curl -s -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  https://api.agentmail.to/v0/inboxes/{inbox_id}/messages
```

### Reply to a message

```bash
curl -s -X POST -H "Authorization: Bearer $AGENTMAIL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Thanks for your email!"}' \
  https://api.agentmail.to/v0/inboxes/{inbox_id}/messages/{message_id}/reply
```
---
name: line
version: 1.0.0
description: LINE Messaging API webhook handler for Smith (Work)
channel: line
commands:
  - /start
  - /help
  - /status
  - /briefing
  - /tasks
  - /traffic
  - /email
  - /ping
---

# LINE Messaging API - Smith (Work)

## Overview

Webhook-based LINE bot handler. Receives messages via LINE Messaging API,
validates signatures, and routes commands to handlers.

## Setup

### 1. Credentials

Save to `~/.config/smith/.env`:

```bash
LINE_CHANNEL_ID=2010426394
LINE_CHANNEL_SECRET=your_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
```

### 2. Expose webhook endpoint

LINE requires a public HTTPS URL. Use one of:

| Method | Command |
|--------|---------|
| ngrok | `ngrok http 8080` |
| Cloudflare Tunnel | `cloudflared tunnel --url http://localhost:8080` |

Copy the HTTPS URL (e.g. `https://abc123.ngrok-free.app`).

### 3. Configure webhook in LINE Developers Console

1. Go to [developers.line.biz/console](https://developers.line.biz/console/)
2. Select your Messaging API channel
3. Go to **Messaging API** tab
4. Set **Webhook URL** to `https://your-tunnel-url/`
5. Click **Verify**
6. Enable **Use webhook** toggle

### 4. Run the handler

```bash
# Option A: Using run.sh (loads env automatically)
bash skills/line/run.sh

# Option B: Manual
source ~/.config/smith/.env
python3 skills/line/handler.py
```

### 5. Test

Open LINE on your phone, search for your Official Account, send `/ping`.
You should get `pong` back.

## Architecture

```
LINE User → LINE Platform → HTTPS POST (webhook) → handler.py
                                                     ↓
                                              validate signature
                                                     ↓
                                              route command
                                                     ↓
                                              reply via API
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `LINE_CHANNEL_SECRET` | Yes | - | For signature validation |
| `LINE_CHANNEL_ACCESS_TOKEN` | Yes | - | For sending replies |
| `LINE_CHANNEL_ID` | No | - | Channel ID (reference) |
| `LINE_WEBHOOK_PORT` | No | 8080 | HTTP server port |
| `LINE_OWNER_USER_IDS` | No | - | Comma-separated allowed user IDs |

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Intro message |
| `/help` | Show available commands |
| `/status` | Health check, uptime, env status |
| `/briefing` | Morning/evening digest (placeholder) |
| `/tasks` | Todoist summary (placeholder) |
| `/traffic` | Commute traffic (placeholder) |
| `/email` | Unread AgentMail count (placeholder) |
| `/ping` | Quick health check |

## Signature Validation

LINE sends an `X-Line-Signature` header with every webhook POST.
The handler validates it using HMAC-SHA256 with the channel secret.

```python
mac = hmac.new(channel_secret, request_body, hashlib.sha256)
expected = base64.b64encode(mac.digest()).decode()
hmac.compare_digest(expected, signature_header)
```

## Files

| File | Purpose |
|------|---------|
| `handler.py` | Webhook server + command routing |
| `run.sh` | Launcher (loads .env, runs handler) |
| `SKILL.md` | This documentation |

## Limits

- LINE free tier: 1,000 push messages/month
- Reply tokens expire in ~30 seconds (must reply quickly)
- Webhook must respond with HTTP 200 within ~5 seconds

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "invalid signature" | Check CHANNEL_SECRET matches console |
| No replies | Check CHANNEL_ACCESS_TOKEN is valid |
| Webhook verify fails | Ensure tunnel is running and URL is correct |
| 403 on POST | Signature validation failing — check secret |

# AgentMail Setup

## API Key Location

The `AGENTMAIL_API_KEY` environment variable is defined in:

```
~/.openclaw/.env
```

This is the only place the key lives — it is **not** in `~/.hermes/.env`, `~/Smith/.env`, or any profile-level env file.

## Finding the Key

```bash
source ~/.openclaw/.env
echo $AGENTMAIL_API_KEY
```

## Inbox

- **Address:** `smith-agent@agentmail.to`
- **API Base:** `https://api.agentmail.to/v0`
- **Auth:** Bearer token via `Authorization: Bearer $AGENT..._KEY` header

## Common Gotchas

- The key contains special characters — `curl` with `$AGENTMAIL_API_KEY` inline can fail due to shell escaping. Prefer `urllib` / Python `requests` with the header set directly, or `source` the env file first before using the variable in a shell command.
- The v0 API uses Bearer auth; query-param auth (`?api_key=...`) returns 401 Unauthorized.
- The v1 API endpoint (`/v1/inbox?api_key=...`) returns 404 NotFound — don't use it.

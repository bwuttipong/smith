---
name: gog
description: Google Workspace CLI for Gmail, Calendar, Drive, Contacts, Sheets, and Docs.
homepage: https://gogcli.sh
metadata: {"clawdbot":{"emoji":"🎮","requires":{"bins":["gog"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/gogcli","bins":["gog"],"label":"Install gog (brew)"}]}}
---

# gog

Use `gog` for Gmail/Calendar/Drive/Contacts/Sheets/Docs. Requires OAuth setup.

Setup (once)
- `gog auth credentials /path/to/client_secret.json`
- `gog auth add you@gmail.com --services gmail,calendar,drive,contacts,sheets,docs`
- `gog auth list`

Common commands
- Gmail search: `gog gmail search 'newer_than:7d' --max 10`
- Gmail send: `gog gmail send --to a@b.com --subject "Hi" --body "Hello"`
- Calendar: `gog calendar events <calendarId> --from <iso> --to <iso>`
- Drive search: `gog drive search "query" --max 10`
- Contacts: `gog contacts list --max 20`
- Sheets get: `gog sheets get <sheetId> "Tab!A1:D10" --json`
- Sheets update: `gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED`
- Sheets append: `gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS`
- Sheets clear: `gog sheets clear <sheetId> "Tab!A2:Z"`
- Sheets metadata: `gog sheets metadata <sheetId> --json`
- Docs export: `gog docs export <docId> --format txt --out /tmp/doc.txt`
- Docs cat: `gog docs cat <docId>`

Notes
- Set `GOG_ACCOUNT=you@gmail.com` to avoid repeating `--account`.
- For scripting, prefer `--json` plus `--no-input`.
- Sheets values can be passed via `--values-json` (recommended) or as inline rows.
- Docs supports export/cat/copy. In-place edits require a Docs API client (not in gog).
- Confirm before sending mail or creating events.

## Pitfalls

### OAuth Token Expiry
Tokens expire after ~2 weeks of inactivity. Symptom: `invalid_grant "Token has been expired or revoked"` on any gog command.

**Re-auth workflow (agent-driven):**
1. Run `gog auth add <email> --services <list>` in `background=true`
2. Poll the process — it prints an auth URL and starts a local HTTP server on a random port
3. Send the user the full auth URL to open in their browser
4. User signs in → Google redirects to `127.0.0.1:<port>/oauth2/callback` → gog captures it automatically
5. Process completes with exit code 0

**Do NOT** try to curl the callback URL yourself — the local server only lives as long as the background process, and it restarts with a new port each time. Just give the user the URL.

Check token age: `gog auth list` — the timestamp column shows last refresh.

### Calendar Quick Check Pattern
For "do I have work tomorrow" type queries:
```bash
gog calendar events primary --from "YYYY-MM-DDT00:00:00+07:00" --to "YYYY-MM-DDT23:59:59+07:00" --json
```
Use `primary` as calendarId for the default calendar. Parse the JSON `events` array — if empty, no events that day.

### Prefer gog over google-workspace
The `gog` CLI is simpler and already authenticated for this user. Use it as the default for Google Workspace tasks (Gmail, Calendar, Drive, Sheets, Docs) instead of the heavier `google-workspace` Python wrapper.

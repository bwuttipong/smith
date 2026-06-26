# Port Map — Smith Local Stack (verified 2026-06-24)

## Open ports on Jeff's Mac

| Port  | Process                        | Framework  | Bind         | Notes                                                                                  |
|-------|--------------------------------|------------|--------------|----------------------------------------------------------------------------------------|
| 18789 | node (openclaw gateway)        | openclaw   | 127.0.0.1    | Primary openclaw gateway. Hosts the smith profile. Web UI: /chat?session=main           |
| 18790 | socat + cloudflared            | openclaw   | 0.0.0.0      | External tunnel forward to 18789 (cloudflared + socat)                                 |
| 9119  | python3.11 (hermes dashboard)  | hermes     | 127.0.0.1    | **Only bound if you start `hermes dashboard` on demand.** Not the gateway.              |
| 11434 | ollama                         | ollama     | 127.0.0.1    | Local LLM inference                                                                    |
| 7000  | ControlCenter                 | macOS      | 0.0.0.0      | macOS AirPlay/Handoff (system)                                                         |
| 5000  | ControlCenter                 | macOS      | 0.0.0.0      | macOS AirPlay/Handoff (system)                                                         |

## The "9119 confusion" — read this

Port 9119 has meant different things at different times on this machine:

- **Default-profile hermes gateway** (when running): binds 9119 directly. The gateway itself is the HTTP server.
- **Smith-profile hermes gateway** (current setup, launchd-managed as `ai.hermes.gateway-smith`): does **NOT** bind 9119. It's messaging-only and runs headless. No HTTP port, no uvicorn.
- **Hermes dashboard** (a separate `hermes dashboard` subprocess): if launched with `--port 9119`, binds 9119. This is the only thing that puts HTTP on 9119 in the smith profile.

So when you `curl 127.0.0.1:9119` and get connection refused, it doesn't mean the gateway is dead — it just means the dashboard isn't running. Check `launchctl list | grep hermes` for gateway state, and `hermes dashboard --status` for the dashboard.

## Verification commands

```bash
# Quick port scan — what's actually listening
lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null | grep -v "Chrome\|rapportd\|ControlCe\|Code\x20H" | head -10

# Probe a specific port
curl -s -I http://127.0.0.1:9119

# Show openclaw gateway status
openclaw status
openclaw status --deep

# Show hermes dashboard status
hermes dashboard --status

# Show hermes gateway (launchd) status
launchctl list | grep hermes
```

## Source-of-truth paths

- openclaw gateway: `/opt/homebrew/lib/node_modules/openclaw/dist/index.js`
- hermes source: `~/.hermes/hermes-agent/`
- hermes dashboard entry: `~/.hermes/hermes-agent/hermes_cli/subcommands/dashboard.py`
- hermes web build: `~/.hermes/hermes-agent/web/dist/` (must exist for `hermes dashboard` to serve UI)
- agent profile home: `~/.hermes/profiles/smith/`
- smith gateway logs: `~/.hermes/profiles/smith/logs/gateway.log` and `gateway.error.log`
- smith launchd plist: `~/Library/LaunchAgents/ai.hermes.gateway-smith.plist`
- default launchd plist: `~/Library/LaunchAgents/ai.hermes.gateway.plist`

## Lessons from 2026-06-24

- When the user says "restart the gateway" in the smith profile, they mean the **launchd-managed** `ai.hermes.gateway-smith`, not the openclaw gateway on 18789 and not the dashboard.
- The right command is `hermes gateway restart` (not `launchctl kickstart` directly, and **definitely not** manual `kill`).
- After restart, verify with `tail ~/.hermes/profiles/smith/logs/gateway.log` — look for "✓ telegram connected". A process with PID ≠ healthy.
- The MCP `qmd` server fails to connect on every gateway boot. Not blocking, but if you see "unhandled errors in a TaskGroup (1 sub-exception)" in `gateway.error.log`, that's the cause.

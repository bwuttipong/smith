# Launch commands — Smith Local Stack

All commands assume macOS. Run as Jeff (not root). Hermes uses `terminal(background=true, notify_on_complete=true)` — never shell-level `nohup &` (Hermes' soft guard blocks it).

**Mental model — the three things you might want to start/stop:**

1. **openclaw gateway** (port 18789) — wraps the smith profile, always running.
2. **hermes gateway** (no port in smith profile) — launchd-managed messaging service, runs headless, no HTTP.
3. **hermes dashboard** (port 9119, if launched) — separate web UI; you start it on demand.

Don't conflate them. The user asking "restart the gateway" almost always means #2 (the launchd service), not #3.

---

## openclaw gateway (port 18789)

Already running. To check or restart:

```bash
# Status
openclaw status
openclaw status --deep

# Open the control panel (tokenized URL)
openclaw dashboard
# Opens: http://127.0.0.1:18789/chat?session=main
```

If the gateway is dead, restart via launchd or the openclaw CLI per local setup. Not covered here.

---

## hermes GATEWAY (messaging — no web port in smith profile)

This is the launchd-managed service `ai.hermes.gateway-smith`. It runs **headless** (telegram polling, no HTTP port) in the smith profile. **Do not expect anything on port 9119 from this service.** To get a web UI on 9119 you must start the hermes dashboard separately (see next section).

**Restart the supervised way — never kill the process manually:**

```bash
# Correct: launchd sequences stop+start cleanly
hermes gateway restart

# Verify
launchctl list | grep hermes                       # should show ai.hermes.gateway-smith with a PID
tail -20 ~/.hermes/profiles/smith/logs/gateway.log
# Look for: "✓ telegram connected" and "Gateway running with N platform(s)"
```

**Why not manual kill?** If the old PID still holds the Discord bot token when a new gateway starts, you'll get:
```
ERROR gateway.platforms.base: [Discord] Discord bot token already in use (PID XXXX).
```
…and the new gateway exits cleanly with non-zero status. `hermes gateway restart` handles the sequencing correctly so this doesn't happen.

**Also don't try to start a foreground gateway** with `python -m hermes_cli.main gateway run` — the supervised service detects it and refuses:
```
✗ A gateway is already running under launchd for this profile.
  Pass --force to start a foreground gateway anyway (not recommended).
```

**Two launchd services exist — don't conflate them:**

```bash
launchctl list | grep hermes
# ai.hermes.gateway          <- default profile (not our concern on smith)
# ai.hermes.gateway-smith    <- THIS is the smith gateway
```

To poke launchd directly for smith: `launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway-smith`.

**Quick health check after restart:**

```bash
ps -p <pid> -o pid,command                                    # process alive
grep -E "✓ telegram connected|Gateway running" \
  ~/.hermes/profiles/smith/logs/gateway.log | tail -5         # platform actually attached
```

**Known issue (2026-06-24, recurring):** The MCP `qmd` server fails its 3 startup attempts on every gateway boot and gives up:
```
WARNING tools.mcp_tool: MCP server 'qmd' initial connection failed (attempt 3/3), retrying in 4s: unhandled errors in a TaskGroup (1 sub-exception)
WARNING tools.mcp_tool: MCP server 'qmd' failed initial connection after 3 attempts, giving up
```
The gateway runs fine without it (qmd is not required for telegram/discord routing), but if you ever need qmd, restart the gateway and tail `gateway.error.log` for the same `unhandled errors in a TaskGroup` signature.

---

## hermes dashboard (port 9119)

Not running by default. Launch it on demand:

```bash
# Foreground (interactive)
hermes dashboard --host 127.0.0.1 --port 9119 --skip-build

# Background (long-lived daemon)
# Use Hermes terminal tool with background=true
hermes dashboard --host 127.0.0.1 --port 9119 --skip-build --no-open
# Then open: http://127.0.0.1:9119

# Stop all running hermes dashboards
hermes dashboard --stop

# List running
hermes dashboard --status
```

## Pre-flight: build the web UI

`--skip-build` requires the web dist to exist. If it doesn't:

```bash
cd ~/.hermes/hermes-agent/web && npm run build
```

This step takes a few minutes on first run. Not needed if `~/.hermes/hermes-agent/web/dist/` already exists.

## Auth

The hermes dashboard requires authentication (password or OAuth) on every bind as of June 2026 hardening. Bind to 127.0.0.1 + tunnel to keep it local. The `--insecure` flag is a no-op as of this version.

## Background process pattern (Hermes)

```python
# Good — Hermes tracks lifecycle
terminal(command="hermes dashboard --port 9119 --skip-build --no-open", background=True, notify_on_complete=True)

# Bad — soft guard blocks it
nohup hermes dashboard --port 9119 --skip-build --no-open &
```

## Stopping everything

```bash
hermes dashboard --stop          # stop hermes dashboard
# openclaw gateway managed by launchd — use `launchctl` or openclaw CLI
# hermes gateway managed by launchd — use `hermes gateway restart` (don't kill manually)
```

---
name: local-service-discovery
description: "Discover and open local web UIs the user runs on their own machine — openclaw gateway, ollama, hermes control panel, home dashboards, dev servers, etc. Use when the user says 'open X web' / 'open the dashboard' / 'go to the control panel' / 'open local X' and X is plausibly a local service, OR when no public URL is obviously the answer. Triggers on 'open the gateway', 'open ollama', 'open hermes control', 'open localhost', 'go to the panel', 'dashboard please'. Does NOT apply to opening public websites (github.com, docs, etc.) — when in doubt, check what's listening on localhost first."
---

# Local Service Discovery

A recurring pattern: the user runs a fleet of local services (openclaw gateway, ollama, hermes control panel, dev servers, home dashboards) and asks "open the web UI for X" expecting the local instance — not the public homepage, not the docs site.

## Core Rule

**When the user says "open X web/dashboard/control panel" and X is something they (probably) run locally, check what's listening on localhost BEFORE defaulting to a public URL.** When in doubt, ask — but only AFTER running the discovery scan, since you can often resolve it from listening ports alone.

## Discovery Procedure

Run these in parallel:

```bash
# 1. What's listening locally?
lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null

# 2. Cross-reference running processes for known services
ps aux | grep -iE "(openclaw|gateway|hermes|ollama|jupyter|notebook|homeassistant|node.*server|python.*app|uvicorn|gunicorn)" | grep -v grep

# 3. If you have a domain-of-truth (e.g. config.yaml), grep for port assignments
grep -iE "(port|host|url|base_url)" ~/.hermes/config.yaml 2>/dev/null
```

Then map listening ports → known services. Open the right one.

## Known Local Services in This Stack (Jeff's machine)

| Service | Port | URL pattern | How to verify |
|---|---|---|---|
| **OpenClaw Gateway** (control panel) | `18789` | `http://127.0.0.1:18789/chat?session=main` | `lsof -iTCP:18789` |
| **Ollama** | `11434` | `http://127.0.0.1:11434` | `lsof -iTCP:11434` |
| **Hermes agent local** | varies | check `hermes gateway status` | `ps aux \| grep hermes` |

When the user says "open hermes web" or "open the control panel" with no other context, the openclaw gateway at 18789 is the default for this user. Auth: gateway token (paste in the form, or run `openclaw dashboard` to get a tokenized URL).

## Pitfalls

### 🚨 Don't default to public docs / marketing sites
If the user says "open hermes web", the local control panel is far more likely than https://hermes-agent.nousresearch.com/docs. The docs site is for learning; the local panel is for using. If you pick the public site, you'll be corrected.

### 🚨 Headless browser ≠ user's screen
The `browser_navigate` tool drives a headless browser session that is often NOT visible on the user's screen. Navigating somewhere is not the same as "opening it" for the user. After navigation, **always** either:
- give them the URL to paste in their own browser, OR
- run a local command that opens a real browser tab (`open http://...` on macOS, `xdg-open` on linux), OR
- confirm they have a way to see the headless session (rarely the case)

If the user is on a desktop, the `open` command (macOS) / `xdg-open` (linux) is the right tool. The headless browser is for reading/scraping/automating, not for "showing" the user something.

### 🚨 Tokenized URLs
Local control panels often require a session token. If you see an auth form, **don't** try to paste a token from memory or guess — run the documented command to mint a fresh URL (e.g. `openclaw dashboard`). Then offer to copy it for the user.

### 🚨 "Open X" without context — when to ask
If discovery returns multiple plausible services (e.g. two things listening on different ports, both match the name), ask. A 5-second clarifying question beats opening the wrong thing. If only one matches, just go.

### 🚨 Don't waste a turn saying "it is open" when nothing visibly changed
If you called `browser_navigate` and the user's screen didn't change (because the browser is headless), saying "it is open!" is confidently wrong. Either route the URL to the user's actual browser or admit the gap.

## Quick Decision Tree

```
User: "open X web" / "open the dashboard" / "open the control panel"
        │
        ├── Is X clearly a public site (github, docs, a SaaS)?
        │     YES → navigate. DONE.
        │     NO  ↓
        │
        ├── Run discovery (lsof + ps + config grep)
        │     │
        │     ├── Found a clear local match → open it locally
        │     │   (and tell user the URL in case headless)
        │     │
        │     ├── Found multiple matches → ask user which one
        │     │
        │     └── Found nothing local → ask user, or fall back to public
        │
        └── Confirm: did the user actually see something open?
              NO → give them the URL or use `open` command
```

## Examples

**Good — local-first:**
> User: "open the openclaw web"
> Action: `lsof -iTCP:18789` → find gateway → `browser_navigate http://127.0.0.1:18789/chat?session=main` + `open http://127.0.0.1:18789/chat?session=main` (so user sees a real tab)

**Bad — assumed public:**
> User: "open the openclaw web"
> Action: navigate to github.com/openclaw/openclaw ❌ (user wanted the running instance)

**Good — disclosure:**
> User: "open hermes web"
> Action: discovery → gateway on 18789 → "Got the local control panel open at http://127.0.0.1:18789/chat?session=main. Headless browser here, so if you don't see a new tab, paste that URL in your browser — or say the word and I'll `open` it in your default."

## When NOT to use this skill

- User is clearly asking for a public URL ("go to github.com/...", "open the React docs")
- The URL is in conversation context already
- User is asking how to *install* a service, not open a running one
- The "web UI" is actually a CLI tool or TUI

## Related

- `user-communication-preferences` — tone rules for confirming/correcting user
- `hermes-agent` skill — for `hermes` CLI commands (note: that's the framework, not the local control panel — the local control panel is the *openclaw* gateway)
- `openclaw-config-maintenance` — for changing openclaw.json, separate concern

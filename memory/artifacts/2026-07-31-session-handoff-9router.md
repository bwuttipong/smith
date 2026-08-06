# Session Handoff — 2026-07-31

## Goal
Set up and configure **9Router Proxy** as a provider for both **OpenClaw** and **Hermes Agent**, configure system environment variables, clean up old providers, set primary agent models, and resolve diagnostic warnings.

---

## Changes Implemented

### 1. Environment & API Key Setup
- Added `NINE_ROUTER_API_KEY` to Hermes environment file (`~/Smith/.hermes/.env`).
- Injected `NINE_ROUTER_API_KEY` into OpenClaw service environment file (`~/.openclaw/service-env/ai.openclaw.gateway.env`).
- Updated `OPENCLAW_SERVICE_MANAGED_ENV_KEYS` to include `NINE_ROUTER_API_KEY`.

### 2. OpenClaw Provider & Agent Model Reconfiguration
- Configured `9router-proxy` in `~/.openclaw/openclaw.json` pointing to `http://localhost:20128/v1`.
- Populated `9router-proxy` provider model list with active models from 9Router (`ag/gemini-3-flash-agent`, `ag/gemini-3.6-flash-high`, `ag/claude-sonnet-4-6`, `gc/gemini-2.5-flash`, etc.).
- Cleaned up obsolete providers: completely removed `xiaomi`, `ollama`, and `nvidia` from `openclaw.json` (providers, plugins.allow, plugins.entries, and agents.defaults.models).
- Set `smith` agent primary model to `9router-proxy/ag/gemini-3-flash-agent` with fallbacks (`9router-proxy/ag/gemini-3.6-flash-high`, `9router-proxy/ag/claude-sonnet-4-6`, `9router-proxy/gc/gemini-2.5-flash`).
- Re-mapped all other subagents (`kermit`, `cookie`, `beaker`, `fozzie`, `samantha`, `bunsen`, `janitor`) to use `9router-proxy` models.

### 3. Hermes Agent Configuration
- Added `nine-proxy` provider definition to `~/.hermes/config.yaml`:
  ```yaml
  providers:
    nine-proxy:
      api_key: ${NINE_ROUTER_API_KEY}
      base_url: http://localhost:20128/v1
      api_mode: chat_completions
  ```
- Now `/model nine-proxy/...` works directly inside Hermes Agent CLI and desktop.

### 4. OpenClaw Service Health & Verification
- Ran `openclaw doctor --fix` to clean configuration references.
- Restarted OpenClaw gateway daemon (`openclaw gateway restart`).
- Verified service state: **Active / Running** (PID 52254, probe OK).

---

## Current Status & Next Steps
- **9Router Proxy**: Operational on `http://localhost:20128/v1`.
- **OpenClaw Gateway**: Healthy and using `9router-proxy/ag/gemini-3-flash-agent` as Smith's primary model.
- **Hermes Agent**: `nine-proxy` provider registered in `config.yaml`.
- **Ready for resumption**: Any new session in OpenClaw or Hermes can freely use 9Router proxy models.

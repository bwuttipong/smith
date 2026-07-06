# Agent Ports — Current Mapping

Last verified: 2026-07-05

## Running Agents

| Agent | Port | Process | Status |
|-------|------|---------|--------|
| Hermes (dashboard) | 9120 | hermes_cli.main dashboard | LIVE |
| Hermes (gateway) | 9120 | hermes_cli.main gateway run | LIVE |
| OpenClaw | 18789 | openclaw gateway | LIVE |
| Ollama | 11434 | ollama serve | LIVE |
| ZCode/Codex | 3001 | — | OFFLINE |
| Claude Code | 3002 | — | OFFLINE |
| Paperclip | 3100 | — | OFFLINE |

## Notes

- Hermes.app (Electron) runs separately from the CLI agent
- OpenClaw Control UI is a web app, not just an API
- Ollama model: `gemma4:12b-mlx` (7.6GB)
- Health check timeout: 3 seconds per agent

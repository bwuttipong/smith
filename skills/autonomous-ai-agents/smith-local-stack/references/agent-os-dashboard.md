# Agent OS Dashboard

Local mission control dashboard for managing AI agents.

## Location
`~/Workspaces/agentos/source/`

## Stack
- Next.js 16 + TypeScript
- Tailwind CSS
- Framer Motion (animations)
- Lucide React (icons)

## Start
```bash
cd ~/Workspaces/agentos/source && PORT=3737 npm run start
```

## Build (after changes)
```bash
cd ~/Workspaces/agentos/source && PORT=3737 npm run build
```

## Agents configured (verified 2026-07-05)
| Agent | Port | Real Port | Chat API | Status |
|-------|------|-----------|----------|--------|
| Hermes | 9119 | 9120 | via OpenClaw gateway | LIVE (needs auth) |
| OpenClaw | 18789 | 18789 | `openclaw agent -m "..." --json` | LIVE |
| ZCode (Codex) | CLI only | — | not wired | OFFLINE |
| Claude Code | CLI only | — | not wired | OFFLINE |
| Ollama | 11434 | 11434 | `curl localhost:11434/api/chat` | LIVE |
| Paperclip | 3100 | — | not wired | OFFLINE |

## API Routes (working)
- `GET /api/agents/health` — pings all 6 agents, returns `[{id, name, status}]`
- `POST /api/chat` — sends message to agent (`{agent, message}` → `{reply}`)
- `POST /api/obsidian` — saves chat to Obsidian vault as markdown (`{agent, messages}`)
- `GET /api/obsidian` — lists saved chat files

## Obsidian sync
Saves to: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/Agent OS/YYYY-MM-DD.md`
Format: `## AgentName — HH:MM` sections with **You:** / **Agent:** messages

## Standards framework (from buildermethods/agent-os)
- `~/Workspaces/agentos/standards/` — coding standards as markdown
- `~/Workspaces/agentos/commands/` — 5 command definitions (discover, inject, index, plan, shape)
- `~/Workspaces/agentos/specs/` — feature specs (timestamped folders)
- `~/Workspaces/agentos/product/` — mission, roadmap, tech-stack

## Build after changes
```bash
cd ~/Workspaces/agentos/source && PORT=3737 npm run build && PORT=3737 npm run start
```

## Source references
- Julian Goldie's Agent OS vault: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/Julian Goldie SEO/How to Build Your Own Agent Operating System!`
- buildermethods/agent-os (standards framework): https://github.com/buildermethods/agent-os

## Key lesson
Jeff wants functional features, not just scaffolding. When he says "build X", wire real API calls and integrations before declaring done. (2026-07-05)

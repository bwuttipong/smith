---
name: building-agent-os
description: "Build local AI agent dashboards with Next.js — wire real agent connections, status polling, Obsidian sync."
platforms: [macos, linux]
---

# Building Agent OS Dashboards

When the user wants to build a local AI agent dashboard (mission control), follow this workflow.

## Stack
- Next.js 16 (App Router) + TypeScript
- Tailwind CSS + clsx + twMerge
- Framer Motion (animations)
- Lucide React (icons)

## Agent Connection Pattern

Each agent has a different connection method. Use switch/case dispatch:

| Agent | Method | Port | API |
|-------|--------|------|-----|
| Hermes | OpenClaw CLI | 9120 | `openclaw agent -m "..." --json` |
| OpenClaw | OpenClaw CLI | 18789 | `openclaw agent -m "..." --json` |
| Ollama | Direct API | 11434 | `curl http://localhost:11434/api/chat` |
| ZCode/Codex | Not wired | 3001 | Return 501 |
| Claude Code | Not wired | 3002 | Return 501 |
| Paperclip | Not wired | 3100 | Return 501 |

## API Routes to Build

1. **`/api/agents/health`** — GET, pings all agents, returns status array
2. **`/api/chat`** — POST, sends message to agent, returns reply
3. **`/api/obsidian`** — POST (save), GET (list), syncs to vault

## Health Check Pattern

```typescript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 3000);
const res = await fetch(agent.url, { signal: controller.signal });
clearTimeout(timeout);
```

## Obsidian Vault Path

Default: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/Agent OS/`

Save format: `YYYY-MM-DD.md` with `## AgentName — HH:MM` sections.

## Dashboard Component Structure

- Sidebar with agent list + status badges
- ChatPanel per agent with message history
- Voice input (browser SpeechRecognition)
- Save to Obsidian button
- Status polling every 30 seconds

## Pitfalls

- Hermes runs on port 9120 (not 9119 as some docs say)
- OpenClaw gateway is on 18789 (not 4444)
- `openclaw agent` requires the gateway to be running
- Ollama model names must match exactly (e.g., `gemma4:12b-mlx`)
- Voice recognition only works in Chrome/Safari

## References

- See `references/agent-ports.md` for current port mapping
- See `references/obsidian-sync.md` for vault integration details

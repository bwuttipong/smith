---
id: entities/agent-os
pageType: entity
title: Agent OS
created: 2026-07-05
updated: 2026-07-05
type: entity
tags: [project, dashboard, nextjs, ai-agents, mission-control]
sources: [Smith/memory/2026-07-05.md]
confidence: high
---

# Agent OS

Local "Mission Control" dashboard for Jeff's AI agents. Next.js 16 + Tailwind v4 + Framer Motion, at `~/Workspaces/agentos` (app in `source/`, runs on **:3737**). One screen to chat with all agents, plus Goals + Journal pages backed by the Obsidian vault.

- **Repo:** only `source/` is git-tracked (branch `main`); the `agentos/` root is not versioned.
- **Preview launch config:** `~/Smith/.claude/launch.json` (name `agentos-dashboard`).
- **Chat routing:** `source/src/app/api/chat/route.ts` · **Health:** `source/src/app/api/agents/health/route.ts`

## Agent tabs (as of 2026-07-05)

| Agent | Status | Chat | Backend |
|-------|--------|------|---------|
| Hermes | LIVE | ✅ | `hermes -z` one-shot (:9120 app) |
| OpenClaw | LIVE | ✅ | `openclaw agent --agent smith --model xiaomi-token-plan/mimo-v2.5` |
| Ollama | LIVE | ✅ | `localhost:11434/api/chat` (gemma4:12b-mlx) |
| Claude Code | LIVE | ✅ | Free Claude Code proxy → free NVIDIA Nemotron (:8082) |
| ZCode (Codex) | LIVE | ❌ | OpenAI quota exhausted until 2026-07-22 |
| Paperclip | OFFLINE | ❌ | not installed |

## Non-obvious facts

- **OpenClaw ≠ Hermes.** OpenClaw is the multi-agent gateway (agent [[smith]] et al.); Hermes is a separate standalone app on :9120. The dashboard's OpenClaw tab targets the `smith` agent.
- **Health detection is mixed:** port-ping for servers (Hermes/OpenClaw/Ollama/Paperclip), CLI-presence (`which`) for Codex/Claude Code. LIVE = installed/reachable, not "can complete a request."
- **OpenClaw gateway token** is an env secret-ref only the daemon holds; the chat route resolves it live from the daemon process env (survives rotation).
- **Free Claude Code** ([[free-claude-code]]) proxy shares `~/.fcc/.env` with the Step-2 voice-build config.

## Reference

- Session detail + all fixes: `~/Smith/memory/2026-07-05.md`
- Install/troubleshooting docs: `~/Workspaces/agentos/install/*.md`
- Handoff doc: `/private/tmp/agentos-handoff-2026-07-05.md`

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

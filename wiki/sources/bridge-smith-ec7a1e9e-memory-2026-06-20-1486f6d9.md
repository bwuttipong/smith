---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-06-20-1486f6d9
title: "Memory Bridge (smith): 2026-06-20"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-06-20.md
bridgeRelativePath: memory/2026-06-20.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-20T16:37:42.587Z
---

# Memory Bridge (smith): 2026-06-20

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-06-20.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-20T16:37:42.587Z

## Content
```markdown
# 2026-06-20 — Saturday

## Plugin cleanup (7:38 PM)
- Removed stale `opencode-zen` plugin references from config
  - Removed from `plugins.allow` array
  - Removed from `plugins.entries` object
  - Direct file edit at `~/.openclaw/openclaw.json` (API blocked protected paths)
  - Gateway reloaded via SIGUSR1
- Flagged broken primary model: `agents.defaults.model.primary` = `opencode/deepseek-v4-flash-free` (provider not registered)
  - Jeff hasn't responded yet on whether to fix this

- Added OpenCode Zen models (`deepseek-v4-flash-free`, `mimo-v2.5-free`, `north-mini-code-free`, and `nemotron-3-ultra-free`) to `opencode-zen` provider in `openclaw.json` 🎩.
- Restarted OpenClaw gateway service successfully 🔄.

## Groq Provider — Tested 2026-06-20 23:36

Jeff asked: "is Groq provider works properly?" / "I can't use groq/compound how to do?"

**Findings:**
- Groq IS configured in `~/.openclaw/openclaw.json` under `models.providers.groq`
- `GROQ_API_KEY` is set in `~/.openclaw/.env`
- Base URL: `https://api.groq.com/openai/v1` (OpenAI-compatible)
- Plain chat models work fine (live-tested `llama-3.1-8b-instant` — ✅ returned "Hello, how are you today?")
- `groq/compound` and `groq/compound-mini` are NOT accessible with current key — Groq returns 404 `model_not_found`: "The model `compound` does not exist or you do not have access to it."
- Reason: Compound models are gated behind explicit access request (agentic tier with web/code tools)

**Action needed (Jeff):** Apply for Compound access at https://console.groq.com if needed, or use the working models: `groq/llama-3.1-8b-instant`, `groq/llama-3.3-70b-versatile`, `groq/qwen/qwen3-32b`, `groq/openai/gpt-oss-120b`.

**Lesson for me:** When asked about provider status, do a live API test via curl instead of just reading config. Config can say "configured" but the upstream model can still be 404.

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

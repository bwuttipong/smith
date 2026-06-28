---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-freeride-2026-06-26-01d99a82
title: "Memory Bridge (smith): freeride-2026-06-26"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/freeride-2026-06-26.md
bridgeRelativePath: memory/freeride-2026-06-26.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-28T10:41:21.649Z
---

# Memory Bridge (smith): freeride-2026-06-26

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/freeride-2026-06-26.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-28T10:41:21.649Z

## Content
```markdown
# FreeRide Check — 2026-06-26

**24 free models available** via OpenRouter.

## Top 3
1. nvidia/nemotron-3-super-120b-a12b:free — 0.897
2. nvidia/nemotron-3-ultra-550b-a55b:free — 0.883
3. openrouter/owl-alpha — 0.868

## System Health
- **Primary:** ollama/gemma4:31b-cloud
- **Fallbacks (7):** configured — some routes still oddly namespaced (nvidia/openai/gpt-oss-120b, openrouter/openrouter/owl-alpha)
- **Model Cache:** 24 models, just refreshed
- **OpenClaw config:** exists
- **OpenRouter API:** healthy

## Changes from previous run (earlier today)
- No changes detected. Same 24 models, same scores, same config.

## Notes
- Fallback model paths still have that double-namespacing issue (e.g. `nvidia/openai/gpt-oss-120b` instead of `openai/gpt-oss-120b:free`). Might be worth a cleanup pass — those won't resolve correctly on failover.
- Second run today, everything consistent.

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

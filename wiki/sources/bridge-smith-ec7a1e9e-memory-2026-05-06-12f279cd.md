---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-05-06-12f279cd
title: "Memory Bridge (smith): 2026-05-06"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-05-06.md
bridgeRelativePath: memory/2026-05-06.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-05-06T03:51:03.538Z
---

# Memory Bridge (smith): 2026-05-06

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-05-06.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-05-06T03:51:03.538Z

## Content
```markdown
# 2026-05-06

## Discord Typing Indicator Bug (Known Issue)

OpenClaw's Discord integration has a known bug where the "is typing..." indicator gets stuck indefinitely after bot replies. Root cause: keepalive timer fails to clear after message send.

### Fixes if typing gets stuck:
1. `openclaw gateway restart` — most effective workaround
2. Disable streaming in `openclaw.json` under Discord channel config
3. Update OpenClaw (was a regression in v2026.2.24)
4. Check `agents.defaults.llm.idleTimeoutSeconds` if bot stops responding

### Other causes of stuck typing:
- Gateway crash/restart (e.g., 1006 error) — typing stops
- Long tool chains (vision + browsing) — can hold typing for up to 25 min
- LLM timeout — bot may stop responding entirely

## Session Notes
- No discord session visible in session list (discord sessions only appear after activity)
- Asked to "bring current session from Discord" but only telegram session found

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

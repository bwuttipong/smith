---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-05-08-1411-9b099619
title: "Memory Bridge (smith): 2026-05-08-1411"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-05-08-1411.md
bridgeRelativePath: memory/2026-05-08-1411.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-05-08T07:11:48.684Z
---

# Memory Bridge (smith): 2026-05-08-1411

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-05-08-1411.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-05-08T07:11:48.684Z

## Content
```markdown
# Session: 2026-05-08 14:11:48 GMT+7

- **Session Key**: agent:main:telegram:direct:8611951691
- **Session ID**: 892c01c5-fb60-4c55-b85f-210fa94c0fc7
- **Source**: telegram

## Conversation Summary

user: what's new in OpenClaw 2026.5.7
assistant: 

**openclaw v2026.5.7** dropped May 7th — here's what's new:

### 🔧 Fixes
- **ClawHub publishing** — better retry logic for transient dependency failures, plugin publishes now verify every expected package version after publish so maintenance releases recover faster
- **OpenAI** — supports `openai/chat-latest` as an explicit API-key override for the new ChatGPT Instant API alias
- **Cron CLI** — `cron list --json` and `cron show --json` now include computed status (disabled/running/ok/error/skipped/idle)
- **Channels CLI** — new `--all` flag for bundled/catalog channels, model auth moved to `openclaw models auth list`
- **Telegram** — fixed polling watchdog so unrelated outbound API calls can't mask a stuck inbound poller; now honors `accessGroup:*` sender allowlists for DMs and groups
- **WhatsApp** — proactive sends now route through Baileys LID forward mappings properly; fixed captioned media auto-replies sending twice
- **Discord** — fixes cross-channel agent message routing that was misrouting channel IDs; voice capture improved with 2.5s post-speech silence grace
- **Codex approvals** — stops installing the pre-guardian PermissionRequest hook by default so Codex reviewer can approve safe commands first
- **Active Memory** — requires admin scope for global memory toggles
- **Context engine** — invalidates cached assembled context when source history shrinks, fixing stale pre-reset history being reused
- **Cron doctor** — repairs persisted jobs with bad `payload.model` stored as "default"/"null"/blank/JSON null

### 🚀 Improvements
- **Discord voice** — auto-audit permissions (Connect/Speak/Read Message History) before `/vc join`
- **Model providers** — normalized APNG uploads, preserved Gemini 3 tool-call thought-signature replay, accepts legacy `__env__:VAR` custom-provider keys
- **Control UI** — compaction count now shows "N Checkpoint(s)" with expanded session details and modern history cards
- **Subagent registry** — completed session-mode rows now honor `agents.defaults.subagents.archiveAfterMinutes` instead of hardcoded 5-min TTL

---

lots of polish across Telegram, WhatsApp, Discord, and the plugin system. you're up to date, sir 🎩

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

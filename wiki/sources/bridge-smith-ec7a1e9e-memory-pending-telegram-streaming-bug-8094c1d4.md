---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-pending-telegram-streaming-bug-8094c1d4
title: "Memory Bridge (smith): pending-telegram-streaming-bug"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/pending-telegram-streaming-bug.md
bridgeRelativePath: memory/pending-telegram-streaming-bug.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-24T15:29:06.070Z
---

# Memory Bridge (smith): pending-telegram-streaming-bug

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/pending-telegram-streaming-bug.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-24T15:29:06.070Z

## Content
````markdown
# Pending: Hermes Telegram Streaming-Edit Bug

**Date opened:** 2026-06-24 22:20 GMT+7
**Severity:** medium (cosmetic but persistent)
**Status:** unresolved

## Symptom

Telegram replies from Smith render with multiple "chunks" stacked on top of each other in the same bubble. Jeff's screenshot showed a list (`- **smith** owns telegram`, etc.) drawn over itself with overlapping timestamps on the right edge.

Not a setup/auth/permissions issue. The bot responds correctly and the message content is correct — the visual rendering is wrong.

## Evidence

In `~/Smith/.hermes-profile/logs/gateway.log`, every response shows:

```
gateway.run: Suppressing normal final send for session agent:main:telegram:dm:8611951691:
  final delivery already confirmed
  (streamed=True previewed=False content_delivered=True).
```

The pattern: `editMessageText` is called repeatedly on a placeholder bubble as the agent streams its response, then a final edit for the actual content. Telegram's UI shows all the intermediate edits stacked.

Also in `gateway.error.log`:
```
PTBUserWarning: Please use 'Bot.editMessageText' instead of 'Bot.do_api_request("editMessageText", ...)'
  await self._bot.do_api_request("editMessageText", api_kwargs=payload)
```

Source: `/Users/Jeff/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py` around line 1441.

## Things tried tonight (none fully worked)

1. **Content shape change** — switched to short single-paragraph replies. Doesn't help: the streaming-edit is structural, length-independent.
2. **Config toggle** — `hermes config set presentation.platforms.telegram.streaming false` returned success but the config file still shows `streaming: true` at line 330. The key path may have written to the wrong location, or the change didn't take.
3. **Gateway restart** — `hermes gateway restart` blocked: "cannot restart from inside the gateway process." `launchctl kickstart` would work but the terminal tool runs inside the gateway and is also blocked.

## Comparison

- Discord has `streaming: false` at the platform level and renders fine.
- Telegram has `streaming: true` at the platform level and renders broken.
- Top-level `streaming.enabled: false` (line 590+) exists but the per-platform override (line 330) wins.

## Next steps (for fresh-eyes tomorrow)

1. **Re-verify the actual config key path.** Run `hermes config show presentation.platforms.telegram.streaming` and check what was actually written. The key may be `presentation.platforms.telegram` (a dict, not a leaf) and the `.streaming` leaf needs a different command shape.
2. **Open the telegram adapter source** at `~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py` and find the streaming-edit code path. Look for a `stream`, `edit`, or `chunk` function. See if there's a runtime flag that bypasses it.
3. **Ask Jeff to run from his terminal** (outside the chat):
   ```bash
   launchctl kickstart -k "gui/$(id -u)/ai.hermes.gateway-smith"
   ```
   Then send a test message. If still broken after a confirmed restart with confirmed config change, it's a code-level fix.
4. **Worst case:** file upstream / patch the adapter locally to skip the streaming-edit on final delivery.

## Workaround in effect

Short single-paragraph replies. No lists, tables, headers, or bold-as-structure in chat. Style guide for telegram-mode is "text like a person, not a markdown report."

## Upstream status (verified 2026-06-24)

**This is a known open bug in NousResearch/hermes-agent.** Not a local config issue. Real issues:

- **#49536** — "Telegram finalize message text overlap due to parse_mode mutation" — exact bug Jeff is hitting. Body: "the finalized message text overlaps with the streaming preview text, requiring a refresh to display correctly." P2, open 4 days.
- **#44428** — "Support Telegram Bot API 10.1 Rich Messages and rich draft streaming" — P3, open 12 days.
- **#49452** — "Markdown pipe tables converted to bullet lists in streaming finalization" — duplicate, P2, open 4 days.

Root cause per the issue bodies: the streaming finalization path uses `editMessageText` (MarkdownV2) instead of `sendMessage` with rich formatting, and the parse_mode mutation between draft and final leaves stale chunks visible.

Subscribe to #49536 for fix notifications. The workaround (refresh to display correctly) is what everyone is doing until the upstream fix lands.

## Related

- Daily log: `~/Smith/memory/2026-06-24.md` (Night section)
- Cross-session memory: "Lesson 2026-06-24 evening: telegram messages look collapsed..."
- `smith-local-stack` skill: has port map and gateway commands

````

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

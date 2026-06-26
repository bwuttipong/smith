# Telegram Streaming-Edit Bug (hermes-agent upstream)

**Status:** known open bug, workaround in place, no upstream fix yet (verified 2026-06-24).

## What it looks like

A single agent reply arrives in telegram as ONE bubble, but with multiple chunks of the response drawn **on top of each other**. Bullet items, headers, timestamps on the right edge — all overlap. Jeff described it as "messages are collapsed each other" / "mass up."

This is **not a setup or auth issue.** The bot responds correctly. The message content is correct. The visual rendering is wrong.

## Root cause

The hermes-agent telegram adapter's streaming finalization path uses `editMessageText` (MarkdownV2) on a placeholder bubble. As the agent streams its response, the adapter edits the same message in place with each chunk. Telegram's UI shows all the intermediate edits stacked, with parse_mode mutation between draft and final leaving stale chunks visible.

The relevant code: `~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py` around line 1441. The python-telegram-bot library even warns about this:

```
PTBUserWarning: Please use 'Bot.editMessageText' instead of 'Bot.do_api_request("editMessageText", ...)'
  await self._bot.do_api_request("editMessageText", api_kwargs=payload)
```

## Tracked upstream

- **NousResearch/hermes-agent#49536** — "Telegram finalize message text overlap due to parse_mode mutation" — P2, open 4 days
- **NousResearch/hermes-agent#44428** — "Support Telegram Bot API 10.1 Rich Messages and rich draft streaming" — P3, open 12 days
- **NousResearch/hermes-agent#49452** — "Markdown pipe tables converted to bullet lists in streaming finalization" — P2, open 4 days (duplicate)

All three describe the same underlying pathology from different angles. Subscribe to #49536 for fix notifications.

## Workarounds (in order of effectiveness)

1. **Config toggle** — set `messaging.platforms.telegram.streaming: false` in `~/Smith/.hermes-profile/config.yaml`, then restart the gateway from a separate shell (gateway can't restart itself from inside):
   ```bash
   # from outside the chat (e.g. Jeff's terminal)
   launchctl kickstart -k "gui/$(id -u)/ai.hermes.gateway-smith"
   ```
   Tradeoff: no live "typing" indicator. Replies arrive as single clean bubbles.

   **Caveat:** `hermes config set presentation.platforms.telegram.streaming false` may report success without actually writing to the right key. Always re-verify with `grep -n "streaming" ~/Smith/.hermes-profile/config.yaml` after the set.

2. **Content shape** — send short single-paragraph replies (1-2 sentences, no lists/tables/headers/bold-as-structure). Doesn't fix the underlying edit-loop but reduces visual impact. This is the default in `user-communication-preferences` for telegram.

3. **Refresh to display correctly** — what other users do per the upstream issue. Telegram user pulls down to refresh the chat; the bubbles re-render correctly. Cosmetic only.

## What DOESN'T help

- Troubleshooting blog posts (e.g. `hermify.io/en/blog/hermes-agent-telegram-troubleshooting`) cover setup/auth/silent-bot, not streaming. Don't waste time on them for this bug.
- Restarting the gateway without changing the config.
- Setting `streaming: false` only at the top-level (`streaming.enabled: false` at line ~590) — the per-platform override (line ~330) wins.

## When to surface this to Jeff

- If he says "messages are overlapping / collapsed / massed up" — load this file.
- If he asks why config-toggle changes don't stick — `hermes config set` key-path trap, also documented in `openclaw-config-maintenance`.
- If he sends a link to a hermes troubleshooting page expecting it to fix this — read the page first, but the streaming-edit class of bug isn't there.

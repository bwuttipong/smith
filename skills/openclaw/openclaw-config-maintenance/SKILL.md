---
name: openclaw-config-maintenance
description: Class-level skill for reading, modifying, and maintaining OpenClaw configuration in openclaw.json. Covers agent primary/fallback model changes, provider sections, auth profiles, channel account structure, and safe edit rules. Use when the user asks to inspect or change OpenClaw configuration.
---

# OpenClaw Config Maintenance

## Target file
- Primary config: `openclaw.json` at project root or under `.openclaw/openclaw.json`.
- Preserve JSON validity after edits and keep backups clean.

## Preferred workflow
1. Read the relevant section, not the whole file, to limit context pressure.
2. Use `search_files` for provider/model keys before guessing paths.
3. Use `patch` for surgical edits with exact surrounding context.
4. Re-read the modified section to verify; confirm structure matches sibling entries.

## Provider/auth consistency rule
If `auth.profiles` has a provider key, `models.providers` also needs a provider block for it. Missing provider blocks surface as “Unknown model: …” even when the API key is present in env.

When adding a missing provider:
1. Add the provider block under `models.providers.<provider>`.
2. Use env-backed credentials: `"apiKey": "${GROQ_API_KEY}"`.
3. Register only the model IDs actually referenced by agents/defaults.
4. Restart the gateway to pick up the new provider registration.

## Restart / verification
- Restart with: `launchctl kickstart -k 'gui/501/ai.openclaw.gateway'`
- Verify via: `launchctl list | grep ai.openclaw.gateway`
- A nonzero exit or missing entry means the restart did not take.

## Agent lifecycle — prefer the CLI over hand-editing

For spawning, binding, unbinding, and inspecting agents, use the `openclaw agents` subcommands rather than editing `openclaw.json` directly:

```bash
openclaw agents list                    # all agents + routing-rule counts
openclaw agents add <name> --workspace <dir> --agent-dir <dir/agent> --model <id> --non-interactive
openclaw agents bind <id> <channel[:accountId]>    # the "spawn" verb
openclaw agents unbind ...              # remove a binding
openclaw agents set-identity <id> ...   # name/emoji/avatar
openclaw agents bindings               # all routing rules
```

**Symptom that means an agent is defined but dormant:** `openclaw agents list` shows the agent with `Routing rules: 0`. Fix: bind it to a channel — `agents add` will error with "agent already exists" because the config entry is already there.

Hand-edit `openclaw.json` only for things the CLI doesn't expose: provider blocks, model allowlist tweaks, hooks, memory backend, auth profile structural changes, channel account additions. After hand-edits, run `openclaw doctor` to validate.

**Workflow note (2026-06-24):** when Jeff says "spawn X" / "set X up" / "bring X online," the verb already implies the action. Take the most direct interpretation, execute, report. Skip the option matrix. See `references/agent-lifecycle.md` for the full worked example.

## Per-platform streaming toggle — telegram message collapse fix (lesson from 2026-06-24)

Hermes' `streaming: true` per platform (under `messaging.platforms.<platform>`) makes the agent **stream-edit a single message** while thinking. On telegram this causes messages to render **stacked / collapsed on top of each other** in the same bubble, because every intermediate `editMessageText` call lands on the same message ID. Discord renders this fine (different client behavior); telegram doesn't.

**Symptom (telegram only):** a single reply arrives as one bubble but with the bullet items / headers drawn on top of each other. User sees "messages overlapping each other / massed up."

**Fix:** in `~/.hermes/profiles/<profile>/config.yaml`, set the per-platform streaming flag:

```yaml
messaging:
  platforms:
    telegram:
      streaming: false   # was true — causes the collapse
    discord:
      streaming: false   # already false; keep matching
```

Then restart the gateway (`hermes gateway restart`). Replies will arrive as **single fresh messages per turn** instead of stream-edits. Tradeoff: no live "typing" indicator in telegram. Most users prefer clean bubbles over the typing cue.

**Content-side mitigation (works without config change):** in `user-communication-preferences` the rule is "short chunky multiple bubbles" — reply in 2–4 short messages rather than one wall. This avoids the collapse visually but doesn't fix the underlying edit-loop. The config toggle is the real fix.

**Verification after the change:**
```bash
tail -f ~/Smith/.hermes-profile/logs/gateway.log
# Send a test message to the bot. Expect ONE inbound log line, ONE response.
# No "Suppressing normal final send" entries for that turn.
```

**This is an upstream bug, not a misconfiguration (verified 2026-06-24 via GitHub):**
- `NousResearch/hermes-agent#49536` — "Telegram finalize message text overlap due to parse_mode mutation" — P2, open
- `NousResearch/hermes-agent#44428` — "Support Telegram Bot API 10.1 Rich Messages and rich draft streaming" — P3, open
- `NousResearch/hermes-agent#49452` — "Markdown pipe tables converted to bullet lists in streaming finalization" — P2, open

Root cause: streaming finalization path uses `editMessageText` (MarkdownV2) instead of `sendMessage` with rich formatting; the parse_mode mutation between draft and final leaves stale chunks visible. The config toggle above is a **workaround** until upstream ships a fix — don't tell Jeff "your config is wrong," tell him "known upstream issue, here's the workaround + the tracking issue."

**Don't trust the troubleshooting blog post (lesson 2026-06-24):** `hermify.io/en/blog/hermes-agent-telegram-troubleshooting` covers setup/auth/silent-bot problems but does NOT cover the streaming-edit collapse. If Jeff points you to that page expecting it to fix the collapse, read the issue list above first — the page is for a different class of bug.

**Profile-merge context (2026-06-24):** the config path the skill references is `~/Smith/.hermes-profile/config.yaml` (not `~/.hermes/profiles/smith/config.yaml`) because the smith profile was relocated to a subdir of the workspace. The symlink at the old path makes the old path still work, but new file paths in any future patches should use `~/Smith/.hermes-profile/`.

## Alibaba Model Studio access check
- 400 / overdue-payment failures come from account status, not config.
- The provider block can stay; calls will fail again once billing is restored not because config is wrong, but because the account status changes.
- Before removing a provider as a “fix,” confirm the error source is the account status page, then either wait for payment or remove it intentionally.

## Safety rules
- Edit within `.openclaw/` by default unless cross-profile changes are explicitly approved.
- Do not alter auth tokens, channel tokens, or secrets unless the user explicitly requests it.
- Do not rename provider keys unless needed for a request; model id names must match registered provider model entries.
- Prefer minimal diff; avoid reformatting unrelated blocks.

## Hermes CLI gotchas (learned 2026-06-24)

### `hermes config set` may write to the wrong key path (silent success)

`hermes config set <key> <value>` accepts dotted keys and reports `✓ Set ...` on success, but does NOT validate the parent structure. Setting `presentation.platforms.telegram.streaming false` may write to a different parent than you expect — the file mtime changes and the CLI reports success, but the value doesn't land where you read it back via `grep`.

After any `hermes config set`:
1. Re-read the actual file at the path you expected: `grep -n "<key-fragment>" /path/to/config.yaml`
2. Verify the file's mtime changed: `ls -la /path/to/config.yaml`
3. If the value didn't land, use `hermes config edit` (opens in $EDITOR) for explicit, file-level edits. This bypasses the dotted-key path resolution.

### Gateway restart from inside the chat is blocked

`hermes gateway restart` returns: **"Blocked: cannot restart or stop the gateway from inside the gateway process. The gateway would kill this command before it could complete (SIGTERM propagates to child processes)."**

`launchctl kickstart -k "gui/$(id -u)/ai.hermes.gateway-smith"` ALSO fails from inside the chat, because the terminal tool itself runs as a child of the gateway process — SIGTERM propagates to the kickstart before it can complete.

**Workaround:** ask Jeff to run the restart command from a separate shell OUTSIDE the chat. One command, ~5 seconds:

```bash
launchctl kickstart -k "gui/$(id -u)/ai.hermes.gateway-smith"
```

Then have him send a test message to verify the new config took effect. Don't try to do it yourself from the chat — it will always fail.
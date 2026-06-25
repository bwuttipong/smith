---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-samantha-openclaw-update-2026-06-21-46022429
title: "Memory Bridge (smith): samantha-openclaw-update-2026-06-21"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/samantha-openclaw-update-2026-06-21.md
bridgeRelativePath: memory/samantha-openclaw-update-2026-06-21.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-21T07:00:22.146Z
---

# Memory Bridge (smith): samantha-openclaw-update-2026-06-21

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/samantha-openclaw-update-2026-06-21.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-21T07:00:22.146Z

## Content
````markdown
# OpenClaw Update Attempt — 2026-06-21

**Attempted by:** Samantha (subagent, requester: Smith)
**Target version:** 2026.6.9
**Current version:** 2026.6.8
**Result:** ❌ FAILED — cannot update from inside the gateway process

## Commands Run

### 1. `openclaw update --yes --no-restart 2>&1`

Output:
```
Updating OpenClaw...

--no-restart is set while the managed gateway service is running; the package update will not stop or restart that process.
Package updates cannot run from inside the gateway service process.
That path replaces the active OpenClaw dist tree while the live gateway may still lazy-load old chunks.
Run `openclaw update` from a shell outside the gateway service, or stop the gateway service first and then update.

(Command exited with code 1)
```

Exit code: 1

### 2. `openclaw --version 2>&1`

```
OpenClaw 2026.6.8 (844f405)
```

## Why It Failed

OpenClaw's updater explicitly refuses to run from inside the gateway service process. The error message states that the update replaces the active dist tree while the live gateway may still lazy-load old chunks — a safety guard against in-place upgrades that could leave the running process in a broken hybrid state.

`--no-restart` does not bypass this check; it only affects whether the gateway is restarted *after* a successful update. The precondition is: must be run from outside the gateway service process.

## What I Did NOT Do

- Did **not** stop or restart the gateway
- Did **not** run without `--no-restart` (would not have helped anyway — the blocker is the process context, not the restart policy)
- Did **not** attempt workarounds that could destabilize the running gateway

## Recommended Next Steps for Smith

1. **Run from an external shell** (SSH, Terminal.app, or any process spawned outside the managed gateway service). Any subagent spawned by the gateway itself will hit this same guard.
2. Or **stop the gateway first**, then update, then restart it manually:
   ```
   openclaw gateway stop
   openclaw update --yes
   openclaw gateway start
   ```
3. Verify with `openclaw --version` afterwards.

## Notes

- Workspace path: `/Users/Jeff/Agents/Samantha`
- Time of attempt: 2026-06-21 13:59 GMT+7
- No restart was triggered; gateway should still be running on 2026.6.8

````

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

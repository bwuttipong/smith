---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-artifacts-evolution-2026-06-04-cron-delivery-548854d0
title: "Memory Bridge (smith): artifacts / evolution-2026-06-04-cron-delivery"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/artifacts/evolution-2026-06-04-cron-delivery.md
bridgeRelativePath: memory/artifacts/evolution-2026-06-04-cron-delivery.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-04T00:18:08.720Z
---

# Memory Bridge (smith): artifacts / evolution-2026-06-04-cron-delivery

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/artifacts/evolution-2026-06-04-cron-delivery.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-04T00:18:08.720Z

## Content
````markdown
# Evolution: Cron Delivery Failure — Multi-Account Discord Routing

**Date:** 2026-06-04
**Incident:** `memory-midnight-maintenance` cron job ran successfully but delivery failed
**Filed by:** Smith
**Status:** ✅ Resolved — delivery verified working

## Summary

The midnight memory maintenance job executed correctly but its results never reached the alerts channel on Discord. The error — `OutboundDeliveryError: Invalid Recipient(s)` — was misleading; the recipient was valid, but the delivery target format was wrong.

## Root Cause

OpenClaw has **5 Discord bot accounts** registered under different agent accounts:

| Agent    | Account ID    | Bot ID (Application)       |
|----------|---------------|----------------------------|
| Smith    | `default`     | `1500141409380859944`      |
| Kermit   | `kermit`      | `1499760048459747339`      |
| Cookie   | `cookie`      | `1505229846765375528`      |
| Beaker   | `beaker`      | `1505261795072544989`      |
| Fozzie   | `fozzie`      | `1505271799154217031`      |

All of them share the same guild (`1487738757326049391`) and have access to the alerts channel (`1501840214874914836`).

The cron job's delivery config had two issues:

1. **Missing `accountId`** — The delivery said `channel: "discord"` without specifying which Discord bot account to use. With multiple accounts registered, the system couldn't resolve which bot should send the message.
2. **Wrong channel target format** — The `to` field used either a bare numeric ID (`1501840214874914836`) or `discord:` prefix (`discord:1501840214874914836`). Both resolved to `user:1501840214874914836` — a user DM — rather than a channel. The correct format is `channel:1501840214874914836`.

**Per OpenClaw docs** (config-channels.md line 337):
> *"Use `user:<id>` (DM) or `channel:<id>` (guild channel) for delivery targets; bare numeric IDs are rejected."*

## Timeline

| Time (BKK) | Event |
|------------|-------|
| Jun 3 ~23:30 | `memory-midnight-maintenance` cron job created and enabled |
| Jun 4 00:00 | Job executed — maintenance ran successfully but delivery failed ❌ |
| Jun 4 06:56 | Issue detected during morning check-in |
| Jun 4 07:03 | First fix attempt: added `accountId: "default"` + `to: "discord:1501840214874914836"` — still failed (resolved as `user:` not channel) |
| Jun 4 07:07 | Evolution doc written capturing the failure |
| Jun 4 07:10 | Manual test run triggered to verify |
| Jun 4 07:12 | First test run failed — same delivery error (still `discord:` prefix) |
| Jun 4 07:12 | FailureAlert fired — Jeff got pinged on Telegram ✅ (alerter works) |
| Jun 4 07:14 | Config fixed: changed `to` from `discord:` to `channel:` prefix |
| Jun 4 07:15 | Second test run triggered |
| Jun 4 07:17 | **Delivery succeeded** — `lastDelivered: true`, consecutive errors reset to 0 ✅ |

## Why It Wasn't Caught Sooner

- The maintenance *script* (qmd indexing, wiki lint, artifact logging) completed successfully — no script-level failure signal.
- The delivery failure was silent — no notification was configured for delivery errors (no `failureAlert` on the job).
- The artifact files (`maintenance-summary.md`, logs) were written to disk correctly, masking the issue locally.
- The docs weren't checked early enough — `channel:` prefix requirement was documented but not discovered until the third attempt.

## Fix Applied

```json
// Before (original — crashed)
"delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "1501840214874914836"
}

// First attempt — still crashed (resolved as user DM)
"delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "discord:1501840214874914836",
    "accountId": "default"
}

// Final fix — delivered successfully 🎉
"delivery": {
    "mode": "announce",
    "channel": "discord",
    "to": "channel:1501840214874914836",
    "accountId": "default"
}
```

## Preventive Checks

1. **Cron delivery checklist** — When creating isolated cron jobs with Discord delivery, always include:
   - `delivery.accountId` (the agent's Discord account name — required when multiple accounts exist)
   - `delivery.to` in `channel:<channelID>` format (not raw ID, not `discord:` prefix)

2. **Failure alerts** — Add `failureAlert` to critical cron jobs so delivery failures surface immediately:

   ```json
   "failureAlert": {
       "after": 1,
       "channel": "telegram",
       "to": "8611951691",
       "mode": "announce"
   }
   ```

3. **Delivery testing** — After creating or modifying a cron job's delivery config, run it once to verify delivery (use `cron run` action).

4. **Docs-first debugging** — Before guessing delivery formats, consult `docs/gateway/config-channels.md` for the channel's delivery target syntax.

## Current State

- ✅ Delivery fixed and verified — Discord alerts channel receiving maintenance summaries
- ✅ Failure alert wired — Telegram ping if delivery ever bounces again
- ✅ Evolution doc updated with final root cause
- ⚠️ Model `nvidia/nemotron-3-super-120b-a12b` still in use (noted flakiness but maintenance exec-heavy)

````

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

---
pageType: synthesis
id: synthesis.system-audit-2026-06-26
title: System Audit — 2026-06-26
sourceIds:
  - claw-mechanic-audit-2026-06-26
status: active
updatedAt: 2026-06-26T00:04:00.418Z
---

# System Audit — 2026-06-26

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Summary
<!-- openclaw:wiki:generated:start -->
# System Audit — 2026-06-26

Ran full `/claw-mechanic audit check system` at 07:02 BKK.

## 🟢 Healthy

- **OpenClaw:** 2026.6.10 (up to date), gateway healthy, event loop clean (p99 23ms)
- **Channels:** Telegram ✅ Discord (×5) ✅ LINE ✅ Slack ✅ — all connected and running
- **Memory engine:** enabled, operational
- **Plugins:** no install-tree issues
- **Auth:** 14 of 21 providers configured

## Fixed This Session

- **`memory-midnight-maintenance` cron** — model rejected by allowlist. Swapped to `google/gemini-2.5-flash`. Verified.

## 🟡 Minor / Cosmetic

- **Stale `openclaw-web-search` plugin config** — TypeScript-only, no compiled dist. Needs `openclaw doctor --fix`.
- **13 old task warnings** — stale blocked taskflows + old delivery failures.
- **41 plaintext secret findings** — keys in local config/sqlite. Low risk on isolated host.

## 🔴 Action Items

1. **Small model no sandbox (CRITICAL)** — `gemma4:31b-cloud` (31B) default with sandbox off + web tools.
2. **google-gemini-cli OAuth expires ~07:52 BKK** — needs re-auth soon.
3. **xAI OAuth expired** — stale, not blocking.
4. **`allowInsecureAuth=true`** — fine behind Tailscale, flag off if needed.
<!-- openclaw:wiki:generated:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

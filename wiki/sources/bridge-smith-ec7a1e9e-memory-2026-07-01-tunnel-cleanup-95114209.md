---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-07-01-tunnel-cleanup-95114209
title: "Memory Bridge (smith): 2026-07-01-tunnel-cleanup"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-07-01-tunnel-cleanup.md
bridgeRelativePath: memory/2026-07-01-tunnel-cleanup.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-07-01T15:50:15.097Z
---

# Memory Bridge (smith): 2026-07-01-tunnel-cleanup

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-07-01-tunnel-cleanup.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-07-01T15:50:15.097Z

## Content
```markdown
# 2026-07-01 Tunnel Cleanup

## Task
Remove cloudflared and ngrok from local machine as requested.

## Actions Taken
- **cloudflared**: Removed `C:\Users\Wuttipong.t\cloudflared.exe` and `.cloudflared\` config directory (tunnel: line-bot, hostname: line.bestwuttipong.dev → localhost:8081)
- **ngrok**: Uninstalled Windows Store package (ngrok.ngrok_3.39.8.0_x64__1g87z0zv29zzc)

## Verification
- No cloudflared processes running
- No ngrok processes running  
- Ports 8080/8081 not in use
- Both executables/configs removed

## Impact
LINE bot handler on port 8081 still operates locally — no external tunnel access until new tunnel is established.

## Timestamp
2026-07-01 09:02 UTC
```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

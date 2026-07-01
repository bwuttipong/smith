---
pageType: synthesis
id: synthesis.workspace-git-setup-platform-context
title: Workspace Git Setup & Platform Context
sourceIds:
  - sum_chat_2026-06-30_workspace_git_setup
status: active
updatedAt: 2026-06-30T03:36:11.439Z
---

# Workspace Git Setup & Platform Context

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Summary
<!-- openclaw:wiki:generated:start -->
# Workspace Git Setup & Platform Context

## Repository
- **URL**: `https://github.com/bwuttipong/smith.git`
- **Path**: `~/Smith` (macOS) / wherever cloned on Windows
- **Branch**: `master`

## Gitignore Policy
Repo is **private**, but some files are still gitignored for practical reasons:
| Pattern | Reason |
|---------|--------|
| `node_modules/` | Reproducible from `package.json` / `npm install` |
| `.venv/` | Reproducible from `pip install` / `pyproject.toml` |
| `__pycache__/`, `*.pyc` | Compiled Python bytecache |
| `*.db`, `*.sqlite*` | Binary blobs, diff nightmare |
| `.openclaw/` | Runtime gateway state |
| `.gemini/tmp/` | Large chat logs (some >100MB, blocked by GitHub) |
| `sessions/` | Session history blobs |
| `state.db*` | OpenClaw runtime SQLite databases |
| `*.tail*.ts.net.crt/key` | Tailscale certs (private keys!) |

## Tracked Files of Note
- `.claude/` — Claude Code state
- `.gemini/history/` — Gemini prompt history (small markdown files)
- `.hermes-profile/` — Hermes runtime cron state
- `.hermes_history` — Hermes command history log
- `bin/` — Binaries (including ~46MB `uv`)

## Platforms Running This Workspace
1. **macOS (MacBook Air)** — primary runtime, Smith/OpenClaw runs here
2. **Windows (work laptop)** — runs Hermes, Antigravity, OpenClaw Windows Companion
   - After `git pull` on Windows: node_modules, .venv won't exist
   - Only install if needed: `npm install` in skill dirs, `pip install -e .` in agent-reach etc.

## Nested Git Fix
Cloned projects inside the workspace (agent-reach, lossless-claw, .gemini/history/*) had their own `.git` folders, causing GitHub to show them as empty submodules. Fix: removed nested `.git` folders so actual files are tracked directly.
<!-- openclaw:wiki:generated:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-weekly-report-2026-06-27-to-2026-07-03-21e83b4a
title: "Memory Bridge (smith): weekly-report-2026-06-27-to-2026-07-03"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/weekly-report-2026-06-27-to-2026-07-03.md
bridgeRelativePath: memory/weekly-report-2026-06-27-to-2026-07-03.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-07-04T03:17:27.250Z
---

# Memory Bridge (smith): weekly-report-2026-06-27-to-2026-07-03

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/weekly-report-2026-06-27-to-2026-07-03.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-07-04T03:17:27.250Z

## Content
```markdown
# Weekly Report — June 27 – July 3, 2026

## Key Accomplishments

### CirculatingBox (June 27)
- Fixed "Doubling Quantity" transfer bug — root cause was UI summing stock across all locations instead of selected source, plus incorrect query parameter (`Id` vs `BoxNo`). Shipped as v3.1.0.35.
- Standardized 176 location names in production DB via `sqlcmd` UPDATE.
- Added About Form with company logo and User Manual wiring to Help menu.
- Refactored `TransferService.vb` to merge quantities into existing destination layers.
- Resolved MRP ghost Purchase Requisition recommendation (stuck Requisition Line status) and documented Customer Order cross-reference item mismatch workaround.

### Agent Infrastructure (June 28 – July 2)
- Indexed "High Agency in 30 Minutes" (George Mack) into LLM wiki.
- Created Antigravity Windows migration script (`migrate-antigravity-windows.ps1`).
- Moved `.gemini`, `.claude` configs into workspace with symlinks for portability.
- Diagnosed and resolved OpenRouter API key issues (invalid key → rate-limited key → free model fallback).
- Installed **Agent-Reach** (web, YouTube, GitHub, V2EX, RSS, Bilibili, Twitter, Reddit) — zero-config channels wired into Hermes.
- Built **MCP Memory Bridge** — shared memory server (SQLite FTS5) indexing 552 files across `memory/` and `wiki/`, exposed via 7 MCP tools. Passed 10/10 interop audit between OpenClaw and Hermes.
- Configured exec approvals (Telegram as approval surface, `ask: always`).

### Kilo Code Workspace Setup (July 2–3)
- Set up Kilo Code with MCP memory-bridge, Smith agent persona, and 10 slash commands (`/soul`, `/memory`, `/search`, `/wiki`, `/morning`, `/evening`, `/weekly`, `/projects`, `/delegate`, `/traffic`).
- Installed Python 3.12 on work machine, wired MCP server with correct Windows paths.
- Deployed `.kilo/` + `kilo.json` to all three project workspaces (OutsourceEF9, TPK QA Hold, CirculatingBox) — Smith loads in any project.
- Installed Notion CLI (`ntn` v0.18.1) via winget, authenticated with API key, bot "Smith" confirmed in workspace.

### Work Machine Bootstrap (July 3)
- Copied 3 projects from atlas server: OutsourceEF9 (149 MB), TPK QA Hold (191 MB), Circulating_Box (2.0 GB).
- Created project registry (`~/Smith/projects/`) with architecture context files for each.
- Updated MEMORY.md with real paths and architecture details.

## Ongoing Projects/Tasks

| Project | Status |
|---------|--------|
| CirculatingBox v3.1.0.35 | Deployed to production. Monitor for stock quantity anomalies. |
| OutsourceEF9 | Codebase on work machine. Ready for development. |
| TPK QA Hold | Codebase on work machine. Ready for development. |
| Move Apps Migration | TPK database hosting decision made (keep at TPK). Outsource migration deployment pending. |
| MCP Memory Bridge | Running on work machine. Hermes side TODO: install Hermes Agent, add MCP server, choose free model provider. |
| Kilo Code | Wired across all projects. VS Code reload needed to activate MCP. |

## Challenges/Blockers

- **OpenRouter API key exhaustion** — default key hit $0.01 limit. Workaround: switched to Xiaomi MiMo model + free-tier fallbacks (Cohere north-mini-code, Gemma).
- **Brave Search rate limiting** (HTTP 429) — use Prismfy as backup.
- **MCP Memory Bridge on Windows** — initially had macOS paths in config; fixed by updating to full Windows Python paths.
- **`.kilo/kilo.json` validation error** ("Conf is invalid") — appeared on first session; resolved after PATH refresh and config verification.

## Next Steps

1. **CirculatingBox** — Monitor production for transfer bug regressions. Clear MRP backlog (Customer Orders + Purchase Order Requisitions) in Test DB.
2. **Move Apps** — Begin Outsource migration deployment now that TPK database hosting is confirmed.
3. **Hermes Agent** — Install on work machine, wire MCP Memory Bridge, select free model provider.
4. **Notion Integration** — Start using `ntn` CLI for page/data management workflows.
5. **Project Development** — Pick up OutsourceEF9 or TPK QA Hold tasks as priorities emerge.

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

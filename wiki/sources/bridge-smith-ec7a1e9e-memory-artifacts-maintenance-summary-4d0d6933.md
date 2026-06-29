---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-artifacts-maintenance-summary-4d0d6933
title: "Memory Bridge (smith): artifacts / maintenance-summary"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/artifacts/maintenance-summary.md
bridgeRelativePath: memory/artifacts/maintenance-summary.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-28T17:33:57.487Z
---

# Memory Bridge (smith): artifacts / maintenance-summary

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/artifacts/maintenance-summary.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-28T17:33:57.487Z

## Content
```markdown
# Memory Maintenance Summary
**Date:** 2026-06-29 00:31 ICT (UTC 2026-06-28 17:31)
**Trigger:** Cron `memory-midnight-maintenance`
**Duration:** ~1 second (script), +5 min for full embed attempt

## Steps

| Step | Result |
|------|--------|
| **qmd update** (7 collections) | ✅ — All collections up to date, no changes |
| **qmd embed** (memory) | ✅ — Already embedded, no action needed |
| **qmd embed** (workspaces) | ✅ — Already embedded, no action needed |
| **qmd cleanup** | ✅ — No orphaned embeddings, DB vacuumed |
| **wiki lint** | ⚠️ 4 errors, 13 warnings (see below) |
| **memory search** | ✅ — Index healthy, CLI search returning results |

## Details

### Collections (unchanged from last run)
- `memory`: 15 files indexed, 0 changes
- `workspaces`: 265 files indexed, 0 changes
- Groot: 136 sessions (+0)
- Jarvis: 2 sessions (+0)
- Morgan: 0 sessions
- Star Lord: 0 sessions
- Trinity: 4 sessions (+0)

### qmd Status
- **Total vectors:** 12,107 embedded
- **Pending:** 140 need embedding (session collections — skipped in midnight script)
- **Database size:** 259.5 MB
- **Updated:** 14h ago

### Wiki Lint (4 errors, 13 warnings)
- 4 errors: missing `id` + `pageType` frontmatter on `concepts/high-agency.md` and `entities/george-mack.md`
- 13 warnings: missing provenance, missing updatedAt, broken wikilinks (same state as last run)

## Health
🟢 Script completed successfully. All core systems nominal.
🟡 140 pending embeddings (pre-existing, session collections — not critical)
⚠️ Wiki lint has pre-existing issues (frontmatter gaps + broken wikilinks) — same state as last run, no regression.

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

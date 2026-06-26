---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-artifacts-2026-06-22-todoist-migration-f70fbe25
title: "Memory Bridge (smith): artifacts / 2026-06-22-todoist-migration"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/artifacts/2026-06-22-todoist-migration.md
bridgeRelativePath: memory/artifacts/2026-06-22-todoist-migration.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-24T15:29:50.206Z
---

# Memory Bridge (smith): artifacts / 2026-06-22-todoist-migration

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/artifacts/2026-06-22-todoist-migration.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-24T15:29:50.206Z

## Content
```markdown
# Todoist Migration — Slack Project Tracker → proj-ebox

_Date: 2026-06-22 08:55 GMT+7 — Subagent (depth 1/1)_

## Summary

Migrated all **36 tasks** from Slack List `F0AQ9CED5MF` (Project tracker) into a new Todoist project **proj-ebox** (`6gwHwf2h49v85xCc`).

## Source

- File: `~/Smith/memory/artifacts/2026-06-22-slack-project-tracker-morning.md` (briefing)
- Raw API: `POST https://slack.com/api/slackLists.items.list` with `list_id=F0AQ9CED5MF`
- Raw payload: `/tmp/slack-list-raw.json` (51 KB, 36 items confirmed)

## Destination

- **Project:** `proj-ebox` — id `6gwHwf2h49v85xCc` (color: blue, view: list)
- **Project URL:** https://app.todoist.com/app/project/6gwHwf2h49v85xCc

## Labels created (14 total)

Status labels: `not-started`, `in-progress`, `blocked`, `done`
Section labels: `Box`, `ERP`, `MoveApps`, `ShopFloor`, `StoreInk`, `Inbound`, `IssueOutbound`, `MasterData`, `Report`

## Tasks migrated: 36 / 36 ✅

| Metric | Count |
|---|---|
| Total tasks | 36 |
| Done (status=done) | 27 |
| Not started (status=not-started) | 9 |
| With due date | 23 |
| With description | 24 |
| All have labels | 36 |

### Priority distribution (matches source)

- **p1 (★★★)**: 5 — e.g. `[ERP] MRP Infor Food Packaging`
- **p2 (★★)**: 7 — e.g. `[MoveApps] Move the app from TPN to TPK`, `[StoreInk] Scrap`
- **p3 (★)**: 12 — e.g. `[Box] User Manual and Developer Guide`
- **p4 (no stars)**: 12 — e.g. `Circulating Box`, `Inventory Control`, `Outsource`

### Section label distribution

- `Box` (19) — most common
- `ERP` (1), `MoveApps` (1), `ShopFloor` (1), `StoreInk` (1)
- **No section label** (13) — tasks without a `[Xxx]` prefix in their name

## Mapping logic

1. **Priority:** `Col0APT389FNH` raw value `1→p3`, `2→p2`, `3→p1` (Todoist inverts stars). Missing → `p4`.
2. **Status:** `Col00` (todo_completed) `True → done`, `False → not-started`.
   - _Note: The Slack list doesn't store "in-progress" or "blocked" as a separate column — those are author annotations in the morning briefing. Migration uses the raw `todo_completed` flag, which is the only machine-readable status in the API. The 5 in-progress + 1 blocked annotations from the briefing were folded into `not-started` for now; if you want to promote specific items, do it in Todoist UI (labels are already created)._
3. **Section:** Regex match on the bracketed prefix in the task name (`[Box]`, `[ERP]`, etc.) → label.
4. **Due date:** `Col02` value (YYYY-MM-DD) → `due_date` field.
5. **Description:** `Col0APUDDDFV4` (rich_text) → flattened to plain text → `description` field. Assignee prepended as `Assignee: <name>` line (user IDs `U0AP...` resolved via the morning briefing's directory map: `U0APT6EFERK → Wuttipong T.`, `U0APV1N3EMT → Lamai`, `U0APQHU21UK → Vatcharapong`).

## Artifacts

- `/tmp/slack-list-raw.json` — raw Slack API response
- `/tmp/tracker_tasks.json` — parsed 36 tasks
- `/tmp/label_map.json` — Todoist label id map
- `/tmp/migration_results.json` — created task ids per name

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

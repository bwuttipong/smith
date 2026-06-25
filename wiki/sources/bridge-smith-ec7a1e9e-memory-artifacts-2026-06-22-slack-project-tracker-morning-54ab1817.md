---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-artifacts-2026-06-22-slack-project-tracker-morning-54ab1817
title: "Memory Bridge (smith): artifacts / 2026-06-22-slack-project-tracker-morning"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/artifacts/2026-06-22-slack-project-tracker-morning.md
bridgeRelativePath: memory/artifacts/2026-06-22-slack-project-tracker-morning.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-22T01:46:55.898Z
---

# Memory Bridge (smith): artifacts / 2026-06-22-slack-project-tracker-morning

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/artifacts/2026-06-22-slack-project-tracker-morning.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-22T01:46:55.898Z

## Content
```markdown
# Morning Briefing — Project Tracker (Slack List) — 2026-06-22 (Monday, 08:42 GMT+7)

_Source: Slack List `F0AQ9CED5MF` "Project tracker" (mimetype `application/vnd.slack-list`), workspace FlexPak `T0AMK5LU20P`, channel `#projects` (`C0ANY2EULCA`). Pulled via `slackLists.items.list` API. 36 rows total. 17 Done, 19 still active._

---

## 📋 Tracker snapshot

- **36 tasks total** — 17 Done (47%), 19 active
- **5 In progress** • **1 Blocked** • **13 Not started**
- **3 overdue items** • **0 due this week** • **1 high-priority (★★★) item active**
- *Last update on the tracker: 2026-06-18 09:49 GMT+7* (4 days stale — no movement since the previous Friday)

## ⚠️ Overdue (3)

| Task | Status | ★ | Assignee | Due | Days late |
|---|---|---|---|---|---|
| [Box] Criteria search | 🚧 Blocked | ★ | Lamai | 2026-04-30 | **53** |
| [Box] User Manual and Developer Guide | 🔄 In progress | ★ | Wuttipong T. | 2026-05-09 | **44** |
| User requirement - Transaction report (excel) | 🔄 In progress | ★ | (unassigned) | 2026-06-11 | **11** |

## 🔄 In progress (5)

| Task | ★ | Assignee | Due |
|---|---|---|---|
| [ERP] MRP Infor Food Packaging | ★★★ | (unassigned) | 2027-06-30 |
| [MoveApps] Move the app from TPN to TPK | ★★ | (unassigned) | 2026-06-30 |
| [Box] User Manual and Developer Guide | ★ | Wuttipong T. | **2026-05-09** ⚠️ (44d late) |
| User requirement - Transaction report (excel) | ★ | (unassigned) | **2026-06-11** ⚠️ (11d late) |
| [ShopFloor] TPK QA Hold | ★ | (unassigned) | 2026-06-30 |

## 🚧 Blocked (1)

- **[Box] Criteria search** ★ — Lamai — due 2026-04-30 (53d late)
  - Dimension criteria (width, height, length) → leverage BOXSOFT if available

## 📅 Due this week (0)

_No active tasks due in the next 7 days._

## ⭐ High priority (3★) active (1)

- **[ERP] MRP Infor Food Packaging** — In progress — (unassigned) — due 2027-06-30
  - https://app.notion.com/p/MRP-Infor-Food-Packaging-3680da1b1be6807b9d22ce2a5a212ad0?source=copy_link

## ⬜ Not started — with due dates (1)

- **[StoreInk] Scrap** ★★ — (unassigned) — 2026-06-30

## 🆕 Not started — no due date (12)

- AI Automation QC/AI ASM
- Circulating Box
- Inventory Control
- Notification Demo Form
- Notification Hub
- Outsource
- Parameter Viewer
- QC_HandSET (QC)
- Remove decimals from reports
- Rename "Box No." → "Item"
- Sort by box number
- Streamline Box Profile

## 🎯 Suggested focus for today (Mon 2026-06-22)

1. **Unblock "[Box] Criteria search"** — 53 days overdue, blocked. Talk to Lamai about BOXSOFT integration to break the blocker.
2. **"[Box] User Manual and Developer Guide"** — 44 days overdue, in progress. Wuttipong T. needs to publish what's done; this is documentation, not blocked.
3. **"User requirement - Transaction report (excel)"** — 11 days overdue, in progress, unassigned. Decide owner and ship Excel export.
4. **Friday's commits already moved 4 items** (UI polish batch, Notification feature → Done; ShopFloor TPK QA Hold → In progress; Criteria search → Blocked). Use that momentum — get the unblockers on the table first thing.
5. **"[StoreInk] Scrap"** (Not started, ★★, due 2026-06-30 in 8 days) — needs a kickoff or it'll join the overdue pile.

---

**API path used:** `POST https://slack.com/api/slackLists.items.list` with `{list_id: F0AQ9CED5MF, limit: 200}` — this is the official endpoint and returned all 36 rows.

**Alternative (CSV):** `GET https://files.slack.com/files-pri/T0AMK5LU20P-F0AQ9CED5MF/csv/list` — the `list_csv_download_url` from `files.info`. **Warning: only returns 24 of 36 rows** (the default view excludes the 12 untracked / not-started rows without due dates). Don't use the CSV alone.

**Auth:** `Authorization: Bearer $SLACK_BOT_TOKEN` — bot identity is `friday` (B0AV64L5C30). Bot scopes include `lists:read` and `lists:write`. `users:read` is **not** on the token, so assignee IDs could not be resolved live; the names above are inferred from the CSV's email column and the workspace directory (U0APT6EFERK → Wuttipong T., U0APV1N3EMT → Lamai, U0APQHU21UK → Vatcharapong). To get live names, add `users:read` scope to the bot.

_Generated: 2026-06-22 08:42 GMT+7 (subagent, depth 1/1)._

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

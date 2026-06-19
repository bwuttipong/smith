# Slack Files, Canvases & Lists — Operations Guide

## Overview

The `message` tool has limited Slack file/canvas/list support. For advanced operations, use the Slack HTTP API directly via `curl` with the bot token from env: `$SLACK_BOT_TOKEN`.

---

## Authentication

```bash
# All requests use this header
-H "Authorization: Bearer ${SLACK_BOT_TOKEN}"
-H "Content-Type: application/json; charset=utf-8"
```

The bot token is already set in the environment. **Do not hardcode tokens.**

---

## Canvas Operations

### Create a Canvas

```bash
curl -X POST https://slack.com/api/canvases.create \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "title": "Canvas Title Here",
    "document_content": {
      "type": "markdown",
      "markdown": "Your markdown content here"
    }
  }'
```

**Returns:** `{"ok": true, "canvas_id": "F0XXXXXXXXX"}`

**Important notes:**
- `document_content` must use `type: "markdown"` with `markdown` field — plain string or block kit format will fail with `invalid_arguments`
- Markdown supports: headers (`#`), bold (`*`), lists, tables, dividers (`---`), links, emoji
- Canvas is created but **not shared to any channel yet**

### Make Canvas Visible (Share it)

Canvases don't appear in the "Canvases" tab until they're shared to a channel/DM. The `files.share` endpoint requires a **user token** (not bot token), so use `chat.postMessage` instead:

```bash
curl -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "channel": "CHANNEL_OR_DM_ID",
    "text": "📝 <https://flexpakhq.slack.com/docs/TEAM_ID/CANVAS_ID|Canvas Title>",
    "blocks": [
      {
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "📝 *Canvas created:* <https://flexpakhq.slack.com/docs/TEAM_ID/CANVAS_ID|Canvas Title>"
        }
      }
    ]
  }'
```

### Update Canvas Content

```bash
curl -X POST https://slack.com/api/canvases.sections.update \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "canvas_id": "CANVAS_ID",
    "section_id": "SECTION_ID",
    "document_content": {
      "type": "markdown",
      "markdown": "Updated content"
    }
  }'
```

### Delete Canvas Sections

```bash
curl -X POST https://slack.com/api/canvases.sections.delete \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "canvas_id": "CANVAS_ID",
    "section_ids": ["SECTION_ID_1", "SECTION_ID_2"]
  }'
```

---

## File Operations

### Get File Info

```bash
curl -s "https://slack.com/api/files.info?file=FILE_ID" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}"
```

Returns full metadata: title, type, channels, DMs, editors, permalink, etc.

### List/Search Files

```bash
# All files
curl -s "https://slack.com/api/files.list?count=20" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}"

# Only canvases (quips)
curl -s "https://slack.com/api/files.list?types=quip&count=20" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}"

# Search by query
curl -s "https://slack.com/api/files.list?query=Weekly+May&count=10" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}"
```

**Useful filter types:** `quip` (canvases), `csv` (lists/tables), `images`, `docs`, `all`

### Find Canvas ID by Name

```bash
curl -s "https://slack.com/api/files.list?types=quip&count=20" \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" | python3 -c "
import json, sys
data = json.load(sys.stdin)
if data.get('ok'):
    for f in data.get('files', []):
        print(f\"{f['id']}  |  {f.get('title','(no title)')}  |  {f['created']}\")
"
```

### Upload a File (Regular File, Not Canvas)

```bash
# Use the message tool instead:
message(action="upload-file", channel="slack", filePath="/path/to/file", filename="name.md", target="user:USER_ID")
```

Or via curl:

```bash
curl -X POST https://slack.com/api/files.upload \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -F "file=@/path/to/file" \
  -F "filename=name.md" \
  -F "title=File Title" \
  -F "channels=CHANNEL_ID"
```

---

## List (Tracker) Operations

### Read List Content

Lists are Slack files with `filetype: "list"`. When Jeff shares a list file, the full JSON metadata is included — parse `list_records` for rows and `list_metadata.schema` for columns.

### Known Lists

| List Name | File ID | Description |
|-----------|---------|-------------|
| Project tracker | `F0AQ9CED5MF` | Task tracker (Task, Assignee, Due date, Priority, Status, Description) |
| Project overview | `F0APUDFHR54` | Project overview canvas |

---

## Known Canvases

| Canvas Name | File ID | Description |
|-------------|---------|-------------|
| MRP — Infor Food Packaging Weekly | `F0AMYHAAS3Y` | MRP project weekly updates |
| Weekly (May 25–30, 2026) | `F0B5P2JEE5C` | Weekly review |
| Draft Weekly | `F0B6KDRJH24` | Draft weekly template |
| Weekly | `F0B74U0FDK4` | Generic weekly |
| Draft Weekly (July 1 - 6, 2026) | `F0B8J1SNX2M` | Future weekly draft |
| Weekly (June 2–6, 2026) | `F0B8F657ENA` | Work-only weekly review (2026-06-05) |
| Weekly (June 2–6, 2026) | `F0B8H4JJ02W` | Updated weekly review (2026-06-05) |
| Weekly (June 1–6, 2026) | `F0B8D8HP0VC` | Cloned weekly report |
| Weekly (June 8–13, 2026) | `F0BABJ39FJ6` | Previous weekly report |
| Weekly (June 15–19, 2026) | `F0BB9M0BZST` | Current weekly report |

---

## Known Team/Channel IDs

| Name | ID |
|------|-----|
| Team (FlexpakHQ) | `T0AMK5LU20P` |
| DM with Jeff (Wuttipong) | `D0AV4PTTKDK` |
| #proj-ebox channel | `C0ANY2EULCA` |
| Jeff (Wuttipong) | `U0AMYH7KZLN` |
| Friday (bot) | `U0B073HPFC1` |

---

## Key IDs Reference

- **Team ID:** `T0AMK5LU20P`
- **Canvas URL pattern:** `https://flexpakhq.slack.com/docs/T0AMK5LU20P/FILE_ID`

---

## What Works with Bot Token ✅

- Create canvases (`canvases.create`)
- Post messages with canvas links (`chat.postMessage`)
- Get file info (`files.info`)
- List/search files (`files.list`)
- Upload regular files (`files.upload`)
- Read/write/delete messages
- Reactions, pins, emoji

## What Does NOT Work with Bot Token ❌

- `files.share` — requires **user token** (workaround: use `chat.postMessage` with canvas link)
- `download-file` via message tool for channels not in bot's allowed channels
- Direct canvas content editing (use `canvases.sections.update` instead)

---

## Common Patterns

### Weekly: Create Draft Canvas + Share to DM

```bash
# 1. Create canvas
CANVAS_ID=$(curl -s -X POST https://slack.com/api/canvases.create \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "title": "Draft Weekly (DATE RANGE)",
    "document_content": {
      "type": "markdown",
      "markdown": "📋 *Status at a Glance*\n\n| Project | Status | Key Update | Blocker |\n|---|---|---|---|\n| | | | |\n\n---\n\n📋 *Executive Summary*\n\n📌 *DATE* — \n\n---\n\n🚀 *This Week*\n\n- \n\n---\n\n🥅 *Next Week*\n\n- [ ] \n\n---\n\n🔥 *Notes to Self*\n\n- \n\n---\n\n📅 *Work Schedule*\n\n- \n\n---\n\n_Generated by Smith_"
    }
  }' | python3 -c "import json,sys; print(json.load(sys.stdin)['canvas_id'])")

# 2. Share to DM
curl -s -X POST https://slack.com/api/chat.postMessage \
  -H "Authorization: Bearer ${SLACK_BOT_TOKEN}" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "{
    \"channel\": \"D0AV4PTTKDK\",
    \"text\": \"📝 <https://flexpakhq.slack.com/docs/T0AMK5LU20P/${CANVAS_ID}|Draft Weekly>\"
  }"
```

---

## Rules for Future Sessions

1. **Never say "I can't access Slack files/canvases"** — use `curl` with `$SLACK_BOT_TOKEN` instead of relying solely on the `message` tool
2. **Always share canvases after creating** — otherwise they don't appear in the Canvases tab
3. **Use `files.list` to find canvas IDs** — don't guess or ask Jeff
4. **Document every new canvas ID** in the Known Canvases table above
5. **For regular file uploads**, use `message(action="upload-file")` — for canvases, use `curl`

---

_Created: 2026-06-05 by Smith | Updated as new patterns are discovered_

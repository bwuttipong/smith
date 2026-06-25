---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-05-05-slack-canvas-access-abce9a56
title: "Memory Bridge (smith): 2026-05-05-slack-canvas-access"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-05-05-slack-canvas-access.md
bridgeRelativePath: memory/2026-05-05-slack-canvas-access.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-05-05T14:25:08.515Z
---

# Memory Bridge (smith): 2026-05-05-slack-canvas-access

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-05-05-slack-canvas-access.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-05-05T14:25:08.515Z

## Content
````markdown
# Memory

## How to Access Slack Canvas Files

Slack Canvas files are stored as `application/vnd.slack-docs` (filetype: `quip`). They're accessible via the standard Slack file API — no special Canvas API needed.

### Steps:

1. **Find the file ID** — Scan channel messages for files with `filetype: "quip"` or `pretty_type: "Canvas"`. The file ID is in the `id` field (e.g., `F0AMYHAAS3Y`).

2. **Download via the file API** — Canvas files have a download endpoint:
   ```
   https://files.slack.com/files-pri/{team_id}-{file_id}/download/canvas
   ```
   Example:
   ```bash
   curl -s -L "https://files.slack.com/files-pri/T0AMK5LU20P-F0AMYHAAS3Y/download/canvas" \
     -H "Authorization: Bearer {bot_token}"
   ```

3. **Parse the response** — Canvas files come back as HTML (Quip-based). Parse headings, lists, and checked states to extract content.

### Prerequisites:
- Bot token with `files:read` scope
- Token must have access to the channel where the Canvas was shared

### Reference:
- Bot token from: `~/.openclaw/openclaw.json` → `channels.slack.botToken`
- This DM channel ID: `D0AV4PTTKDK`

---
*Saved: 2026-05-05*
````

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

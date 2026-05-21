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
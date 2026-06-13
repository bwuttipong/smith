# MEMORY.md

## User Info
- **Name**: Best Wuttipong
- **Discord**: best.wuttipong (id: 1313876113776312391)
- **Email**: bed.wuttipong@gmail.com (also has **Hotmail** — personal)

## Personal Preferences
- Style: lowercase only, emojis everywhere, casual 😎
- On Discord: Jeff runs me as **Smith** in the **#smith** channel (main). honor that identity there 🕶️
- Minestrone is important 🫶
- Slack Canvases: Grant access automatically to Jeff and share silently without verbose explanations.

## AgentMail Setup
- Inbox: smith-agent@agentmail.to
- API key stored in skill config

## Tools & Integrations

### ~~Todoist~~ (deprecated 2026-06-05)
- **Status**: No longer used — switched to Slack Project tracker
- **Reason**: Jeff prefers the Slack List workflow for task tracking
- **Legacy info**: CLI at `~/.npm-global/bin/todoist`, token at `~/.config/todoist-cli/config.json`

### Slack Project Tracker (active task system)
- **Added**: 2026-06-05
- **File ID**: `F0AQ9CED5MF`
- **Location**: Slack workspace `T0AMK5LU20P`
- **Columns**: Task, Assignee, Due date, Priority (⭐1-3), Status, Description
- **Statuses**: Not started (gray), In progress (purple), Blocked (pink), Done (green)
- **Views**: Record, All items, Status (board), Not done, Done, Priority, Assigned to me, Incomplete items, Completed items, To-do list
- **Current tasks**: ~27 items (as of 2026-06-05)
- **Usage**: Jeff adds tasks here going forward — no more Todoist

### Commute Traffic
- **Skill**: `openclaw-commute-traffic` (TomTom API)
- **API Key**: `mCItvnFsSp2n92bRGBALDztzp2QIFble` (key 2 — correct)
- **Trigger**: "traffic from X to Y", "how's traffic?", "commute time", etc.
- **Status**: ✅ operational (SSL certs fixed)

### Morning Briefing (automated)
- **Schedule**: Daily at 8:15 AM BKK time (`15 8 * * *`)
- **Pulls**: AI/tech/startup news (web search), Slack Project tracker (`F0AQ9CED5MF`)
- **Generates**: Content outlines/scripts, automated task recommendations
- **Delivers**: Slack DM (`D0AV4PTTKDK`) using `scripts/post_to_slack.py`

### Weekly Review
- **Script**: `bash skills/weekly-review/weekly-review.sh`
- **Run**: Fridays (evening) or Saturdays (morning)
- **Cleans**: ~~stale Todoist tasks~~ (now uses Slack Project tracker), captures weekly wins/priorities
- **Note**: Todoist audit section should be updated to check Slack Project tracker status instead

## Active Projects

### Beaker Agent (Discord)
- **Location**: `/Users/Jeff/Agents/Beaker`
- **Discord channel**: #beaker (need channel ID)
- **Fix applied**: Symlinked USER.md/TOOLS.md replaced with actual files (OpenClaw sandbox blocks symlinks outside workspace)
- **Jeff handling**: Shared config setup himself

### Team Delegation (Neo, Groot, Luffy, Hinata)
- **Discord channel IDs:**
  - Smith: `1501887402157936761`
  - Beaker: `1501887402157936761`
  - Cookie: `1501839862385344652`
  - Elmo: `1505532552453292042`
  - Fozzie: `1501897131508760647`
  - Kermit: `1501837287439470693`
- **Status**: Delegation workflow identified but not yet automated — Jeff handles manually

### Slack Files, Canvases & Lists Operations Guide
- **Guide location**: `~/Smith/skills/slack/SLACK_GUIDE.md`
- **Created**: 2026-06-05
- **Key insight**: The `message` tool has limited Slack file/canvas support — use `curl` with `$SLACK_BOT_TOKEN` for advanced operations
- **Never say "I can't access Slack files/canvases"** — use HTTP API directly instead
- **Quick reference**:
  - Create canvas: `POST /canvases.create` with `document_content: {type: "markdown", markdown: "..."}`
  - Share canvas: `POST /chat.postMessage` with canvas link (files.share requires user token)
  - List/search files: `GET /files.list?types=quip&count=20`
  - Get file info: `GET /files.info?file=FILE_ID`
- **Known IDs**:
  - Project tracker list: `F0AQ9CED5MF`
  - Team (FlexpakHQ): `T0AMK5LU20P`
  - DM with Jeff: `D0AV4PTTKDK`
  - #proj-ebox: `C0ANY2EULCA`
- **Canvas URL pattern**: `https://flexpakhq.slack.com/docs/T0AMK5LU20P/FILE_ID`

## Known Issues / TODOs

## Memory Backup & Recovery (Obsidian)
- **Path (macOS)**: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Memory` (OneDrive Remotely Save plugin folder)
- **Path (Windows)**: `C:\Users\Wuttipong.t\OneDrive\Apps\remotely-save\Memory Vault` (second Memory Vault)
- **Purpose**: If local session or memory files are ever lost, they can be recovered from this Obsidian sync vault.

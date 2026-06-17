# MEMORY.md

## User Info
- **Name**: Best Wuttipong
- **Discord**: best.wuttipong (id: 1313876113776312391)
- **Email**: bed.wuttipong@gmail.com (also has **Hotmail** — personal)

## Personal Preferences
- Style: lowercase only, emojis everywhere, casual 😎
- On Discord: Jeff runs me as **Smith** in the **#smith** channel (main). honor that identity there 🕶️
- Minestrone is important 🫶
- **Trigger alias (permanent, survives /reset + model changes):** `dict <word>` = `/english-thai-dict <word>` — run `python3 /Users/Jeff/.agents/skills/english-thai-dict/dict.py <word>`. Treat it as the english-thai-dict skill invocation in any context.

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

### english-thai-dict (personal skill + workspace mirror)
- **Personal (source of truth):** `/Users/Jeff/.agents/skills/english-thai-dict/`
- **Workspace mirror (added 2026-06-15):** `~/Smith/skills/english-thai-dict/` — pushed to github.com/bwuttipong/smith
- **CLI:** `python3 /Users/Jeff/.agents/skills/english-thai-dict/dict.py <word>` (both paths work)
- Built 2026-04-09, last sync 2026-06-03
- Single-word lookup, ~20-word built-in dictionary; `words.txt` has reference list
- Trigger: "what does X mean in Thai", "แปลว่าอะไร", vocab help
- Optional: `pip install pythainlp requests` for API expansion
- **Sync rule:** personal is the source of truth — if you change it, mirror to workspace and push.

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

### OutsourceEF9 (tpn-outsource)
- **Location**: `c:\Users\Wuttipong.t\Workspaces\OutsourceEF9`
- **Framework**: WinForms, .NET 9.0 (windows), EF Core 9.0.0, ClosedXML 0.105.0
- **Database Config**: `config.json` path resolved dynamically via `OUTSOURCE_CONFIG_PATH` environment variable, falling back to `\\192.168.95.200\TPKShare\IT\Outsource\config.json`.
- **Deploy**: Run `./publish.ps1` script to build and copy ClickOnce setup files to `\\192.168.95.200\TPKShare\IT\Outsource\OutsourceEF9\`.
- **Repository**: Initialized Git to track source control.

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

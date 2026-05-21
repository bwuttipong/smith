# MEMORY.md

## User Info
- **Name**: Best Wuttipong
- **Discord**: best.wuttipong (id: 1313876113776312391)
- **Email**: bed.wuttipong@gmail.com

## Personal Preferences
- Style: lowercase only, emojis everywhere, casual 😎
- On Discord: Jeff runs me as **Smith** in the **#smith** channel (main). honor that identity there 🕶️
- Minestrone is important 🫶

## AgentMail Setup
- Inbox: smith-agent@agentmail.to
- API key stored in skill config

## Tools & Integrations

### Todoist
- **Skill**: `skills/todoist/SKILL.md`
- **CLI**: `~/.npm-global/bin/todoist`
- **Token**: stored at `~/.config/todoist-cli/config.json`
- **Commands**: today, tasks, add, done, projects, search
- **Setup**: Installed `todoist-ts-cli@^0.2.0`, authenticated on 2026-05-11
- **Stale onboarding tasks to delete (from July):**
  - `66JVrQMcwJVpWWJP` — productivity method quiz
  - `66JWCcCpRVxWqjfw` — free apps and plugins  
  - `66JWQjRr2p4QXj4w` — getting started guide

### Commute Traffic
- **Skill**: `openclaw-commute-traffic` (TomTom API)
- **API Key**: `mCItvnFsSp2n92bRGBALDztzp2QIFble` (key 2 — correct)
- **Trigger**: "traffic from X to Y", "how's traffic?", "commute time", etc.
- **Status**: ✅ operational (SSL certs fixed)

### Morning Briefing
- **Script**: `bash skills/morning-briefing/morning-briefing.sh`
- **Run**: During morning heartbeats (7-9 AM) or on demand
- **Pulls**: weather, Todoist today, AgentMail inbox, Obsidian recent note

### Weekly Review
- **Script**: `bash skills/weekly-review/weekly-review.sh`
- **Run**: Fridays (evening) or Saturdays (morning)
- **Cleans**: stale Todoist tasks, captures weekly wins/priorities

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

## Known Issues / TODOs

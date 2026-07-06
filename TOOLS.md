# TOOLS.md - Local Notes

Environment-specific setup: camera names, SSH hosts, TTS voices, device nicknames. Kept separate from skills so skills stay shareable and this stays private.

## Gotchas

- **LINE strips triple-backtick code blocks** — content inside ``` goes blank. Send commands/code as plain text on LINE.

## Work Devices

- **FX-Programmer-NB1** → `10.100.99.24` (Jeff's company laptop, TPN internal network @ Wellgrow)
- **Employer ID** → `3253768` (TPN Flexpak)

---

## Skills Reference

### Bear Notes (`grizzly` CLI) 🐻
- Skill: `bear-notes/SKILL.md` · Requires Bear app running + API token at `~/.config/grizzly/token`
- `grizzly create --title "..." --tag work`, `open-note --id X`, `add-text --id X --mode append`, `open-tag --name work`

### Oracle — code review/debug 🧿
- CLI: `oracle` (`npm install -g @steipete/oracle`) · Sessions at `~/.oracle/sessions`
- `oracle --dry-run summary -p "<task>" --file "src/**"` · `--engine browser --model gpt-5.2-pro` for full runs
- One-shot: include full context (stack, build cmds, errors, paths) upfront. Reattach: `oracle status --hours 72`

### Commute Traffic 🚗
- Script: `skills/commute-traffic/scripts/check_traffic_google.py` · Key: `~/.config/gmaps/api_key`
- Trigger: "traffic from X to Y", "should I leave now?" → returns route, delay, congestion (🟢/🟡/🔴), alternatives
- Migrated TomTom → Google Maps (2026-06-29). Incident detection solid on main highways, thin on local sois.
- Jeff's default route: Ban Suan, Chonburi → Wellgrow Industrial Estate

### Web Search
- **Primary:** Brave Search — key stored in `~/.config/brave/api_key` (do not paste the raw key into notes). Script: `skills/brave-search/search.js "query" -n 5`; page content via `content.js <url>`
- **Backup 1:** free-google-search-with-browser
- **Backup 2 (on Brave 429):** Prismfy — `skills/prismfy-search/search.sh "query" --engine brave` (separate rate-limit bucket; try `--engine google` too)

### English Learning
Rotate by need — vocab: `english-daily` (SRS flashcards, streaks); conversation: `english-bestie` (voice-first) or `english-oral-tutor` (pronunciation, TTS/STT); grammar/writing/exam prep: `english-learning-coach`; quick word lookups: `english-thai-dict` (personal skill, single-word EN↔TH, `python3 .../dict.py <word>`; source of truth is the personal copy at `~/.agents/skills/`, mirror to `~/Smith/skills/` after edits).

### Google Antigravity 2.0
- Google's agentic IDE/CLI (replaces Gemini CLI), launched May 2026. Docs: antigravity.google/docs
- MCP Memory Bridge already configured (shared with OpenClaw + Hermes)
- Models: Gemini 3.1 Pro/3 Flash, Claude Sonnet 4.6/Opus 4.6, GPT-OSS 120B. Free tier rate-limited (quotas cut 4x since Dec 2025).
- If Jeff brings it up: check `antigravity --version`, confirm MCP bridge connects, remind him of the three-way memory share.

### Apple Reminders
- CLI: `remindctl` (`brew install steipete/tap/remindctl`) — `today`, `add --title "..." --due tomorrow`, `complete <id>`, `list <name> --create`

### GOG (Google CLI)
- CLI: `gog` v0.12.0 · Account: `bed.wuttipong@gmail.com` · Publishing domain: `bestwuttipong.dev`
- Covers Calendar/Gmail/Drive/Contacts/Sheets/Docs
- **Token expires weekly** (testing mode) — re-auth: `gog auth credentials <client_secret.json> && gog auth add bed.wuttipong@gmail.com --services gmail,calendar,drive,contacts,sheets,docs`

### Obsidian
- Vault: `~/Smith/wiki/` — daily notes, structured knowledge, memory sync

### Sticky Notes (Windows)
- New note + paste: `Set-Clipboard -Value "text"`; launch via ONENOTE.EXE `/stickynotes`; send `^n` then `^v` via WScript.Shell

---

Add whatever helps you do your job. This is your cheat sheet.
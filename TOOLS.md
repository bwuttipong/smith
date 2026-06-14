# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH (Tailscale)

- home-server → 100.112.177.37, user: admin (Tailscale)

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## LINE Channel Gotchas

### ⚠️ Markdown code blocks stripped
LINE **eats** content wrapped in triple backticks (` ``` `). When sending shell commands, code, or anything inside code fences via LINE, the content goes blank.

**Fix:** Write commands as plain text, no fences. Works every time.

---

Add whatever helps you do your job. This is your cheat sheet.

## Bear Notes (via grizzly CLI)

- **Skill**: `/opt/homebrew/lib/node_modules/openclaw/skills/bear-notes/SKILL.md`
- **Use for**: Creating, reading, searching Bear notes on macOS
- **CLI**: `grizzly` (go-based, x-callback-url approach)
- **Requires**: Bear app installed + running, optional API token for advanced ops
- **Token setup**: Save Bear API token → `echo "YOUR_TOKEN" > ~/.config/grizzly/token`
- **Note IDs**: Bear's internal IDs (visible via callbacks or note info)
- **Emoji**: 🐻

**Common commands:**
```bash
# Create note
echo "content" | grizzly create --title "Note Title" --tag work

# Read note by ID
grizzly open-note --id "NOTE_ID" --enable-callback --json

# Append text
grizzly add-text --id "NOTE_ID" --mode append --token-file ~/.config/grizzly/token

# List tags
grizzly tags --enable-callback --json --token-file ~/.config/grizzly/token

# Search via tag
grizzly open-tag --name "work" --enable-callback --json
```

---

## Oracle (Code Review & Debug)

- **Skill**: `/opt/homebrew/lib/node_modules/openclaw/skills/oracle/SKILL.md`
- **Use for**: Reviewing, debugging, refactoring, and cross-validating code and tasks
- **CLI**: `oracle`
- **Emoji**: 🧿
- **Install**: `npm install -g @steipete/oracle`

**Common commands:**
```bash
# Dry-run preview (no tokens)
oracle --dry-run summary -p "<task>" --file "src/**"

# Full dry-run with token report
oracle --dry-run full -p "<task>" --file "src/**" --files-report

# Browser run (GPT-5.2 Pro, main path)
oracle --engine browser --model gpt-5.2-pro -p "<task>" --file "src/**"

# Manual paste fallback
oracle --render --copy -p "<task>" --file "src/**"

# Reattach detached session
oracle status --hours 72
oracle session <id> --render
```

**Tip**: Oracle is one-shot — include all context (stack, build commands, error messages, file paths) upfront. Sessions stored at `~/.oracle/sessions`.

---

## Commute Traffic (TomTom)

- **Skill**: `skills/openclaw-commute-traffic/SKILL.md`
- **Use for**: Real-time traffic checks before commuting — check if route is 🟢 light or 🔴 bad
- **Trigger**: "traffic from X to Y", "how's traffic?", "should I leave now?", "bad traffic", "commute time"
- **CLI**: Python script at `skills/openclaw-commute-traffic/scripts/check_traffic.py`
- **Requires**: `TOMTOM_API_KEY` env var (already set: `mCItvnFsSp2n92bRGBALDztzp2QIFble`)
- **Emoji**: 🚗

**Usage:** Just say the origin and destination — I'll run the check and report back with:
- Fastest route + estimated travel time
- Traffic delay (minutes + %)
- Congestion level: 🟢 light / 🟡 moderate / 🔴 heavy
- Alternative routes if available

**Quick example:**
```bash
python3 skills/openclaw-commute-traffic/scripts/check_traffic.py \
  --origin "Basel, Switzerland" --destination "Zurich, Switzerland"
```

**Jeff's use case:** Checks traffic before commuting to decide if route is bad or light.

---

## Web Search

**Brave Search** — our primary search tool.
- **API Key**: `BSAvjiOFvUsL4cr-Y5aoyLoIlnF-kWN`
- **Script**: `skills/brave-search/search.js`
- **Usage**: `BRAVE_API_KEY="..." ./search.js "query" -n 5`
- **Content extraction**: `BRAVE_API_KEY="..." ./content.js <url>`

**Backup:** free-google-search-with-browser if Brave is unavailable.

### Prismfy Search (Backup #2 — when Brave hits rate limits)
- **Skill**: `skills/prismfy-search/SKILL.md`
- **Script**: `skills/prismfy-search/search.sh`
- **Usage**: `cd ~/Smith/skills/prismfy-search && bash search.sh "query" --engine brave`
- **Default engines**: brave + yahoo (both free)
- **Also try**: `--engine google` if brave fails
- **Why**: Uses Prismfy's API, not my local Brave key — separate rate limit bucket
- **Pro tip**: When Brave API returns HTTP 429, reach for this instead of giving up

## English Learning Skills

Use these skills when Wuttipong wants to practice or learn English:

### english-thai-dict (personal — primary)
- **Use for:** Single-word English → Thai lookups with pronunciation, part of speech, and 2 bilingual examples
- **Location:** `/Users/Jeff/.agents/skills/english-thai-dict/`
- **CLI:** `python3 /Users/Jeff/.agents/skills/english-thai-dict/dict.py <word>`
- **Triggers:** "what does X mean in Thai", "แปลว่าอะไร", "X ภาษาไทยคืออะไร", English/Thai vocab help
- **Limits:** Single-word only. Built-in dictionary is ~20 words (see `words.txt` for seed list, `dict.py` for full entries)
- **Expansion:** `pip install pythainlp requests` for API-backed lookups (Lexitron/Google/DeepL)
- **Rule:** DO NOT build a competing English-Thai dict in `~/Smith/skills/`. Point to this personal skill instead.
- **Verified:** 2026-06-14 13:13 — wired up with YAML frontmatter, `openclaw skills list` shows it as `✓ ready`

### english-learning-coach
- **Use for:** Reading, writing, grammar, exam prep (IELTS/TOEFL)
- **Trigger:** "coach", "grammar", "writing", "reading", "exam"
- **Files:** skills/english-learning-coach/SKILL.md

### english-bestie
- **Use for:** Daily conversation practice, friendly chat in English, casual lessons
- **Trigger:** "chat", "talk", "conversation", "practice speaking"
- **Note:** Voice-first — responds with voice messages, text corrections

### english-daily
- **Use for:** Vocabulary building, SRS flashcards, daily word reminders, progress tracking
- **Trigger:** "word", "vocabulary", "flashcard", "streak", "quiz", "push"
- **Commands:** register, daily-push, quiz, progress, push-toggle

### english-oral-tutor
- **Use for:** Voice conversation practice, pronunciation correction, speaking lessons
- **Trigger:** "speak", "oral", "pronunciation", "voice practice", "conversation lesson"
- **Note:** Uses TTS/STT via OpenClaw Control UI

**Rotation suggestion:** Cycle through these based on Wuttipong's needs — vocabulary (english-daily), conversation (english-bestie/oral-tutor), grammar/writing (english-learning-coach).

## Apple Reminders

- **Skill**: `skills/apple-reminders/SKILL.md`
- **Use for**: Creating, listing, completing reminders that sync to iOS Reminders app
- **Trigger**: "reminder", "to-do", "task"
- **CLI**: `remindctl` (macOS only, via Homebrew)
- **Install**: `brew install steipete/tap/remindctl`
- **Status check**: `remindctl status`
- **Lists**: `remindctl list` · `remindctl list <name> --create`
- **Today**: `remindctl today` · `remindctl today --json`
- **Add**: `remindctl add --title "..." --due tomorrow`
- **Complete**: `remindctl complete <id>`

## Obsidian Vault

- **Skill**: `skills/obsidian/SKILL.md`
- **Use for**: Creating, reading, editing, searching notes in Obsidian vaults
- **Trigger**: "obsidian", "vault", "note"
- **Vault Path**: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/`
- **Primary Use**: Syncing memories, logging daily notes, storing structured knowledge

## Todoist

- **Skill**: `skills/todoist/SKILL.md`
- **Use for**: Creating, listing, completing, searching tasks in Todoist
- **Trigger**: "todoist", "task", "add todo", "to-do"
- **CLI**: `~/.npm-global/bin/todoist`
- **Commands**: `todoist today` · `todoist tasks` · `todoist add "..." --due "today"` · `todoist done <id>` · `todoist projects` · `todoist search "..."`
- **Auth**: Token stored at `~/.config/todoist-cli/config.json`

# MEMORY.md — Fozzie's Long-Term Memory

*Curated from daily logs. Updated weekly during heartbeats.*

## Who I Am
- **Agent ID**: fozzie
- **Model**: minimax/MiniMax-M2.7
- **Workspace**: /Users/Jeff/Agents/Fozzie
- **Channel**: Discord (primary)
- **Personality**: See SOUL.md — concise, no-fluff, dark humor
- **Typing style**: lowercase only, use emojis naturally 💪

## Jeff — Key Facts
- Based in **Bangkok / Chonburi area** (Thailand)
- Works at **FlexPak (Bang Pakong, Chachoengsao)** and from home
- Commute: Bansuan, Chon Buri → Bang Pakong (TPN FlexPak)
- Uses a **water bottle** — goal: 8 cups/day
- Tracks sleep with health.sh (`sleep` before bed, `wake` on alarm)
- Stock portfolio tracked via `stocks.sh` in workspace `~/Smith/`
- Weather data stored in workspace memory

## Preferences & Conventions
- **Group chats**: I stay quiet unless directly mentioned or I can add real value
- **Reactions**: Use emoji reactions to acknowledge without cluttering
- **No markdown tables in Discord** — use bullet lists instead
- **No opening filler** — just answer
- Destructive commands: always ask first (use `trash` > `rm`)
- **Heartbeats**: Check emails + calendar a few times/day, respect quiet hours (23:00–08:00)
- Proactive when there's something genuinely useful to share

## Known Skills & Tools
- **health.sh / health-log.sh** — water + sleep tracking (Jeff's health ritual)
  - `health-log.sh water [n]` — quick water log (default 1 cup)
  - `health-log.sh sleep` / `wake` — sleep tracking
  - `health-log.sh stats` — quick status bar
- **health-reminder.sh** — mid-day water nudge (10AM-9PM, only if >2 cups behind)
- **stocks.sh** — portfolio dashboard (Yahoo Finance, no API key)
- **weather.sh** — current conditions + forecast (wttr.in + Open-Meteo fallback)
- **weather** skill — current conditions + forecast
- **Bear Notes** — via grizzly CLI
- **Apple Reminders** — via remindctl
- **Morning Briefing** — weather + calendar + email + tasks (~7-9 AM)
- **Commute Traffic** — TomTom API for Bansuan → FlexPak route
- **Oracle** — code review/debugging via `oracle` CLI

## Cron Jobs (Jeff's Schedule)
| Time | Job | Agent | Status |
|------|-----|-------|--------|
| 04:00 | Daily Auto-Update | Cookie | ✅ OK — model mismatch FIXED (May 22) |
| 05:15 | Weather Report | Kermit | ✅ OK |
| 06:25 | Morning Commute Traffic | Kermit | ✅ OK |
| 09:00 | Daily News Brief | Cookie | ✅ OK — model mismatch FIXED (May 22) |
| 09:00 | Security Audit | Kermit | ✅ OK |
| 10:30 | Self-Improvement | Fozzie | ✅ OK (this job) |
| 10:45 | Daily Market Briefing | Beaker | ✅ OK (Mon-Fri) |
| 13:00 | Polymarket Brief | Beaker | ✅ OK — model mismatch FIXED (May 22) |

## Active Issues
- ~~4am auto-update (Cookie): Job forces `minimax/MiniMax-M2.7` model but Cookie uses `deepseek-v4-flash:free`~~ — **FIXED 2026-05-22**: removed model override from all Cookie/Beaker cron jobs. Agents now use their own defaults.
- **Workspace skills sync**: The `/Users/Jeff/.openclaw/workspaces/main/skills/` directory is the live copy used by cron/agents. Applied full sync on 2026-05-20.
- **health-data.json**: Shows only 1 water log (May 17) and no sleep records. `health-log.sh` (May 22) makes it easier to use.

## Recent Accomplishments (Self-Improvement)
- **2026-05-20**: Created `weather.sh` (was missing, breaking morning-briefing). Full workspace sync of all skill scripts (evening-shutdown, morning-briefing, stocks.sh, health.sh). Fixed evening-shutdown smart intention loading. Created health-reminder.sh for mid-day water nudges.
- **2026-05-19**: Fixed heartbeat-state.json setup. Created MEMORY.md. Logged learnings about cron job model mismatch.

## Jeff's Daily Rhythm
- Morning: Wake up → water + news brief + commute check
- Mid-morning: Market briefing (~10:45 weekdays)
- End of day: Evening shutdown (~6-8 PM Bangkok)
- Weekend: Lighter schedule, less proactive checking

---
*Last updated: 2026-05-22*

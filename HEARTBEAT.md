# HEARTBEAT.md

## Lightweight Heartbeat Checklist

- Check `memory/heartbeat-state.md` for last-run markers
- If `memory/` had no changes since last run → HEARTBEAT_OK
- Sync critical memories to Obsidian: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/`
- Log significant events to `memory/YYYY-MM-DD.md`
- **Morning (7-9 AM):** Run `bash skills/morning-briefing/morning-briefing.sh` for Jeff's daily briefing (weather + tasks + inbox + obsidian)
- **Evening (6-8 PM):** Run `bash skills/evening-shutdown/evening-shutdown.sh` for Jeff's end-of-day shutdown (tomorrow's calendar + task review + daily log + tomorrow's priorities)

**Rule:** Keep heartbeat lean. If nothing needs attention, respond HEARTBEAT_OK.
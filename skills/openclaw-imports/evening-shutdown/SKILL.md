---
name: evening-shutdown
description: Jeff's end-of-day shutdown routine — reviews tomorrow's calendar, clears today's tasks, logs a brief reflection, and prepares the workspace for tomorrow. Run during evening heartbeats (6-8 PM Bangkok time) or when Jeff asks for an "evening check-in" / "end of day" / "shutdown".
metadata:
  clawdbot:
    emoji: "🌙"
    requires: []
---

# Evening Shutdown Skill

Jeff's end-of-day ritual: clears cognitive load, logs what happened today, previews tomorrow.

## Two Modes

### Interactive (manual)
```bash
./evening-shutdown.sh
```
Reads from terminal: reflection log, tomorrow's priorities.

### Auto (cron-ready)
```bash
./evening-shutdown-auto.sh
```
Non-interactive. Reads intentions from `memory/.tomorrow-intentions.txt` if pre-written, otherwise skips. Perfect for automatic 6-7PM cron runs.

## What Each Does

| Step | Interactive | Auto |
|------|-------------|------|
| Tomorrow's calendar | ✓ | ✓ |
| Today's task summary | ✓ | ✓ |
| Daily reflection log | ✓ (prompts) | ✓ (auto from `.last-session-log.txt`) |
| Tomorrow's priorities | ✓ (prompts) | ✓ (reads from intentions file) |
| Carry-over to tomorrow's memory | ✓ | ✓ |

## Interactive Mode Output

```
🌙 Evening shutdown, Jeff — Friday, May 15
⏰ Time: 06:30 PM (Bangkok)

📅 TOMORROW (Saturday, May 16)
----------------------------------------
• 10:00 AM — Coffee with Sarah
• ...

✅ TODAY — Task Summary
----------------------------------------
( Todoist output )

📓 DAILY LOG
----------------------------------------
Type one line — what mattered most today? (Enter to skip)
> _

🔭 TOMORROW — Top Priorities
----------------------------------------
What are your 1-3 must-dos tomorrow? (one per line, empty line to finish)
> _
> _
>

🌙 Good night, Jeff. Tomorrow's a clean slate.
```

## Module Subcommands (interactive)

```bash
./evening-shutdown.sh calendar   # Just tomorrow's calendar
./evening-shutdown.sh tasks      # Just task summary
./evening-shutdown.sh log        # Just log entry prompt
```

## Pre-writing Tomorrow's Priorities (for auto mode)

Write your intentions to `memory/.tomorrow-intentions.txt` during the day:
```
Finish project proposal
Call dentist
Prep slides for Monday
```
Each line becomes one bullet in tomorrow's memory note.

## Notes

- Calendar: `gog` → `himalaya` → Obsidian daily note (fallback order)
- Log entry goes to `memory/YYYY-MM-DD.md`
- Priorities saved to `memory/YYYY-MM-DD.md` under "## Top Priorities"
- If any source fails, output the others — ritual still completes
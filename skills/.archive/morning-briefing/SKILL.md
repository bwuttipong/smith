---
name: morning-briefing
description: Generate a morning briefing for Jeff — weather, today's calendar, urgent emails, Todoist tasks, and any other relevant items. Run during morning heartbeats or when Jeff asks for a "morning update" / "daily briefing".
homepage: https://github.com/smith
metadata:
  clawdbot:
    emoji: "🌅"
    requires: []
---

# Morning Briefing Skill

Assembles a concise, actionable morning briefing for Jeff. Run this during morning heartbeats (~7-9 AM Bangkok time) or whenever Jeff asks for his daily update.

## What It Pulls

The briefing aggregates from multiple sources into one clean snapshot:

- **Weather** — current conditions + forecast for Bangkok
- **Calendar** — today's events (via himalaya or gog if available)
- **Email** — urgent/unread emails (AgentMail inbox)
- **Todoist** — today's tasks

## Output Format

```
🌅 Good morning, Jeff — here's your day.

📅 CALENDAR
• [time] Event Name (location)
• ...

📧 INBOX
• [from] Subject — one line summary
• ...

✅ TASKS
• [p1] Task name
• ...

🌤️ WEATHER
• 28°C, partly cloudy, 70% humidity
• Rain expected 3PM+

⏰ TIME NOW: 8:00 AM Bangkok
```

## Usage

```bash
# Run full briefing
./morning-briefing.sh

# Individual modules
./morning-briefing.sh weather
./morning-briefing.sh tasks
./morning-briefing.sh email
```

## Notes

- Weather uses `skills/weather/weather.sh` or direct API call
- Email uses AgentMail inbox API (smith-agent@agentmail.to)
- Todoist uses `~/.npm-global/bin/todoist today`
- If any source fails, output the others without error
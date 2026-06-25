---
name: weekly-review
description: Jeff's weekly review ritual — audits Todoist stale tasks, logs the week's wins and next week's priorities, and previews the calendar. Run Fridays (evening) or Saturdays (morning) or on demand.
metadata:
  clawdbot:
    emoji: "🧹"
    requires: []
---

# Weekly Review Skill

Jeff's Saturday morning (or Friday evening) ritual for closing out the week with clarity and starting the next one with intention.

## Why It Exists

Todoist is full of onboarding cruft from July. Calendar is unverified. There's no consolidated weekly review — just tasks accumulating without review. A weekly ritual prevents this leak from compounding.

## What It Does

| Step | What | Source |
|------|------|--------|
| 📓 Week in review | Scans memory files from the past week | `memory/YYYY-MM-DD.md` |
| ✅ Todoist audit | Flags overdue + onboarding-cruft tasks | Todoist CLI (`~/.npm-global/bin/todoist`) |
| 📅 Week ahead | Shows next 7 days of calendar events | gog calendar |
| 🌟 Wins | Captures what went well this week | User input → memory |
| 🎯 Priorities | Sets top 3 intentions for next week | User input → memory |
| 💾 Memory | Saves full review to `memory/weekly-review-YYYY-MM-DD.md` | Workspace |

## Output Format

```
🧹 Weekly Review — Jeff
⏰ 10:00 AM (Bangkok)

📓 WEEK IN REVIEW
📌 2026-05-15.md
   Evening shutdown ran at 6:14 PM...
📌 2026-05-14.md
   Created morning-briefing skill...

✅ TODOIST AUDIT — Stale & Overdue
⚠️  6 onboarding tasks detected (created Jul — likely obsolete)
→ Suggested action: delete these 6 onboarding tasks

📅 WEEK AHEAD — May 17 → May 23
(gog calendar output or: not yet connected)

🌟 THIS WEEK'S WINS
• [user input]

🎯 NEXT WEEK — Top 3 Priorities
• [user input]

✓ Saved to: weekly-review-2026-05-16.md
```

## Usage

```bash
# Run full weekly review
bash skills/weekly-review/weekly-review.sh

# No interactive — just audit & save (good for cron)
bash skills/weekly-review/weekly-review.sh --audit-only
```

## Notes

- Uses `~/.npm-global/bin/todoist tasks` and `today`
- Uses `gog calendar events` for week-ahead (gog must be authenticated)
- Creates `memory/weekly-review-YYYY-MM-DD.md` with full review
- If any source fails, output the others without error — the ritual still completes
- **Todoist cleanup**: The 6 July onboarding tasks should be deleted; the script surfaces their IDs for manual cleanup

## What This Saves Jeff

- ~10-15 min/week of Todoist chaos management
- Automatic memory of week wins (leverage for future decisions)
- Clear weekly intention instead of task drift
- Surfaces the 6 stale July onboarding tasks for one-shot cleanup
# Weekly System Maintenance — real check

Timestamp: 2026-07-26 21:44 ICT
Notion page: Weekly System Maintenance — 3a80da1b1be680c49ddce1b3957168ed

## Verified and checked

- Reset checklist state before work: all checklist boxes were unchecked when inspected.
- Hermes/session health: `hermes doctor` ran successfully.
- Active profile/config/model: live session is on OpenAI Codex / gpt-5.5; fallbacks not set.
- Scheduled jobs: `hermes cron list` reports no scheduled jobs.
- Logs/errors: checked recent Hermes logs; only old memory-bridge MCP warnings from 2026-07-20 surfaced in the sampled recent files.
- Memory/skills health: profile memory is near full; doctor sees 1244 sessions and memory files present.
- Gateway restart: not needed.
- Delivery targets: Telegram and LINE have configured DM targets; Discord has none.
- Notion To-do list: queried successfully; counts before update were Done 1, Not started 2.
- Weekly memory review: checked 2026-07-21 through 2026-07-26; 2026-07-20 daily file missing.
- Git status: 147 tracked modifications, 137 untracked files; branch master is ahead 1, behind 0.
- AgentOS dashboard: localhost:3737 returned HTTP 200.
- English Recall/SRS: cards file exists; 2875 cards, 2864 due, CEFR B2; helper scripts in ~/Smith/scripts are missing.
- Apollo/voice: active in this interface; no desktop/media app opened.
- Disk space: 98 GiB available, 78% used.
- Payday/admin reminder check: current date is 2026-07-26; next payday cycle is later.

## Left unchecked / carryover

- Run Hermes update: update available, 417 commits behind; not run during voice maintenance to avoid a live-agent upgrade surprise.
- Google Calendar review: blocked; Google Workspace token is not authenticated and `googleapiclient` is missing.
- LINE/Telegram test message: not sent; external sends need explicit approval.
- Commit and push Smith repo: not done; repo has 284 dirty paths and needs review before committing.
- Close completed tasks / move unfinished tasks / create next weekly duplicate: not done automatically.
- Work / BOXSOFT review: no live source inspected in this run.
- Cleanup downloads/desktop/stale processes: inspected system/disk/processes only; no destructive cleanup or process killing done.

## Top 3 next priorities

1. Repair Google Workspace auth/dependency so calendar review can run.
2. Decide whether to run `hermes update` and clear MESSAGING_CWD deprecation.
3. Review Smith dirty repo state before any commit/push.

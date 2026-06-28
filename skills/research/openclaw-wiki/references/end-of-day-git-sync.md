# End-of-Day Git Sync Ritual

When Jeff says "good night" (or equivalent end-of-day signal), run this on **every active profile** (Mac/Hermes and Windows/OpenClaw on Antigravity):

```bash
cd ~/Smith
git add -A
git commit -m "date summary — brief keyword description"
git push
```

## Why

- Ensures all changes flow between the Mac (daytime) and Windows/Antigravity (daytime) machines
- The repo is the single source of truth — both machines pull and push to it
- Prevents drift and lost work

## When

- **Trigger phrase**: "good night", "goodnight", "shutting down", "end of day"
- **Scope**: every profile that pushed changes during the day
- **Not needed**: if no files changed (check `git status` first)

## Commit message style

Keep it short and scannable. Include the date and 2-5 keywords:

```
sun 28 june: high agency wiki, antigravity migration prep
```

## On the company laptop (Monday morning first-run)

The script `scripts/migrate-antigravity-windows.ps1` must run first to move Antigravity into the workspace. After that, the normal git sync is ready.

## Related

- `openclaw-wiki` skill — ingesting wiki content that should also be synced
- `evening-shutdown` skill (hub-installed) — broader end-of-day routine that this complements

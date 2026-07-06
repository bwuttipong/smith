# Obsidian Vault Sync

## Vault Path

```
~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/Agent OS/
```

## Save Format

Files: `YYYY-MM-DD.md`

```markdown
# Agent OS — 2026-07-05

## Hermes — 14:30

**You:** What's the weather?

**Hermes:** It's sunny and 28°C in Chon Buri.

## OpenClaw — 14:35

**You:** Summarize my todos.

**OpenClaw:** You have 3 pending tasks...
```

## API Endpoints

- `POST /api/obsidian` — Save chat messages
- `GET /api/obsidian` — List saved files

## Request Body (POST)

```json
{
  "agent": "Hermes",
  "messages": [
    { "role": "user", "text": "Hello" },
    { "role": "agent", "text": "Hi there!" }
  ],
  "date": "2026-07-05"  // optional, defaults to today
}
```

## Notes

- Uses OneDrive sync (remotely-save plugin)
- Timezone: Asia/Bangkok (ICT)
- Creates folder if it doesn't exist
- Appends to existing file if same date

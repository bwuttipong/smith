# OpenRouter — Credits Reference

## API Endpoint

```bash
curl -s "https://openrouter.ai/api/v1/auth/key" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

## Response Format

```json
{
  "data": {
    "label": "sk-or-v1-569...9b9",
    "is_management_key": false,
    "is_provisioning_key": false,
    "limit": 0.01,              // Credit limit in USD (0 = unlimited)
    "limit_remaining": 0,       // Remaining credits in USD
    "limit_reset": null,        // ISO timestamp or null
    "include_byok_in_limit": false,
    "usage": 18.026186499,      // Total usage in USD
    "usage_daily": 0,           // Daily usage in USD
    "usage_weekly": 0,          // Weekly usage in USD
    "usage_monthly": 0,         // Monthly usage in USD
    "byok_usage": 0,            // Bring-your-own-key usage
    "byok_usage_daily": 0,
    "byok_usage_weekly": 0,
    "byok_usage_monthly": 0,
    "is_free_tier": false,
    "expires_at": null,         // ISO timestamp or null
    "creator_user_id": "user_3Acnw8TjZjbBlJqMY9iTDeQvNmp",
    "rate_limit": {
      "requests": -1,           // -1 = unlimited
      "interval": "10s",
      "note": "Deprecated field"
    }
  }
}
```

## Key Fields

| Field | Meaning |
|-------|---------|
| `limit` | Total credit limit in USD (0 = unlimited) |
| `limit_remaining` | Remaining credits (0 = empty) |
| `usage` | Total spent in USD |
| `is_free_tier` | Whether on free tier |
| `limit_reset` | When credits reset (null = no reset) |

## Quick Check One-Liner

```bash
source ~/.openclaw/.env && curl -s "https://openrouter.ai/api/v1/auth/key" -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f\"Credits: \${d['limit_remaining']:.2f} / \${d['limit']:.2f}\nUsed: \${d['usage']:.2f}\nFree tier: {d['is_free_tier']}\")"
```

## Troubleshooting

- **"User not found" (401)**: API key invalid or wrong key — check `~/.openclaw/.env` vs `~/.hermes/.env`
- **Rate limits**: Check `rate_limit.requests` (-1 = unlimited)
- **Key location varies**: Some users have keys in `~/.openclaw/.env`, others in `~/.hermes/.env`

## Notes

- OpenRouter credits are shared across all models
- Free models (`:free` suffix) don't consume credits
- BYOK (Bring Your Own Key) usage is tracked separately

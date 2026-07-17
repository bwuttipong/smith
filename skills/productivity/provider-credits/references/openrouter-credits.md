# OpenRouter — Credits Reference

## Two Endpoints — Different Data

### 1. `/v1/credits` — Account Balance (RECOMMENDED)
Shows total account balance across all keys. This is what you want for "how much do I have left?"

```bash
source ~/.openclaw/.env && curl -s "https://openrouter.ai/api/v1/credits" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

Response:
```json
{
  "data": {
    "total_credits": 52,        // Total deposited (USD)
    "total_usage": 41.56        // Total spent (USD)
  }
}
```
**Remaining = total_credits - total_usage**

### 2. `/v1/auth/key` — Per-Key Details
Shows limits, usage breakdown, and tier info for a specific key.

```bash
source ~/.openclaw/.env && curl -s "https://openrouter.ai/api/v1/auth/key" \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

Response:
```json
{
  "data": {
    "label": "sk-or-v1-569...9b9",
    "limit": 0.01,              // Per-key credit limit (0 = unlimited)
    "limit_remaining": 0,       // Remaining on this key's limit
    "usage": 18.026186499,      // This key's usage
    "usage_daily": 0,
    "usage_weekly": 0,
    "usage_monthly": 0,
    "is_free_tier": false,
    "expires_at": null
  }
}
```

⚠️ **The `limit` field is the PER-KEY limit, not account balance.** Use `/v1/credits` for actual balance.

## Quick Check One-Liner

```bash
source ~/.openclaw/.env && curl -s "https://openrouter.ai/api/v1/credits" -H "Authorization: Bearer $OPENROUTER_API_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin)['data']; print(f\"Balance: \${d['total_credits'] - d['total_usage']:.2f} remaining\nUsed: \${d['total_usage']:.2f} / \${d['total_credits']:.2f}\")"
```

## Free Models

Free models (`:free` suffix) don't consume credits. Available to everyone regardless of balance.

| Model | Suffix |
|-------|--------|
| tencent/hy3 | :free |
| nvidia/nemotron-3-ultra-550b-a55b | :free |
| google/gemma-4-31b-it | :free |

Rate limits apply on free tier (~20-30 req/min, ~500K-1M tokens/day).

## Key Fields

| Field | Meaning |
|-------|---------|
| `total_credits` | Total deposited (USD) |
| `total_usage` | Total spent (USD) |
| Remaining | `total_credits - total_usage` |
| `is_free_tier` | Whether on free tier |

## Troubleshooting

- **"User not found" (401)**: API key invalid — check `~/.openclaw/.env` vs `~/.hermes/.env`
- **Per-key limit confusion**: `/auth/key` shows per-key limits; use `/credits` for account balance
- **Key location varies**: Some users have keys in `~/.openclaw/.env`, others in `~/.hermes/.env`

## Notes

- OpenRouter credits are shared across all models
- Free models (`:free` suffix) don't consume credits
- BYOK (Bring Your Own Key) usage is tracked separately

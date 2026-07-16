---
name: provider-credits
description: "Check API credits, token balances, and billing status across AI providers. Use when the user asks about remaining tokens, credits, billing, or account balance for any AI provider."
version: 1.0.0
author: Smith
---

# Provider Credits

Check API credits, token balances, and billing status across AI providers.

## Quick Reference

### Xiaomi MiMo
- **API key location:** `~/.openclaw/.env` as `XIAOMI_API_KEY` (NOT `~/.hermes/.env`)
- **Base URL:** Check profile config (`~/.hermes/profiles/*/config.yaml`) for the actual base URL — may differ from plugin config
- **Credits endpoint:** NOT available — Xiaomi MiMo does not expose a credits/balance API
- **Key format:** `tp-` prefix = "token plan" key
- **Manual check:** Log into xiaomimimo.com portal

### Finding the Correct Base URL
1. Check plugin config: `~/.hermes/hermes-agent/plugins/model-providers/<provider>/plugin.yaml`
2. Check profile config: `~/.hermes/profiles/*/config.yaml` (may override plugin)
3. Test with models list: `curl -s "<base_url>/v1/models" -H "Authorization: Bearer <key>"`

### Common Provider Credits Endpoints

| Provider | Endpoint | Notes |
|----------|----------|-------|
| OpenRouter | `GET https://openrouter.ai/api/v1/auth/key` | Returns credits remaining |
| Anthropic | No API — check console | console.anthropic.com |
| OpenAI | Limited — `GET /v1/dashboard/billing/usage` | Requires cookie auth |
| Google | No API — check console | aistudio.google.com |
| Xiaomi MiMo | None | Check portal manually |

## Reference Files

- `references/xiaomi-mimo.md` — Xiaomi MiMo provider details, models, and debugging path.
- `references/openrouter-credits.md` — OpenRouter credits endpoint, response format, and troubleshooting.

## Pitfalls
- **Profile config overrides plugin config** for base URLs — always check both
- **Some providers don't expose credits endpoints** — user must check portal manually
- **API key location varies** by provider: `~/.openclaw/.env`, `~/.hermes/.env`, or config files
- **Key format hints at plan type:** `tp-` = token plan, `sk-` = standard API key

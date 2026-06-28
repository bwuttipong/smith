# Cron Duty Officer Pattern — Samantha + FreeRide

Set up Samantha as the cron duty officer to periodically check free model availability and report to Jeff.

## Setup

1. Install freeride if not already: `cd ~/.hermes/profiles/smith/skills/free-ride && uv pip install -e .`
2. Verify `OPENROUTER_API_KEY` is set in the gateway env file.
3. Create a cron job with Samantha as the executor:

```
cronjob action=create \
  name="samantha-duty-check" \
  schedule="0 */4 * * *" \
  prompt="You are Samantha... run freeride list, check availability, report to Jeff" \
  model="deepseek-v4-flash" \
  provider="opencode-go"
```

## Duty Checklist

Each shift Samantha runs:
1. `freeride list -n 30` — check all free models, note new/dropped
2. `freeride status` — verify current config is healthy
3. Save log to `~/Smith/memory/freeride-YYYY-MM-DD.md`
4. Report brief findings to Jeff

## Why This Pattern

Free models on OpenRouter come and go (rate limits, token depletion, new models appearing). A periodic check keeps Jeff aware without him having to manually poll. Samantha handles the routine; Smith handles the strategy.

## File Log

Each check saves to: `~/Smith/memory/freeride-YYYY-MM-DD.md`

---
name: crash-check
description: Check for car accidents on a commute route using TomTom traffic incident data. Use when the user asks about crashes, accidents, or incidents along their drive.
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    emoji: 💥
    requires:
      bins: [bash, curl, python3]
      env: [TOMTOM_API_KEY]
---

# Crash Check

Fetches and reports **accidents only** along a route. No travel times, no congestion levels, no routing — just crashes.

## Usage

```bash
bash {baseDir}/scripts/check_crashes.sh ["<origin>" "<destination>"]
```

Defaults to **Bansuan, Chonburi → Bang Pakong, Chachoengsao** (home→work).
Override both or either by passing arguments.

## Examples

```bash
# Default home→work
bash {baseDir}/scripts/check_crashes.sh

# Custom route
bash {baseDir}/scripts/check_crashes.sh "Siam BTS, Bangkok" "Don Mueang Airport"
```

## Output

Returns JSON with only accident-related incidents:

```json
{
  "status": "ok",
  "origin": "Bansuan, Chonburi",
  "destination": "Bang Pakong, Chachoengsao",
  "accident_count": 1,
  "accidents": [
    {
      "type": "accident",
      "description": "Accident on Route 3 near Bang Pakong",
      "from": "Bang Pakong",
      "to": "Chon Buri",
      "length_m": 500,
      "delay_s": 300,
      "delay_min": 5.0
    }
  ]
}
```

No accidents → `"accident_count": 0` and empty `accidents` array.

## When to use

- User asks "any crashes on my way to work?"
- User asks "accidents on the commute?"
- User asks "any accidents home?"
- Any crash/accident/injury query about a route

## Requirements

- `TOMTOM_API_KEY` environment variable must be set
- bash, curl, python3

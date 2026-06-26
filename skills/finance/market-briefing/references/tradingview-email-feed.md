# TradingView Email Feed (free tier)

TradingView free accounts cannot use webhooks; alert emails are the reliable emit path.

## gog gmail search patterns

- base query: `from:hello@tradingview.com newer_than:Nd -category:promotions`
- always use `--json -j --account bed.wuttipong@gmail.com`
- inspect thread fields: `subject`, `snippet`, `date`

Prompt style keeps output JSON-safe and parseable.

## State file schema

Path: `data/tv_signals.json`

```json
{
  "updated": "2026-06-03",
  "signals_today": [
    {
      "date": "2026-06-03",
      "time": "2026-06-03 14:05",
      "tickers": ["SMH", "O"]
    }
  ]
}
```

## Filtering rules

Keep a message iff ANY apply:
- subject matches `triggered|alert|signal|scan`

Reject if ANY apply:
- subject matches `black friday|begins now|offer ends|upgrade|promo|sale`

## Ticker extraction

- regex: `\b[A-Z]{1,5}(?:/[A-Z]{1,5})?\b`
- map back to configured watchlist
- ignore markets/prices/generic words by intersection

## Delivery contract

Briefings read this file as truth for "TV Signal Activity".
If `updated != today`, briefing should display `no tv signals synced yet for today`.

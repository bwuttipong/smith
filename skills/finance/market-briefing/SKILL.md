---
name: market-briefing
description: >
  Build and maintain automated market briefing pipelines: pre-market previews,
  end-of-day summaries, watchlist tracking, and alert-feed integration (TradingView
  email, Yahoo Finance, etc.). Use when the user asks for trade briefings, market
  summaries, watchlist updates, signal counts, or wants to schedule recurring
  financial briefings via cron or push them to Discord/Telegram.
---

# Market Briefing

Covers data sourcing, caching, formatting, and scheduling for financial briefings.

## Trigger conditions

- User requests market/stock briefings, watchlist summaries, or index roundups
- User wants to integrate TradingView, Yahoo Finance, or email-based alert feeds
- User asks for pre-market previews or end-of-day trade summaries
- User wants to schedule recurring financial briefings (cron + delivery)

## Standard project layout

Use a dedicated project dir unless the user prefers Hermes skills in-repo.

- `scripts/eod_summary.py` — end-of-day close summary
- `scripts/pre_market_briefing.py` — pre-market preview
- `scripts/sync_tv_alerts.py` — TradingView email → local cache
- `data/tv_signals.json` — local signal cache with `updated` + `signals_today`

WATCHLIST lives in both briefing scripts; keep it single-source if possible.

## Timezone rule (hard)

- Market data (index closes, futures, earnings) → **America/New_York**
- Local date and delivery scheduling → user’s local **Asia/Bangkok**

Never derive “today” for messages from ET when the runner isn’t timezone-aware.

## Feed integration: TradingView free tier

The free plan has no webhooks; use alert emails as the source-of-truth.

See `references/tradingview-email-feed.md` for exact gog gmail queries and
state-file schema, and `templates/sync_tv_alerts.py` for a runnable sync script.

Core pattern:
1. `gog gmail search 'from:hello@tradingview.com newer_than:Nd -category:promotions'`
2. Filter subjects: require `triggered|alert|signal|scan`, reject promos (`black friday|begins now|offer ends|upgrade|promo|sale`)
3. Extract tickers with ASCII uppercase regex; intersect with WATCHLIST
4. Write `data/tv_signals.json` with `updated` date and per-ticker counts
5. Briefing scripts read that file and replace placeholder lines

## Consumer script contract

Briefings should treat missing/empty signal cache gracefully:

- no state file → `no tv signals synced yet for today`
- matched watchlist alerts → per-ticker alert count lines
- cache stale (≠ today) → same as empty; the sync step is responsible for refresh

Keep placeholder wording actionable so delivery still looks intentional when there’s no data.

## Cron / scheduling pattern

Pre-market target: ~30 min before US equities open in ET.
EOD target: ~30 min after US equities close.

Use a lightweight sync-up script before each briefing run when delivery must be live.

## Pitfalls

- **Marketing noise.** TradingView sends promos from the same sender. `-category:promotions` plus subject regex is usually enough; if new promo patterns appear, reject any subject containing both “tradingview” and promo keywords regardless of `CATEGORY_PROMOTIONS` label.
- **Cache freshness.** State is date-keyed on the local TH date, not market date. Cross-midnight cron runs may mismatch ET “today” if the runner doesn’t respect TH/ET split.
- **Yahoo Finance flakiness.** futures and index symbols change names across sources. Stick to `ES=F`, `NQ=F`, `^GSPC`, `^IXIC`, `^FTSE`, `^GDAXI`, `^FCHI`, `000001.SS`, `9988.T` unless the user expands coverage.
- **gog auth drift.** `gog gmail search` will silently return `{}` if the account flag or token is stale. Check `gog auth status` before debugging search patterns.

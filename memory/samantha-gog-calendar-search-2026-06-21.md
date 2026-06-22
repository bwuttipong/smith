# TPN FlexPak 2026 Holiday Calendar — Search Results

**Date:** 2026-06-21
**Searched by:** Samantha 🌸 (subagent for Jeff, via Telegram/Smith)
**gog account used:** `bed.wuttipong@gmail.com`
**gog version:** v0.12.0

---

## TL;DR

✅ **Found it.** Jeff's primary Google Calendar (`bed.wuttipong@gmail.com`) is itself titled
**"TPN FlexPak Holiday 2026"** (description: *"IT's Holidays"*, timezone: Asia/Bangkok).
It contains the full 2026 holiday schedule already — **378 events total** covering every day
of 2026 with bilingual TH/EN labels. The auth scope is `calendar` only, so Drive/Sheets/Docs
searches failed and were skipped.

## Authentication

```
$ gog auth list
bed.wuttipong@gmail.com   default   calendar   2026-06-18T09:17:19Z   oauth
```

Only `calendar` service is authorized. Drive/Sheets/Docs return 403 `insufficientPermissions`.
**Jeff needs to re-run `gog auth add … --services calendar,drive,sheets,docs,contacts,gmail`
if Drive search is required later.**

## Calendar Inventory

| Calendar ID | Summary | Description | Primary | Selected |
|---|---|---|---|---|
| `bed.wuttipong@gmail.com` | **TPN FlexPak Holiday 2026** | IT's Holidays | ✅ | ✅ |

Only one calendar in Jeff's list. No other shared/company calendars visible.

## Commands Run

```bash
gog calendar calendars --json
gog calendar events bed.wuttipong@gmail.com --from 2026-01-01 --to 2026-12-31 \
    --max 2500 --all-pages --json   # → /tmp/tpn-events-full.json
gog drive search "holiday 2026" --max 10   # 403 insufficientPermissions
```

> Note: the task brief said `gog calendar list --json`, but in v0.12.0 the correct subcommand
> is `gog calendar calendars`. `gog calendar list` is an alias for `events` and returns events,
> not the calendar inventory.

## TPN FlexPak 2026 Official Public Holidays

| # | Date | Holiday (TH) | Holiday (EN) | Day of week |
|---|---|---|---|---|
| 1 | 2026-01-01 | วันขึ้นปีใหม่ 🎉 | New Year's Day | Thu |
| 2 | 2026-03-03 | วันมาฆบูชา 🙏 | Makha Bucha Day | Tue |
| 3 | 2026-04-13 | สงกรานต์ 💦 | Songkran Festival | Mon |
| 4 | 2026-04-14 | สงกรานต์ 💦 | (Songkran) | Tue |
| 5 | 2026-04-15 | สงกรานต์ 💦 | (Songkran) | Wed |
| 6 | 2026-05-01 | วันแรงงานแห่งชาติ 🔧 | Labour Day | Fri |
| 7 | 2026-06-03 | วันเฉลิมฯ พระบรมราชินี 👑 | Queen's Birthday | Wed |
| 8 | 2026-07-28 | วันเฉลิมฯ ร.10 👑 | King's Birthday | Tue |
| 9 | 2026-07-29 | อาสาฬหบูชา 🙏 | Asalha Bucha Day | Wed |
| 10 | 2026-08-12 | วันแม่แห่งชาติ 🌸 | Mother's Day | Wed |
| 11 | 2026-10-13 | วันนวมินทรมหาราช 🙏 | Rama IX Memorial Day | Tue |
| 12 | 2026-12-05 | วันพ่อแห่งชาติ 👑 | Father's Day | Sat |
| 13 | 2026-12-31 | วันสิ้นปี 🎆 | New Year's Eve | Thu |

**Plus 2 company annual-leave days** bracketing the New Year break:
- 2026-01-02 (Fri) — "ลาพักร้อน (Day off)" — "Annual Leave (Jan 2-3)"
- 2026-01-03 (Sat) — "ลาพักร้อน (Day off)"

→ **15 paid days off total** (13 official holidays + 2 annual leave).

## Weekends Marked in the Calendar

The calendar also explicitly labels Saturdays and Sundays, so it can be used as a full
working-day vs day-off reference. Saturdays are marked `วันหยุด SAT (Day off)` and Sundays
`วันหยุด (Day off)`. All other weekdays are marked `Work day 💼` (including the working
Sat 2026-08-15 — Jeff's birthday — which is also tagged "Happy birthday!").

## Quick Stats

- **Total events in 2026:** 378 (one entry per calendar day, plus a few extra all-day events
  on holiday days for the EN/TH label pairs)
- **Named holidays:** 13 distinct public holidays
- **Annual leave days:** 2 (Jan 2–3)
- **Timezone:** Asia/Bangkok
- **Owner:** `bed.wuttipong@gmail.com`

## Data Files

- Raw JSON dump (all 378 events): `/tmp/tpn-events-full.json`
- First-page preview: `/tmp/tpn-events.json`

## Recommendation for Jeff

The calendar data is already in `bed.wuttipong@gmail.com` — no Drive/Sheet doc to hunt for.
If he wants a portable copy, options are:
1. Subscribe to it from any Google account via the calendar's sharing settings.
2. Export as `.ics` from Google Calendar UI (Settings → Import & export).
3. Convert `/tmp/tpn-events-full.json` to a Markdown table or CSV with a small script.

If the goal is a long-term reference doc, say the word and I'll turn the 13 holidays
+ 2 leave days into a clean `memory/tpn-flexpak-2026-holidays.md` or paste it back here.

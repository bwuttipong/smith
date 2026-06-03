#!/usr/bin/env python3
from datetime import date, datetime, timezone
import math

import yfinance as yf
from zoneinfo import ZoneInfo

WATCHLIST = ["O", "SMH", "JEPQ"]


def close_of(sym):
    t = yf.Ticker(sym)
    hist = t.history(period="5d")
    if hist is None or hist.empty:
        return {"price": None, "prev": None, "pct": None}
    close = float(hist["Close"].iloc[-1])
    prev = float(hist["Close"].iloc[-2]) if len(hist) > 1 else None
    pct = ((close / prev) - 1) * 100 if prev and prev > 0 else None
    return {"price": close, "prev": prev, "pct": pct}


def fmt_money(v):
    if v is None:
        return "n/a"
    return f"${v:,.2f}"


def fmt_chg(pct, signed=True):
    if pct is None:
        return "0.00%"
    sign = "+" if pct >= 0 else ""
    if not signed:
        sign = ""
    return f"{sign}{pct:.2f}%"


def index_perf(sym, label):
    r = close_of(sym)
    if r["price"] is None:
        return f"- {label}: no close data"
    return f"- {label}: {fmt_money(r['price'])} ({fmt_chg(r['pct'])})"


def build_eod(date_val=None):
    date_val = date_val or date.today()
    lines = [f"📊 Market Close Summary — {date_val:%B %d, %Y}"]

    lines.append("\n📈 Index Performance:")
    lines.append(index_perf("^GSPC", "S&P 500"))
    lines.append(index_perf("^IXIC", "NASDAQ"))

    rows = []
    for t in WATCHLIST:
        r = close_of(t)
        rows.append((t, r))
    rows_sorted = sorted(rows, key=lambda x: (x[1]["pct"] if isinstance(x[1]["pct"], (int,float)) else -999))
    best = rows_sorted[-1]
    worst = rows_sorted[0]

    def mov(ticker, r):
        if r["price"] is None:
            return f"- {ticker}: no close data"
        return f"- {ticker}: {fmt_money(r['price'])} ({fmt_chg(r['pct'])})"

    lines.append("\n🏆 Top Movers (Watchlist):")
    lines.append(mov(best[0], best[1]))
    lines.append(mov(worst[0], worst[1]))

    lines.append("\n📋 Signal Activity:")
    lines.append("- Signals generated today: 0 (placeholder — wire TradingView/webhook source)")
    lines.append("- Signals acted upon: 0")

    lines.append("\n📅 Tomorrow's Calendar:")
    lines.append("- Earnings / macro: placeholder — connect econcal or similar feed")

    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    print(build_eod())

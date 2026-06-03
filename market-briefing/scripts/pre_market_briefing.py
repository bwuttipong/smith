#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import date, datetime
from zoneinfo import ZoneInfo

import yfinance as yf

WATCHLIST = ["O", "SMH", "JEPQ"]
TH_TZ = ZoneInfo("Asia/Bangkok")
ET_TZ = ZoneInfo("America/New_York")
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "tv_signals.json"


def fmt_chg(pct, signed=True):
    if pct is None:
        return "0.00%"
    sign = "+" if pct >= 0 else ""
    if not signed:
        sign = ""
    return f"{sign}{pct:.2f}%"


def quote(ticker):
    try:
        obj = yf.Ticker(ticker)
        fi = obj.fast_info
        price = getattr(fi, "last_price", None)
        prev = getattr(fi, "previous_close", None)
        pct = None if (price is None or prev is None or prev == 0) else (price / prev - 1) * 100
        return {"ticker": ticker, "price": price, "prev": prev, "pct": pct}
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def yahoo_summary(symbols):
    syms = " ".join(symbols)
    try:
        tickers = yf.Tickers(syms)
    except Exception:
        return {}
    out = {}
    for sym in symbols:
        try:
            td = getattr(tickers.tickers, sym, None)
            fi = getattr(td, "fast_info", None) or {}
            hist = td.history(period="2d") if td is not None else None
            price = getattr(fi, "last_price", None) or (
                float(hist["Close"].iloc[-1]) if hist is not None and not hist.empty else None
            )
            prev = getattr(fi, "previous_close", None) or (
                float(hist["Close"].iloc[-2]) if hist is not None and len(hist) > 1 else None
            )
            pct = None if (price is None or prev is None or prev == 0) else (price / prev - 1) * 100
            out[sym] = {"price": price, "pct": pct}
        except Exception as e:
            out[sym] = {"error": str(e)}
    return out


def global_markets():
    today_et = datetime.now(ET_TZ).date()
    futures = yahoo_summary(["ES=F", "NQ=F"]) if True else (lambda: {})()

    def fmt(sym, default_display):
        x = futures.get(sym, {})
        if "error" in x:
            return f"{default_display} — unavailable"
        price = x.get("price")
        pct = x.get("pct")
        price_s = f"{price:,.2f}" if isinstance(price, (int, float)) else str(price)
        pct_s = fmt_chg(pct) if isinstance(pct, (int, float)) else "n/a"
        return f"{sym.replace('=F','')}: {price_s} ({pct_s})"

    sp = fmt("ES=F", "S&P 500 futures")
    nq = fmt("NQ=F", "NASDAQ futures")

    eu = yahoo_summary(["^FTSE", "^GDAXI", "^FCHI"])
    as_ = yahoo_summary(["000001.SS", "9988.T"])

    eu_lines = []
    for sym, label in [("^FTSE", "FTSE"), ("^GDAXI", "DAX"), ("^GCHI", "CAC")]:
        sym = "^FCHI" if sym == "^GCHI" else sym
        x = eu.get(sym, {})
        if "error" in x:
            eu_lines.append(f"{label}: unavailable")
            continue
        if x.get("price") is None:
            eu_lines.append(f"{label}: not open / no data")
        else:
            eu_lines.append(f"{label}: {x['price']:,.2f} ({fmt_chg(x.get('pct'))})")

    as_lines = []
    for sym, label in [("000001.SS", "Shanghai"), ("9988.T", "Nikkei proxy unavailable — using Alibaba ADR")]:
        x = as_.get(sym, {})
        if "error" in x:
            as_lines.append(f"{label}: unavailable")
            continue
        if x.get("price") is None:
            as_lines.append(f"{label}: closed / no data")
        else:
            as_lines.append(f"{label}: {x['price']:,.2f} ({fmt_chg(x.get('pct'))})")

    eu_summary = "; ".join(eu_lines)
    as_summary = "; ".join(as_lines)
    return sp, nq, eu_summary, as_summary


def watchlist_updates():
    blocks = []
    for t in WATCHLIST:
        r = quote(t)
        if "error" in r:
            blocks.append(f"- {t}: data unavailable ({r['error']})")
            continue
        price = r["price"]
        pct = r["pct"]
        blocks.append(f"- {t}: {('$'+f'{price:.2f}') if isinstance(price, (int,float)) else str(price)} overnight ({fmt_chg(pct)})")
    return "\n".join(blocks)


def risk_alerts():
    v = yf.Ticker("^VIX")
    fi = v.fast_info
    vix = getattr(fi, "last_price", None)
    vix_prev = getattr(fi, "previous_close", None)
    vix_gap = 0 if (vix is None or vix_prev is None or vix_prev == 0) else (vix / vix_prev - 1) * 100
    alert = "elevated volatility expected" if isinstance(vix, (int, float)) and vix >= 20 else "quiet-ish"
    return f"- VIX: {vix:.2f} ({fmt_chg(vix_gap)}) — {alert}"


def load_signals(target_date=None):
    target_date = target_date or datetime.now(TH_TZ).date()
    if not DATA_PATH.exists():
        return {"tickers": {}, "total": 0}
    try:
        state = json.loads(DATA_PATH.read_text())
    except Exception:
        return {"tickers": {}, "total": 0}
    signals = state.get("signals_today", [])
    hits = [s for s in signals if s.get("date") == str(target_date)]
    tickers = {t: 0 for t in WATCHLIST}
    total = 0
    for h in hits:
        for t in h.get("tickers", []):
            if t in tickers:
                tickers[t] += 1
                total += 1
    return {"tickers": tickers, "total": total}


def build_morning_brief(target_date=None):
    target_date = target_date or datetime.now(TH_TZ).date()
    sp, nq, eu, as_ = global_markets()
    watch = watchlist_updates()
    risk = risk_alerts()
    signals = load_signals(target_date)
    sig_lines = []
    if signals["total"] == 0:
        sig_lines.append("- no tv signals synced yet for today")
    else:
        for t in WATCHLIST:
            n = signals["tickers"].get(t, 0)
            if n:
                sig_lines.append(f"- {t}: {n} alert(s)")
    if not sig_lines:
        sig_lines.append("- no matching watchlist alerts for today")
    text = f"""📊 Pre-Market Briefing — {target_date:%B %d, %Y}

🌍 Global Markets:
- S&P 500 Futures: {sp}
- NASDAQ Futures: {nq}
- European Markets: {eu}
- Asian Markets: {as_}

📰 Key Events Today:
- US earnings on deck: check finviz/econcal for today's releases
- Economic data: see economic calendar for scheduled macro prints
- Fed/central banks: no auto feed — confirm via calendar source

📈 Watchlist Updates:
{watch}

📊 TV Signal Activity:
""" + "\n".join(sig_lines) + f"""

⚠️ Risk Alerts:
{risk}
""".rstrip() + "\n"
    return text


if __name__ == "__main__":
    print(build_morning_brief())

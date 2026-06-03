#!/usr/bin/env python3
"""Update TradingView email synced signal counts inside pre_market_briefing.py in place."""

import json
import re
from pathlib import Path

SCRIPT = Path("/Users/Jeff/Smith/market-briefing/scripts/pre_market_briefing.py")
STATE = Path("/Users/Jeff/Smith/market-briefing/data/tv_signals.json")


def load_signals(target_date):
    if not STATE.exists():
        return {"tickers": {}, "total": 0}
    try:
        data = json.loads(STATE.read_text())
    except Exception:
        return {"tickers": {}, "total": 0}
    signals = data.get("signals_today", [])
    hits = [s for s in signals if s.get("date") == str(target_date)]
    tickers = {}
    total = 0
    for h in hits:
        for t in h.get("tickers", []):
            tickers[t] = tickers.get(t, 0) + 1
            total += 1
    return {"tickers": tickers, "total": total}


def patch_signal_block(block_text: str, target_date) -> str:
    signals = load_signals(target_date)
    if signals["total"] == 0:
        return "- no tv signals synced yet for today"
    lines = []
    for t, n in signals["tickers"].items():
        if n:
            lines.append(f"- {t}: {n} alert(s)")
    return "\n".join(lines) if lines else "- no matching watchlist alerts for today"


def main():
    text = SCRIPT.read_text()
    marker = '        text = f"""\\n📋 Signal Activity:\\n'
    m = re.search(r'text = f"""\n📋 Signal Activity:\n(.*?)""".rstrip\(\) \+ "\\n"', text, re.S)
    if not m:
        raise SystemExit("signal block marker not found")
    block = m.group(1)
    lines = [x for x in block.splitlines() if x.startswith("-")]
    dates = re.findall(r"target_date or datetime\.now\(TH_TZ\)\.date\(\)", text)
    target_date_placeholder = "datetime.now(TH_TZ).date()"
    from datetime import date, datetime
    from zoneinfo import ZoneInfo
    TH_TZ = ZoneInfo("Asia/Bangkok")
    target_date = datetime.now(TH_TZ).date()
    repl = patch_signal_block(block, target_date)
    old = '    text = f"""\\n📈 Watchlist Updates:\\n{watch}\\n\\n📋 Signal Activity:\\n' + block + '\\n"""' if "Watchlist Updates" in block else None
    if "Watchlist Updates" not in block:
        raise SystemExit("watchlist anchor not found")
    old_block_start = '📈 Watchlist Updates:\n{watch}\n\n📋 Signal Activity:\n'
    old_full = old_block_start + block + "\n"
    new_full = old_block_start + repl + "\n"
    if old_full not in text:
        old_full = old_full.replace('"""', '"""')  # noop space holder for exact match
    new_text = text.replace(old_full, new_full)
    if new_text == text:
        raise SystemExit("no replacement made")
    SCRIPT.write_text(new_text)
    print(SCRIPT)
    print("patched:", repl.replace("\n", " | "))


if __name__ == "__main__":
    main()

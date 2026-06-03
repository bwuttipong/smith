#!/usr/bin/env python3
"""Sync TradingView alert emails from Gmail into a small local signal cache.

Output: /Users/Jeff/Smith/market-briefing/data/tv_signals.json
Shape: {"updated":"2026-06-03","signals_today":[...]}
"""

import json
import os
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

ACCOUNT = os.getenv("GOG_ACCOUNT", "bed.wuttipong@gmail.com")
MAX_DAYS = int(os.getenv("TV_SIGNALS_DAYS_BACK", "7"))
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_PATH = DATA_DIR / "tv_signals.json"

WATCHLIST = ["O", "SMH", "JEPQ"]

TICKER_RE = re.compile(r"\b[A-Z]{1,5}(?:/[A-Z]{1,5})?\b", re.ASCII)
MARKETING_RE = re.compile(r"black friday|begins now|offer ends|upgrade|promo|sale", re.IGNORECASE)


def run_gog_search(query: str):
    cmd = [
        "gog",
        "gmail",
        "search",
        query,
        "--json",
        "-j",
        "--account", ACCOUNT,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=False
        )
    except FileNotFoundError:
        return {"threads": []}
    if not result.stdout.strip():
        return {"threads": []}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"threads": []}


def looks_like_tv_alert(subject: str) -> bool:
    subj = subject or ""
    if MARKETING_RE.search(subj):
        return False
    return any(k in subj.lower() for k in ["triggered", "alert", "signal", "scan"])


def extract_date_from_thread(thread: dict):
    return thread.get("date") or thread.get("updated")


def load_state():
    if DATA_PATH.exists():
        try:
            return json.loads(DATA_PATH.read_text())
        except Exception:
            return {}
    return {}


def save_state(state):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(state, indent=2))


def main():
    today = datetime.now().date()
    state = load_state()

    try:
        updated = datetime.strptime(state.get("updated", ""), "%Y-%m-%d").date()
    except Exception:
        updated = today - timedelta(days=60)

    if updated >= today:
        print(json.dumps({
            "updated": state.get("updated"),
            "signals_today": state.get("signals_today", []),
            "note": "already synced today"
        }, indent=2))
        return

    days_back = min((today - updated).days + 1, MAX_DAYS)
    data = run_gog_search(
        f"from:hello@tradingview.com newer_than:{days_back}d -category:promotions"
    )

    threads = data.get("threads", [])
    signals_today = []
    by_date = {}

    for thread in threads:
        date_str = extract_date_from_thread(thread)
        if not date_str:
            continue
        try:
            d = datetime.strptime(date_str[:10], "%Y-%m-%d").date()
        except Exception:
            continue
        subject = thread.get("subject", "")
        snippets = [thread.get("snippet", "")]
        if looks_like_tv_alert(subject):
            snippets.append(subject)
        text = "\n".join(snippets)
        tickers = sorted(set(
            t.replace(".", "") for t in TICKER_RE.findall(text) if t in WATCHLIST
        ))
        if not tickers:
            continue
        by_date.setdefault(str(d), []).append({"time": date_str, "tickers": tickers})

    for d_str in sorted(by_date):
        for item in by_date[d_str]:
            signals_today.append({"date": d_str, "time": item["time"], "tickers": item["tickers"]})

    state.update({
        "updated": str(today),
        "signals_today": signals_today[-50:],
    })
    save_state(state)

    print(json.dumps(state, indent=2))


if __name__ == "__main__":
    main()

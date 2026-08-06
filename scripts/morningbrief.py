#!/usr/bin/env python3
"""Lean on-demand morning brief for Jeff.

Designed for Hermes quick command /morningbrief. No scheduling here.
Keeps output short enough for LINE and avoids printing secrets.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import random
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

TZ = dt.timezone(dt.timedelta(hours=7), name="BKK")
NOW = dt.datetime.now(TZ)
TODAY = NOW.date()
EMAIL = "bed.wuttipong@gmail.com"
NAME = "Jeff"

IDIOMS = [
    ("call it a day", "stop working for today", "Let's call it a day and finish this tomorrow."),
    ("on the same page", "understand or agree about the same thing", "Before we start, let's make sure we're on the same page."),
    ("figure it out", "find the answer or solution", "Give me a minute — I'll figure it out."),
    ("hang in there", "keep going during something difficult", "Hang in there. We're almost done."),
    ("take it easy", "relax or don't work too hard", "Take it easy tonight."),
    ("cut to the chase", "get to the main point", "Let's cut to the chase — what's broken?"),
    ("in a nutshell", "said briefly", "In a nutshell, the report needs cleanup."),
]

def run(cmd: list[str], timeout: int = 8) -> str:
    try:
        p = subprocess.run(cmd, text=True, capture_output=True, timeout=timeout)
        return (p.stdout or p.stderr or "").strip()
    except Exception:
        return ""

def clean_task(s: str) -> str:
    s = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", s)
    s = s.replace("**", "").replace("_", "")
    return re.sub(r"\s+", " ", s).strip()

def todoist_label_map() -> dict[str, str]:
    raw = run(["todoist", "labels", "--json"], timeout=8)
    try:
        labels = json.loads(raw)
        return {str(x.get("id")): x.get("name", "") for x in labels}
    except Exception:
        return {}


def todoist_top() -> list[str]:
    raw = run(["todoist", "tasks", "--json"], timeout=10)
    try:
        tasks = json.loads(raw)
    except Exception:
        return []
    labels = todoist_label_map()

    def task_labels(t: dict) -> set[str]:
        return {labels.get(str(x), str(x)) for x in t.get("labels", [])}

    def due_rank(t: dict) -> int:
        d = (t.get("due") or {}).get("date")
        if not d:
            return 3
        try:
            day = dt.date.fromisoformat(d[:10])
        except Exception:
            return 3
        if day == TODAY:
            return 0
        if day < TODAY:
            return 1
        return 2

    # Filter uncompleted top-level tasks
    top = [
        t for t in tasks
        if not t.get("parentId")
        and "done" not in task_labels(t)
        and not clean_task(t.get("content", "")).lower().startswith(("perform a workday", "todoist integrations", "explore todoist"))
    ]
    top.sort(key=lambda t: (due_rank(t), -int(t.get("priority", 1)), t.get("childOrder", 999)))
    out = []
    for t in top:
        name = clean_task(t.get("content", ""))
        if not name:
            continue
        due = t.get("due") or {}
        d_str = due.get("date", "")[:10]
        if d_str == str(TODAY):
            due_text = due.get("string") or ""
            tag = f" — Today ({due_text})" if due_text else " — Today"
            out.append(f"{name}{tag}")
        elif due.get("string"):
            tag = f" — {due['string']}"
            out.append(f"{name}{tag}")
        if len(out) == 5:
            break
    return out

def calendar_items() -> tuple[list[str], list[str]]:
    # khal output is human-readable but stable enough for a short brief.
    out = run(["khal", "list", "today", "tomorrow"], timeout=8)
    events, birthdays = [], []
    for line in out.splitlines():
        line = line.strip()
        if not line or line.lower().startswith(("today", "tomorrow")):
            continue
        compact = re.sub(r"\s+", " ", line)
        if "birthday" in compact.lower() or "วันเกิด" in compact:
            birthdays.append(compact)
        else:
            events.append(compact)
    return events[:3], birthdays[:3]

def fyi_trends() -> list[str]:
    # Fast, best-effort. If OpenCLI/browser bridge is unavailable, stay quiet.
    query = "AI OR startup OR tech min_faves:100"
    raw = run(["opencli", "twitter", "search", query, "-f", "json"], timeout=8)
    trends = []
    try:
        data = json.loads(raw)
        # tolerate list or object-ish output
        items = data if isinstance(data, list) else data.get("results") or data.get("tweets") or []
        for x in items[:8]:
            text = x.get("text") or x.get("content") or x.get("full_text") or ""
            text = re.sub(r"https?://\S+", "", text)
            text = re.sub(r"\s+", " ", text).strip()
            if len(text) > 110:
                text = text[:107].rstrip() + "…"
            if text:
                trends.append(text)
            if len(trends) == 2:
                break
    except Exception:
        pass
    if not trends:
        trends = ["AI/tooling: watch model, automation, and workflow updates today."]
    return trends

def weather() -> str:
    url = "https://wttr.in/Thailand?format=" + urllib.parse.quote("%c %t, rain %p")
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.read().decode().strip()
    except Exception:
        return "Weather unavailable"

def main() -> None:
    top = todoist_top()
    events, birthdays = calendar_items()
    trends = fyi_trends()
    idiom, meaning, example = IDIOMS[NOW.timetuple().tm_yday % len(IDIOMS)]

    lines = []
    lines.append("🌅 See Your Day Ahead")
    lines.append(f"Morning, {NAME}. Here's your game plan for the day.")
    lines.append("")
    lines.append("🎯 Top of mind")
    if top:
        lines += [f"- {x}" for x in top[:5]]
    else:
        lines.append("- No urgent Todoist items found.")
    lines.append("")
    lines.append("💡 FYI")
    lines.append(f"- Weather: {weather()}")
    for x in trends[:2]:
        lines.append(f"- {x}")
    for x in birthdays[:2]:
        lines.append(f"- Birthday: {x}")
    lines.append("")
    lines.append("📅 On your calendar")
    if events:
        lines += [f"- {x}" for x in events[:3]]
    else:
        lines.append("- No calendar items found.")
    lines.append("")
    lines.append("🗣️ English idiom")
    lines.append(f"- {idiom}: {meaning}. Example: {example}")
    lines.append("")
    lines.append("Have a wonderful day.")

    print("\n".join(lines))

if __name__ == "__main__":
    main()

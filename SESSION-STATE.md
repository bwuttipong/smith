# SESSION-STATE.md — Active Working Memory (WAL Target)

> **Law:** Chat history is a BUFFER, not storage. This file is your "RAM" — the ONLY place specific details are safe.
> **Rule:** If it's important enough to remember, write it down NOW — not later.

---

## Current Task

- initialized git repository, refactored contexts to load config path via environment variable, set up env variable, and created VS Code launch/build configurations.

---

## Active Context

| Field | Value |
|-------|-------|
| **Project** | OutsourceEF9 |
| **Channel** | IDE (direct) |
| **Last Updated** | 2026-06-17 |

---

## Decisions Log

| Decision | When | Details |
|----------|------|---------|
| initialized git repo and cleaned obj folders | 2026-06-17 | staged files and ignored build directories |

---

## Corrections Log

| Correction | When | Details |
|------------|------|---------|
| | | |

---

## Preferences

| Category | Preference |
|----------|------------|
| Tone | lowercase, witty, British gentleman |
| Emoji | yes, tastefully |
| Language | English |
| External actions | always get approval first |
| Slack canvases | grant access automatically and share silently without verbose explanations |

---

## Key Details (Proper Nouns, Numbers, URLs)

| Detail | Value |
|--------|-------|
| Config File Path | `\\192.168.10.2\ShareCenter\Program\Outsource\config.json` |

---

## WAL Triggers (scan every message for these)

- ✏️ Corrections — "It's X, not Y" / "Actually..." / "No, I meant..."
- 📍 Proper nouns — Names, places, companies, products
- 🎨 Preferences — "I like/don't like"
- 📋 Decisions — "Let's do X" / "Go with Y" / "Use Z"
- 📝 Draft changes — Edits to something being worked on
- 🔢 Specific values — Numbers, dates, IDs, URLs

**If ANY of these appear: STOP → WRITE to this file → THEN respond**

---

## Danger Zone Protocol

- **Threshold:** 60% context (check via `session_status`)
- **When triggered:** Start logging to `memory/working-buffer.md`
- **Every message after 60%:** Append both human message + agent summary
- **After compaction:** Read buffer FIRST, extract context into this file

---

*Last write: 2026-06-17*
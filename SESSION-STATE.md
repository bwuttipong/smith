# SESSION-STATE.md — Active Working Memory (WAL Target)

> **Law:** Chat history is a BUFFER, not storage. This file is your "RAM" — the ONLY place specific details are safe.
> **Rule:** If it's important enough to remember, write it down NOW — not later.

---

## Current Task

- Resolved a major ClickOnce deployment bug in the CirculatingBox project.
- Fixed the silent startup crash where the runtime couldn't locate ConfigurationManager.dll and deps.json due to MSBuild subfolder assembly separation.
- Enforced <PublishSingleFile>True</PublishSingleFile> and <IncludeNativeLibrariesForSelfExtract>True</IncludeNativeLibrariesForSelfExtract> to fix missing WebView2Loader.dll.
- Bumped versions up to 3.1.0.31 and successfully deployed to the local network share (\\192.168.95.200\TPKShare\IT\Box\).
- Committed all changes to the local Git repository for the CirculatingBox project.

---

## Active Context

| Field | Value |
|-------|-------|
| **Project** | CirculatingBox |
| **Channel** | IDE (direct) |
| **Last Updated** | 2026-06-26 |

---

## Decisions Log

| Decision | When | Details |
|----------|------|---------|
| Enable SingleFile and IncludeNativeLibs | 2026-06-26 | Bypasses ClickOnce folder separation bug and fixes WebView2Loader missing native dll crash. |
| Commit to local Git | 2026-06-26 | No remote configured, so changes are securely versioned locally. |

---

## WAL Triggers (scan every message for these)

- ?? Corrections — "It's X, not Y" / "Actually..." / "No, I meant..."
- ?? Proper nouns — Names, places, companies, products
- ?? Preferences — "I like/don't like"
- ?? Decisions — "Let's do X" / "Go with Y" / "Use Z"
- ?? Draft changes — Edits to something being worked on
- ?? Specific values — Numbers, dates, IDs, URLs

**If ANY of these appear: STOP  WRITE to this file  THEN respond**

---

*Last write: 2026-06-26*

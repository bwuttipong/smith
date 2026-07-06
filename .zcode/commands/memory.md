---
description: Append an entry to today's daily memory file
argument-hint: <entry>
---

Append the following to `~/Smith/memory/YYYY-MM-DD.md` (today's date, Asia/Bangkok), under a `## Claude Code — HH:MM ICT` heading:

> $ARGUMENTS

Rules:
- Create the file (with `# YYYY-MM-DD` header) and the `memory/` directory if missing.
- Always append, never rewrite.
- If a Stop hook has stamped a `_session ended_` marker for the current minute or later, start a fresh section after it.

Confirm with one line: "logged." — nothing more.

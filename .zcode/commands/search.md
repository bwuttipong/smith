---
description: Search shared memory bridge (memory + wiki, FTS5)
argument-hint: <query> [limit]
---

Full-text search across the indexed memory bridge (`~/Smith/memory/` + `~/Smith/wiki/`).

Query: `$1`
Limit: `$2` (default 10)

Use `qmd query "$1"` first (handles FTS5 + multiple docs). Fall back to `grep -ri` over `~/Smith/memory/` and `~/Smith/wiki/` if the bridge is offline.

Return only the matching snippets with file paths — not full files. Address the user as "sir".

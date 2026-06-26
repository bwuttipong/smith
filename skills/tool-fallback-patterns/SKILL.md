---
name: tool-fallback-patterns
description: "Reliable fallback chains for information lookup and tool usage when primary paths fail. Use when web fetching, searching, or accessing skills hits blocks/disambiguation."
---

# Tool Fallback Patterns

## Information Lookup Fallback Chain
When searching for factual information or troubleshooting:

1. **Prefer dedicated skills first** — if a skill exists (e.g., `web-search`, `blogwatcher`, `arxiv`), use it directly.
2. **Avoid browser navigation for plain text endpoints** — URLs ending in `.md`, `.txt`, `.json`, `.yaml`, `.yml`, `.csv`, `.xml`, `raw.githubusercontent.com`, or documented API endpoints should use `curl` via terminal or `web_extract` instead; browser is overkill.
3. **When shell search fails** (empty results, blocked services, parsing issues), stop and switch tool class — don’t repeat similar commands expecting different output.
4. **If still blocked**, ask the user for clarification rather than blind retrying.

## Skill Loading / Disambiguation
- `skill_view` requires the full relative path for ambiguous names.
- If two skills share a base name (e.g., `brave-search`), load via `category/skill-name`.
- If ambiguity persists after explicit path attempt, prefer skipping the skill and using a general fallback (terminal/web) instead of cycling.
- Alternative: use `skills_list` to enumerate available skills and resolve the right one.

## Memory Tool Exact-Match Behavior
- `memory replace` depends on exact old_text matching.
- Match on a small unique substring when the full entry is uncertain.
- If the first `replace` fails, reduce the matching fragment before retrying.

## Google Search Caveats
- Google HTML/search endpoints may trigger bot detection/redirect to CAPTCHA.
- Prefer Brave Search API, DuckDuckGo HTML (`html.duckduckgo.com/html/`), or direct site URLs over bare `curl` against Google.

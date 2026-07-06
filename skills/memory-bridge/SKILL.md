---
name: memory-bridge
description: "Bridge context across sessions — recall past work, connect dots, maintain continuity. Use when the user references something from a prior conversation, asks 'what did we do about X', or needs cross-session context."
version: 1.0.0
author: Smith
metadata:
  hermes:
    tags: [memory, continuity, session-search, recall]
---

# Memory Bridge

Keep context alive across sessions. No more "I don't remember" — you have the tools, use them.

## When to Load

- User references something from a past conversation
- User asks "what did we do about X" or "where did we leave Y"
- You suspect relevant cross-session context exists
- User says "remember when..." or "last time we..."

## Recall Strategy

### 1. Start with QMD (fastest, most comprehensive)

```bash
# Search the wiki — 400+ bridged session docs
mcp_qmd_query(searches=[{"type": "lex", "query": "topic keywords"}, {"type": "vec", "query": "natural language question about the topic"}])
```

QMD has session transcripts, reports, entity pages. It's the first place to look.

### 2. Fall back to session_search (raw transcripts)

```
session_search(query="topic keywords", limit=3, sort="newest")
```

FTS5-backed, searches the SQLite session store. Good for finding exact conversations.

### 3. Check daily memory files

```
read_file(path="~/Smith/memory/YYYY-MM-DD.md")
```

Raw logs from past days. Check recent dates when user references "yesterday" or "last week".

### 4. Check MEMORY.md (curated long-term)

```
read_file(path="~/Smith/memories/MEMORY.md")
```

Only in main sessions (never in group chats). Contains distilled insights, not raw logs.

## The Bridge Pattern

When you find relevant context from a past session:

1. **Don't dump the raw transcript** — summarize what's relevant
2. **Connect it to now** — "Last time you were working on X, you decided Y. Want to pick up from there?"
3. **Offer next steps** — don't just recall, propose what to do with the memory

## Anti-Patterns

- ❌ Loading full MEMORY.md on every session start
- ❌ Asking the user to repeat themselves before checking
- ❌ Dumping 200 lines of old transcript as context
- ❌ "I don't have memory of that" without searching first

## Verification

After bridging context, confirm accuracy:
- "I found a session from [date] where you [summary]. Is that the one?"
- Better to confirm than confidently recall wrong details

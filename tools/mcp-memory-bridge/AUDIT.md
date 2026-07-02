# OpenClaw × Hermes Interop Audit

Run each test on BOTH agents. Compare results. Pass = identical or consistent behavior.

---

## Test 1: MCP Memory Bridge Connectivity

### On OpenClaw (Smith)
```
Use memory_bridge_stats and report the results.
```

### On Hermes
```
Use memory_bridge_stats and report the results.
```

### Expected
- Both return: indexed_files, structured_entries, total_size_bytes
- Numbers must match exactly
- Both show watch_paths: ~/Smith/memory, ~/Smith/wiki

---

## Test 2: Shared Search — Known Content

### On OpenClaw (Smith)
```
Search memory_bridge_search for "Returnable Box" and show the top 3 results.
```

### On Hermes
```
Search memory_bridge_search for "Returnable Box" and show the top 3 results.
```

### Expected
- Same file paths returned
- Same snippets
- Same ranking order

---

## Test 3: Cross-Write Test (Agent A writes, Agent B reads)

### On OpenClaw (Smith)
```
Write a memory entry using memory_bridge_write:
- title: "Audit Test Entry from Smith"
- content: "This entry was written by Smith at [current timestamp]. If Hermes can read this, interop works."
- tags: ["audit", "interop-test"]
- source_agent: "openclaw"
Report the returned entry ID.
```

### On Hermes
```
Search memory_bridge_search for "Audit Test Entry from Smith".
Then read it with memory_bridge_get using the entry ID from the search.
Confirm the content matches what Smith wrote.
```

### Expected
- Hermes finds the entry Smith wrote
- Content is identical
- source_agent shows "openclaw"
- Tags show ["audit", "interop-test"]

---

## Test 4: Cross-Write Test (Agent B writes, Agent A reads)

### On Hermes
```
Write a memory entry using memory_bridge_write:
- title: "Audit Test Entry from Hermes"
- content: "This entry was written by Hermes at [current timestamp]. If Smith can read this, interop works."
- tags: ["audit", "interop-test"]
- source_agent: "hermes"
Report the returned entry ID.
```

### On OpenClaw (Smith)
```
Search memory_bridge_search for "Audit Test Entry from Hermes".
Then read it with memory_bridge_get using the entry ID.
Confirm the content matches what Hermes wrote.
```

### Expected
- Smith finds the entry Hermes wrote
- Content is identical
- source_agent shows "hermes"

---

## Test 5: Filesystem Read — Shared Files

### On OpenClaw (Smith)
```
Read the file ~/Smith/AGENTS.md using memory_bridge_read.
Report the first 5 lines.
```

### On Hermes
```
Read the file ~/Smith/AGENTS.md using memory_bridge_read.
Report the first 5 lines.
```

### Expected
- Both read the same file
- First 5 lines are identical
- Neither agent has a different version

---

## Test 6: Filesystem Read — Memory Files

### On OpenClaw (Smith)
```
Read ~/Smith/memory/2026-07-02.md using memory_bridge_read.
Report the first 10 lines.
```

### On Hermes
```
Read ~/Smith/memory/2026-07-02.md using memory_bridge_read.
Report the first 10 lines.
```

### Expected
- Same content from both agents

---

## Test 7: Scan Consistency

### On OpenClaw (Smith)
```
Run memory_bridge_scan. Report indexed, updated, skipped, total_files.
```

### On Hermes
```
Run memory_bridge_scan. Report indexed, updated, skipped, total_files.
```

### Expected
- total_files must match
- Both agents see the same filesystem state

---

## Test 8: No Cross-Contamination — Sessions

### On OpenClaw (Smith)
```
What is your current session key? What model are you running?
```

### On Hermes
```
What is your current session key? What model are you running?
```

### Expected
- Different session keys (each agent has its own)
- Same or different models (depends on config) — but neither should see the other's session
- Neither agent should have access to the other's conversation history

---

## Test 9: No Cross-Contamination — State

### On OpenClaw (Smith)
```
List your available tools (just the names).
```

### On Hermes
```
List your available tools (just the names).
```

### Expected
- Each agent has its own tool set
- OpenClaw tools include: read, write, edit, exec, workboard_*, memory_search, etc.
- Hermes tools include: terminal, file, code_execution, memory_bridge_*, etc.
- memory_bridge_* tools appear in BOTH lists (shared MCP)
- Neither agent has the other's proprietary tools

---

## Test 10: Profile Isolation

### On OpenClaw (Smith)
```
What is your agent identity? What profile are you using?
```

### On Hermes
```
What is your agent identity? What profile are you using?
```

### Expected
- Smith identifies as Smith (OpenClaw agent)
- Hermes identifies as Hermes Agent (smith profile)
- Neither confuses itself with the other
- Both read the same SOUL.md? (Check if Hermes loads ~/Smith/SOUL.md or its own ~/.hermes/SOUL.md)

---

## Summary Checklist

| # | Test | Smith | Hermes | Match? |
|---|------|-------|--------|--------|
| 1 | MCP Stats | | | □ |
| 2 | Shared Search | | | □ |
| 3 | Smith→Hermes Write | | | □ |
| 4 | Hermes→Smith Write | | | □ |
| 5 | AGENTS.md Read | | | □ |
| 6 | Memory File Read | | | □ |
| 7 | Scan Consistency | | | □ |
| 8 | Session Isolation | | | □ |
| 9 | Tool Isolation | | | □ |
| 10 | Profile Isolation | | | □ |

**10/10 pass = fully compatible.**
**< 10 = note which failed and why.**

# OpenClaw × Hermes Interop Audit — Smith Side
## Run Date: 2026-07-02 09:14 GMT+7

---

## Test 1: MCP Memory Bridge Stats ✅
```
indexed_files: 553
structured_entries: 1
total_size_bytes: 2,212,887
watch_paths: ["/Users/Jeff/Smith/memory", "/Users/Jeff/Smith/wiki"]
db_path: "/Users/Jeff/Smith/tools/mcp-memory-bridge/memory.db"
```
**Expected match:** Hermes memory_bridge_stats should return identical numbers.

---

## Test 2: Shared Search — "Returnable Box" ✅
```
1. wiki/sources/bridge-smith-ec7a1e9e-memory-reference-returnable-box-a42091c4.md (rank -8.51)
2. memory/reference_returnable_box.md (rank -8.35)
3. memory/MEMORY.md (rank -7.97)
```
**Expected match:** Hermes memory_bridge_search "Returnable Box" should return same 3 files in same order.

---

## Test 3: Smith→Hermes Write ✅
```
Entry written:
  id: 028d5777b8d5
  title: "Audit Test Entry from Smith"
  content: "This entry was written by Smith at 2026-07-02T09:14+07:00. If Hermes can read this, interop works."
  tags: ["audit", "interop-test"]
  source_agent: "openclaw"
  created_at: "2026-07-02T02:14:24.716580+00:00"
```
**Expected match:** Hermes should find this via memory_bridge_search "Audit Test Entry from Smith", then read it with memory_bridge_get id="028d5777b8d5". Content and tags must be identical.

---

## Test 4: Entry Search Verification ✅
```
Search: "Audit Test Entry from Smith"
Result: id=028d5777b8d5, source_agent=openclaw, tags=["audit","interop-test"]
Snippet: "This entry was written by Smith at 2026-07-02T09:14+07:00..."
```
**Expected match:** Same result from Hermes.

---

## Test 5: AGENTS.md Read ✅
```
Line 1: # AGENTS.md - Your Workspace
Line 2: (blank)
Line 3: This folder is home. Treat it that way.
Line 4: (blank)
Line 5: ## Session Startup
```
**Expected match:** Hermes memory_bridge_read "/Users/Jeff/Smith/AGENTS.md" should return identical first 5 lines.

---

## Test 6: Memory File Read ✅
```
memory/2026-07-02.md first 10 lines:
Line 1: # 2026-07-02
Line 2: (blank)
Line 3: ## Morning
Line 4: - Disabled `memory-midnight-maintenance` cron job (was under samantha's agent, not smith's — lesson: always scan all agents)
Line 5: - Job was failing due to `opencode-go/deepseek-v4-flash` rejected by models allowlist
Line 6: - OpenCode tokens depleted — Jeff bought Xiaomi MiMo as replacement
Line 7: - Model: `xiaomi-token-plan/mimo-v2.5-pro` (current default)
Line 8: (blank)
Line 9: ## MCP Memory Bridge (Built Today)
Line 10: - **Purpose**: Shared memory server for OpenClaw + Hermes Agent interop
```
**Expected match:** Hermes memory_bridge_read should return identical content.

---

## Test 7: Scan Consistency ✅
```
Scan result: indexed=0, updated=0, skipped=553, total_files=553
Stats after scan: indexed_files=553, structured_entries=2, total_size_bytes=2,212,887
```
Note: structured_entries is now 2 (1 original + 1 audit entry from Test 3).
**Expected match:** Hermes memory_bridge_scan should show total_files=553. Stats should show indexed_files=553.

---

## Test 8: Session Isolation ✅
```
Session key: agent:smith:telegram:default:direct:alice
Model: xiaomi-token-plan/mimo-v2.5-pro
Platform: Telegram
Agent: Smith
```
**Expected:** Hermes should have a DIFFERENT session key. Neither agent should see the other's conversation history.

---

## Test 9: Tool Isolation ✅
Smith's tools (from OpenClaw):
- Core: read, write, edit, apply_patch, exec, process, nodes, cron, message, gateway
- Agent: agents_list, sessions_list, sessions_history, sessions_send, sessions_spawn, sessions_yield, subagents, session_status
- Memory: memory_search, memory_get, lcm_grep, lcm_describe, lcm_expand, lcm_expand_query
- Wiki: wiki_search, wiki_get, wiki_apply, wiki_lint, wiki_status
- Workboard: workboard_*, workboard_board_*, workboard_notify_*
- Media: image, image_generate, video_generate, music_generate, pdf, tts
- MCP (shared): memory_bridge_scan, memory_bridge_search, memory_bridge_read, memory_bridge_write, memory_bridge_list, memory_bridge_get, memory_bridge_stats

**Expected:** Hermes should have its own tools (terminal, file, code_execution, web, browser, etc.) PLUS the 7 memory_bridge_* MCP tools. Hermes should NOT have workboard_*, lcm_*, wiki_*, or sessions_* tools.

---

## Test 10: Profile Isolation ✅
```
Identity: Smith (OpenClaw agent)
Emoji: 📦
Persona: Executive AI partner for Jeff
SOUL.md loaded from: ~/Smith/SOUL.md
AGENTS.md loaded from: ~/Smith/AGENTS.md
```
**Expected:** Hermes should identify as Hermes Agent (smith profile). It loads its own SOUL.md from ~/.hermes/SOUL.md, NOT ~/Smith/SOUL.md. Both load the same AGENTS.md from ~/Smith/AGENTS.md (cwd-dependent).

---

## Summary (Smith Side Complete)

| # | Test | Smith Result | Hermes Expected |
|---|------|-------------|-----------------|
| 1 | MCP Stats | indexed=553, entries=1, size=2,212,887 | Same numbers |
| 2 | Search "Returnable Box" | 3 files, specific order | Same 3 files, same order |
| 3 | Write entry | id=028d5777b8d5, source=openclaw | Can read it |
| 4 | Search verification | Found, correct content | Same result |
| 5 | AGENTS.md read | Lines 1-5 as shown | Identical content |
| 6 | Memory file read | Lines 1-10 as shown | Identical content |
| 7 | Scan consistency | total_files=553 | Same count |
| 8 | Session isolation | agent:smith:telegram:... | Different session key |
| 9 | Tool isolation | Has workboard_*, lcm_*, etc. | Has terminal, file, etc. + 7 shared MCP tools |
| 10 | Profile isolation | Smith, ~/Smith/SOUL.md | Hermes, ~/.hermes/SOUL.md |

**Next:** Jeff runs Hermes side with the same prompts and compares.

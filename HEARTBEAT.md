# HEARTBEAT.md

## Lightweight Heartbeat Checklist

- Check `memory/heartbeat-state.md` for last-run markers
- If `memory/` had no changes since last run → HEARTBEAT_OK
- Sync critical memories to Obsidian: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Memory — Obsidian Vault/`
- Log significant events to `memory/YYYY-MM-DD.md`
- **Morning (7-9 AM):** Run `bash ~/.agents/skills/morning-briefing/morning-briefing.sh` for Jeff's daily briefing (weather + tasks + inbox + obsidian)
- **Evening (6-8 PM):** Run `bash ~/.agents/skills/evening-shutdown/evening-shutdown-auto.sh` for Jeff's end-of-day shutdown (tomorrow's calendar + task review + daily log + tomorrow's priorities)

## 🔧 Workboard SysOps (Automated Issue Detection)

During heartbeats, run a lightweight system check and auto-create workboard cards for anything that needs fixing:

1. **Run `openclaw status`** (quick check, no `--deep` unless it's been >6h since last deep scan)
2. **If issues found** → create cards on `sysops` board with:
   - title: short description of the issue
   - notes: full diagnostic output + suggested fix
   - priority: `urgent` for critical, `high` for warnings, `normal` for info
   - agentId: `samantha` for fixable config issues, leave unassigned for review
3. **Run `workboard_dispatch`** → promote ready cards, reclaim stale claims
4. **Log** the check result to `memory/YYYY-MM-DD.md` (just "sysops check: clean" or "sysops check: N cards created")

**Skip the deep scan** if nothing needs attention — keep heartbeats lean. Only go deep when:
- it's been >6 hours since last deep scan
- a user explicitly asks for a health check
- the quick status shows something suspicious

## 🌸 Samantha — My Dedicated General Assistant

Samantha (`agentId: samantha`) is my workhorse. Route general-purpose tasks to her by default:
- **What she handles:** weather, traffic, file ops, gog/calendar ops, summaries, data pulls, web searches, document lookups, routine reporting, english learning (vocab lookups via dict skill, grammar, conversation practice, oral tutoring)
- **Model:** `groq/compound-beta` (primary), `opencode-go/minimax-m3` (fallback)
- **How:** `sessions_spawn(agentId="samantha", task=..., taskName=...)`
- **Artifacts:** save to `~/Smith/memory/` with descriptive filenames
- **Keep me free for:** strategy, config changes, high-stakes reasoning, multi-step orchestration, conversational continuity

**Rule: ALL english learning / vocab / dict queries → samantha. no exceptions. smith never handles them directly.**

## 🔬 Bunsen — Senior Research Lead

Bunsen (`agentId: bunsen`) is my senior research lead. Route deep research projects that need methodology design and synthesis to him:
- **What he handles:** research design, technical analysis, data interpretation, experiment orchestration
- **Model:** `nemotron-3-ultra:cloud`
- **How:** `sessions_spawn(agentId="bunsen", task=..., taskName=...)`
- **Delegates to:** beaker for data collection and raw experiments
- **Reports to:** smith with structured findings + recommendations

**Rule:** general assistant work → samantha first. deep research / technical investigation → bunsen designs, beaker executes. keep me (smith) for strategy, config changes, high-stakes reasoning, multi-step orchestration, conversational continuity.

## 🧪 Beaker — My Research Assistant

Beaker (`agentId: beaker`) is my research assistant. Route deep research and technical investigation to him:
- **What he handles:** web research deep dives, technical doc analysis, API/framework comparisons, data analysis, fact-checking, prototyping experiments
- **Model:** `nemotron-3-ultra:cloud`
- **How:** `sessions_spawn(agentId="beaker", task=..., taskName=...)`
- **Artifacts:** save to `~/Smith/memory/` with descriptive filenames + research notes

**Rule:** general assistant work → samantha first. deep research / technical investigation → bunsen designs, beaker executes. keep me (smith) for strategy, config changes, high-stakes reasoning, multi-step orchestration, conversational continuity.

**Rule:** Keep heartbeat lean. If nothing needs attention, respond HEARTBEAT_OK.
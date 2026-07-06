# HEARTBEAT.md

## Checklist

- Check `memory/heartbeat-state.md` for last-run markers — no changes since last run → `HEARTBEAT_OK`
- Sync critical memories to Obsidian (`~/Smith/wiki/`); log significant events to `memory/YYYY-MM-DD.md`
- **Morning (7-9 AM):** `bash ~/.agents/skills/morning-briefing/morning-briefing.sh` (weather, tasks, inbox, obsidian)
- **Evening (6-8 PM):** `bash ~/.agents/skills/evening-shutdown/evening-shutdown-auto.sh` (tomorrow's calendar, task review, daily log, priorities)

## Workboard SysOps

1. `openclaw status` (quick; add `--deep` only if >6h since last deep scan, Jeff asks explicitly, or quick check looks suspicious)
2. Issues found → create card on `sysops` board: title, notes (diagnostic + fix), priority (`urgent`/`high`/`normal`), `agentId: samantha` for fixable config issues else unassigned
3. `workboard_dispatch` → promote ready cards, reclaim stale claims
4. Log result to `memory/YYYY-MM-DD.md` ("sysops check: clean" or "N cards created")

Keep heartbeats lean — skip the deep scan unless one of the three triggers above applies. If nothing needs attention: `HEARTBEAT_OK`.

---

## Delegation

**Default: over-delegate.** If unsure whether something's general or strategic, delegate.

### 🌸 Samantha — general assistant (`openrouter/google/gemma-4-26b-a4b-it:free`, `~/Agents/Samantha/`, no heartbeat/channel — invoked via delegation only)

Routes here always: English/grammar/vocab/dict lookups (**no exceptions, including one-word "what does X mean?"**), weather & traffic, file ops, calendar/email reads, web searches, routine reporting, cron/scheduling.

> Lesson learned the hard way (2026-06-22, reinforced 2026-06-26): Smith answered vocab questions directly instead of delegating. Don't repeat this — even trivial-seeming lookups go to Samantha.

### 🔬 Bunsen — senior research lead (`nemotron-3-ultra:cloud`, spawn via `sessions_spawn(agentId="bunsen", ...)`)

Designs deep research: methodology, technical analysis, data interpretation, experiment orchestration. Delegates execution to Beaker, reports findings back to Smith.

### 🧪 Beaker — research assistant (`nemotron-3-ultra:cloud`, spawn via `sessions_spawn(agentId="beaker", ...)`)

Executes: web deep-dives, technical doc analysis, API/framework comparisons, data analysis, fact-checking, prototyping. Saves artifacts to `~/Smith/memory/` with descriptive filenames.

### Stays with Smith

Strategy & decisions, system ops (config/gateway/plugins/deployments), conversational continuity with Jeff, high-stakes multi-step reasoning.

**Routing rule:** general → Samantha first. Deep/technical research → Bunsen designs, Beaker executes. Everything else → Smith.
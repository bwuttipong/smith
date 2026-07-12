---
id: deliverables/2026-07-12-state-of-the-system-brief
pageType: deliverable
title: "State of the System — Brief"
created: 2026-07-12
type: deliverable
tags: [brief, synthesis, agent-infrastructure, projects, status]
built_from:
  - sources/bridge-smith (memory corpus, 268 pages)
  - sources/bridge-smith-*weekly-report-2026-06-27-to-2026-07-03*
  - sources/bridge-smith-*2026-07-05*
  - entities/agent-os.md
  - concepts/high-agency.md
confidence: medium-high
---

# State of the System — Brief
*Compiled 2026-07-12 from the memory wiki (295 sources). Provenance traces to `raw/` and `sources/`.*

> First deliverable in the new `deliverables/` layer — a worked example of the
> **query → synthesis → ship** operation over the existing wiki corpus.

## 1. The one-paragraph picture

Jeff runs a multi-agent operation coordinated by **Smith** (executive AI, OpenClaw
gateway) with a fleet including **Hermes**, **Beaker**, **Cookie**, **Fozzie**, and
**Kermit**. The knowledge substrate is this **LLM wiki** (Karpathy pattern) fed by a
**Memory Bridge** that indexes ~552 files across `memory/` and `wiki/`. The human-facing
control surface is **Agent OS**, a local Next.js mission-control dashboard. Alongside the
agent tooling, real revenue-side engineering work runs on **CirculatingBox** and two
other ERP/QA projects.

## 2. Where the wiki's attention actually is

By source volume (295 pages), the corpus is dominated by Smith's own operational memory:

| Cluster | Pages | What it covers |
|---|---:|---|
| `bridge-smith` | 268 | Daily memory, weekly reports, decisions — the operational core |
| `bridge-beaker` | 9 | Beaker agent memory |
| `bridge-cookie` | 7 | Cookie agent memory |
| `bridge-fozzie` | 6 | Fozzie agent memory |
| `bridge-kermit` | 3 | Kermit agent memory |

Recurring themes by mention: **OpenClaw** (infra/gateway), **wiki**, **Slack**,
**English** (learning), **calendar**, **Obsidian**, **Hermes**. Read that as: the system
spends most of its recorded effort on *agent infrastructure and coordination*, with a
steady thread of English-learning and calendar/comms support.

## 3. What shipped (week of Jun 27 – Jul 3)

Grounded in the weekly-report source:

**CirculatingBox (ERP / SyteLine)**
- Fixed the "Doubling Quantity" transfer bug — UI was summing stock across all
  locations instead of the selected source (`Id` vs `BoxNo` query param). Shipped v3.1.0.35.
- Standardized 176 production location names via `sqlcmd`.
- Resolved an MRP ghost Purchase Requisition; documented a Customer Order cross-reference workaround.

**Agent infrastructure**
- Indexed "High Agency in 30 Minutes" into the wiki (→ `concepts/high-agency`, `entities/george-mack`).
- Built the **MCP Memory Bridge** — SQLite FTS5 server indexing 552 files, 7 MCP tools,
  passed a 10/10 interop audit between OpenClaw and Hermes.
- Installed **Agent-Reach** (web, YouTube, GitHub, Reddit, Twitter, RSS, …) into Hermes.
- Resolved OpenRouter key issues with a free-model fallback path.

**Workspace bootstrap**
- Kilo Code wired with the memory-bridge, Smith persona, and 10 slash commands across
  three project workspaces (OutsourceEF9, TPK QA Hold, CirculatingBox).
- Copied all three projects to the work machine; built a project registry under `~/Smith/projects/`.

## 4. Agent OS — the control surface

Local mission-control dashboard at `~/Workspaces/agentos` (Next.js 16 + Tailwind v4 +
Framer Motion, port **:3737**). One screen to chat with every agent, plus Goals and
Journal pages backed by this Obsidian vault. *(As of this session it also has custom
skills/agents: run-agentos, add-workflow, add-agent, bridge-doctor, session-handoff.)*

## 5. Open threads worth watching

- **Model context mismatch**: `gemma4:12b-mlx` was set to 262K context but the model
  only supports 4K (janitor/kermit fix pending as of 2026-07-05).
- **Session churn**: the 2026-07-05 daily shows many rapid session-end stamps — worth
  checking whether something is cycling sessions unintentionally.
- **English learning** is a persistent, under-formalized thread (166 mentions) with no
  dedicated concept page yet — a candidate for the next ingest.

## 6. Provenance & confidence
- **High confidence**: items quoted from the weekly report and dated daily memories.
- **Medium**: thematic weighting inferred from keyword frequency, not full reads of all 268 pages.
- Every claim above traces to a `sources/bridge-smith-*` page → original `~/Smith/memory/*.md`.
- **Not verified live**: current running state of agents/services (this is a wiki
  synthesis, not a health check — run `bridge-doctor` / the Agent OS health route for live status).

# Memory Wiki — Agent Schema

The rulebook for any LLM agent operating this vault. Based on Andrej Karpathy's
"LLM Wiki" pattern: **Obsidian is the IDE, the LLM is the programmer, the wiki is the
codebase.** Knowledge is *compiled* into the wiki, not re-retrieved on every query.

Vault mode: `bridge` · Render mode: `obsidian` · maintained by the OpenClaw
memory-wiki plugin.

## Architecture — three layers

| Layer | Folder(s) | Owner | Rule |
|---|---|---|---|
| **Raw** | `raw/` | human / bridge | Immutable source of truth (articles, agent memory, clips). **Never edit.** Evidence layer. |
| **Wiki** | `sources/`, `concepts/`, `entities/`, `syntheses/` + `index.md`, `log.md` | LLM (plugin) | Compiled, cross-linked synthesis. The human-readable knowledge layer. |
| **Deliverables** | `deliverables/` | LLM on demand | Polished, purpose-built outputs synthesized *from* the wiki. The artifacts you ship. |

Supporting:
- `reports/` — plugin-generated **health/lint** output (contradictions, stale pages,
  open questions, provenance). Machine-owned; read it, don't hand-edit it.
- `.openclaw-wiki/cache/agent-digest.json` + `claims.jsonl` — the agent-facing compiled
  digest. Use these for machine reads; markdown pages are the human view.

### Wiki sub-layers
- `sources/` — one page per `raw/` item: summary + key takeaways (plugin-synced, fingerprinted).
- `concepts/` — technical/idea deep-dives (e.g. `high-agency.md`).
- `entities/` — people, orgs, tools (e.g. `george-mack.md`).
- `syntheses/` — high-level articles combining multiple sources.

## The three operations

**Ingest** — a new item lands in `raw/`:
1. Create/refresh its `sources/` page (summary + takeaways).
2. Update the relevant `concepts/` and `entities/` pages; add `[[wikilinks]]` both ways.
3. Update `index.md`'s human-curated sections.
4. Append one line to `log.md`: `## [YYYY-MM-DD] ingest | Title`.

**Query** — answer from the wiki, not the raw pile. Search `sources`/`concepts`/
`entities`, synthesize. If the answer is worth keeping, file it as a new page in
`syntheses/`; if it's a finished output for a purpose, write it to `deliverables/`.

**Lint** — health-check for drift (the #1 failure mode): contradictions, stale claims,
orphan pages, missing cross-references. Output lives in `reports/`.

## Standing rules (load-bearing — do not violate)
- Treat generated blocks as plugin-owned; preserve human notes outside managed markers
  (`<!-- openclaw:human:start/end -->`).
- Prefer source-backed claims over wiki-to-wiki citation loops — every claim traces to `raw/`.
- Prefer structured `claims` with evidence over burying key beliefs only in prose.
- **Never move `sources/`, `concepts/`, `entities/`, `syntheses/`, or `reports/`** — the
  plugin hardcodes these relative paths in `source-sync.json` and `agent-digest.json`.
  Moving them orphans the 295 synced sources. The vault root *is* the wiki layer.
- Wikilinks `[[Page Name]]` everywhere; YAML frontmatter (source, date, tags) on every page.

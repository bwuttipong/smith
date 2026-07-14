# Wiki Log

> Chronological record of all wiki actions. Append-only.

## [2026-06-28] ingest | High Agency in 30 Minutes
- URL: https://www.highagency.com/
- New raw source: `raw/articles/high-agency-in-30-minutes.md`
- New concept: `concepts/high-agency.md`
- New entity: `entities/george-mack.md`
- Updated: `index.md` with human-curated sections

## [2026-07-12] restructure | Align to Karpathy raw→wiki→deliverables model
- Added: `deliverables/` (finished human-facing outputs, synthesized from the wiki)
- Rewrote `AGENTS.md` as a full Karpathy-style schema (3 layers, ingest/query/lint ops)
- No content moved — plugin-managed folders (`sources/` ×295, `concepts/`, `entities/`,
  `syntheses/`, `reports/`) left in place to preserve `source-sync.json` path integrity

## [2026-07-12] deliver | State of the System — Brief
- New deliverable: `deliverables/2026-07-12-state-of-the-system-brief.md`
- Synthesized from the `bridge-smith` memory corpus (268 pages) + weekly report + entities
- First worked example of the query→synthesis→ship operation over the wiki

## [2026-07-12] index | Workspace Map + CLAUDE.md wiring
- Added "🗺️ Workspace Map" to `index.md` (below the plugin marker, human-owned zone) —
  references raw / wiki / deliverables / reports; lists deliverables + key entry points
- Wired `~/.claude/CLAUDE.md` session-startup to read `index.md` on every new chat
- New skill `summarize-large-files` (in agentos/.claude/skills) — one-line summary for
  files >100L/6KB; skips plugin-managed (`sources/`, `reports/`, `openclaw:` markers)
- Applied it: added `summary:` frontmatter to `raw/articles/high-agency-in-30-minutes.md`

## [2026-07-14] index | Agent OS project pointer
- Added "🛠️ Active Projects" to `index.md` (human-owned Workspace Map zone) — Agent OS
  dashboard isn't raw/sources material (it's code), so it's pointed-to rather than ingested:
  links to the project's own memory (`~/.claude/projects/.../memory/MEMORY.md`), Smith's
  daily memory, and today's handoff doc (`/private/tmp/claude-501/agentos-handoff-2026-07-14-2209.md`)
- Session covered: Manage tab (iframes Hermes/OpenClaw native dashboards), two Claude agent
  cards (claude-direct + claude, same CLI bridge), Claude page sub-tabs, SEO Content Pipeline
  rebuild (Generate/Deploy/History/Transcripts/Tasks)

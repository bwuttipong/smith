# Deliverables

Finished, human-facing outputs synthesized *from* the wiki — briefs, reports you
actually send, decision memos, drafts. This is the "compiled binary you ship."

Distinct from the other layers:
- `raw/`      — immutable source material (never edit)
- wiki layer  — LLM-maintained knowledge (`sources/`, `concepts/`, `entities/`, `syntheses/`)
- `reports/`  — plugin-generated *health/lint* output (contradictions, stale pages) — machine-owned
- `deliverables/` — **this** — polished artifacts produced on demand for a purpose

Naming: `YYYY-MM-DD-<slug>.md`. Each deliverable should cite the wiki pages / sources
it was built from so provenance is traceable back to `raw/`.

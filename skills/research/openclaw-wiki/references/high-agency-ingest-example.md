# High Agency Ingest — Worked Example

Ingested on 2026-06-28 from https://www.highagency.com/

## Steps Taken

### 1. Fetch article content
Used `browser_navigate` → `browser_console` with JS expression to extract all text content (p, h1-h3, li, blockquote elements joined by newlines). The `browser_snapshot` was truncated at ~1300+ lines.

### 2. Save raw source
Created `raw/articles/high-agency-in-30-minutes.md` with YAML frontmatter:
```yaml
---
source_url: https://www.highagency.com/
ingested: 2026-06-28
sha256: <computed via sha256sum after writing>
---
```

### 3. Compute sha256
```bash
sha256sum ~/Smith/wiki/raw/articles/high-agency-in-30-minutes.md | awk '{print $1}'
```
Then used `patch` to update the frontmatter sha256 value.

### 4. Create concept page
Created `concepts/high-agency.md` with:
- YAML frontmatter (title, created/updated, type: concept, tags, sources)
- Overview definition
- The Tricycle Model table (Clear thinking × Bias to action × Disagreeability)
- The Software: 5 mental models (bullet list)
- Low Agency Traps: table with Trap / Root Cause / Escape Route
- Key Insight quote
- Source attribution

### 5. Create entity page
Created `entities/george-mack.md` with:
- YAML frontmatter (title, created/updated, type: entity, tags, sources)
- Bio and links
- Attribution context

### 6. Update index.md
Added sections AFTER the `<!-- openclaw:wiki:index:end -->` marker:
```markdown
## Concepts (Human-curated)
- [[concepts/high-agency|High Agency]] — one-line summary

## Entities (Human-curated)
- [[entities/george-mack|George Mack]] — one-line summary

## Raw Sources
- [[raw/articles/high-agency-in-30-minutes|High Agency in 30 Minutes]] — description
```

### 7. Create/update log.md
Created `log.md` with format:
```markdown
## [2026-06-28] ingest | High Agency in 30 Minutes
- URL: https://www.highagency.com/
- Created: `raw/articles/high-agency-in-30-minutes.md`
- Created: `concepts/high-agency.md`
- Created: `entities/george-mack.md`
- Updated: `index.md`
```

## Key Decisions

- **No SCHEMA.md**: the OpenClaw wiki doesn't have one; skip SCHEMA-related steps from llm-wiki skill
- **raw/ didn't exist**: created `raw/articles/` manually
- **Entity threshold**: George Mack got an entity page because the article is central to one source (his original essay) — meets the "central to one source" criterion
- **Tags used**: `[psychology, decision-making, mindset, productivity]` — no strict taxonomy in this wiki, but kept them consistent

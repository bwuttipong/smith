---
name: openclaw-wiki
description: "Work with an OpenClaw-managed markdown wiki: orient, ingest sources, create human-curated pages alongside plugin-generated content, and maintain navigation."
version: 1.1.0
author: Smith
tags: [wiki, openclaw, knowledge-base, markdown, ingestion]
---

# OpenClaw Wiki

**This wiki is NOT a Karpathy-style llm-wiki.** It's an OpenClaw-managed wiki where the `.openclaw-wiki/` plugin auto-generates source pages from memory bridges, manages the index with `<!-- openclaw:wiki:... -->` markers, and owns certain sections. Human-curated content lives **outside** those markers.

The wiki at `~/Smith/wiki/` is an instance of this pattern.

## Key Differences from llm-wiki

| Aspect | llm-wiki (Karpathy) | OpenClaw wiki |
|--------|--------------------|---------------|
| Schema | `SCHEMA.md` defines domain, tags, conventions | No SCHEMA.md — orient via `AGENTS.md` and existing structure |
| Raw sources | `raw/` directory, agent-managed | No `raw/` by default — sources auto-bridged from memory into `sources/` |
| Index | Agent owns the whole index | Plugin owns `<!-- openclaw:wiki:index:start -->` block; human additions go **after** `<!-- openclaw:wiki:index:end -->` |
| Entity/Concept pages | Agent creates freely | Plugin generates empty index stubs; human pages go outside `<!-- openclaw:wiki:entities:index:start/end -->` markers |
| Log | Agent creates and maintains | Create `log.md` manually if missing |

## Orientation (every session)

Before any operation:

1. **Read `AGENTS.md`** at wiki root — it overrides the llm-wiki skill's SCHEMA.md conventions
2. **Read `index.md`** — see what exists, note plugin-generated vs human-curated sections
3. **Create or read `log.md`** — check recent activity
4. **Check `.openclaw-wiki/state.json`** for render mode and metadata

## Ingesting an External Source (URL / Article)

When adding content **not** from a memory bridge (e.g. a web article):

### Step 1: Capture the raw source

Create `raw/articles/` if it doesn't exist. Save the article with frontmatter:

```yaml
---
source_url: https://example.com/article
ingested: YYYY-MM-DD
sha256: <hex digest of body content>
---
```

Compute the sha256 with: `sha256sum path/to/file.md | awk '{print $1}'`

Update the frontmatter after computing the hash.

### Step 2: Check what already exists

Search the wiki for existing entity/concept pages that cover the article's topics. Avoid creating duplicates.

### Step 3: Create wiki pages (outside plugin markers)

Entity pages go in `entities/`, concept pages in `concepts/`. Use YAML frontmatter:

```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept
tags: [tag1, tag2]
sources: [raw/articles/filename.md]
---
```

**CRITICAL:** The `<!-- openclaw:wiki:entities:index:start -->` block is plugin-owned. Your page files and index references must go **after** the `<!-- ...:end -->` marker.

### Step 4: Update the index

Add a new section **after** `<!-- openclaw:wiki:index:end -->`:

```markdown
## Concepts (Human-curated)
- [[concepts/slug|Display Name]] — One-line summary

## Entities (Human-curated)
- [[entities/slug|Display Name]] — One-line summary

## Raw Sources
- [[raw/articles/slug|Display Name]] — Brief description
```

### Step 5: Update log.md

Create if missing. Append entries in this format:

```markdown
## [YYYY-MM-DD] ingest | Source Title
- URL: https://...
- Created: `raw/articles/filename.md`
- Created: `concepts/slug.md`
- Created: `entities/slug.md`
- Updated: `index.md`
```

## Creating Human-Curated Content

- **Put files in the correct directory** (`entities/`, `concepts/`, `syntheses/`)
- **Do NOT write inside** `<!-- openclaw:wiki:...:start -->` ... `<!-- ...:end -->` blocks — those are overwritten by the plugin
- **Add index references below** the generated block, in a clearly labeled human-curated section
- **Cross-reference** with `[[wikilinks]]` between pages when possible
- **Tags are optional** (the OpenClaw wiki doesn't enforce a strict taxonomy)

## Pitfalls

- **Don't modify files in `sources/`** — those are auto-generated from memory bridges and will be overwritten
- **Don't edit inside plugin markers** — your changes will be lost on next plugin sync
- **Don't assume SCHEMA.md exists** — this isn't a Karpathy wiki; orient from AGENTS.md and existing files
- **raw/ may not exist** — create it manually; it's not part of the default OpenClaw wiki structure
- **llm-wiki skill instructions often don't apply** — skip steps about SCHEMA.md, tag taxonomies, and page thresholds unless you've established them yourself
- **Keep human sections scannable** — one line per entry in the index, bullet-form summaries

## Reference Files

- `references/high-agency-ingest-example.md` — Concrete worked example of ingesting a web article (George Mack's High Agency essay): browser extraction, raw source, concept page, entity page, index update, log creation
- `references/end-of-day-git-sync.md` — End-of-day git commit+push ritual for cross-machine sync. Run on all profiles when Jeff says "good night"

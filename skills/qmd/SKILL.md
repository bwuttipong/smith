---
name: qmd
description: Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode.
homepage: https://github.com/tobi/qmd
metadata:
  hermes:
    tags: [search, indexing, mcp]
---

# qmd — Quick Markdown Search

Local search engine over markdown/code files. Supports BM25 keyword search, vector similarity, and hybrid search with query expansion and reranking.

## Setup (Jeff's MacBook Air)

- **Install**: `npm install -g @tobilu/qmd` → `/opt/homebrew/bin/qmd`
- **Native module fix**: If `better-sqlite3` errors after Node.js upgrade:
  1. Try rebuild: `npm rebuild better-sqlite3 --prefix /opt/homebrew/lib/node_modules/@tobilu/qmd`
  2. If rebuild fails (permission issues or version mismatch persists): `npm install -g @tobilu/qmd --prefix ~/.local` then `ln -sf ~/.local/bin/qmd /opt/homebrew/bin/qmd`
- **Ollama removed** (July 2026) — BM25 keyword search (`qmd search`) and embedding (`qmd embed`) work without it. Vector search (`vsearch`) and hybrid reranking (`query`) are broken without Ollama (fall back to BM25 only).
- **GPU**: Apple M4 with Metal acceleration

## MCP Integration (configured in ~/.hermes/config.yaml)

```yaml
mcp_servers:
  qmd:
    command: "qmd"
    args: ["mcp"]
    timeout: 60
    connect_timeout: 30
```

Tools exposed via MCP: `mcp_qmd_query`, `mcp_qmd_get`, `mcp_qmd_multi_get`
**Requires Hermes restart** to pick up MCP config changes.

## Collections (current)

| Collection | Files | Description |
|---|---|---|
| memory | 15 | Jeff's persistent memory — SOUL.md, USER.md, MEMORY.md, daily logs |
| workspaces | 210 | Per-agent workspace memory (jarvis, morgan, etc.) |
| avengers-groot | 123 | groot agent session transcripts |
| avengers-jarvis | 2 | jarvis agent session transcripts |
| sessions | 7 | session data |
| avengers-trinity | 14 | trinity agent session transcripts |
| matrix-trinity | 2 | trinity agent session transcripts |

## CLI Usage

### Indexing
```bash
qmd collection add /path --name docs --mask "**/*.md"
qmd update                                    # re-index all collections
qmd embed                                     # generate/refresh vector embeddings
qmd status                                    # health check
```

### Search
```bash
qmd search "query"                            # BM25 keyword only (no LLM)
qmd vsearch "query"                           # vector similarity only
qmd query "query"                             # hybrid: auto-expand + rerank (recommended)
qmd get qmd://collection/file.md:10 -l 40    # get specific doc with line range
```

### Query Syntax (qmd query)
```
qmd query "how does auth work"                # single-line → auto expand
qmd query $'lex: exact term\nvec: concept'   # typed query document
qmd query $'intent: find error handling\nlex: error\nvec: graceful failure'
```

### Maintenance
```bash
qmd embed -f                                  # force re-embed everything
qmd cleanup                                   # clear caches, vacuum DB
qmd collection update-cmd <name> 'git pull'   # auto-update on index
```

## Pitfalls

- **Node version mismatch kills `qmd embed` silently.** If `qmd` was compiled against NODE_MODULE_VERSION 147 but the shell running `embed` has a different Node (e.g. via nvm/fnm in Ghostty vs system Node), ~70% of chunks fail with no visible error. Run `node --version` in the shell before `qmd embed`. If mismatched, either use the same Node version that compiled qmd, or rebuild: `npm rebuild better-sqlite3 --prefix /opt/homebrew/lib/node_modules/@tobilu/qmd`.

## Notes
- Index lives at `~/.cache/qmd/index.sqlite` (350+ MB, grows with collections)
- `qmd embed` works without Ollama (generates vector embeddings successfully)
- `qmd vsearch` and reranking in `qmd query` need Ollama — without it, `query` falls back to BM25 only
- MCP mode: `qmd mcp` (stdio transport)

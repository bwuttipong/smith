# SEARCH - Search Shared Memory Bridge

Full-text search across all indexed memory files and structured entries via MCP memory-bridge.

## Usage
```
/search <query> [limit]
```

## Description
Uses the `memory_bridge_search` MCP tool (FTS5 with porter stemming + unicode). Searches across:
- `~/Smith/memory/` — daily logs, artifacts, reports
- `~/Smith/wiki/` — knowledge base pages
- Structured entries written by both OpenClaw and Hermes

## Examples
```
/search "Returnable Box"
/search "weekly review" 5
/search "TODO"
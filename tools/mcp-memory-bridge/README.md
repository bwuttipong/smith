# MCP Memory Bridge

Shared memory server for **OpenClaw** and **Hermes Agent**. Both frameworks connect to this MCP server and get the same search, read, write, and list capabilities over a unified memory corpus.

## Architecture

```
┌──────────┐     stdio/MCP     ┌──────────────────┐
│ OpenClaw │ ◄──────────────► │                  │
│ (Smith)  │                   │  Memory Bridge   │  ◄── SQLite FTS5
└──────────┘                   │  MCP Server      │  ◄── ~/Smith/memory/*.md
                               │                  │  ◄── ~/Smith/wiki/*.md
┌──────────┐     stdio/MCP     │                  │  ◄── ~/Smith/MEMORY.md
│  Hermes  │ ◄──────────────► │                  │
└──────────┘                   └──────────────────┘
                               ▲         ▲
                               │         │
┌──────────────┐  stdio/MCP    │         │  stdio/MCP  ┌──────────────┐
│ Kilo Code    │ ◄────────────┘         └────────────► │ Antigravity  │
│ (VS Code)    │                                       │ (Google IDE) │
└──────────────┘                                       └──────────────┘
```

Four surfaces, one shared memory.

## Tools Exposed

| Tool | Description |
|------|-------------|
| `memory_bridge_scan` | Re-scan filesystem, update index |
| `memory_bridge_search` | Full-text search (FTS5) across all memory |
| `memory_bridge_read` | Read a specific file by path |
| `memory_bridge_write` | Write a structured entry (title + content + tags) |
| `memory_bridge_list` | List indexed files or structured entries |
| `memory_bridge_get` | Get a structured entry by ID |
| `memory_bridge_stats` | Store statistics |

## Setup for OpenClaw

Add to OpenClaw config (`~/.openclaw/config.yaml`):

```yaml
mcp:
  servers:
    memory-bridge:
      command: python3
      args:
        - ~/Smith/tools/mcp-memory-bridge/server.py
```

## Setup for Hermes

Add to Hermes config (`~/.hermes/config.yaml`):

```yaml
mcp:
  servers:
    memory-bridge:
      command: python3
      args:
        - ~/Smith/tools/mcp-memory-bridge/server.py
```

Or via CLI:
```bash
hermes mcp add memory-bridge --command "python3 ~/Smith/tools/mcp-memory-bridge/server.py"
```

## Setup for Kilo Code (VS Code)

### macOS

1. Install Kilo Code from VS Code Extensions marketplace
2. Click gear icon → Agent Behaviour → MCP Servers → Add Server → Local (stdio)
3. Fill in:
   - **Name:** `memory-bridge`
   - **Command:** `python3`
   - **Args:** `/Users/Jeff/Smith/tools/mcp-memory-bridge/server.py`
4. Save

Or copy `kilo-code-mcp.json` contents to:
```
~/Library/Application Support/Code/User/globalStorage/kilocode.kilo-code/kilo.jsonc
```

### Windows (work machine)

1. Install Kilo Code from VS Code Extensions marketplace
2. Click gear icon → Agent Behaviour → MCP Servers → Add Server → Local (stdio)
3. Fill in:
   - **Name:** `memory-bridge`
   - **Command:** `python`
   - **Args:** `C:\Users\Wuttipong.t\Smith\tools\mcp-memory-bridge\server.py`
4. Save

Or copy `kilo-code-mcp.windows.json` contents to:
```
%APPDATA%\Code\User\globalStorage\kilocode.kilo-code\kilo.jsonc
```

**Note:** Adjust the path if your Smith workspace is at a different location.

## Setup for Google Antigravity 2.0

Add to `~/.gemini/config/mcp_config.json` (or `~/.gemini/antigravity/mcp_config.json`):

```json
{
  "mcpServers": {
    "memory-bridge": {
      "command": "python3",
      "args": ["/Users/Jeff/Smith/tools/mcp-memory-bridge/server.py"]
    }
  }
}
```

Or via Antigravity IDE: agent side panel → Manage MCP Servers → View raw config → paste.

## How It Works

1. On startup, the server scans `~/Smith/memory/` and `~/Smith/wiki/` for `.md` and `.txt` files
2. All content is indexed in a local SQLite database with FTS5 full-text search
3. Both agents can search across all memory, read files, and write structured entries
4. Structured entries are stored in the DB (not filesystem) and tagged with the source agent
5. Run `memory_bridge_scan` to pick up new filesystem changes

## Storage

- **SQLite DB**: `~/Smith/tools/mcp-memory-bridge/memory.db`
- **Source files**: `~/Smith/memory/`, `~/Smith/wiki/`, `~/Smith/MEMORY.md`
- **Structured entries**: stored in the DB with title, content, tags, source agent

## Running Standalone

```bash
python3 ~/Smith/tools/mcp-memory-bridge/server.py
```

Reads from stdin, writes to stdout (MCP stdio transport).

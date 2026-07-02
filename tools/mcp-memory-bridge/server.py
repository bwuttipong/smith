#!/usr/bin/env python3
"""
MCP Memory Bridge — shared memory server for OpenClaw + Hermes.

Exposes a SQLite FTS5-backed memory store as MCP tools.
Both agents connect via stdio transport and get the same
search, read, write, and list capabilities over a shared
memory corpus.

Usage:
    python server.py                     # default paths
    python server.py --paths ~/Smith/memory ~/Smith/wiki
    python server.py --db /path/to/memory.db
"""

import argparse
import os
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
)

from store import MemoryStore

# ---------------------------------------------------------------------------
# CLI args
# ---------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="MCP Memory Bridge Server")
parser.add_argument("--db", default=os.path.expanduser("~/Smith/tools/mcp-memory-bridge/memory.db"))
parser.add_argument("--paths", nargs="*", default=None,
                    help="Directories to index (default: ~/Smith/memory, ~/Smith/wiki)")
args, _ = parser.parse_known_args()

watch_paths = args.paths or [
    os.path.expanduser("~/Smith/memory"),
    os.path.expanduser("~/Smith/wiki"),
]

store = MemoryStore(db_path=args.db, watch_paths=watch_paths)

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------
server = Server("memory-bridge")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="memory_bridge_scan",
            description="Re-scan the filesystem and update the memory index. Run this to pick up new or changed files.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
        Tool(
            name="memory_bridge_search",
            description="Full-text search across all indexed memory files and structured entries. Uses FTS5 (porter stemming + unicode). Returns matching file paths, snippets, and structured entry hits.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (FTS5 syntax: AND by default, use OR explicitly, quotes for phrases)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default 10)",
                        "default": 10,
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="memory_bridge_read",
            description="Read the contents of a specific memory file by path.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Absolute path to the file (e.g. ~/Smith/memory/2026-07-02.md)",
                    },
                },
                "required": ["path"],
            },
        ),
        Tool(
            name="memory_bridge_write",
            description="Write a structured memory entry (title + content + tags). Stored in the shared DB, accessible by both OpenClaw and Hermes.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Entry title",
                    },
                    "content": {
                        "type": "string",
                        "description": "Entry content (markdown)",
                    },
                    "tags": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Tags for categorization",
                        "default": [],
                    },
                    "source_agent": {
                        "type": "string",
                        "description": "Which agent wrote this (openclaw or hermes)",
                        "default": "unknown",
                    },
                },
                "required": ["title", "content"],
            },
        ),
        Tool(
            name="memory_bridge_list",
            description="List indexed memory files or structured entries.",
            inputSchema={
                "type": "object",
                "properties": {
                    "kind": {
                        "type": "string",
                        "enum": ["files", "entries"],
                        "description": "List filesystem files or structured entries (default: files)",
                        "default": "files",
                    },
                    "directory": {
                        "type": "string",
                        "description": "Filter files by directory prefix (optional)",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results (default 50)",
                        "default": 50,
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="memory_bridge_get",
            description="Get a specific structured memory entry by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "entry_id": {
                        "type": "string",
                        "description": "The entry ID",
                    },
                },
                "required": ["entry_id"],
            },
        ),
        Tool(
            name="memory_bridge_stats",
            description="Return store statistics: file count, entry count, total size, watch paths.",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": [],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    import json

    if name == "memory_bridge_scan":
        result = store.scan_filesystem()
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "memory_bridge_search":
        query = arguments["query"]
        limit = arguments.get("limit", 10)
        file_hits = store.search(query, limit=limit)
        entry_hits = store.search_entries(query, limit=limit)
        return [TextContent(type="text", text=json.dumps({
            "file_matches": file_hits,
            "entry_matches": entry_hits,
            "total": len(file_hits) + len(entry_hits),
        }, indent=2))]

    elif name == "memory_bridge_read":
        content = store.read_file(arguments["path"])
        if content is None:
            return [TextContent(type="text", text=f"File not found: {arguments['path']}")]
        return [TextContent(type="text", text=content)]

    elif name == "memory_bridge_write":
        result = store.write_entry(
            title=arguments["title"],
            content=arguments["content"],
            tags=arguments.get("tags", []),
            source_agent=arguments.get("source_agent", "unknown"),
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "memory_bridge_list":
        kind = arguments.get("kind", "files")
        limit = arguments.get("limit", 50)
        if kind == "files":
            result = store.list_files(directory=arguments.get("directory"), limit=limit)
        else:
            result = store.list_entries(limit=limit)
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "memory_bridge_get":
        entry = store.get_entry(arguments["entry_id"])
        if entry is None:
            return [TextContent(type="text", text=f"Entry not found: {arguments['entry_id']}")]
        return [TextContent(type="text", text=json.dumps(entry, indent=2))]

    elif name == "memory_bridge_stats":
        return [TextContent(type="text", text=json.dumps(store.stats(), indent=2))]

    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
async def main():
    # Initial filesystem scan
    scan_result = store.scan_filesystem()
    sys.stderr.write(f"[memory-bridge] indexed {scan_result['indexed']} files, "
                     f"updated {scan_result['updated']}, "
                     f"skipped {scan_result['skipped']}\n")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

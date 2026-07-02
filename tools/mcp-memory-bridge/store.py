"""
Shared memory store backed by SQLite FTS5 + filesystem.
Both OpenClaw and Hermes read/write the same files.
"""

import os
import json
import sqlite3
import hashlib
import glob
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

DEFAULT_PATHS = [
    os.path.expanduser("~/Smith/memory"),
    os.path.expanduser("~/Smith/wiki"),
]
MEMORY_FILE = os.path.expanduser("~/Smith/MEMORY.md")
DB_PATH = os.path.expanduser("~/Smith/tools/mcp-memory-bridge/memory.db")


class MemoryStore:
    def __init__(self, db_path: str = DB_PATH, watch_paths: list[str] | None = None):
        self.db_path = db_path
        self.watch_paths = watch_paths or DEFAULT_PATHS
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_files (
                path TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                size_bytes INTEGER NOT NULL,
                modified_at TEXT NOT NULL,
                indexed_at TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT 'filesystem'
            )
        """)
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                path,
                content,
                content_rowid='rowid',
                tokenize='porter unicode61'
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memory_entries (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                source_agent TEXT DEFAULT 'unknown'
            )
        """)
        conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS entries_fts USING fts5(
                title,
                content,
                tags,
                tokenize='porter unicode61'
            )
        """)
        conn.commit()
        conn.close()

    def scan_filesystem(self) -> dict:
        """Scan watch_paths and index all .md files."""
        conn = sqlite3.connect(self.db_path)
        indexed = 0
        updated = 0
        skipped = 0

        # Also index MEMORY.md if it exists
        all_files = []
        if os.path.exists(MEMORY_FILE):
            all_files.append(MEMORY_FILE)

        for watch_path in self.watch_paths:
            if not os.path.exists(watch_path):
                continue
            for ext in ("*.md", "*.txt"):
                all_files.extend(glob.glob(os.path.join(watch_path, "**", ext), recursive=True))

        for fpath in all_files:
            try:
                content = Path(fpath).read_text(encoding="utf-8", errors="replace")
                content_hash = hashlib.sha256(content.encode()).hexdigest()
                size = len(content.encode("utf-8"))
                mtime = datetime.fromtimestamp(os.path.getmtime(fpath), tz=timezone.utc).isoformat()

                existing = conn.execute(
                    "SELECT content_hash FROM memory_files WHERE path = ?", (fpath,)
                ).fetchone()

                if existing and existing[0] == content_hash:
                    skipped += 1
                    continue

                conn.execute("""
                    INSERT OR REPLACE INTO memory_files (path, content, content_hash, size_bytes, modified_at, indexed_at, source)
                    VALUES (?, ?, ?, ?, ?, ?, 'filesystem')
                """, (fpath, content, content_hash, size, mtime, datetime.now(timezone.utc).isoformat()))

                # Update FTS index
                row = conn.execute("SELECT rowid FROM memory_files WHERE path = ?", (fpath,)).fetchone()
                if row:
                    conn.execute("DELETE FROM memory_fts WHERE rowid = ?", (row[0],))
                    conn.execute("INSERT INTO memory_fts (rowid, path, content) VALUES (?, ?, ?)", (row[0], fpath, content))

                if existing:
                    updated += 1
                else:
                    indexed += 1
            except Exception as e:
                pass  # skip unreadable files

        conn.commit()
        conn.close()
        return {"indexed": indexed, "updated": updated, "skipped": skipped, "total_files": len(all_files)}

    def search(self, query: str, limit: int = 10) -> list[dict]:
        """Full-text search across all indexed memory files."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        results = []
        try:
            rows = conn.execute("""
                SELECT mf.path, mf.size_bytes, mf.modified_at,
                       snippet(memory_fts, 1, '>>>', '<<<', '...', 50) as snippet,
                       rank
                FROM memory_fts
                JOIN memory_files mf ON memory_fts.rowid = mf.rowid
                WHERE memory_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit)).fetchall()
            results = [dict(r) for r in rows]
        except Exception:
            pass
        conn.close()
        return results

    def read_file(self, path: str) -> Optional[str]:
        """Read a memory file by path."""
        expanded = os.path.expanduser(path)
        if os.path.exists(expanded):
            return Path(expanded).read_text(encoding="utf-8", errors="replace")
        return None

    def write_entry(self, title: str, content: str, tags: list[str] | None = None,
                    entry_id: str | None = None, source_agent: str = "unknown") -> dict:
        """Write a structured memory entry (stored in DB, not filesystem)."""
        conn = sqlite3.connect(self.db_path)
        now = datetime.now(timezone.utc).isoformat()
        eid = entry_id or hashlib.md5(f"{title}{now}".encode()).hexdigest()[:12]
        tags_json = json.dumps(tags or [])

        conn.execute("""
            INSERT OR REPLACE INTO memory_entries (id, title, content, tags, created_at, updated_at, source_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (eid, title, content, tags_json, now, now, source_agent))

        # Update FTS
        row = conn.execute("SELECT rowid FROM memory_entries WHERE id = ?", (eid,)).fetchone()
        if row:
            conn.execute("DELETE FROM entries_fts WHERE rowid = ?", (row[0],))
            conn.execute("INSERT INTO entries_fts (rowid, title, content, tags) VALUES (?, ?, ?, ?)",
                         (row[0], title, content, tags_json))

        conn.commit()
        conn.close()
        return {"id": eid, "title": title, "created_at": now}

    def search_entries(self, query: str, limit: int = 10) -> list[dict]:
        """Search structured memory entries."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        results = []
        try:
            rows = conn.execute("""
                SELECT me.id, me.title, me.tags, me.created_at, me.updated_at, me.source_agent,
                       snippet(entries_fts, 1, '>>>', '<<<', '...', 50) as snippet,
                       rank
                FROM entries_fts
                JOIN memory_entries me ON entries_fts.rowid = me.rowid
                WHERE entries_fts MATCH ?
                ORDER BY rank
                LIMIT ?
            """, (query, limit)).fetchall()
            results = [dict(r) for r in rows]
        except Exception:
            pass
        conn.close()
        return results

    def list_files(self, directory: str | None = None, limit: int = 50) -> list[dict]:
        """List indexed memory files."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        if directory:
            pattern = os.path.expanduser(directory) + "%"
            rows = conn.execute(
                "SELECT path, size_bytes, modified_at, source FROM memory_files WHERE path LIKE ? ORDER BY modified_at DESC LIMIT ?",
                (pattern, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT path, size_bytes, modified_at, source FROM memory_files ORDER BY modified_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def list_entries(self, limit: int = 50) -> list[dict]:
        """List structured memory entries."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, title, tags, created_at, updated_at, source_agent FROM memory_entries ORDER BY updated_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_entry(self, entry_id: str) -> Optional[dict]:
        """Get a specific structured entry."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM memory_entries WHERE id = ?", (entry_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    def stats(self) -> dict:
        """Return store statistics."""
        conn = sqlite3.connect(self.db_path)
        file_count = conn.execute("SELECT COUNT(*) FROM memory_files").fetchone()[0]
        entry_count = conn.execute("SELECT COUNT(*) FROM memory_entries").fetchone()[0]
        total_size = conn.execute("SELECT COALESCE(SUM(size_bytes), 0) FROM memory_files").fetchone()[0]
        conn.close()
        return {
            "indexed_files": file_count,
            "structured_entries": entry_count,
            "total_size_bytes": total_size,
            "watch_paths": self.watch_paths,
            "db_path": self.db_path
        }

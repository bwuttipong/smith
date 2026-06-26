# OpenClaw workspace inspection via attached context

This reference supplements the config-maintenance skill when the user pastes
an attached `.openclaw/` file tree instead of the file itself.

## Pattern

1. Treat the attached tree as a real filesystem snapshot.
2. Use `search_files` against `.openclaw/` before reading full files when you only need locations.
3. Collapse redundant line reads when the same N-line excerpt keeps returning unchanged; switch to `search_files` or a smaller range/offset for a focused slice.

## Action mapping for this workspace

| Need | Tool / approach |
|---|---|
| find files | `search_files(path=".openclaw", ...)` |
| inspect config section | `read_file(path=".openclaw/openclaw.json", offset=..., limit=...)` |
| verify edit | re-read the same offset after `patch` |
| provider search anywhere | `search_files(path=".openclaw", pattern="ollama", target="content")` |

## Pitfall

The root tool tree from the user is often truncated and line-broken. Do not trust
indent counts across line wraps. Aim for exact substrings when patching.
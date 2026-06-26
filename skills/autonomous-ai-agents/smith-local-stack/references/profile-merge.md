# Profile Merge — Move Hermes Profile into Workspace

**Status:** completed 2026-06-24. This is the runbook pointer, not the runbook itself.

## When this skill applies

When Jeff (or any user) wants to:
- Consolidate "scattered" profile/workspace state into one location
- Move a hermes profile from `~/.hermes/profiles/<name>/` into a workspace directory (e.g. `~/Smith/`)
- Reduce the cognitive cost of "is the file under `~/.hermes/` or `~/Smith/`?"

## The full runbook

`~/Smith/docs/hermes-profile-merge-to-workspace.md` — 10 sections, ~14KB, includes:
1. Pre-flight (verify gateway up, free disk, **mandatory tarball backup**)
2. Stop gateway via `launchctl stop` (NEVER `kill -9`)
3. Move contents with `rsync -aAX` (resumable, verifiable, then `rm -rf` source)
4. Update launchd plist via `plutil` (HERMES_HOME, WorkingDirectory, both log paths)
5. Reload plist, start gateway, verify
6. Optional symlink trick for backward compat
7. Full rollback procedure
8. 10 pitfalls (Discord token conflict, qmd MCP failure, session DB lock, etc)
9. Post-merge layout
10. Done checklist (10 boxes)

## Design decisions to make BEFORE running

1. **Subdir vs top-level merge** — subdir (`~/Smith/.hermes-profile/`) avoids collision with workspace folders (`~/Smith/agent/`, `~/Smith/memory/`, `~/Smith/Agents/`). Top-level is "truly one place" but creates rename risk. Default to subdir unless user explicitly says "I want it top-level, no subdir." **Jeff chose top-level on 2026-06-25** — final state is `~/Smith/` with all profile contents merged in directly.
2. **Backup retention** — keep the tarball for at least 7 days post-move. Rollback depends on it existing.
3. **Symlink compat** — strongly recommend creating `~/.hermes/profiles/<name>` as a symlink to the new location, so anything that still hardcodes the old path keeps working. Jeff's merge did this.

## Pitfalls specific to this kind of move

- **Don't `kill -9`.** Use `launchctl stop` (or `hermes gateway restart` from a separate shell). `kill -9` leaves launchd's PID pointer dangling, and the next start fails with "Discord bot token already in use" — this exact error happened on this machine the night of the merge.
- **Session DB is locked while gateway is up.** Stop first, verify stopped, then move `sessions/`.
- **`HERMES_HOME` and `WorkingDirectory` must change together.** If only one updates, gateway either can't find config or can't write logs.
- **Don't try to restart the gateway from inside the chat.** `hermes gateway restart` blocks with "cannot restart from inside the gateway process," and `launchctl kickstart` fails the same way because the terminal tool is also a child of the gateway. Restart must come from a separate shell.
- **`HERMES_HOME` env var may be set in shell rc too** — check for stale references.

## Post-merge state (Jeff's machine, 2026-06-25 — FINAL)

| | old (06-24) | new (06-25) |
|---|---|---|
| physical location | `~/Smith/.hermes-profile/` | `~/Smith/` (no subdir) |
| symlink compat | `~/.hermes/profiles/smith` → `~/Smith/.hermes-profile` | now → `~/Smith/` directly |
| `HERMES_HOME` in plist | `/Users/Jeff/Smith/.hermes-profile` | `/Users/Jeff/Smith` |
| Log paths | `~/Smith/.hermes-profile/logs/` | `~/Smith/logs/` |
| Skills | split across `.hermes-profile/skills/` + `~/Smith/skills/` | all 73 in `~/Smith/skills/` |
| `.gitignore` | `.hermes-profile/` | added: profile runtime (cron, sessions, config, state.db, etc.) |
| Backup tarball | `~/.hermes/.hermes-profile-backup-20260624-*.tar.gz` | same, still available |

## If asked to do this for a different profile

Use the runbook as a template. Most steps transfer directly. Differences for a non-smith profile:
- Update the launchd label (`ai.hermes.gateway-<name>`)
- Use that profile's `WorkingDirectory`
- Back up to a profile-specific path
- The other agents in the workspace may or may not be affected; check `openclaw agents list` for the binding map

## If asked to undo / revert

The rollback section of the runbook has the exact steps. Key commands:
```bash
launchctl stop ai.hermes.gateway-smith
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist
mkdir -p ~/.hermes/profiles
tar -xzf ~/.hermes/.hermes-profile-backup-*.tar.gz -C ~/.hermes/profiles
cp ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist.bak-* ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist
launchctl load ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist
launchctl start ai.hermes.gateway-smith
```

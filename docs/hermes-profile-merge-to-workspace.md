# Runbook: Merge Hermes `smith` Profile into `~/Smith`

**Goal:** make `~/Smith/` the single home for everything Smith — the user workspace, the agent persona files, *and* the Hermes runtime profile. No more two-place navigation.

**Owner:** Jeff (execute on Antigravity)
**Risk tier:** medium-high. Runtime state is moved mid-stack. Expect one session restart.
**Estimated time:** 15–25 min if everything goes right. 60+ if something fights back.

---

## 0. TL;DR

| step | what | downtime |
|---|---|---|
| 1 | preflight + backup | 0 |
| 2 | stop the gateway cleanly | ~5s |
| 3 | move profile contents into `~/Smith/.hermes-profile/` (note: subdir, not top-level — see "design note" below) | 0 |
| 4 | relaunch gateway pointing at new `HERMES_HOME` | ~10s |
| 5 | verify | 0 |
| 6 | cleanup old profile dir | 0 |

**Design note — subdir vs top-level merge:**
- Top-level merge (move every file/dir into `~/Smith/` next to `SOUL.md`, `AGENTS.md`, etc.) creates collision risk: `~/Smith/agent/`, `~/Smith/memory/`, `~/Smith/skills/`, `~/Smith/cron/` would overlap with workspace folders.
- **Subdir merge** (`~/Smith/.hermes-profile/`) keeps the hermes runtime state in a clearly separated, dot-prefixed location, but inside the workspace. No collisions. Easier to gitignore the runtime state if you want.
- This runbook uses subdir merge. If you want top-level, the move commands are the same — just drop the `.hermes-profile/` layer.

---

## 1. Preflight (do all of these BEFORE moving anything)

### 1.1 Confirm gateway is up and reachable

```bash
launchctl list | grep ai.hermes.gateway-smith
# expect: PID  <some-number>  0  ai.hermes.gateway-smith

curl -s http://127.0.0.1:18789/health 2>/dev/null | head -50
# expect: "reachable" or similar
```

If the gateway is *not* running, skip step 2.1 (no need to stop what's not up). All other steps still apply.

### 1.2 Check free disk space

```bash
du -sh ~/.hermes/profiles/smith
df -h ~ | tail -1
```

Need at least 2× the profile size free (for backup + work). Profile is usually 200MB–2GB. If you have <5GB free, free some up first.

### 1.3 Back up the profile to a dated archive (non-negotiable)

```bash
TS=$(date +%Y%m%d-%H%M%S)
BACKUP=~/Smith/.hermes-profile-backup-$TS.tar.gz

# Verify the source first
ls -la ~/.hermes/profiles/smith/ | head -20

# Create archive (preserves permissions, hidden files, follows symlinks)
tar -czf "$BACKUP" -C ~/.hermes/profiles smith

# Verify archive isn't empty/corrupt
tar -tzf "$BACKUP" | wc -l
# expect: a number in the hundreds (or thousands if `sessions/` is big)

# Move archive OUTSIDE the workspace so it isn't part of the move
mv "$BACKUP" ~/.hermes/
ls -lh ~/.hermes/.hermes-profile-backup-*.tar.gz
```

**Do not skip this.** If something goes wrong, this tarball is your rollback.

### 1.4 Snapshot `openclaw.json` (separately)

The openclaw config lives at `~/.openclaw/openclaw.json` and references `~/Smith` as the agent workspace. We don't need to change it for the merge, but snapshot anyway:

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-$(date +%Y%m%d)
```

### 1.5 Inspect what will move

```bash
du -sh ~/.hermes/profiles/smith/* | sort -h
# Identify anything unusually large (sessions DB? models cache? logs?)
```

Notable items to expect:
- `logs/` — runtime critical, must move
- `sessions/` — runtime critical, must move (DB-locked while gateway is up)
- `skills/` — 67 skills, the bulk of the dir size
- `memories/`, `cron/`, `state/`, `cache/` — runtime
- `config.yaml`, `.env`, `auth.json`, `profile.yaml` — must move
- `models_dev_cache.json` (2.3MB) — cache, move is fine
- `gateway.pid`, `gateway.lock` — DO NOT move these (they're tied to the running PID); will be recreated on next start

### 1.6 Read the current launchd plist

```bash
cat ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist
```

Note especially:
- `HERMES_HOME` env var
- `WorkingDirectory`
- `StandardOutPath` / `StandardErrorPath` (log paths)

You will change all of these.

---

## 2. Stop the gateway cleanly

**Do NOT `kill -9` or `launchctl kill`.** Use the supervised path so launchd sequences stop+start correctly. (Lesson documented: `~/.hermes/profiles/smith/.learnings/`.)

```bash
# Preferred: use the hermes CLI
hermes gateway restart
# This will stop, then start. We want ONLY stop here, so:
# (if restart fires before we move, just stop again)

# Or stop only:
launchctl stop ai.hermes.gateway-smith
```

### 2.1 Verify it actually stopped

```bash
sleep 2
launchctl list | grep ai.hermes.gateway-smith
# expect: "-" in PID column, exit code "1" or non-zero (Stopped)

pgrep -fl "hermes_cli.main.*smith"
# expect: no output

# Confirm log went quiet
tail -3 ~/.hermes/profiles/smith/logs/gateway.log
# expect: last line timestamped BEFORE your stop command, no new lines
```

### 2.2 Remove stale PID/lock files

```bash
rm -f ~/.hermes/profiles/smith/gateway.pid
rm -f ~/.hermes/profiles/smith/gateway.lock
```

(If the gateway is truly stopped, these are stale and safe to remove. The new instance will recreate them.)

---

## 3. Move the profile

### 3.1 Create the new location

```bash
mkdir -p ~/Smith/.hermes-profile
```

### 3.2 Move everything (use rsync for safety, then delete source)

**Option A — rsync + rm (recommended, atomic-ish, can resume if interrupted):**

```bash
rsync -aAX --info=progress2 ~/.hermes/profiles/smith/ ~/Smith/.hermes-profile/
# ↑ trailing slash on source matters (copies contents, not dir itself)

# Verify the copy
diff -rq ~/.hermes/profiles/smith/ ~/Smith/.hermes-profile/ | head -20
# expect: no output (or only symlink-related noise — investigate any real diffs)

# Now delete the source
rm -rf ~/.hermes/profiles/smith
```

**Option B — plain mv (faster, less safe, no resume):**

```bash
mv ~/.hermes/profiles/smith ~/Smith/.hermes-profile
```

**If `mv` is interrupted, do NOT retry blindly.** Check the state of both halves first.

### 3.3 Re-verify the move

```bash
ls -la ~/Smith/.hermes-profile/ | head -20
# expect: config.yaml, .env, profile.yaml, skills/, logs/, sessions/, etc.

# Confirm old path is gone
ls ~/.hermes/profiles/ 2>&1
# expect: only "default" or whatever other profiles exist; "smith" is GONE
```

---

## 4. Update the launchd plist

### 4.1 Edit the plist

```bash
PLIST=~/Library/LaunchAgents/ai.hermes.gateway-smith.plist
# back it up first
cp "$PLIST" "$PLIST.bak-$(date +%Y%m%d)"
```

Change these three keys:

| key | old value | new value |
|---|---|---|
| `HERMES_HOME` | `/Users/Jeff/.hermes/profiles/smith` | `/Users/Jeff/Smith/.hermes-profile` |
| `WorkingDirectory` | `/Users/Jeff/.hermes/profiles/smith` | `/Users/Jeff/Smith/.hermes-profile` |
| `StandardOutPath` | `/Users/Jeff/.hermes/profiles/smith/logs/gateway.log` | `/Users/Jeff/Smith/.hermes-profile/logs/gateway.log` |
| `StandardErrorPath` | `/Users/Jeff/.hermes/profiles/smith/logs/gateway.error.log` | `/Users/Jeff/Smith/.hermes-profile/logs/gateway.error.log` |

Edit with `plutil` (preserves formatting) or your editor:

```bash
plutil -replace EnvironmentVariables.HERMES_HOME -string "/Users/Jeff/Smith/.hermes-profile" "$PLIST"
plutil -replace WorkingDirectory -string "/Users/Jeff/Smith/.hermes-profile" "$PLIST"
plutil -replace StandardOutPath -string "/Users/Jeff/Smith/.hermes-profile/logs/gateway.log" "$PLIST"
plutil -replace StandardErrorPath -string "/Users/Jeff/Smith/.hermes-profile/logs/gateway.error.log" "$PLIST"

# Validate
plutil -lint "$PLIST"
# expect: OK
```

### 4.2 Reload the plist

```bash
# Unload (will fail if not loaded — that's fine)
launchctl unload "$PLIST" 2>&1 | head -5

# Load with the new path
launchctl load "$PLIST"
```

### 4.3 Start the gateway

```bash
launchctl start ai.hermes.gateway-smith
# OR let load + RunAtLoad fire it
```

---

## 5. Verify

### 5.1 Process is up

```bash
sleep 5
launchctl list | grep ai.hermes.gateway-smith
# expect: a PID, exit code 0

pgrep -fl "hermes_cli.main.*smith"
# expect: a PID with the full command line
```

### 5.2 Gateway log shows clean startup at the new path

```bash
tail -30 ~/Smith/.hermes-profile/logs/gateway.log
# expect:
#   - "telegram connected"
#   - "Gateway running with N platform(s)"
#   - no traceback, no "config not found" errors
```

### 5.3 Verify the OLD path is truly gone

```bash
ls ~/.hermes/profiles/ 2>&1
# expect: no "smith" entry

# Check the new path is being written to
ls -la ~/Smith/.hermes-profile/logs/
# expect: gateway.log + gateway.error.log with FRESH mtimes (within the last minute)
```

### 5.4 Smoke-test from a client channel

Send yourself a message on **telegram** (smith's primary channel). The bot should respond. Same for **discord** and **line** if you use them.

If the bot doesn't respond within 30s, check `~/Smith/.hermes-profile/logs/gateway.error.log` first.

### 5.5 Confirm session continuity (optional but recommended)

Pick up a session that was active before the move (e.g. this Telegram DM). It should still load history. If session DB read fails:

```bash
ls -la ~/Smith/.hermes-profile/sessions/
# Sessions should be present. If DB lock errors, restart the gateway one more time.
```

---

## 6. Cleanup

### 6.1 Decide on the symlink trick (optional)

If you want `~/.hermes/profiles/smith` to *resolve* to the new location, for any tooling that still uses the old path:

```bash
ln -s ~/Smith/.hermes-profile ~/.hermes/profiles/smith
# Now the old path works, but everything is physically in ~/Smith
```

Skip this if you're confident nothing references the old path.

### 6.2 Keep the backup tarball for at least 7 days

```bash
ls -lh ~/.hermes/.hermes-profile-backup-*.tar.gz
```

After a week of clean operation:

```bash
# ONLY after you've confirmed everything works
rm ~/.hermes/.hermes-profile-backup-*.tar.gz
```

### 6.3 Open `config.yaml` and consider updating any hardcoded paths

```bash
grep -nE "~?/.hermes/profiles/smith" ~/Smith/.hermes-profile/config.yaml
# Anything that hardcodes the old path? Update to ~/Smith/.hermes-profile
# (Most paths are relative to HERMES_HOME and won't need touching.)
```

---

## 7. Rollback (if anything is broken)

```bash
# 1. Stop the gateway
launchctl stop ai.hermes.gateway-smith
launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist

# 2. Restore from the backup
mkdir -p ~/.hermes/profiles
tar -xzf ~/.hermes/.hermes-profile-backup-*.tar.gz -C ~/.hermes/profiles
# ^ this puts 'smith/' back under ~/.hermes/profiles/

# 3. Restore the original plist
cp ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist.bak-* ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist

# 4. Reload and start
launchctl load ~/Library/LaunchAgents/ai.hermes.gateway-smith.plist
launchctl start ai.hermes.gateway-smith
```

---

## 8. Pitfalls (things that will bite you if you don't read this)

1. **Don't `kill -9` the gateway.** Use `launchctl stop` or `hermes gateway restart`. The launchd label points at the PID; killing without the supervisor's involvement leaves the label dangling and the next start fails with "Discord bot token already in use" (this exact error has happened on this machine — see `gateway.error.log` from earlier today).

2. **Don't forget the `StandardOutPath` and `StandardErrorPath` in the plist.** If the logs path doesn't exist, launchd won't start the service and you'll get cryptic errors.

3. **Don't skip the backup tarball.** This is the kind of operation that, on a bad day, leaves the gateway wedged. The tarball is your safety net.

4. **The session DB is locked while the gateway is up.** If you try to move `sessions/` without stopping the gateway first, you get partial / corrupt files. Always stop first, verify stopped (step 2.1), then move.

5. **`HERMES_HOME` and `WorkingDirectory` must change together.** If only one is updated, the gateway either can't find config or can't write logs.

6. **There may be a second `HERMES_HOME` reference somewhere.** Grep the codebase or your shell rc if the env var persists across reboots. It's typically only in the plist, but worth checking.

7. **Discord bot token conflict** (recurring on this machine, see `~/.hermes/profiles/smith/logs/gateway.error.log` from earlier today): if you see `Discord bot token already in use (PID XXXX)`, there is a stale process holding the token. `pgrep -fl discord` to find it, then `kill -TERM <PID>` (not `-9`). Wait 5s. Retry launchctl start.

8. **The MCP `qmd` server will fail 3 startup attempts every time the gateway boots.** This is a known issue (`unhandled errors in a TaskGroup (1 sub-exception)` in `mcp-stderr.log`). Not caused by this move, not blocking, will happen regardless. Don't waste time on it.

9. **If you move the `logs/` directory while the gateway is still running**, the gateway holds open file descriptors and keeps writing to the *old* path (which no longer exists, so writes fail silently or to deleted inodes). Stop first.

10. **The `agent/` subdir is the agent-state dir, separate from `~/Smith/agent/`.** Don't conflate them when reading the file listing — the path is `~/Smith/.hermes-profile/agent/` after the move, not `~/Smith/agent/`.

---

## 9. Aftermath: what "one place" means going forward

After the merge:
- `~/Smith/` is your one source of truth
- `~/Smith/.hermes-profile/` is the hermes runtime state (mostly hidden, mostly internal)
- `~/Smith/agent/`, `~/Smith/memory/`, `~/Smith/Agents/` are *your* workspace, not hermes state
- The two layers are clearly separated by the dot-prefix
- A single `cd ~/Smith` gets you to everything
- The `.gitignore` should now exclude `.hermes-profile/` if you don't want runtime state in git (your call)

If at any point you want the hermes state *truly* top-level (no subdir), you can do a second pass: move `~/Smith/.hermes-profile/*` up one level. But the subdir is the safer intermediate state and is what this runbook produces.

---

## 10. Done checklist

- [ ] backup tarball exists at `~/.hermes/.hermes-profile-backup-*.tar.gz` and is non-empty
- [ ] gateway was stopped via `launchctl stop` (not `-9`)
- [ ] `~/.hermes/profiles/smith/` is GONE
- [ ] `~/Smith/.hermes-profile/` contains config.yaml, .env, skills/, sessions/, logs/, etc.
- [ ] launchd plist updated and `plutil -lint` clean
- [ ] gateway running, telegram/discord responsive
- [ ] fresh log lines appearing at the new path
- [ ] session history still loadable
- [ ] `~/.hermes/profiles/` shows no `smith` entry
- [ ] old-path smoke test: nothing still references `/Users/Jeff/.hermes/profiles/smith`

**If all 10 boxes ticked: you're done. Don't forget the samantha bind.**

---
name: node-abi-mismatch-debugging
description: Diagnose and fix NODE_MODULE_VERSION mismatches when a Node CLI works in one launch context but crashes in another (background job, cron, Apollo) with "compiled against a different Node.js version using NODE_MODULE_VERSION 137 / requires 147". Covers the two-Node PATH-drift root cause, native-module rebuild at the correct install path, launcher pinning, and the separate session-duration-cap trap. Applies to any tool bundling better-sqlite3 / sqlite-vec / node-llama-cpp / GGUF embeddings.
---

# Node Native-Module ABI Mismatch Debugging

## Symptom
A Node CLI works in your interactive shell but crashes in another launch context
(background job, cron, Apollo) with:
```
Error: The module '.../better_sqlite3/build/Release/better_sqlite3.node'
was compiled against a different Node.js version using NODE_MODULE_VERSION 137.
This version of Node.js requires NODE_MODULE_VERSION 147.
```

## Root cause: two Node installs + PATH drift (NOT a rebuild problem, usually)
Native modules (better-sqlite3, sqlite-vec, node-llama-cpp) are compiled for ONE Node
ABI. If a launch context resolves `node` to a different version, the module won't load.
- `/usr/local/bin/node` → v24, ABI **137** (the version modules were built for)
- `/opt/homebrew/bin/node` → v26, ABI **147** (the troublemaker a background/cron context may pick up via PATH)

The interactive shell may use v24; a background terminal or Apollo may resolve homebrew v26.

## Debug path
1. **Trace which Node actually runs.** Wrap the CLI entry with a require hook:
   ```js
   // /tmp/hook.js
   console.error(`PID=$$ EXEC=${process.execPath} VER=${process.version} ABI=${process.versions.modules}`);
   ```
   Run: `NODE_OPTIONS="--require /tmp/hook.js" <cli> status`
   Then re-run with a HOSTILE PATH to expose drift:
   `export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH`
   If the CLI child process shows ABI 147 while the module is 137 → confirmed drift.

2. **Rebuild native modules against the CORRECT node at the CORRECT install path.**
   Find where the tool actually loads from (e.g. `~/.local/lib/node_modules/<pkg>`, NOT the
   homebrew prefix `/opt/homebrew/lib/node_modules/<pkg>` — that's a DIFFERENT install):
   ```bash
   cd ~/.local/lib/node_modules/<pkg>
   /usr/local/bin/npm rebuild better-sqlite3 sqlite-vec
   /usr/local/bin/node -e "require('./node_modules/better-sqlite3');require('./node_modules/sqlite-vec')"
   # prints OK under v24.15.0 abi 137
   ```

3. **Pin the launcher** so the CLI child ALWAYS spawns the absolute pinned node, not a bare
   `node` string PATH can hijack. Patch the launcher's `spawn(runner, ...)` to use
   `const nodeBin = existsSync(PINNED_NODE) ? PINNED_NODE : "node";` for the node runner.

4. **Beware a SEPARATE session-duration cap.** After the module loads, a long job may still
   abort with "Session expired" and report 0 chunks if `maxDuration` (e.g. `30*60*1000`) is
   shorter than a full run. Raise it for big jobs (e.g. `6*60*60*1000`).

## Pitfalls
- **Don't conclude "it works" from `status`/`doctor` alone.** They may not load the native
  module the same way `embed` does. A status pass hides an embed crash.
- **Rebuilding at the wrong prefix does nothing.** Verify the install path the tool resolves.
- **macOS has no `timeout` command** — use `terminal(background=true)` for long embed jobs;
  `timeout ... cmd` fails with "command not found".
- The embed progress bar writes to a TTY only; when piped/redirected it's silent. Watch
  vector count via `qmd status` (Vectors: N), not the log file.

## Verification
Run the CLI under a hostile homebrew-first PATH. The trace should show the CLI child
re-execing under the pinned v24/ABI137 node and loading clean. For embed, confirm the vector
count (`qmd status`) climbs past the point where it previously aborted.

# qmd Embed Fix — COMPLETED

Two independent bugs blocked `qmd embed`. Both fixed.

## Bug 1: Native module ABI mismatch (the original symptom)
`qmd embed` died with:
> The module '.../better_sqlite3/build/Release/better_sqlite3.node' was compiled against
> a different Node.js version using NODE_MODULE_VERSION 137. This version requires 147.

**Root cause:** two Node installs, and qmd picked runtime from `env node` PATH.
- `/usr/local/bin/node` → v24, ABI **137**  ← "the one we use" (qmd's native modules built for this)
- `/opt/homebrew/bin/node` → v26, ABI **147** ← homebrew, the troublemaker

In Jeff's shell `node`=v24 → embed worked. In other launch contexts (Apollo background,
cron) `node` resolved to homebrew v26 → the 137-built native module exploded. `status`/
`doctor` looked fine because they don't load the module the same way `embed` does. The
original task note had the mismatch *direction* backwards (it's 137 module vs 147 runtime).

**Fix:** rebuilt both native modules against v24 at the CORRECT path
(`~/.local/lib/node_modules/@tobilu/qmd`, NOT the homebrew prefix the steps pointed at):
```bash
cd /Users/Jeff/.local/lib/node_modules/@tobilu/qmd
/usr/local/bin/npm rebuild better-sqlite3 sqlite-vec
```
Then pinned `bin/qmd` so the CLI child always spawns via absolute `/usr/local/bin/node`
(not a bare `node` string PATH can hijack). Now `qmd <anything>` runs under v24 regardless
of which PATH/context launches it.

## Bug 2: 30-minute session cap aborts long runs (the real blocker to completion)
After Bug 1, the real `qmd embed` still reported **"Embedded 0 chunks ... in 30m 8s"** with
22,241 "session expired" failures. The embed session (`dist/store.js` generateEmbeddings)
had `maxDuration: 30 * 60 * 1000` (30 min). A full run on ~22k pending chunks (32/batch)
takes ~85 min, so the cap fired mid-first-batch and rolled back the partial batch → 0 recorded.

**Fix:** raised the cap to 6h in `dist/store.js`:
```js
}, { maxDuration: 6 * 60 * 60 * 1000, name: 'generateEmbeddings' });
```

**Verified:** post-fix run embeds at ~256 vectors/min, vectors climbing 22,860 → 26,092+
with no abort. Pending count heads to 0.

## Notes
- qmd package: `~/.local/lib/node_modules/@tobilu/qmd` (symlink from `~/.local/bin/qmd`).
  Homebrew prefix `/opt/homebrew/lib/node_modules/@tobilu/qmd` is a DIFFERENT install;
  rebuilding there does nothing for the real one.
- Index: `~/.cache/qmd/index.sqlite` (351 MB). 359 docs pending at start of fix session;
  split across `embeddinggemma:legacy` (49 docs/12,672 chunks) and current Q8 model
  (61 docs/10,188 chunks) by fingerprint.
- Models are local GGUF (embeddinggemma-300M-Q8_0.gguf) — no network needed.
- Darwin Metal residency mitigation active: `GGML_METAL_NO_RESIDENCY=1` set by launcher on
  macOS to avoid the ggml-org/llama.cpp#22593 exit assert. Don't "fix" that away.
- `timeout` command does NOT exist on macOS — use terminal(background=true) for long jobs.
- Don't trust `process.execPath` inside qmd to be the node you expect; trace it.
- The progress bar writes to a TTY only; when piped/redirected it's silent. Watch vectors
  via `qmd status` (Vectors: N) or the DB WAL size, not the log.

---
name: macos-system-diagnostics
description: Investigate macOS system resource usage — RAM/memory, top processes, memory pressure. Use when Jeff asks "what's using RAM", "why is my Mac slow", "free up memory", or you need the biggest memory consumer before recommending a cleanup. Covers the Apple-Silicon vm_stat page-size gotcha and the reliable ps-RSS method (Jeff's Mac is Apple Silicon, 16 GB).
---

# macOS System Diagnostics (RAM / Memory)

When Jeff asks what's eating RAM, give a real answer — not a guessed one. macOS `vm_stat`
is easy to misread (see Gotcha). The reliable path is `ps -o rss` for per-process numbers,
plus `vm_stat`/`memory_pressure` for system totals done with the CORRECT page size.

## Method
1. **Per-process RAM (most trustworthy):** `ps -o rss,comm -ax` reports resident set in KB.
   Sum by command to find the real top consumer (a browser like Chrome shows as ~17
   separate helper processes — never report them individually):
   ```bash
   ps -o rss,comm -ax | awk '{rss[$2]+=$1} END {for (c in rss) printf "%8.0f MB  %s\n", rss[c]/1024, c}' | sort -rn | head -8
   ```
   RSS is the honest "what's in RAM right now" number. Use it for the ranking.

2. **System totals (vm_stat) — DO IT RIGHT:** Apple Silicon page size is **16384 bytes**
   (NOT 4096). Convert pages→GB with factor `16384/1024/1024/1024`. A wrong factor produces
   absurd output (e.g. "865 GB active" on a 16 GB box). See `references/ram-one-liners.md`.

3. **Memory pressure:** `memory_pressure` → "System-wide memory free percentage: N%".
   >50% free = healthy; don't over-warn unless pressure is genuinely low.

## What usually eats RAM on Jeff's Mac
- **Chrome** — consistently the top consumer (~2.5 GB across ~17 helper processes). It
  reloads on its own; clearing it is the single biggest reclaim. Jeff has a recurring
  pattern of clearing Chrome in the morning to free RAM, then switching to Brave.
- Dev/AI stack: Claude (Electron ~1.2 GB), VS Code (~1.1 GB), qmd embed worker node
  (~1 GB while embedding locally), Hermes python (~250 MB).
- **Brave** is light (~150–400 MB) — good default browser swap-in.

## Cleanup playbook (when Jeff wants RAM back)
- Biggest reclaimable chunk is usually Chrome. Clean quit preserves tabs for next launch:
  `osascript -e 'tell application "Google Chrome" to quit'`
- Verify reclaimed with the ps-RSS one-liner above.
- Don't kill the qmd embed worker mid-run unless told — it frees ~1 GB when the job ends on
  its own.

## Pitfalls
- **vm_stat page size is 16384 on Apple Silicon.** Using 4096 (or forgetting /1024³) yields
  gigabyte-scale nonsense. Always use the factor in `references/ram-one-liners.md`.
- `vm_stat` "Free" reads near-zero even when healthy (macOS prefers caching). Trust
  `memory_pressure` % and the ps-RSS totals over raw free pages.
- Don't report the raw ps COMMAND path (e.g. `/Applications/Google`) as the app name —
  aggregate by summing, or Chrome looks like 17 tiny processes instead of one 2.5 GB hog.

## Verification
After a cleanup, re-run the ps-RSS one-liner; the target app should be gone and total used
RAM should drop. Confirm with `memory_pressure` staying >50% free.

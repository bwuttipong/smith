# RAM Diagnostics One-Liners (Jeff's Mac — Apple Silicon, 16 GB)

## Per-process RAM ranking (sum by command, MB)
```bash
ps -o rss,comm -ax | awk '{rss[$2]+=$1} END {for (c in rss) printf "%8.0f MB  %s\n", rss[c]/1024, c}' | sort -rn | head -8
```

## System totals (vm_stat — page size is 16384 bytes, NOT 4096)
```bash
vm_stat | awk '
/^Pages free/ {free=$3+0} /^Pages active/ {active=$3+0}
/^Pages inactive/ {inactive=$3+0} /^Pages wired down/ {wired=$3+0}
/^Pages speculative/ {spec=$3+0} /^Pages occupied by compressor/ {comp=$3+0}
END { g=16384/1024/1024/1024;
  printf "Free:%.2fGB Active:%.2fGB Inactive:%.2fGB Wired:%.2fGB Spec:%.2fGB Compressed:%.2fGB\n",
    free*g, active*g, inactive*g, wired*g, spec*g, comp*g }'
```

## Memory pressure
```bash
memory_pressure 2>/dev/null | grep -iE "free percentage|pressure"
```

## Clean-quit Chrome (tabs preserved for next launch)
```bash
osascript -e 'tell application "Google Chrome" to quit'
```

## Notes
- vm_stat "Free" reads near-zero even when healthy — trust `memory_pressure` % and ps-RSS
  totals, not the raw free-page count.
- `sysctl -n hw.memsize` gives total RAM in bytes (divide by 1024³ for GB).
- macOS has NO `timeout` command — use `terminal(background=true)` for long jobs, not
  `timeout ... cmd` (it fails with "command not found").

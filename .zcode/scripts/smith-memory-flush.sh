#!/usr/bin/env bash
# Stop-hook: stamps a session boundary in today's Smith memory file.
# Idempotent — collapses repeated Stop events within the same minute.

set -u

TZ_ICT="Asia/Bangkok"
MEM_DIR="${HOME}/Smith/memory"
DATE_STAMP="$(TZ="$TZ_ICT" date +%Y-%m-%d)"
TIME_STAMP="$(TZ="$TZ_ICT" date +%H:%M)"
MEM_FILE="${MEM_DIR}/${DATE_STAMP}.md"

mkdir -p "$MEM_DIR" || exit 0

# Initialize file with date heading if missing.
if [ ! -f "$MEM_FILE" ]; then
  printf '# %s\n' "$DATE_STAMP" > "$MEM_FILE"
fi

MARKER="_session ended ${TIME_STAMP} ICT_"

# If the most recent boundary marker is for the same minute, skip.
LAST_MARKER="$(grep -E '^_session ended [0-9]{2}:[0-9]{2} ICT_$' "$MEM_FILE" | tail -n 1 || true)"
if [ "$LAST_MARKER" = "$MARKER" ]; then
  exit 0
fi

# Ensure separation from any preceding content.
LAST_LINE="$(tail -n 1 "$MEM_FILE" 2>/dev/null || true)"
if [ -n "$LAST_LINE" ]; then
  printf '\n' >> "$MEM_FILE"
fi

printf '%s\n' "$MARKER" >> "$MEM_FILE"
exit 0

#!/bin/bash
# evening-shutdown-auto.sh — Non-interactive evening shutdown for cron
# Run this automatically at 6-8 PM. It does everything the interactive version does,
# but reads intentions from a pre-written intentions file or skips gracefully.

WORKSPACE="/Users/Jeff/.openclaw/workspaces/main"
MEMORY_DIR="$WORKSPACE/memory"
TODAY=$(date +"%Y-%m-%d")
TOMORROW_DATE=$(date -v+1d +"%Y-%m-%d")
TOMORROW_DISPLAY=$(date -v+1d +"%A, %B %d")
TODAY_DISPLAY=$(date +"%A, %B %d")
TIME_NOW=$(TZ="Asia/Bangkok" date +"%I:%M %p")

OUTPUT="🌙 Evening shutdown, Jeff — $TODAY_DISPLAY
⏰ Time: $TIME_NOW (Bangkok)

"

# ── TOMORROW'S CALENDAR ─────────────────────────────────
OUTPUT+="📅 TOMORROW ($TOMORROW_DISPLAY)
----------------------------------------"

CALENDAR_FOUND=0
if command -v gog &>/dev/null; then
  EVENTS=$(gog calendar tomorrow 2>/dev/null | head -15)
  if [ -n "$EVENTS" ]; then
    OUTPUT+="$EVENTS"$'\n'
    CALENDAR_FOUND=1
  fi
fi

if [ "$CALENDAR_FOUND" -eq 0 ] && command -v himalaya &>/dev/null; then
  EVENTS=$(himalaya calendar list 2>/dev/null | grep -A5 "$TOMORROW_DATE" | head -15)
  if [ -n "$EVENTS" ]; then
    OUTPUT+="$EVENTS"$'\n'
    CALENDAR_FOUND=1
  fi
fi

if [ "$CALENDAR_FOUND" -eq 0 ]; then
  VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault"
  for ext in md txt; do
    TOMORROW_NOTE="$VAULT_DIR/Daily/$TOMORROW_DATE.$ext"
    if [ -f "$TOMORROW_NOTE" ]; then
      OUTPUT+="(from Obsidian daily note)"$'\n'
      head -10 "$TOMORROW_NOTE" 2>/dev/null | sed 's/^/   /' | while IFS= read -r line; do
        OUTPUT+="$line"$'\n'
      done
      CALENDAR_FOUND=1
      break
    fi
  done
fi

if [ "$CALENDAR_FOUND" -eq 0 ]; then
  OUTPUT+="(no calendar events found — clean slate tomorrow!)"$'\n'
fi

# ── TODAY'S TASKS ─────────────────────────────────────
OUTPUT+=$'\n'"✅ TODAY — Task Summary"$'\n'"----------------------------------------"$'\n'
TODOIST_BIN="$HOME/.npm-global/bin/todoist"
if [ -f "$TODOIST_BIN" ] || command -v todoist &>/dev/null; then
  TODOIST_BIN="${TODOIST_BIN:-todoist}"
  TODAY_OUTPUT=$("$TODOIST_BIN" today 2>/dev/null || echo "")
  OUTPUT+="$TODAY_OUTPUT"$'\n'
  TOTAL=$(echo "$TODAY_OUTPUT" | grep -c "^[0-9]" || echo "0")
  OUTPUT+="→ $TOTAL tasks listed for today"$'\n'
else
  OUTPUT+="(Todoist not available)"$'\n'
fi

# ── SESSION LOG ENTRY ─────────────────────────────────
OUTPUT+=$'\n'"📓 DAILY LOG"$'\n'"----------------------------------------"$'\n'
TODAY_MEM="$MEMORY_DIR/$TODAY.md"
INTENTION_FILE="$MEMORY_DIR/.tomorrow-intentions.txt"
TOMORROW_MEM="$MEMORY_DIR/$TOMORROW_DATE.md"

if [ -f "$TODAY_MEM" ]; then
  if grep -q "🌙 EVENING SHUTDOWN" "$TODAY_MEM" 2>/dev/null; then
    OUTPUT+="(already logged today)"$'\n'
  else
    # Read auto-reflection from session log if available
    AUTO_LOG=""
    if [ -f "$MEMORY_DIR/.last-session-log.txt" ]; then
      AUTO_LOG=$(cat "$MEMORY_DIR/.last-session-log.txt" 2>/dev/null | head -1)
    fi
    if [ -n "$AUTO_LOG" ]; then
      OUTPUT+="Auto-log: $AUTO_LOG"$'\n'
      echo "" >> "$TODAY_MEM"
      echo "## 🌙 Evening Shutdown — $(TZ='Asia/Bangkok' date +'%I:%M %p')" >> "$TODAY_MEM"
      echo "$AUTO_LOG" >> "$TODAY_MEM"
    else
      OUTPUT+="(no session log found — add reflection manually)"$'\n'
    fi
  fi
else
  OUTPUT+="(no memory file for today)"$'\n'
fi

# ── CARRY OVER INCOMPLETE TASKS TO TOMORROW ───────────
if [ -f "$INTENTION_FILE" ]; then
  mkdir -p "$MEMORY_DIR"
  if [ ! -f "$TOMORROW_MEM" ]; then
    echo "# $TOMORROW_DATE" > "$TOMORROW_MEM"
    echo "" >> "$TOMORROW_MEM"
  fi
  echo -e "\n## ⏰ Carried Over from $TODAY" >> "$TOMORROW_MEM"
  cat "$INTENTION_FILE" >> "$TOMORROW_MEM"
  echo "→ $(wc -l < "$INTENTION_FILE") items carried to tomorrow's memory ✓" | sed 's/^/   /'
  rm "$INTENTION_FILE"
fi

# ── TOMORROW'S TOP PRIORITIES (if pre-written) ───────
if [ -f "$INTENTION_FILE" ]; then
  OUTPUT+=$'\n'"🔭 TOMORROW — Top Priorities (from intentions file)"$'\n'"----------------------------------------"$'\n'
  cat "$INTENTION_FILE" | while IFS= read -r line; do
    OUTPUT+="• $line"$'\n'
  done
fi

# ── CLOSING ───────────────────────────────────────────
OUTPUT+=$'\n'"🌙 Good night, Jeff. Tomorrow's a clean slate."$'\n'
OUTPUT+="Shutdown complete — $(TZ='Asia/Bangkok' date +'%I:%M %p')"

echo "$OUTPUT"

# Save to today's memory
if [ -n "$TODAY_MEM" ]; then
  mkdir -p "$(dirname "$TODAY_MEM")"
  echo "## 🌙 Auto Evening Shutdown — $(TZ='Asia/Bangkok' date +'%I:%M %p')" >> "$TODAY_MEM"
  echo "$OUTPUT" >> "$TODAY_MEM"
  echo "" >> "$TODAY_MEM"
fi
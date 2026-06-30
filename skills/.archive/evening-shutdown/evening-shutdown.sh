#!/bin/bash
# evening-shutdown.sh — Jeff's end-of-day shutdown ritual
# Run during evening heartbeats (~6-8 PM Bangkok) or on demand.
# Completes the day: reviews what happened, clears cognitive load, preps tomorrow.

set -e

WORKSPACE="/Users/Jeff/.openclaw/workspaces/main"
TODAY=$(date +"%Y-%m-%d")
TOMORROW_DATE=$(date -v+1d +"%Y-%m-%d")
TOMORROW_DISPLAY=$(date -v+1d +"%A, %B %d")
TODAY_DISPLAY=$(date +"%A, %B %d")
TIME_NOW=$(TZ="Asia/Bangkok" date +"%I:%M %p")

echo "🌙 Evening shutdown, Jeff — $TODAY_DISPLAY"
echo "⏰ Time: $TIME_NOW (Bangkok)"
echo ""

# ── TOMORROW'S CALENDAR ─────────────────────────────────
echo "📅 TOMORROW ($TOMORROW_DISPLAY)"
echo "----------------------------------------"

CALENDAR_FOUND=0

# Try gog calendar first
if command -v gog &>/dev/null; then
  EVENTS=$(gog calendar tomorrow 2>/dev/null | head -15)
  if [ -n "$EVENTS" ]; then
    echo "$EVENTS"
    CALENDAR_FOUND=1
  fi
fi

# Fall back to himalaya
if [ "$CALENDAR_FOUND" -eq 0 ] && command -v himalaya &>/dev/null; then
  EVENTS=$(himalaya calendar list 2>/dev/null | grep -A5 "$TOMORROW_DATE" | head -15)
  if [ -n "$EVENTS" ]; then
    echo "$EVENTS"
    CALENDAR_FOUND=1
  fi
fi

# Fall back to a note if we have Obsidian
if [ "$CALENDAR_FOUND" -eq 0 ]; then
  VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault"
  # Look for tomorrow's daily note
  for ext in md txt; do
    TOMORROW_NOTE="$VAULT_DIR/Daily/$TOMORROW_DATE.$ext"
    if [ -f "$TOMORROW_NOTE" ]; then
      echo "(from Obsidian daily note)"
      head -10 "$TOMORROW_NOTE" 2>/dev/null | sed 's/^/   /'
      CALENDAR_FOUND=1
      break
    fi
  done
fi

if [ "$CALENDAR_FOUND" -eq 0 ]; then
  echo "(no calendar events found — clean slate tomorrow!)"
fi

# ── TODAY'S TASKS ─────────────────────────────────────
echo ""
echo "✅ TODAY — Task Summary"
echo "----------------------------------------"
TODOIST_TOKEN="$TODOIST_API_TOKEN"
if [ -n "$TODOIST_TOKEN" ]; then
  TODAY_OUTPUT=$(curl -s -H "Authorization: Bearer $TODOIST_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.todoist.com/api/v2/tasks?filter=today&limit=20" 2>/dev/null)
  if [ -n "$TODAY_OUTPUT" ]; then
    TOTAL=$(echo "$TODAY_OUTPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(len(d.get('results',[])))" 2>/dev/null || echo "?")
    echo "$TODAY_OUTPUT" | python3 -c "
import sys,json
try:
  data=json.load(sys.stdin)
  tasks=data.get('results',[])
  if not tasks: print('(no tasks for today)')
  for t in tasks:
    pmap={4:'🔴',3:'🟠',2:'🟡',1:'⚪'}
    p=pmap.get(t.get('priority',1),'⚪')
    content=t.get('content','?')
    due=t.get('due',{})
    due_str=f\" ({due.get('string','')})\" if due else ''
    checked='✅ ' if t.get('checked') else ''
    print(f'{p} {checked}{content}{due_str}')
except: print('(parse error)')
" 2>/dev/null
    echo ""
    echo "→ $TOTAL tasks listed for today"
  else
    echo "(Todoist API error)"
  fi
elif command -v todoist &>/dev/null; then
  TODOIST_BIN="${TODOIST_BIN:-todoist}"
  TODAY_OUTPUT=$("$TODOIST_BIN" today 2>/dev/null || echo "")
  TOTAL=$(echo "$TODAY_OUTPUT" | grep -c "^[0-9]" || echo "0")
  echo "$TODAY_OUTPUT" | head -20
  echo ""
  echo "→ $TOTAL tasks listed for today"
else
  echo "(Todoist not available)"
fi

# ── SESSION LOG ENTRY ─────────────────────────────────
echo ""
echo "📓 DAILY LOG"
echo "----------------------------------------"

MEMORY_FILE="$WORKSPACE/memory/$TODAY.md"
if [ -f "$MEMORY_FILE" ]; then
  # Check if we already logged today's close
  if grep -q "🌙 EVENING SHUTDOWN" "$MEMORY_FILE" 2>/dev/null; then
    echo "(already logged today)"
  else
    echo "Type one line — what mattered most today? (Enter to skip)"
    read -r -p "> " LOG_LINE
    if [ -n "$LOG_LINE" ]; then
      echo "" >> "$MEMORY_FILE"
      echo "## 🌙 Evening Shutdown — $(TZ='Asia/Bangkok' date +'%I:%M %p')" >> "$MEMORY_FILE"
      echo "$LOG_LINE" >> "$MEMORY_FILE"
      echo "Logged ✓"
    else
      echo "(skipped)"
    fi
  fi
else
  echo "(no memory file for today — skipping log)"
fi

# ── TOMORROW'S TOP PRIORITIES ─────────────────────────
INTENTION_FILE="$WORKSPACE/memory/.tomorrow-intentions.txt"
echo ""
echo "🔭 TOMORROW — Top Priorities"
echo "----------------------------------------"

# If there's a pre-written intentions file, show it and skip input
if [ -f "$INTENTION_FILE" ] && [ -s "$INTENTION_FILE" ]; then
  echo "(loaded from intentions file)"
  cat "$INTENTION_FILE" | while IFS= read -r line; do
    echo "  • $line"
  done
  echo ""
  echo "( intentions file will be carried to tomorrow's memory ✓ )"
else
  echo "What are your 1-3 must-dos tomorrow? (one per line, empty line to finish)"
  PRIORITIES=""
  while true; do
    read -r -p "> " LINE
    if [ -z "$LINE" ]; then
      break
    fi
    PRIORITIES="${PRIORITIES}• ${LINE}"$'\n'
  done
  if [ -n "$PRIORITIES" ]; then
    echo "$PRIORITIES" | head -3
    # Save to tomorrow's memory note for reference
    TOMORROW_MEM="$WORKSPACE/memory/$TOMORROW_DATE.md"
    mkdir -p "$(dirname "$TOMORROW_MEM")"
    if [ ! -f "$TOMORROW_MEM" ]; then
      echo "# $TOMORROW_DATE" > "$TOMORROW_MEM"
      echo "" >> "$TOMORROW_MEM"
    fi
    echo -e "\n## Top Priorities (from evening shutdown)" >> "$TOMORROW_MEM"
    echo "$PRIORITIES" >> "$TOMORROW_MEM"
    echo "(saved to tomorrow's memory note ✓)"
  else
    echo "(no priorities entered)"
  fi
fi

# ── HEALTH CHECK-IN ───────────────────────────────
echo ""
echo "💧 HEALTH"
echo "----------------------------------------"
echo "Log water cups or sleep? (e.g. '3' for cups, 'sleep'/'wake', or Enter to skip)"
read -r -p "> " HEALTH_INPUT
if [ -n "$HEALTH_INPUT" ]; then
  if [ "$HEALTH_INPUT" = "sleep" ] || [ "$HEALTH_INPUT" = "wake" ]; then
    bash "$WORKSPACE/skills/healthcheck/health.sh" "$HEALTH_INPUT" 2>/dev/null || echo "(health tracking unavailable)"
  elif [ "$HEALTH_INPUT" -eq "$HEALTH_INPUT" ] 2>/dev/null; then
    bash "$WORKSPACE/skills/healthcheck/health.sh" water "$HEALTH_INPUT" 2>/dev/null || echo "(health tracking unavailable)"
  fi
fi

# ── CLOSING ───────────────────────────────────────────
echo ""
echo "🌙 Good night, Jeff. Tomorrow's a clean slate."
echo "Shutdown complete — $(TZ='Asia/Bangkok' date +'%I:%M %p')"
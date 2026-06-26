#!/bin/bash
# morning-briefing.sh — Jeff's daily morning briefing
# Run this during morning heartbeats to give Jeff a consolidated view of his day.

set -e

WORKSPACE="/Users/Jeff/.openclaw/workspaces/main"
SKILLS_DIR="$WORKSPACE/skills"
TODAY=$(date +"%A, %B %d")
TIME_NOW=$(TZ="Asia/Bangkok" date +"%I:%M %p")

echo "🌅 Good morning, Jeff — $TODAY"
echo "⏰ Time: $TIME_NOW (Bangkok)"
echo ""
echo "========================================"

# ── WEATHER ──────────────────────────────────
echo ""
echo "🌤️ WEATHER"
echo "----------------------------------------"

# Try weather skill first, fall back to wttr.in
if [ -f "$SKILLS_DIR/weather/weather.sh" ]; then
  bash "$SKILLS_DIR/weather/weather.sh" Bangkok 2>/dev/null | head -10 || echo "Weather unavailable"
elif command -v curl &>/dev/null; then
  WEATHER=$(curl -s "wttr.in/Bangkok?format=%c+%t,+humidity+%h,+wind+%w" 2>/dev/null || echo "Weather unavailable")
  echo "$WEATHER"
else
  echo "Weather unavailable"
fi

# ── TODOIST ───────────────────────────────────
echo ""
echo "✅ TASKS (Todoist)"
echo "----------------------------------------"
TODOIST_BIN="$HOME/.npm-global/bin/todoist"
if [ -f "$TODOIST_BIN" ]; then
  "$TODOIST_BIN" today 2>/dev/null || echo "(Todoist error)"
else
  echo "(Todoist CLI not found)"
fi

# ── EMAIL (AgentMail) ─────────────────────────
echo ""
echo "📧 INBOX (AgentMail)"
echo "----------------------------------------"
AGENTMAIL_KEY=$(grep -o '"api_key":"[^"]*"' "$WORKSPACE/skills/agentmail/config.json" 2>/dev/null | cut -d'"' -f4)
if [ -n "$AGENTMAIL_KEY" ]; then
  INBOX=$(curl -s -X GET "https://api.agentmail.to/v1/inbox?api_key=$AGENTMAIL_KEY&limit=5" 2>/dev/null)
  if [ -n "$INBOX" ] && echo "$INBOX" | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f'• [{m[\"sender_name\"]}] {m[\"subject\"]}') for m in d.get('messages',[])]" 2>/dev/null; then
    : # printed above
  else
    echo "No new emails"
  fi
else
  echo "(AgentMail not configured)"
fi

# ── NOTES ─────────────────────────────────────
echo ""
echo "📝 OBSIDIAN — Recent Daily Notes"
echo "----------------------------------------"
VAULT_DIR="$HOME/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault"
if [ -d "$VAULT_DIR" ]; then
  # Try Daily Notes subfolder first
  DAILY_DIR="$VAULT_DIR/Daily"
  if [ ! -d "$DAILY_DIR" ]; then
    DAILY_DIR="$VAULT_DIR"
  fi
  LAST_NOTE=$(ls -t "$DAILY_DIR/"*.md 2>/dev/null | head -1)
  if [ -n "$LAST_NOTE" ]; then
    NOTE_NAME=$(basename "$LAST_NOTE")
    echo "📌 Latest: $NOTE_NAME"
    head -8 "$LAST_NOTE" 2>/dev/null | sed 's/^/   /' || echo "(unable to read)"
  else
    echo "No daily notes found"
  fi
else
  echo "(Obsidian vault not found)"
fi

echo ""
echo "========================================"
echo "Ready for the day, Jeff. Let's make it count. 🚀"

# ── STOCKS (if configured) ─────────────────────
echo ""
echo "📈 STOCKS"
echo "----------------------------------------"
STOCKS_BIN="$WORKSPACE/skills/stock-monitor/stocks.sh"
if [ -f "$STOCKS_BIN" ]; then
  bash "$STOCKS_BIN" summary 2>/dev/null | head -10 || echo "(stock data unavailable)"
else
  echo "(stock monitor not configured)"
fi

echo ""
echo "========================================"
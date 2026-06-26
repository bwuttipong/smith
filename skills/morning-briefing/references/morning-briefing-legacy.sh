#!/bin/bash
# morning-briefing.sh — Jeff's daily morning briefing
# Run this during morning heartbeats to give Jeff a consolidated view of his day.

set -e

WORKSPACE="/Users/Jeff/.openclaw/workspaces/main"
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

if [ -f "$WORKSPACE/skills/weather/weather.sh" ]; then
  bash "$WORKSPACE/skills/weather/weather.sh" Bangkok 2>/dev/null | head -10 || echo "Weather unavailable"
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
TODOIST_TOKEN="$TODOIST_API_TOKEN"
if [ -n "$TODOIST_TOKEN" ]; then
  TASKS=$(curl -s -H "Authorization: Bearer $TODOIST_TOKEN" \
    -H "Content-Type: application/json" \
    "https://api.todoist.com/api/v2/tasks?filter=today&limit=10" 2>/dev/null)
  if [ -n "$TASKS" ]; then
    echo "$TASKS" | python3 -c "
import sys,json
try:
  data=json.load(sys.stdin)
  tasks=data.get('results',[])
  if not tasks:
    print('(no tasks for today)')
  for t in tasks:
    pmap={4:'🔴',3:'🟠',2:'🟡',1:'⚪'}
    p=pmap.get(t.get('priority',1),'⚪')
    content=t.get('content','?')
    due=t.get('due',{})
    due_str=' (' + due.get('string','') + ')' if due else ''
    checked='✅ ' if t.get('checked') else ''
    print(p + ' ' + checked + content + due_str)
except:
  print('(parse error)')
" 2>/dev/null || echo "(Todoist parse error)"
  else
    echo "(Todoist API error)"
  fi
elif command -v todoist &>/dev/null; then
  todoist today 2>/dev/null || echo "(Todoist error)"
else
  echo "(Todoist not configured)"
fi

# ── EMAIL (AgentMail) ─────────────────────────
echo ""
echo "📧 INBOX (AgentMail)"
echo "----------------------------------------"
AGENTMAIL_KEY="${AGENTMAIL_API_KEY:-}"
if [ -n "$AGENTMAIL_KEY" ]; then
  INBOX=$(curl -s -X GET "https://api.agentmail.to/v1/inbox?api_key=$AGENTMAIL_KEY&limit=5" 2>/dev/null)
  if [ -n "$INBOX" ] && echo "$INBOX" | python3 -c "import sys,json; d=json.load(sys.stdin); [print('• [' + m['sender_name'] + '] ' + m['subject']) for m in d.get('messages',[])]" 2>/dev/null; then
    :
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

# ── COMMUTE ───────────────────────────────────
echo ""
echo "🚗 COMMUTE"
echo "----------------------------------------"
COMMUTE_CONF="$WORKSPACE/memory/commute.conf"
if [ -f "$COMMUTE_CONF" ]; then
  ORIGIN=$(grep '^origin=' "$COMMUTE_CONF" 2>/dev/null | cut -d= -f2-)
  DEST=$(grep '^destination=' "$COMMUTE_CONF" 2>/dev/null | cut -d= -f2-)
  if [ -n "$ORIGIN" ] && [ -n "$DEST" ]; then
    python3 "$WORKSPACE/skills/openclaw-commute-traffic/scripts/check_traffic.py" \
      --origin "$ORIGIN" --destination "$DEST" 2>/dev/null \
      | python3 "$WORKSPACE/skills/openclaw-commute-traffic/scripts/traffic_summary.py"
  else
    echo "(edit $COMMUTE_CONF to set origin= and destination=)"
  fi
else
  echo "(no commute configured — create memory/commute.conf)"
fi

# ── NEWS ─────────────────────────────────────
echo ""
echo "📰 NEWS — Top Headlines"
echo "----------------------------------------"
NEWS=$(curl -s --max-time 8 "https://feeds.bbci.co.uk/news/world/rss.xml" 2>/dev/null | \
  python3 -c "
import sys, re
xml = sys.stdin.read()
items = re.findall(r'<item>(.*?)</item>', xml, re.DOTALL)
count = 0
for item in items:
    title = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
    if not title: title = re.search(r'<title>(.*?)</title>', item)
    desc = re.search(r'<description><!\[CDATA\[(.*?)\]\]></description>', item)
    if not desc: desc = re.search(r'<description>(.*?)</description>', item)
    if title and count < 6:
        t = title.group(1).strip()
        d = desc.group(1).strip()[:100] if desc else ''
        if t and t != 'BBC News':
            print('• ' + t)
            count += 1
" 2>/dev/null)
if [ -n "$NEWS" ]; then
  echo "$NEWS"
else
  echo "(news unavailable)"
fi

echo ""
echo "========================================"
echo "Ready for the day, Jeff. Let's make it count. 🚀"

# ── STOCKS (if configured) ─────────────────────
STOCKS_BIN="$WORKSPACE/skills/stock-monitor/stocks.sh"
if [ -f "$STOCKS_BIN" ] && [ -s "$WORKSPACE/memory/stocks_config.json" ] 2>/dev/null; then
  echo ""
  echo "📈 STOCKS"
  echo "----------------------------------------"
  bash "$STOCKS_BIN" summary 2>/dev/null | head -10 || echo "(stock data unavailable)"
fi

echo ""
echo "========================================"
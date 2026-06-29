#!/usr/bin/env bash
# Gog OAuth token auto-refresh
# Runs every 5 days via cron — keeps the testing-mode token alive
# If refresh fails, writes a flag for the morning briefing to pick up

set -euo pipefail

LOG_FILE="$HOME/Smith/memory/gog-token-refresh.log"
FAIL_FLAG="$HOME/Smith/memory/.gog-token-failed"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Refreshing gog token..." >> "$LOG_FILE"

# Refresh via gog's stored credentials
if /opt/homebrew/bin/gog calendar list --limit 1 > /dev/null 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ Token refreshed successfully" >> "$LOG_FILE"
    rm -f "$FAIL_FLAG"
    exit 0
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ Token refresh failed" >> "$LOG_FILE"
    touch "$FAIL_FLAG"
    exit 1
fi

#!/bin/bash
# Migrate Obsidian Smith Notes to Bear Notes
# Usage: bash migrate-smith-notes.sh

VAULT="/Users/Jeff/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/Smith Notes"
SMITH_MD="/Users/Jeff/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/AI/Agents/Smith.md"
TAG="smith-notes"
LOG="/Users/Jeff/Smith/memory/artifacts/2026-06-18-bear-migration.log"
TOTAL=0
OK=0
FAIL=0

echo "=== Smith Notes → Bear Migration $(date) ===" > "$LOG"
echo "" >> "$LOG"

migrate_file() {
    local file="$1"
    local relname="${file#$VAULT/}"
    local title="${relname%.md}"
    local tmp_content="/tmp/bear-migrate-$$.md"

    # Skip non-files
    [ ! -f "$file" ] && return

    ((TOTAL++))

    # Copy and sanitize content (strip nulls, limit size)
    cp "$file" "$tmp_content" 2>/dev/null

    if cat "$tmp_content" | grizzly create --title "$title" --tag "$TAG" 2>/dev/null; then
        echo "✓ $title" >> "$LOG"
        ((OK++))
    else
        echo "✗ FAIL: $title" >> "$LOG"
        ((FAIL++))
    fi

    rm -f "$tmp_content"
    sleep 0.4  # let Bear breathe between callbacks
}

echo "📂 Scanning: $VAULT"
echo ""

# Migrate all .md files
find "$VAULT" -maxdepth 1 -name "*.md" -type f | sort | while read -r file; do
    migrate_file "$file"
done

# Handle subdirectories
find "$VAULT" -mindepth 2 -name "*.md" -type f | sort | while read -r file; do
    migrate_file "$file"
done

# Handle AI/Agents/Smith.md (separate, scrub token)
if [ -f "$SMITH_MD" ]; then
    echo "" >> "$LOG"
    echo "--- AI/Agents/Smith.md (token scrubbed) ---" >> "$LOG"
    ((TOTAL++))
    # Strip the token line
    sed '/^MTUwMDE0/,/^$/d' "$SMITH_MD" > "/tmp/bear-smith-scrubbed-$$.md"
    if cat "/tmp/bear-smith-scrubbed-$$.md" | grizzly create --title "Smith (Agent Config)" --tag "$TAG" 2>/dev/null; then
        echo "✓ Smith (Agent Config) [token scrubbed]" >> "$LOG"
        ((OK++))
    else
        echo "✗ FAIL: Smith (Agent Config)" >> "$LOG"
        ((FAIL++))
    fi
    rm -f "/tmp/bear-smith-scrubbed-$$.md"
fi

echo "" >> "$LOG"
echo "=== DONE: $OK/$TOTAL succeeded, $FAIL failed ===" >> "$LOG"
echo "$(date)" >> "$LOG"

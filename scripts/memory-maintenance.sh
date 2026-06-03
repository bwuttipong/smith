#!/bin/bash
# 🌙 Midnight Memory Maintenance
# Runs: qmd update, embed (batched), cleanup, wiki lint
# Logs to: ~/Smith/memory/artifacts/maintenance-$(date +%Y-%m-%d).log

LOG_DIR="$HOME/Smith/memory/artifacts"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/maintenance-$(date +%Y-%m-%d).log"

exec > "$LOG" 2>&1
echo "=== 🌙 Midnight Memory Maintenance ===" 
echo "Started: $(date)"

echo ""
echo "--- Step 1: qmd update ---"
qmd update 2>&1
echo "exit: $?"

echo ""
echo "--- Step 2: qmd embed (memory collection, max-batch-mb 64) ---"
qmd embed -c memory --max-batch-mb 64 2>&1
echo "exit: $?"

echo ""
echo "--- Step 3: qmd embed (workspaces collection, max-batch-mb 64) ---"
qmd embed -c workspaces --max-batch-mb 64 2>&1
echo "exit: $?"

echo ""
echo "--- Step 4: qmd cleanup ---"
qmd cleanup 2>&1
echo "exit: $?"

echo ""
echo "--- Final: qmd status ---"
qmd status 2>&1 | grep -E "Vectors|Pending|Updated|Files indexed|Size"

echo ""
echo "Finished: $(date)"
echo "=== Done ==="

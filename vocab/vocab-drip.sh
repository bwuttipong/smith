#!/bin/bash
# vocab-drip.sh — picks a random word from vocab.json, looks it up, sends to LINE
# No model needed, pure exec.

VOCAB=~/Smith/vocab/vocab.json
DICT=~/.agents/skills/english-thai-dict/dict.py
LINE_TOKEN="${1:?Usage: vocab-drip.sh <line-channel-token>}"
LINE_TARGET="U5d4e71e891666ec6b23cb81375bac82d"

# Pick random word
WORD=$(python3 -c "
import json, random
data = json.load(open('$VOCAB'))
w = random.choice(data)
print(json.dumps(w))
")

EN_WORD=$(echo "$WORD" | python3 -c "import json,sys; print(json.load(sys.stdin)['en'])")
TH_MEANING=$(echo "$WORD" | python3 -c "import json,sys; print(json.load(sys.stdin)['th'])")

# Get dict lookup
DICT_OUTPUT=$(cd ~/.agents/skills/english-thai-dict && python3 dict.py "$EN_WORD" 2>&1)

# Build message
MESSAGE="**$EN_WORD**
$DICT_OUTPUT"

# Send to LINE
curl -s -X POST https://api.line.me/v2/bot/message/push \
  -H "Authorization: Bearer $LINE_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"to\": \"$LINE_TARGET\",
    \"messages\": [{\"type\": \"text\", \"text\": $(echo "$MESSAGE" | python3 -c "import json,sys; print(json.dumps(sys.stdin.read().strip()))")}]
  }" 2>&1

echo ""
echo "Sent: $EN_WORD → $TH_MEANING"

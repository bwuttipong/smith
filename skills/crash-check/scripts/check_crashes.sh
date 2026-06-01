#!/usr/bin/env bash
# crash-check — lightweight accident checker
# Uses TomTom Traffic Incident API.
# Minimal output: only crashes/accidents along a route.
set -uo pipefail

ORIGIN="${1:-Bansuan, Chonburi}"
DEST="${2:-Bang Pakong, Chachoengsao}"
API_KEY="${TOMTOM_API_KEY:-}"
if [ -z "$API_KEY" ]; then
  echo '{"status":"error","message":"TOMTOM_API_KEY not set"}'
  exit 1
fi

# urlescape for geocoding
urlenc() { python3 -c "import urllib.parse; print(urllib.parse.quote('''$1'''))"; }

# --- geocode origin ---
oENC=$(urlenc "$ORIGIN")
geo=$(curl -sf "https://api.tomtom.com/search/2/geocode/${oENC}.json?key=${API_KEY}&limit=1" 2>/dev/null || true)
oLAT=$(echo "$geo" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['position']['lat'])" 2>/dev/null)
oLON=$(echo "$geo" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['position']['lon'])" 2>/dev/null)
if [ -z "$oLAT" ] || [ -z "$oLON" ]; then
  echo '{"status":"error","message":"could not geocode origin"}'
  exit 1
fi

# --- geocode dest ---
dENC=$(urlenc "$DEST")
geo=$(curl -sf "https://api.tomtom.com/search/2/geocode/${dENC}.json?key=${API_KEY}&limit=1" 2>/dev/null || true)
dLAT=$(echo "$geo" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['position']['lat'])" 2>/dev/null)
dLON=$(echo "$geo" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['position']['lon'])" 2>/dev/null)
if [ -z "$dLAT" ] || [ -z "$dLON" ]; then
  echo '{"status":"error","message":"could not geocode destination"}'
  exit 1
fi

# --- bounding box with margin ---
minLAT=$(python3 -c "print(max(-90, min($oLAT,$dLAT)-0.05))")
maxLAT=$(python3 -c "print(min(90, max($oLAT,$dLAT)+0.05))")
minLON=$(python3 -c "print(max(-180, min($oLON,$dLON)-0.05))")
maxLON=$(python3 -c "print(min(180, max($oLON,$dLON)+0.05))")

# --- fetch & filter incidents in one python call ---
python3 -c "
import urllib.request, json, sys

url = 'https://api.tomtom.com/traffic/services/5/incidentDetails?key=${API_KEY}&bbox=${minLAT},${minLON},${maxLAT},${maxLON}&fields={incidents{properties{iconCategory,events{description},from,to,length,delay}}}&language=en-GB'

try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = json.loads(resp.read().decode('utf-8'))
except Exception as e:
    print(json.dumps({'status':'error','message':str(e)}))
    sys.exit(1)

incidents = raw.get('incidents', [])
# accident-related iconCategory values
accident_cats = {1, 2, 7, 8}

hits = []
for inc in incidents:
    props = inc.get('properties', {})
    icon = props.get('iconCategory', 0)
    if icon not in accident_cats:
        continue
    desc = props.get('events', [{}])[0].get('description', '')
    if not desc:
        continue
    typ = {1:'unknown accident', 2:'accident', 7:'congestion', 8:'road closed'}.get(icon, 'incident')
    delay_s = props.get('delay', 0) or 0
    hits.append({
        'type': typ,
        'description': desc,
        'from': props.get('from', ''),
        'to': props.get('to', ''),
        'length_m': props.get('length', 0) or 0,
        'delay_s': delay_s,
        'delay_min': round(delay_s / 60, 1),
    })

print(json.dumps({
    'status': 'ok',
    'origin': '$ORIGIN',
    'destination': '$DEST',
    'accident_count': len(hits),
    'accidents': hits,
}, indent=2, ensure_ascii=False))
" 2>&1

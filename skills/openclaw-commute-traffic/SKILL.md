---
name: commute-traffic
description: Check real-time traffic conditions for a route between two locations using Google Maps. Use when the user asks about traffic, commute time, best time to leave, driving conditions, or road congestion. The user provides origin and destination conversationally — extract them from context.
version: 3.0.0
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🚗", "requires": {"bins": ["python3"], "files": ["~/.config/gmaps/api_key"]}, "primaryEnv": "GOOGLE_MAPS_API_KEY"}}
---

# Commute Traffic Checker (Google Maps)

## Purpose

Query real-time traffic data from Google Maps for any route and provide the user with actionable travel advice. The script handles geocoding (resolving place names to coordinates) and routing (calculating travel time with live traffic) via the Google Geocoding API and Directions API.

API key is read from `~/.config/gmaps/api_key` by default, with fallback to the `GOOGLE_MAPS_API_KEY` environment variable.

## Determining Origin and Destination

The origin and destination are **not static** — you must determine them from what the user tells you. Examples:

- "How's traffic from the office to home?" → You must know (or ask) where their office and home are.
- "Check traffic Basel to Zurich" → origin=Basel, destination=Zurich.
- "Should I leave now?" → Use previously discussed or known origin/destination. If unknown, ask.
- "What's the commute like?" → If you know the user's regular commute, use that. Otherwise, ask.

**Rules:**
1. If both origin and destination are clear from context, proceed immediately.
2. If only one is clear, ask for the missing one.
3. If neither is clear and you have no prior context, ask the user for both.
4. Accept any format: addresses, city names, landmarks, coordinates — the script geocodes automatically.

## Running the Traffic Check

Execute the script with origin and destination as arguments:

```bash
python3 {baseDir}/scripts/check_traffic_google.py --origin "<ORIGIN>" --destination "<DESTINATION>"
```

**Examples:**

```bash
python3 {baseDir}/scripts/check_traffic_google.py --origin "Bansuan, Chonburi" --destination "Wellgrow Industrial Estate"
python3 {baseDir}/scripts/check_traffic_google.py --origin "Ban Suan, Chon Buri" --destination "Bang Pakong, Chachoengsao"
python3 {baseDir}/scripts/check_traffic_google.py --origin "13.3511,100.9765" --destination "13.502,100.9903"
```

## Interpreting the Output

The script returns JSON with one or more route alternatives. For each route:

| Field | Meaning |
|-------|---------|
| `travel_time_min` | Total travel time **with current live traffic** |
| `no_traffic_time_min` | Travel time with zero traffic (free-flow) |
| `traffic_delay_min` | Extra delay caused by current traffic |
| `traffic_delay_pct` | Delay as percentage of free-flow time |
| `congestion` | Derived level: `light`, `moderate`, or `heavy` |
| `distance_km` | Route distance in kilometers |
| `main_roads` | Key roads/instructions along the route |

### Congestion classification:
- **Light**: traffic delay adds less than 20% to free-flow time
- **Moderate**: 20–50% above free-flow
- **Heavy**: more than 50% above free-flow

## Presenting Results to the User

When presenting traffic data, always include:

1. **The fastest route** and its estimated travel time.
2. **Traffic delay** in plain language (e.g., "Currently 8 minutes delay due to traffic on the A2, adding about 15% to the normal drive time").
3. **Comparison of alternatives** if multiple routes are returned.
4. **A recommendation**: whether to leave now or wait, based on congestion level.

Keep it concise and practical. The user wants to know: *"How long will it take and should I go now?"*

## Error Handling

- If the script returns `{"status": "error"}`, relay the error message to the user.
- If no API key is found, tell the user to create `~/.config/gmaps/api_key` with their Google Maps API key, or set the `GOOGLE_MAPS_API_KEY` environment variable.
- If geocoding fails (no coordinates found), the location may be too vague — ask the user to be more specific.
- If the Directions API returns `REQUEST_DENIED`, the API key may have restrictions — ensure Directions API and Geocoding API are enabled in the Google Cloud Console and added to the key's allowed APIs.
- If no routes are returned, suggest trying different location descriptions.

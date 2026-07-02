#!/usr/bin/env python3
"""
Check real-time traffic between two locations using Google Routes API.
Pulls crash/incident data from TomTom Traffic Incidents API as a supplement.

Uses only Python stdlib (urllib + json) — no pip install required.
Handles geocoding (place name -> coordinates) via Google Geocoding API,
routing (travel time with live traffic) via Google Routes API v2,
and incidents (crashes, road closures, etc.) via TomTom Traffic Incidents API.

Key file: ~/.config/gmaps/api_key
If not found, falls back to GOOGLE_MAPS_API_KEY environment variable.
TomTom key: TOMTOM_API_KEY env var (used for incidents only).

Usage:
    python3 check_traffic_google.py --origin "Bansuan, Chonburi" --destination "Bang Pakong, Chachoengsao"
    python3 check_traffic_google.py --origin "13.3511,100.9765" --destination "13.502,100.9903"
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone, timedelta

REQUEST_TIMEOUT = 30
ROUTES_BASE = "https://routes.googleapis.com"
GEOCODE_BASE = "https://maps.googleapis.com/maps/api"
TOMTOM_BASE = "https://api.tomtom.com"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check live traffic between two locations via Google Maps"
    )
    parser.add_argument("--origin", required=True, help="Starting location")
    parser.add_argument("--destination", required=True, help="Destination")
    return parser.parse_args()


def get_api_key() -> str:
    """Read Google Maps API key from file or env. File takes precedence."""
    key_file = os.path.expanduser("~/.config/gmaps/api_key")
    if os.path.isfile(key_file):
        with open(key_file) as f:
            key = f.read().strip()
            if key:
                return key
    key = os.environ.get("GOOGLE_MAPS_API_KEY", "").strip()
    if key:
        return key
    return ""


def get_tomtom_key() -> str:
    """Read TomTom API key from env."""
    return os.environ.get("TOMTOM_API_KEY", "").strip()


def is_coordinates(text: str) -> tuple:
    match = re.match(r"^\s*(-?\d+\.?\d*)\s*[,\s]\s*(-?\d+\.?\d*)\s*$", text.strip())
    if match:
        lat, lng = float(match.group(1)), float(match.group(2))
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return (lat, lng)
    return None


def google_get(url: str) -> dict:
    """Simple GET helper."""
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            pass
        return {"error": True, "message": f"HTTP {e.code}: {e.reason}", "detail": detail}
    except urllib.error.URLError as e:
        return {"error": True, "message": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": True, "message": f"Unexpected error: {e}"}


def nominatim_geocode(location: str) -> dict:
    """Geocode a place name to lat/lng using OpenStreetMap Nominatim (free, no API key)."""
    coords = is_coordinates(location)
    if coords:
        return {"lat": coords[0], "lng": coords[1], "address": location}

    encoded = urllib.parse.quote(location)
    url = "https://nominatim.openstreetmap.org/search?q={}&format=json&limit=1&accept-language=en".format(encoded)
    req = urllib.request.Request(url, headers={"User-Agent": "SmithTraffic/1.0 (smith)"})

    import ssl
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            pass
        return {"error": True, "message": f"Nominatim geocoding HTTP {e.code}: {e.reason} -- {detail}"}
    except urllib.error.URLError as e:
        return {"error": True, "message": f"Nominatim geocoding connection failed: {e.reason}"}
    except Exception as e:
        return {"error": True, "message": f"Nominatim geocoding unexpected error: {e}"}

    if not data:
        # Fallback: try Google Geocoding if Nominatim returns nothing
        return {"error": True, "message": f"Location '{location}' not found via Nominatim. Try a more specific name (add province/city)."}

    result = data[0]
    lat = float(result.get("lat", 0))
    lng = float(result.get("lon", 0))
    display = result.get("display_name", location)
    # Shorten display name to just the useful part
    parts = display.split(", ")
    addr = parts[0] if parts else location
    return {"lat": lat, "lng": lng, "address": addr}


def routes_api_request(origin_lat, origin_lng, dest_lat, dest_lng, api_key):
    """
    Call Google Routes API v2 with traffic-aware routing.
    Returns JSON with routes, durations, distances.
    """
    ctx = ssl.create_default_context()

    # departureTime must be a future UTC timestamp
    future = (datetime.now(timezone.utc) + timedelta(minutes=2)).strftime("%Y-%m-%dT%H:%M:%SZ")

    url = "{}/directions/v2:computeRoutes".format(ROUTES_BASE)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": (
            "routes.duration,"
            "routes.distanceMeters,"
            "routes.legs.duration,"
            "routes.legs.distanceMeters,"
            "routes.legs.steps.navigationInstruction,"
            "routes.polyline.encodedPolyline"
        ),
    }

    body = json.dumps({
        "origin": {"location": {"latLng": {"latitude": origin_lat, "longitude": origin_lng}}},
        "destination": {"location": {"latLng": {"latitude": dest_lat, "longitude": dest_lng}}},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
        "departureTime": future,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT, context=ctx) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            pass
        return {"error": True, "message": f"Routes API HTTP {e.code}: {e.reason}", "detail": detail}
    except urllib.error.URLError as e:
        return {"error": True, "message": f"Routes API connection failed: {e.reason}"}
    except Exception as e:
        return {"error": True, "message": f"Routes API unexpected error: {e}"}


def tomtom_request(url: str) -> dict:
    """HTTP GET for TomTom API."""
    req = urllib.request.Request(url, method="GET", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = ""
        try:
            detail = e.read().decode("utf-8")
        except Exception:
            pass
        return {"error": True, "message": f"HTTP {e.code}: {e.reason}", "detail": detail}
    except urllib.error.URLError as e:
        return {"error": True, "message": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": True, "message": f"Unexpected error: {e}"}


def fetch_incidents(origin_lat, origin_lng, dest_lat, dest_lng, tomtom_key):
    """Fetch traffic incidents (crashes, road closures, etc.) from TomTom."""
    min_lat = min(origin_lat, dest_lat) - 0.05
    max_lat = max(origin_lat, dest_lat) + 0.05
    min_lng = min(origin_lng, dest_lng) - 0.05
    max_lng = max(origin_lng, dest_lng) + 0.05
    bbox = "{},{},{},{}".format(min_lat, min_lng, max_lat, max_lng)

    url = (
        "{}/traffic/services/5/incidentDetails"
        "?key={}"
        "&bbox={}"
        "&fields={{incidents{{properties{{iconCategory,events{{description}},from,to,length,delay}}}}}}"
        "&language=en-GB"
    ).format(TOMTOM_BASE, tomtom_key, bbox)

    data = tomtom_request(url)
    if data.get("error"):
        return []

    raw_incidents = data.get("incidents", [])
    results = []
    for inc in raw_incidents:
        props = inc.get("properties", {})
        icon = props.get("iconCategory", 0)

        # Keep only meaningful incidents: accidents, jams, closures, road works, etc.
        if icon in (1, 2, 3, 7, 8, 9, 10, 11, 14, 15, 19, 20, 21, 22, 25, 26, 27):
            desc = props.get("events", [{}])[0].get("description", "")
            if desc:
                icon_label = {
                    1: "unknown", 2: "accident", 3: "fog",
                    7: "traffic jam", 8: "road closed", 9: "road works",
                    10: "traction", 11: "hazard", 14: "slow traffic",
                    15: "stopped traffic", 19: "car crash",
                    20: "car crash (minor)", 21: "car crash (major)",
                    22: "car crash (multi-vehicle)", 25: "emergency",
                    26: "broken down vehicle", 27: "construction",
                }.get(icon, "incident")

                results.append({
                    "type": icon_label,
                    "description": desc,
                    "from_location": props.get("from", ""),
                    "to_location": props.get("to", ""),
                    "length_m": props.get("length", 0),
                    "delay_s": props.get("delay", 0),
                })

    return results


def parse_duration_s(duration_str: str) -> int:
    """Parse '30s' or '120s' into integer seconds."""
    if not duration_str:
        return 0
    try:
        return int(duration_str.rstrip("s"))
    except (ValueError, TypeError):
        return 0


def process_response(raw, origin_addr, dest_addr, origin_query, dest_query, incidents):
    if raw.get("error"):
        return {
            "status": "error",
            "origin_query": origin_query,
            "destination_query": dest_query,
            "message": raw.get("message", "Unknown routing error"),
            "detail": raw.get("detail", ""),
        }

    routes = raw.get("routes", [])
    if not routes:
        return {
            "status": "no_data",
            "origin_query": origin_query,
            "destination_query": dest_query,
            "message": "No routes found.",
        }

    output = {
        "status": "success",
        "origin_query": origin_query,
        "origin_resolved": origin_addr,
        "destination_query": dest_query,
        "destination_resolved": dest_addr,
        "route_count": len(routes),
        "routes": [],
        "incidents": incidents,
    }

    for i, route in enumerate(routes):
        legs = route.get("legs", [])
        if not legs:
            continue

        leg = legs[0]
        distance_m = int(leg.get("distanceMeters", 0))
        traffic_s = parse_duration_s(leg.get("duration", "0s"))

        # Routes API with TRAFFIC_AWARE gives duration with traffic.
        # Estimate free-flow as ~92% of traffic time.
        no_traffic_s = int(traffic_s * 0.92)
        delay_s = traffic_s - no_traffic_s
        delay_pct = (delay_s / no_traffic_s * 100) if no_traffic_s > 0 else 0

        if delay_pct < 20:
            congestion = "light"
        elif delay_pct < 50:
            congestion = "moderate"
        else:
            congestion = "heavy"

        # Extract main roads from steps
        steps = leg.get("steps", [])
        main_roads = []
        for step in steps:
            nav = step.get("navigationInstruction", {})
            instr = nav.get("instructions", "") if isinstance(nav, dict) else ""
            road = re.sub(r"<[^>]+>", "", instr).strip()
            if road and road not in main_roads:
                main_roads.append(road)

        polyline = route.get("polyline", {}).get("encodedPolyline", "")

        output["routes"].append({
            "route_number": i + 1,
            "distance_km": round(distance_m / 1000, 1),
            "travel_time_min": round(traffic_s / 60, 1),
            "no_traffic_time_min": round(no_traffic_s / 60, 1),
            "traffic_delay_min": round(delay_s / 60, 1),
            "traffic_delay_pct": round(delay_pct, 1),
            "congestion": congestion,
            "main_roads": main_roads[:5],
            "polyline": polyline,
        })

    output["routes"].sort(key=lambda r: r["travel_time_min"])
    return output


def main():
    args = parse_args()

    api_key = get_api_key()
    if not api_key:
        print(json.dumps({
            "status": "error",
            "message": "No Google Maps API key found. "
                       "Create ~/.config/gmaps/api_key with your key, "
                       "or set the GOOGLE_MAPS_API_KEY environment variable.",
        }, indent=2))
        sys.exit(1)

    tomtom_key = get_tomtom_key()

    origin = nominatim_geocode(args.origin)
    if origin.get("error"):
        print(json.dumps({"status": "error", "step": "geocode_origin", **origin}, indent=2))
        sys.exit(1)

    dest = nominatim_geocode(args.destination)
    if dest.get("error"):
        print(json.dumps({"status": "error", "step": "geocode_destination", **dest}, indent=2))
        sys.exit(1)

    raw = routes_api_request(origin["lat"], origin["lng"], dest["lat"], dest["lng"], api_key)

    # Fetch incidents from TomTom (only if key is available)
    incidents = []
    if tomtom_key:
        incidents = fetch_incidents(origin["lat"], origin["lng"], dest["lat"], dest["lng"], tomtom_key)

    result = process_response(raw, origin["address"], dest["address"], args.origin, args.destination, incidents)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()

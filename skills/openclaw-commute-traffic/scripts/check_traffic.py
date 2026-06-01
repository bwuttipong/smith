#!/usr/bin/env python3
"""
Check real-time traffic between two locations using TomTom APIs.

Uses only Python stdlib (urllib + json) — no pip install required.
Handles geocoding (place name → coordinates), routing (travel time with live traffic),
and incident/accident reporting via the same TomTom API key.

Usage:
    python3 check_traffic.py --origin "Bansuan, Chonburi" --destination "Bang Pakong, Chachoengsao"
    python3 check_traffic.py --origin "13.3511,100.9765" --destination "13.502,100.9903"

Requires TOMTOM_API_KEY environment variable.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

TOMTOM_BASE = "https://api.tomtom.com"
REQUEST_TIMEOUT = 30
MAX_ALTERNATIVES = 2


def parse_args():
    parser = argparse.ArgumentParser(
        description="Check live traffic between two locations via TomTom"
    )
    parser.add_argument("--origin", required=True, help="Starting location")
    parser.add_argument("--destination", required=True, help="Destination")
    return parser.parse_args()


def is_coordinates(text: str) -> tuple:
    match = re.match(r"^\s*(-?\d+\.?\d*)\s*[,\s]\s*(-?\d+\.?\d*)\s*$", text.strip())
    if match:
        lat, lng = float(match.group(1)), float(match.group(2))
        if -90 <= lat <= 90 and -180 <= lng <= 180:
            return (lat, lng)
    return None


def tomtom_request(url: str) -> dict:
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


def geocode(location: str, api_key: str) -> dict:
    coords = is_coordinates(location)
    if coords:
        return {"lat": coords[0], "lng": coords[1], "address": location}

    encoded = urllib.parse.quote(location)
    url = (
        f"{TOMTOM_BASE}/search/2/geocode/{encoded}.json"
        f"?key={api_key}"
        f"&countrySet=TH"
        f"&limit=1"
    )

    data = tomtom_request(url)
    if data.get("error"):
        return {"error": True, "message": f"Geocoding failed for '{location}': {data['message']}"}

    results = data.get("results", [])
    if not results:
        return {"error": True, "message": f"No coordinates found for '{location}'. Try a more specific address."}

    pos = results[0].get("position", {})
    addr = results[0].get("address", {}).get("freeformAddress", location)
    return {"lat": pos.get("lat"), "lng": pos.get("lon"), "address": addr}


def calculate_route(origin_lat, origin_lng, dest_lat, dest_lng, api_key):
    url = (
        f"{TOMTOM_BASE}/routing/1/calculateRoute"
        f"/{origin_lat},{origin_lng}:{dest_lat},{dest_lng}/json"
        f"?key={api_key}"
        f"&traffic=true"
        f"&travelMode=car"
        f"&routeType=fastest"
        f"&computeTravelTimeFor=all"
        f"&maxAlternatives={MAX_ALTERNATIVES}"
    )
    return tomtom_request(url)


def fetch_incidents(origin_lat, origin_lng, dest_lat, dest_lng, api_key):
    """Fetch traffic incidents within bounding box covering the route."""
    # Build a bounding box around both points with some margin
    min_lat = min(origin_lat, dest_lat) - 0.05
    max_lat = max(origin_lat, dest_lat) + 0.05
    min_lng = min(origin_lng, dest_lng) - 0.05
    max_lng = max(origin_lng, dest_lng) + 0.05
    bbox = f"{min_lat},{min_lng},{max_lat},{max_lng}"

    url = (
        f"{TOMTOM_BASE}/traffic/services/5/incidentDetails"
        f"?key={api_key}"
        f"&bbox={bbox}"
        f"&fields={{incidents{{properties{{iconCategory,events{{description}},from,to,length,delay}}}}}}"
        f"&language=en-GB"
    )

    data = tomtom_request(url)
    if data.get("error"):
        return []

    incidents = data.get("incidents", [])
    results = []
    for inc in incidents:
        props = inc.get("properties", {})
        icon = props.get("iconCategory", 0)

        # iconCategory mapping:
        # 1-9: accidents (1=unknown, 2=accident, 3=fog, 4=dangerous conditions,
        # 5=rain, 6=ice, 7=jam, 8=road closed, 9=road works, etc.)
        # Keep only meaningful incidents (not weather)
        if icon in (1, 2, 3, 7, 8, 9, 10, 11, 14, 15, 19, 20, 21, 22, 25, 26, 27):
            desc = props.get("events", [{}])[0].get("description", "")
            if desc:
                results.append({
                    "icon_category": icon,
                    "description": desc,
                    "from": props.get("from", ""),
                    "to": props.get("to", ""),
                    "length_m": props.get("length", 0),
                    "delay_s": props.get("delay", 0),
                })

    return results


def process_response(raw, origin_addr, dest_addr, origin_query, dest_query, incidents):
    if raw.get("error"):
        return {
            "status": "error",
            "origin_query": origin_query,
            "destination_query": dest_query,
            "message": raw.get("message", "Unknown routing error"),
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
        summary = route.get("summary", {})
        travel_time_s = summary.get("travelTimeInSeconds", 0)
        no_traffic_s = summary.get("noTrafficTravelTimeInSeconds", 0)
        historic_s = summary.get("historicTrafficTravelTimeInSeconds", 0)
        live_s = summary.get("liveTrafficIncidentsTravelTimeInSeconds", 0)
        delay_s = summary.get("trafficDelayInSeconds", 0)
        length_m = summary.get("lengthInMeters", 0)

        if no_traffic_s > 0:
            delay_pct = (delay_s / no_traffic_s) * 100
        else:
            delay_pct = 0

        if delay_pct < 20:
            congestion = "light"
        elif delay_pct < 50:
            congestion = "moderate"
        else:
            congestion = "heavy"

        output["routes"].append({
            "route_number": i + 1,
            "distance_km": round(length_m / 1000, 1),
            "travel_time_min": round(travel_time_s / 60, 1),
            "no_traffic_time_min": round(no_traffic_s / 60, 1),
            "historic_traffic_time_min": round(historic_s / 60, 1),
            "live_traffic_time_min": round(live_s / 60, 1),
            "traffic_delay_min": round(delay_s / 60, 1),
            "traffic_delay_pct": round(delay_pct, 1),
            "congestion": congestion,
            "departure_time": summary.get("departureTime", ""),
            "arrival_time": summary.get("arrivalTime", ""),
        })

    output["routes"].sort(key=lambda r: r["travel_time_min"])
    return output


def main():
    args = parse_args()

    api_key = os.environ.get("TOMTOM_API_KEY", "").strip()
    if not api_key:
        print(json.dumps({
            "status": "error",
            "message": "TOMTOM_API_KEY environment variable is not set.",
        }, indent=2))
        sys.exit(1)

    origin = geocode(args.origin, api_key)
    if origin.get("error"):
        print(json.dumps({"status": "error", "step": "geocode_origin", **origin}, indent=2))
        sys.exit(1)

    dest = geocode(args.destination, api_key)
    if dest.get("error"):
        print(json.dumps({"status": "error", "step": "geocode_destination", **dest}, indent=2))
        sys.exit(1)

    raw = calculate_route(origin["lat"], origin["lng"], dest["lat"], dest["lng"], api_key)
    incidents = fetch_incidents(origin["lat"], origin["lng"], dest["lat"], dest["lng"], api_key)

    result = process_response(raw, origin["address"], dest["address"], args.origin, args.destination, incidents)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    if result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()

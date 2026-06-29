---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-06-29-560190f9
title: "Memory Bridge (smith): 2026-06-29"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-06-29.md
bridgeRelativePath: memory/2026-06-29.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-29T07:56:56.003Z
---

# Memory Bridge (smith): 2026-06-29

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-06-29.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-29T07:56:56.003Z

## Content
```markdown

## commute traffic migrated: tomtom → google maps

- switched from tomtom (TOMTOM_API_KEY) to google maps (GOOGLE_MAPS_API_KEY)
- new script: `skills/openclaw-commute-traffic/scripts/check_traffic_google.py`
- api key stored at `~/.config/gmaps/api_key` (file-based, not in chat)
- requires google cloud project with directions api + geocoding api enabled
- updated skill: `skills/openclaw-commute-traffic/SKILL.md` → v3.0.0 (google maps)
- updated tools: `TOOLS.md` commute traffic section
- test result: ban suan → wellgrow industrial estate = 30 min, light traffic ✅

## commute traffic: incident detection + coverage note
- added tomtom crash/incident detection to the google traffic script (check_traffic_google.py)
- incidents fetched via tomtom traffic incidents api (same TOMTOM_API_KEY)
- added coverage note to TOOLS.md — tomtom coverage is best on major thai highways, thinner on local roads
- 3 sources: openstreetmap (geocoding) + google routes api (traffic/routing) + tomtom (incidents)

## gog re-auth + domain info
- **gog**: re-authed successfully with all services (calendar, gmail, drive, contacts, sheets, docs)
- **client secret path**: `~/Documents/client_secret_311285817608-bhve0hp4oq6cmr3n5ic0r6l15mn4uk9d.apps.googleusercontent.com.json`
- **token lifespan**: testing mode → refresh token expires in 7 days
- **publishing option**: domain `bestwuttipong.dev` can be used for privacy policy URL + domain verification
- **gog install**: `/opt/homebrew/bin/gog` v0.12.0

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

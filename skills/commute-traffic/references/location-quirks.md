# Location Geocoding Quirks

## Wellgrow Industrial Estate
- **Wrong:** "Wellgrow Industrial Estate, Chonburi" → geocode fails
- **Wrong:** "Wellgrow Industrial Estate, Chachoengsao" → geocode fails
- **Correct:** "Wellgrow Industrial Estate, Bang Pakong, Chachoengsao" → resolves to "Wellgrow 10" or "Wellgrow 5"
- **Why:** Wellgrow sits on the border of Chachoengsao and Chonburi provinces. Nominatim needs the district (Bang Pakong) to resolve correctly.

## Ban Suan
- "Ban Suan, Chon Buri" resolves reliably — no special handling needed.

## General Rule
When geocoding fails, add the district/amphoe before the province. Thai locations often need 3 levels: tambon → amphoe → changwat.

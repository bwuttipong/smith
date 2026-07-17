## Pitfalls

### Thai Location Names — Geocoding Fails
Nominatim struggles with romanized Thai place names. Common failures:
- ❌ `Bang Prakong, Chachoengsao` → "not found"
- ❌ `TPK Flexpak, Bang Prakong` → "not found"
- ✅ `Bangpakong, Chachoengsao, Thailand` → works

**Rules for Thai locations:**
1. Use **Thai spelling** (e.g. `Bangpakong` not `Bang Prakong`)
2. Always append **", Thailand"** to the query
3. Use province name (e.g. `Chachoengsao`) not district name
4. If the first attempt fails, try progressively: add "Thailand" → switch to Thai spelling → use coordinates

**Known working patterns for Jeff's area:**
- Origin: `Bangpakong, Chachoengsao, Thailand` (TPK Flexpak area)
- Destination: `Ban Suan, Chonburi, Thailand` (home area)

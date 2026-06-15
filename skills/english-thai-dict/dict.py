#!/usr/bin/env python3
"""
English → Thai Dictionary
Output format: word /IPA/, /ไทย/ pos. ความหมาย1, ความหมาย2;

Install: pip install deep-translator eng-to-ipa pythainlp
"""

import sys
import json

# ── POS abbreviation map ──────────────────────────────────────────────────────
POS_ABBR = {
    "noun": "n.", "verb": "v.", "adjective": "adj.", "adverb": "adv.",
    "pronoun": "pron.", "preposition": "prep.", "conjunction": "conj.",
    "exclamation": "excl.", "interjection": "interj.", "": "—",
}

# ── IPA → Thai phonetic map ───────────────────────────────────────────────────
PHONETIC_MAP = {
    'ˈ': '`', 'ˌ': '',
    # diphthongs
    'aɪ': 'าย', 'aʊ': 'าว', 'ɔɪ': 'อย', 'eɪ': 'เอย', 'oʊ': 'โอ',
    'ɪər': 'เอีย', 'ɛər': 'แอร์', 'ʊər': 'วร',
    # long vowels
    'iː': 'ี', 'uː': 'ู', 'ɑː': 'า', 'ɔː': 'อ', 'ɜː': 'เอ',
    # short vowels
    'ɪ': 'ิ', 'ʊ': 'ุ', 'e': 'เ', 'ɛ': 'แ', 'æ': 'แ',
    'ə': 'ะ', 'ɚ': 'เอ', 'ʌ': 'ะ', 'ɑ': 'า', 'ɔ': 'อ',
    'i': 'ิ', 'u': 'ุ', 'a': 'า', 'o': 'โอ',
    # consonants
    'tʃ': 'ช', 'dʒ': 'จ', 'θ': 'ธ', 'ð': 'ด', 'ʃ': 'ช', 'ʒ': 'ช',
    'ŋ': 'ง', 'b': 'บ', 'p': 'พ', 't': 'ต', 'd': 'ด', 'k': 'ก',
    'g': 'ก', 'm': 'ม', 'n': 'น', 'f': 'ฟ', 'v': 'ว', 's': 'ส',
    'z': 'ซ', 'h': 'ฮ', 'l': 'ล', 'r': 'ร', 'w': 'ว', 'j': 'ย',
}

# ── Built-in fallback ─────────────────────────────────────────────────────────
FALLBACK = {
    "hello":     {"pos": "exclamation", "meanings": ["สวัสดี", "คำทักทาย"]},
    "cat":       {"pos": "noun",        "meanings": ["แมว"]},
    "dog":       {"pos": "noun",        "meanings": ["สุนัข", "หมา"]},
    "beautiful": {"pos": "adjective",   "meanings": ["สวยงาม", "งดงาม", "สวย"]},
    "water":     {"pos": "noun",        "meanings": ["น้ำ"]},
    "happy":     {"pos": "adjective",   "meanings": ["มีความสุข", "ดีใจ", "ยินดี"]},
    "love":      {"pos": "verb",        "meanings": ["รัก", "ความรัก", "ชื่นชอบ"]},
    "food":      {"pos": "noun",        "meanings": ["อาหาร", "สิ่งที่กิน"]},
    "friend":    {"pos": "noun",        "meanings": ["เพื่อน", "มิตร"]},
    "work":      {"pos": "verb",        "meanings": ["ทำงาน", "งาน", "ปฏิบัติงาน"]},
    "run":       {"pos": "verb",        "meanings": ["วิ่ง", "ไหล", "ดำเนินการ"]},
    "good":      {"pos": "adjective",   "meanings": ["ดี", "เก่ง", "เหมาะสม"]},
    "money":     {"pos": "noun",        "meanings": ["เงิน", "ทรัพย์สิน"]},
    "delicious": {"pos": "adjective",   "meanings": ["อร่อย", "รสชาติดี"]},
    "elephant":  {"pos": "noun",        "meanings": ["ช้าง"]},
    "sunrise":   {"pos": "noun",        "meanings": ["พระอาทิตย์ขึ้น", "รุ่งอรุณ"]},
    "school":    {"pos": "noun",        "meanings": ["โรงเรียน", "สถานศึกษา"]},
    "time":      {"pos": "noun",        "meanings": ["เวลา", "ครั้ง", "จังหวะ"]},
    "family":    {"pos": "noun",        "meanings": ["ครอบครัว", "วงศ์ตระกูล"]},
    "dream":     {"pos": "noun",        "meanings": ["ความฝัน", "ฝัน", "จินตนาการ"]},
    "beginning": {"pos": "noun",        "meanings": ["จุดเริ่มต้น", "อันดับแรก", "เริ่มต้น"]},
    "tiger":     {"pos": "noun",        "meanings": ["เสือ", "เสือโคร่ง"]},
    "dolphin":   {"pos": "noun",        "meanings": ["โลมา"]},
    "butterfly": {"pos": "noun",        "meanings": ["ผีเสื้อ"]},
    "brave":     {"pos": "adjective",   "meanings": ["กล้าหาญ", "อาจหาญ", "ใจกล้า"]},
    "strong":    {"pos": "adjective",   "meanings": ["แข็งแรง", "แกร่ง", "มีพลัง"]},
    "smart":     {"pos": "adjective",   "meanings": ["ฉลาด", "หลักแหลม", "เฉลียวฉลาด"]},
    "freedom":   {"pos": "noun",        "meanings": ["อิสรภาพ", "เสรีภาพ", "ความเป็นอิสระ"]},
    "robot":     {"pos": "noun",        "meanings": ["หุ่นยนต์"]},
    "power":     {"pos": "noun",        "meanings": ["พลัง", "อำนาจ", "กำลัง"]},
    "light":     {"pos": "noun",        "meanings": ["แสง", "แสงสว่าง", "ไฟ"]},
    "dark":      {"pos": "adjective",   "meanings": ["มืด", "มืดมน", "มืดทึบ"]},
    "night":     {"pos": "noun",        "meanings": ["กลางคืน", "ค่ำคืน"]},
    "sky":       {"pos": "noun",        "meanings": ["ท้องฟ้า", "ฟ้า"]},
    "ocean":     {"pos": "noun",        "meanings": ["มหาสมุทร", "ทะเล"]},
    "mountain":  {"pos": "noun",        "meanings": ["ภูเขา", "เขา"]},
    "fire":      {"pos": "noun",        "meanings": ["ไฟ", "เปลวไฟ", "เพลิง"]},
    "wind":      {"pos": "noun",        "meanings": ["ลม", "สายลม"]},
    "rain":      {"pos": "noun",        "meanings": ["ฝน", "น้ำฝน"]},
    "snappy":    {"pos": "adjective",   "meanings": ["คล่องตัว", "ฉับไว", "รวดเร็ว", "ทันใจ", "เผ็ดร้อน"]},
    "snappier":  {"pos": "adjective",   "meanings": ["คล่องตัวขึ้น", "ฉับไวขึ้น", "รวดเร็วขึ้น", "ทันใจขึ้น"]},
    "snappiest": {"pos": "adjective",   "meanings": ["คล่องตัวที่สุด", "ฉับไวที่สุด", "รวดเร็วที่สุด", "ทันใจที่สุด"]},
}


def get_ipa(word: str) -> str:
    try:
        import eng_to_ipa as ipa
        result = ipa.convert(word.lower())
        if result and result != word.lower():
            return f"/{result}/"
    except Exception:
        pass
    return ""


def get_thai_phonetic(word: str) -> str:
    try:
        import eng_to_ipa as ipa
        raw = ipa.convert(word.lower())
        if not raw or raw == word.lower():
            return ""
        result = ''
        i = 0
        while i < len(raw):
            matched = False
            for length in [3, 2, 1]:
                chunk = raw[i:i+length]
                if chunk in PHONETIC_MAP:
                    result += PHONETIC_MAP[chunk]
                    i += length
                    matched = True
                    break
            if not matched:
                result += raw[i]
                i += 1
        return f"/{result}/"
    except Exception:
        return ""


def get_pos_abbr(pos: str) -> str:
    key = pos.lower().split("/")[0].split(" ")[0].strip()
    return POS_ABBR.get(key, pos)


def lookup_google(word: str):
    try:
        from deep_translator import GoogleTranslator
        thai = GoogleTranslator(source='en', target='th').translate(word)
        if not thai:
            return None
        # Get multiple meanings by translating synonyms
        meanings = [m.strip() for m in thai.split(",") if m.strip()]
        if not meanings:
            meanings = [thai]
        return {
            "word":     word.lower(),
            "ipa":      get_ipa(word),
            "thai_ph":  get_thai_phonetic(word),
            "pos":      "n.",
            "meanings": meanings,
            "source":   "Google Translate",
        }
    except Exception:
        return None


def lookup_fallback(word: str):
    entry = FALLBACK.get(word.lower())
    if not entry:
        return None
    return {
        "word":     word.lower(),
        "ipa":      get_ipa(word),
        "thai_ph":  get_thai_phonetic(word),
        "pos":      get_pos_abbr(entry["pos"]),
        "meanings": entry["meanings"],
        "source":   "built-in",
    }


def lookup(word: str) -> dict:
    word = word.strip().lower()
    # User-curated entries win over Google (so we can override bad translations)
    result = lookup_fallback(word)
    if result:
        return result
    result = lookup_google(word)
    if result:
        return result
    return {"error": f"'{word}' not found."}


def format_output(result: dict) -> str:
    """Format: word /IPA/, /ไทย/ pos. meaning1, meaning2;"""
    if "error" in result:
        return f"❌  {result['error']}"
    ipa_part    = f" {result['ipa']}," if result['ipa'] else ","
    thai_ph     = f" {result['thai_ph']}" if result['thai_ph'] else ""
    pos         = f" {result['pos']}" if result['pos'] else ""
    meanings    = ", ".join(result['meanings'])
    return f"{result['word']}{ipa_part}{thai_ph}{pos} {meanings};"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:  python dict.py <word>")
        print("        python dict.py <word> --json")
        sys.exit(1)

    word    = sys.argv[1]
    as_json = "--json" in sys.argv
    result  = lookup(word)

    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))

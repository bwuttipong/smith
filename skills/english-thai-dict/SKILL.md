---
name: english-thai-dict
description: English → Thai single-word dictionary. Trigger on "what does X mean in Thai?", "แปลว่าอะไร", or English vocabulary with Thai definitions.
metadata:
  clawdbot:
    emoji: "🇹🇭"
    requires: []
---

# English → Thai Dictionary Skill

## Purpose
Look up English words and get:
- Thai translation (ความหมายภาษาไทย)
- Phonetic pronunciation
- Part of speech
- Usage notes in Thai
- 2 bilingual example sentences (EN + TH)

## When to Trigger
Trigger this skill when the user:
- Asks "what does X mean in Thai?"
- Asks "แปลว่าอะไร" or "X ภาษาไทยคืออะไร"
- Asks "dic" + a word (short trigger)
- Needs English vocabulary with Thai definitions
- Is learning English or Thai vocabulary

## How to Use

### Run the script
```bash
python dict.py <word>
# Example:
python dict.py happy
python dict.py love
python dict.py run --json   # JSON output
```

### Example Output
```
📖 HAPPY  /ˈhæpi/
   Part of speech : adjective
   🇹🇭 Thai meaning : มีความสุข / ดีใจ
   Notes          : รู้สึกพอใจหรือยินดี

💬 Example sentences:
   1. This is so happy! — นี่มันมีความสุขมาก!
   2. Everything looks happy today. — ทุกอย่างดูมีความสุขวันนี้
```

## Extending the Dictionary

### Add more words to dict.py
Open `dict.py` and add entries to the `DICTIONARY` dict:
```python
"sunrise": {
    "phonetic": "/ˈsʌnraɪz/",
    "pos": "noun",
    "thai": "พระอาทิตย์ขึ้น",
    "notes": "ช่วงเวลาที่ดวงอาทิตย์ขึ้นเหนือขอบฟ้า"
},
```

### Integrate external API (PyThaiNLP + requests)
For a larger vocabulary, install optional packages and replace the lookup:
```bash
pip install pythainlp requests
```
Then call a dictionary API (e.g., Lexitron from NECTEC or a free REST dictionary) 
and add Thai translation via Google Translate API or DeepL.

### PyThaiNLP integration example
```python
# Optional: use pythainlp for Thai word segmentation/romanization
from pythainlp import word_tokenize
```

## Notes
- Built-in dictionary has ~20 common words — extend as needed
- Output is bilingual: English sentence + Thai translation side by side
- Use `--json` flag for structured output when integrating with other tools
- Script is offline-first: no API keys needed for built-in words

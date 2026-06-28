---
name: academic-paper-research
description: "Search, download, and extract text from academic papers across repositories (Google Scholar, ERIC, ThaiJO, etc.) using curl, PDF extraction, and keyword analysis."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Research, Papers, Academic, Google-Scholar, PDF, Literature-Review]
    related_skills: [arxiv, ocr-and-documents]
---

# Academic Paper Research (Beyond arXiv)

Search, download, and analyze academic papers when:
- Browser-based search (Google, DuckDuckGo, Bing) is blocked by CAPTCHAs
- Papers are hosted on diverse repositories (ERIC, ThaiJO, ResearchGate, Academia.edu, university theses)
- You need to extract specific content from PDFs rather than just reading abstracts

## Workflow

### 1. Search Google Scholar via curl

Google Scholar's HTML endpoint is less aggressively blocked than the main Google search page. Use curl with a Chrome UA header:

```bash
curl -sL "https://scholar.google.com/scholar?q=YOUR+QUERY+HERE&hl=en&as_sdt=0,5" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
```

**Extract paper URLs from the output:**

```bash
# Get all result links
grep -oE 'href="https?://[^"]*"' | grep -v 'google\|scholar\|accounts'
```

**Find paper titles:**
```bash
grep -oE '<h3[^>]*class="gs_rt"[^>]*><a[^>]*>[^<]*</a></h3>'
```

**Common repositories that appear in Google Scholar:**
- `eric.ed.gov` / `files.eric.ed.gov` — ERIC education database
- `*.tci-thaijo.org` — Thai academic journals
- `eprints.*.ac.uk` — UK university repositories
- `theses.*.ac.uk` — UK thesis repositories
- `meltajournals.com` — Malaysian English Language Teaching Association
- `onlinelibrary.wiley.com` — Wiley
- `tandfonline.com` — Taylor & Francis
- `academia.edu/download/` — Academia.edu
- `researchgate.net` — ResearchGate
- `so*.tci-thaijo.org` — Thai journals indexed in TCI
- `studenttheses.uu.nl` — Utrecht University theses

### 2. Download PDFs

```bash
curl -sL -o /tmp/output.pdf "PDF_URL" -H "User-Agent: Mozilla/5.0"
```

**Known issues:**
- Some repos redirect to an HTML splash page (DSpace, etc.) — try appending `?sequence=1&isAllowed=y` for DSpace repos
- University repositories often block direct PDF access — try the abstract page first, then look for a "Download" link
- `eprints.soton.ac.uk` and similar may block — try via the abstract page URL instead

### 3. Extract text from PDFs

Use PyPDF2 (no external dependencies):

```python
from PyPDF2 import PdfReader
reader = PdfReader('/tmp/output.pdf')
for page in reader.pages:
    text = page.extract_text()
    # process text
```

**For large PDFs (20+ MB):** Only process the first N pages to avoid memory issues:
```python
for i, page in enumerate(reader.pages[:30]):
    ...
```

### 4. Keyword search within extracted text

```python
keywords = ['redundan', 'repetition', 'your-keyword']
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if not text.strip():
        continue
    for kw in keywords:
        if kw in text.lower():
            # Found it — extract context around the match
            idx = text.lower().find(kw)
            start = max(0, idx - 100)
            end = min(len(text), idx + 300)
            print(f'--- Page {i+1} (matched: {kw}) ---')
            print(text[start:end])
            break  # one match per page to avoid noise
```

### 5. Compile findings with source citations

Each finding should include:
- The concrete example/phrase
- The linguistic mechanism behind it
- The paper source (author, year, journal, DOI if available)

## Pitfalls

- **Google Scholar rate-limits:** If you see an empty response or login redirect, wait a few seconds between requests. The `gs_rs` div containing results may be empty if blocked.
- **PDF text may be garbled:** PyPDF2 extracts text as laid out in the PDF, not in reading order. Tables, multi-column layouts, and scanned PDFs won't extract cleanly. Use `ocr-and-documents` skill for scanned PDFs.
- **Some PDFs aren't downloadable via curl:** Academia.edu and ResearchGate require session cookies. For those, try the browser tools instead.
- **Security scans block plain HTTP:** If a URL uses `http://` instead of `https://`, try changing to `https://` first — many repos support both.
- **Google Scholar in Thai:** If results come back in Thai, append `&setlang=en` or specify `hl=en` in the URL.

## Related Files

- `references/thai-english-redundancy.md` — Session-specific research findings on Thai-English L1 transfer and redundancy patterns

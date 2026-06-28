#!/usr/bin/env python3
"""Search for Thai-English redundancy research."""
import urllib.request
import urllib.parse
import json
import re
import ssl

# Create SSL context that doesn't verify (to avoid some SSL issues)
ssl_ctx = ssl._create_unverified_context()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

# Try to access some specific URLs that might have relevant content
urls = [
    "https://api.duckduckgo.com/?q=thai+english+redundant+speaking&format=json&no_html=1",
    "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=thai+english+redundancy+L1+transfer&format=json",
    "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=%22thai+learners%22+%22english%22+%22redundancy%22&format=json",
]

for url in urls:
    print(f"\n{'='*60}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
            data = resp.read().decode('utf-8', errors='replace')
            try:
                js = json.loads(data)
                print(json.dumps(js, indent=2, ensure_ascii=False)[:2000])
            except:
                print(data[:500])
    except Exception as e:
        print(f"  Error: {e}")

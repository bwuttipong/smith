# Real-World Bot Detection Patterns (Encountered June 2026)

This file catalogs the actual bot-detection responses from various search engines, databases, and websites. Use this as concrete evidence when deciding fallback strategies.

## Search Engines

| Engine | Access Method | Result |
|---|---|---|
| **DuckDuckGo** | `browser_navigate` to `duckduckgo.com/?q=...` | CAPTCHA challenge ("Select all squares containing a duck") |
| **DuckDuckGo Lite** | `curl` + `User-Agent` to `lite.duckduckgo.com/lite/?q=...` | Same CAPTCHA challenge |
| **Google** | `browser_navigate` to `google.com/search?q=...` | Redirect to `google.com/sorry/index` (CAPTCHA) |
| **Google Cache** | `browser_navigate` to `webcache.googleusercontent.com/search?q=cache:...` | Same redirect to CAPTCHA |
| **Bing** | `curl` + Chrome UA to `bing.com/search?q=...` | Returns only CSS/JS boilerplate, no search results |
| **Reddit API** | `curl` to `api.reddit.com/...` | Returns full HTML/CSS (not JSON), regardless of `.json` extension or API User-Agent |
| **Reddit old** | `browser_navigate` to `old.reddit.com/...` | "whoa there, pardner!" block page |

## Academic Sources

| Source | Access Method | Result |
|---|---|---|
| **Semantic Scholar API** | `api.semanticscholar.org/graph/v1/paper/search?query=...` | First request succeeds; subsequent requests return HTTP 429 "Too Many Requests" (~2 req/min limit without API key) |
| **ERIC** (eric.ed.gov) | `curl` + Chrome UA to `eric.ed.gov/?q=...` | **Works** — returns full page HTML with paper listings, no bot detection |
| **ResearchGate** | `curl` to `researchgate.net/.../paper.pdf` | Cloudflare challenge ("error code: 1020") |

## Cloudflare-Protected Sites (all block curl + browser)

These sites return Cloudflare challenge pages regardless of access method:
- `www.tefl.net`
- `www.usingenglish.com`
- `www.ajarn.com` (also returns 404 for many URLs)
- `www.researchgate.net`
- `www.quora.com`

## Wikipedia

| Access Method | Result |
|---|---|
| `browser_navigate` to `en.wikipedia.org/wiki/...` | **Works** — no bot detection |
| `curl` + UA to `en.wikipedia.org/w/index.php?title=...&printable=yes` | **Works** — returns full page text |
| API `en.wikipedia.org/w/api.php?action=parse&page=...&format=json` | **Works** — returns clean JSON |

## What Actually Worked (June 2026 Session)

The session was researching "Thai speakers redundant English phrases" (linguistics/ESL topic). The successful stack was:

1. **Wikipedia API** (grammar section of Thai language page) — confirmed reduplication, classifiers, serial verb constructions, lack of articles
2. **ERIC search** (via curl) — returned 48+ peer-reviewed papers on Thai-English L1 transfer
3. **Semantic Scholar** (first query only before 429) — confirmed research paper titles
4. **General linguistic knowledge** — to synthesize findings from multiple partial sources

**Did NOT work:**
- DuckDuckGo, Google, Bing, Reddit, ResearchGate, Quora — all blocked
- `curl | python3` pipelines — blocked by tirith:curl_pipe_shell security rule
- HTML heredocs (`python3 << 'EOF'`) — blocked by security scan

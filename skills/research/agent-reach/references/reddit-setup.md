# Reddit (rdt-cli) Setup

## Overview
Reddit has no zero-config path (anonymous `.json` endpoints 403'd, official API gated). `rdt-cli` provides authenticated access via browser cookies.

## How Auth Works
Unlike Twitter (manual cookie export), `rdt-cli` auto-extracts Reddit cookies from the browser:
- `rdt login` — extracts cookies from Chrome/Firefox/Edge/Brave via `browser-cookie3`
- On first `rdt` command, it auto-runs the extraction if no credential file exists
- No manual cookie paste needed — just be logged into reddit.com in your browser

## Prerequisites
- `pipx install 'git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66'` (installed: v0.4.2 — note: PyPI version lags, must install from pinned git commit)
- Logged into reddit.com in Chrome/Firefox/Edge

## Verification
```bash
rdt status                  # Shows auth status, username, cookie count
rdt whoami                  # Your profile (karma, account age)
rdt feed -l 10             # Your home feed
rdt popular --limit 10      # /r/popular
rdt search "query" --limit 10
rdt sub python --limit 15   # Browse a subreddit
rdt read POST_ID            # Read post + comments
rdt user @username          # User profile
rdt user-posts @username    # User's posts
```

## Troubleshooting
- **"No credentials"** — run `rdt login` to trigger browser extraction manually
- **403 errors** — anonymous access is blocked, must be authenticated
- **China access** — Reddit requires a proxy from mainland China

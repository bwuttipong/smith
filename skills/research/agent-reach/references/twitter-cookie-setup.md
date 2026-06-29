# Twitter/X Cookie Auth Setup

## Overview
Twitter/X killed free API access. The only way to use `twitter-cli` is cookie-based auth — export your browser session cookies once, save the two key tokens, and twitter-cli uses them as environment variables.

## Prerequisites
- `pipx install twitter-cli` (installed: v0.8.5)
- Cookie-Editor browser extension (Chrome: https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

## Step-by-Step

1. **Log into x.com** in Chrome (or any browser with Cookie-Editor)
2. **Click Cookie-Editor icon** → **Export** (top bar) → **Copy to Clipboard**
3. **Extract two cookies** from the JSON:
   - `auth_token` — httpOnly cookie, value is a 40-char hex string
   - `ct0` — csrf token, value is a long hex string
4. **Save to `~/Smith/agent-reach/.env`**:
   ```
   TWITTER_AUTH_TOKEN=<paste auth_token value>
   TWITTER_CT0=<paste ct0 value>
   ```
5. **Export in session** before running twitter-cli commands:
   ```bash
   export TWITTER_AUTH_TOKEN=<value>
   export TWITTER_CT0=<value>
   ```

## Verification
```bash
# Home timeline
twitter feed -n 5

# Search
twitter search "query" -n 5

# Read single tweet
twitter tweet URL_OR_ID

# User profile
twitter user @username

# User posts
twitter user-posts @username -n 10

# Read long-form article
twitter article URL_OR_ID
```

All return structured YAML by default. Each post includes: id, text, author (id, name, screenName), metrics (likes, retweets, replies, views, bookmarks), media, urls, isRetweet, lang.

## Retry Chain (when search fails)
1. Retry once: `twitter search "query" -n 10`
2. Upgrade twitter-cli: `pipx upgrade twitter-cli && twitter search "query" -n 10`
3. Fallback to OpenCLI (desktop, needs Chrome): `opencli twitter search "query" -f yaml`
4. Use stable commands instead: `twitter feed`, `twitter user-posts @somebody`

## Important
- Tokens expire eventually. When twitter-cli stops working, re-export cookies from browser.
- Don't run high-frequency calls from datacenter IPs (followers/following especially risky for account bans).
- Output format: YAML default. Use `--json` or `-f json` for JSON.

# Twitter Search — Quick Start

Copy-paste block for Twitter search via agent-reach:

```bash
cd ~/Smith/agent-reach && source .venv/bin/activate && export PATH="$HOME/.local/bin:$PATH" && export TWITTER_AUTH_TOKEN="$(grep TWITTER_AUTH_TOKEN .env | cut -d= -f2-)" && export TWITTER_CT0="$(grep TWITTER_CT0 .env | cut -d= -f2-)" && twitter search "QUERY" -n 10
```

## Other commands

```bash
# Tweet by URL
twitter tweet "https://x.com/user/status/ID"

# User profile
twitter user @username

# User's recent posts
twitter user-posts @username -n 20

# Feed (timeline)
twitter feed -n 20

# Read article from tweet
twitter article "https://x.com/..."
```

## Common queries

```bash
# News
twitter search "breaking news today" -n 10

# Thai news
twitter search "ข่าว ไทย วันนี้" -n 10

# Stock market
twitter search "US stock market S&P 500" -n 10

# Geopolitics
twitter search "geopolitics world news" -n 10
```

## Notes

- Auth tokens live in `.env` (TWITTER_AUTH_TOKEN + TWITTER_CT0)
- venv must be activated for the twitter-cli command
- twitter-cli v0.8.5
- Output is YAML — parseable but verbose, filter for relevant tweets

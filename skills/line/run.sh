#!/usr/bin/env bash
# Launch Smith LINE webhook handler.
# Sources credentials from ~/.config/smith/.env
set -u

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="${HOME}/.config/smith/.env"

if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck source=/dev/null
  . "$ENV_FILE"
  set +a
fi

if [ -z "${LINE_CHANNEL_SECRET:-}" ] || [ -z "${LINE_CHANNEL_ACCESS_TOKEN:-}" ]; then
  echo "Missing LINE_CHANNEL_SECRET or LINE_CHANNEL_ACCESS_TOKEN"
  echo "  Check ~/.config/smith/.env"
  exit 1
fi

exec python3 "$SCRIPT_DIR/handler.py"

#!/usr/bin/env bash
set -euo pipefail
/Users/Jeff/.local/bin/hermes gateway restart
sleep 3
/Users/Jeff/.local/bin/hermes gateway status

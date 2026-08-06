# LINE channel repair — 2026-08-03 13:14 +0700

## Symptom
LINE channel appeared not to work.

## Findings
- Hermes LINE credentials and home channel were present in `/Users/Jeff/Smith/.env`.
- The running Hermes gateway was listening locally on `127.0.0.1:8646`.
- Local LINE health endpoint was healthy: `http://127.0.0.1:8646/line/webhook/health` → HTTP 200.
- Cloudflare Tunnel ingress incorrectly routed `line.bestwuttipong.dev` to `127.0.0.1:8080`, where nothing was listening; public health returned HTTP 502.
- Hermes LINE webhook path is `/line/webhook`.

## Repair
Changed `/Users/Jeff/.cloudflared/config.yml`:

```yaml
- hostname: line.bestwuttipong.dev
  service: http://127.0.0.1:8646
```

Validated the tunnel configuration and restarted `com.cloudflared.bedwuttipong` via launchd.

## Verification
- Local health: HTTP 200.
- Public health: HTTP 200, body `{"status": "ok", "platform": "line"}`.
- `hermes send --list line --json` sees home channel `U5d4e71e891666ec6b23cb81375bac82d`.
- No outbound LINE test message was sent; send `/status` from LINE to test the bot.

## Remaining issue
`hermes gateway status` still reports the gateway service definition as stale and the active gateway as a detached process (PID 30260). This did not prevent the LINE webhook from functioning, but the service topology should be cleaned up separately.

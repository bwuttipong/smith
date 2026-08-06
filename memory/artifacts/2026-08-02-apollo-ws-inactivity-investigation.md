# Apollo WS Inactivity Investigation

**Date:** 2026-08-02
**Reported message:** `[voice/WS path] no meaningful Hermes activity for 120s; the turn was stopped — last seen: starting Hermes turn…`

## Diagnosis

This is not an Edge TTS failure. It is the Apollo WebSocket watchdog in `src/server/apollo-ws.ts`.

The watchdog starts a 120-second meaningful-activity timer after sending the user's text to the persistent Hermes CLI. It resets only when it parses a tool event, initialization event, reply text, or other non-chrome Hermes output. The reported `last seen: starting Hermes turn…` means no parseable Hermes activity arrived for the full window. The implementation retries one idle timeout with a fresh Hermes process; the message appears after the retry also remains silent.

Likely failure class: transient Hermes/model-provider stall or a wedged persistent PTY/CLI process before the first streamed model activity. It is distinct from the 30-second Edge TTS timeout.

## Evidence

- The persistent Hermes child has `/Users/Jeff/Smith/state.db` open, so it is using the Smith state store.
- A controlled fresh WS request (`Reply with exactly: OK`) completed successfully in approximately 8 seconds:
  - `runtime`
  - `thinking`
  - `warming persistent Hermes session…`
  - `starting Hermes turn…`
  - initialization/tool steps
  - response chunk `OK`
  - `done`
- No permanent WS or provider failure was reproduced.
- The current source notes a known limitation: a PTY bridge can remain alive while the wrapped Hermes CLI is wedged, which is indistinguishable from legitimate model silence without an active probe.

## Immediate recovery

Restart the AgentOS dev stack / Apollo WS process so the persistent Hermes session is replaced. A stale or wedged PTY is not repaired by refreshing the browser alone.

## Remaining engineering gap

The watchdog detects and retries the silence but cannot identify whether the cause is provider latency, an auth/network stall, or the wrapped CLI/PTY wedging. A stronger follow-up would add a bounded model-request watchdog or a deliberate process-group restart/active probe, then surface the provider/runtime reason instead of waiting two full 120-second windows.

## Scope

No code was changed during this investigation.

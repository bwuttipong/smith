# LINE Handoff — OmniRouter custom provider / OpenCode free models

Timestamp: 2026-08-06 08:27:30 +07
Platform handoff target: LINE chat with Smith

## User intent
Jeff said: “Hand off I will chat on you with LINE.”
Meaning: when Jeff continues on LINE, preserve the OmniRouter/OpenCode model-check context and answer directly without asking him to repeat it.

English polish if useful: “I’ll chat with you on LINE.”

## Current technical context
- OmniRouter custom provider endpoint: `http://127.0.0.1:20128/v1`
- Hermes provider slug in `/Users/Jeff/Smith/config.yaml`: `omnirouter`
- Provider name: `OmniRouter`
- Key env: `OMNIROUTER_API_KEY`
- Current configured default model in provider block: `gemini/gemini-3.5-flash`

## Completed check
Smith queried OmniRoute `/v1/models` and smoke-tested candidate routes via `/v1/chat/completions` using prompt `Reply exactly OK`.

Results:
- Total models exposed: 220
- Generic free custom-provider routes that passed smoke test:
  - `auto/coding:free`
  - `kc/openrouter/free`
  - `kilocode/openrouter/free`
- OpenCode namespace models advertised but unavailable right now:
  - `opencode/big-pickle`
  - `opencode/deepseek-v4-flash-free`
  - `opencode/mimo-v2.5-free`
  - `opencode/ling-3.0-flash-free`
  - `opencode/nemotron-3-ultra-free`
  - `opencode/north-mini-code-free`
  - `opencode/laguna-s-2.1-free`
  - `opencode/longcat-2.0-free`
- All 8 `opencode/*` routes failed smoke test with HTTP 403 `insufficient_quota`.

## Artifacts
- `/Users/Jeff/Smith/memory/artifacts/2026-08-06-0728-omnirouter-custom-provider-free-models.json`
- `/Users/Jeff/Smith/memory/artifacts/2026-08-06-0729-omnirouter-opencode-namespace-smoke.json`
- This handoff: `/Users/Jeff/Smith/memory/artifacts/2026-08-06-line-handoff-omnirouter.md`

## Recommended LINE response if Jeff asks “what should I use?”
Use `auto/coding:free` first. If it acts weird, try `kc/openrouter/free`, then `kilocode/openrouter/free`. Do not recommend `opencode/*-free` until quota recovers.

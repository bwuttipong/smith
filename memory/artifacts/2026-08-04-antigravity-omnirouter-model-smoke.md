# Antigravity OmniRouter model smoke test

Timestamp: 2026-08-04 16:32 +07
Endpoint: http://localhost:20128/v1
Test: POST /v1/chat/completions with `Reply exactly OK`, max_tokens=8, temperature=0

## Summary

- Antigravity models exposed by OmniRouter: 30
- Chat-capable models tested: 29
- Passing chat models: 0
- Common failure: HTTP 429 — `All antigravity accounts have exhausted their quota (reset after 23h 50m 12s)`
- Image model: `antigravity/gemini-3.1-flash-image` returned HTTP 400 on chat endpoint because it requires `/v1/images/generations`; not tested further because media generation requires explicit approval.

## Results

| Model | Result | Notes |
|---|---:|---|
| antigravity/gemini-3.6-flash-high | 429 | quota exhausted |
| antigravity/gemini-3.6-flash-medium | 429 | quota exhausted |
| antigravity/gemini-3.6-flash-low | 429 | quota exhausted |
| antigravity/claude-opus-4-6-thinking | 429 | quota exhausted |
| antigravity/claude-sonnet-4-6 | 429 | quota exhausted |
| antigravity/gemini-pro-agent | 429 | quota exhausted |
| antigravity/gemini-3.1-pro-low | 429 | quota exhausted |
| antigravity/gemini-3-flash-agent | 429 | quota exhausted |
| antigravity/gemini-3.5-flash-low | 429 | quota exhausted |
| antigravity/gemini-3.5-flash-extra-low | 429 | quota exhausted |
| antigravity/gemini-3.1-flash-lite | 429 | quota exhausted |
| antigravity/gemini-2.5-flash-thinking | 429 | quota exhausted |
| antigravity/gemini-2.5-flash | 429 | quota exhausted |
| antigravity/gemini-2.5-flash-lite | 429 | quota exhausted |
| antigravity/gpt-oss-120b-medium | 429 | quota exhausted |
| antigravity/gemini-3.1-flash-image | 400 | image model; use `/v1/images/generations` |
| antigravity/claude-opus-4-6-thinking-low | 429 | quota exhausted |
| antigravity/claude-opus-4-6-thinking-medium | 429 | quota exhausted |
| antigravity/claude-opus-4-6-thinking-high | 429 | quota exhausted |
| antigravity/claude-sonnet-4-6-low | 429 | quota exhausted |
| antigravity/claude-sonnet-4-6-medium | 429 | quota exhausted |
| antigravity/claude-sonnet-4-6-high | 429 | quota exhausted |
| no-think/antigravity/claude-opus-4-6-thinking | 429 | quota exhausted |
| no-think/antigravity/claude-sonnet-4-6 | 429 | quota exhausted |
| no-think/antigravity/claude-opus-4-6-thinking-low | 429 | quota exhausted |
| no-think/antigravity/claude-opus-4-6-thinking-medium | 429 | quota exhausted |
| no-think/antigravity/claude-opus-4-6-thinking-high | 429 | quota exhausted |
| no-think/antigravity/claude-sonnet-4-6-low | 429 | quota exhausted |
| no-think/antigravity/claude-sonnet-4-6-medium | 429 | quota exhausted |
| no-think/antigravity/claude-sonnet-4-6-high | 429 | quota exhausted |

## Recommendation

Do not use Antigravity through OmniRouter until account quota resets or another Antigravity account is added. Current working fallback should stay on OmniRouter non-Antigravity models such as `gemini/gemini-3.5-flash`.

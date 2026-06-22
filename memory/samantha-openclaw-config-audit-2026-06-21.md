# OpenClaw Config Audit — 2026-06-21

**Requested by:** Jeff (via Smith)  
**Run by:** Samantha (subagent)  
**Scope:** Read-only audit of OpenClaw gateway config at `/Users/Jeff/.openclaw/openclaw.json`

## TL;DR

| # | Issue | Status |
|---|-------|--------|
| 1 | Groq auth profile | ✅ **Fully working** (env key set, API returns 200) |
| 2 | Broken model alias (`groq/llama-3.1-70b-versatile`) | ❌ **Broken** — model decommissioned by Groq |
| 3 | Qwen prefix fix (Groq provider model IDs include `groq/` prefix) | ⚠️ **Partially fixed** — config still has the bad prefix; API rejects prefixed IDs; bare IDs work |

---

## 1. Groq auth profile — ✅ Fully working

**Config (`openclaw.json`):**
- Provider in `models.providers.groq`: configured with `apiKey: "${GROQ_API_KEY}"`, `baseUrl: "https://api.groq.com/openai/v1"`
- **No `groq:default` entry in `auth.profiles`** — unlike the other providers (openai, openrouter, nvidia, ollama, opencode-go, etc.) which all have a `<provider>:default` entry. The groq provider is wired via the embedded `${GROQ_API_KEY}` in `models.providers.groq.apiKey` instead, which is a different mechanism.
- Groq plugin: enabled (`plugins.entries.groq.enabled: true`)

**Runtime check:**
- Env: `GROQ_API_KEY` is set (length 56)
- Live API call: `POST /openai/v1/chat/completions` with `model: "compound-beta"` → **HTTP 200**, response includes usage breakdown and `x_groq` metadata. Authentication works end-to-end.

**Verdict:** **Fully working.** The missing `groq:default` auth profile is a cosmetic gap (Smith flagged it in earlier audits) but does not block the API — the embedded `apiKey` field in the provider block covers it.

---

## 2. Broken model alias — ❌ Broken (`groq/llama-3.1-70b-versatile`)

**Config (`openclaw.json`):**
- Model `groq/llama-3.1-70b-versatile` appears in `agents.defaults.models` allowlist.
- Underlying provider model in `models.providers.groq.models`:
  ```json
  {
    "id": "llama-3.1-70b-versatile",
    "name": "Llama 3.1 70B Versatile",
    "maxTokens": 1024,
    "reasoning": false
  }
  ```

**Runtime check:**
- Live API call with bare id `llama-3.1-70b-versatile` → **HTTP 400**, body: `"The model \`llama-3.1-70b-versatile\` has been decommissioned and is no longer supported. Please refer to https://console.groq.com/docs/deprecations..."` (error code `model_decommissioned`).
- With `groq/` prefix → **HTTP 404** `model_not_found` (this is the prefix issue from #3, not the deprecation).

**Groq's currently active replacements** (from `/v1/models`):
- `llama-3.3-70b-versatile` (closest successor, context 131k, output 32k)
- `llama-3.1-8b-instant` (smaller, still active)
- `meta-llama/llama-4-scout-17b-16e-instruct` (newer, supports tools)

**Verdict:** **Broken.** The alias is still in the allowlist and would surface in `/model` listings, but any attempt to actually call it returns a decommission error. Jeff should either remove it or repoint to `llama-3.3-70b-versatile`.

---

## 3. Qwen prefix fix — ⚠️ Partially fixed

**Config (`openclaw.json`):**
- `agents.defaults.models` allowlist includes these Groq entries with a `groq/` prefix:
  - `groq/qwen/qwen3-32b`
  - `groq/llama-3.1-70b-versatile` (see #2)
  - `groq/compound-beta`
- Underlying provider model in `models.providers.groq.models`:
  - `id: "qwen/qwen3-32b"` (no `groq/` prefix here — this part is correct)
  - `id: "compound-beta"` (no `groq/` prefix here either)
  - `id: "llama-3.1-70b-versatile"` (no `groq/` prefix)

**Live API tests against Groq:**

| Request `model:` | HTTP | Result |
|------------------|------|--------|
| `qwen/qwen3-32b` (bare) | 200 | ✅ works, response model: `qwen/qwen3-32b` |
| `groq/qwen/qwen3-32b` (with prefix) | 404 | ❌ `model_not_found` |
| `compound-beta` (bare) | 200 | ✅ works, response model: `groq/compound` (Groq normalizes the id) |
| `groq/compound-beta` (with prefix) | 404 | ❌ `model_not_found` |
| `llama-3.1-70b-versatile` (bare) | 400 | ❌ decommissioned (separate issue, see #2) |

**Diagnosis:** The gateway allowlist and the routing layer both treat `groq/...` as a fully-qualified model reference (provider prefix + model id). But Groq's own API only accepts the bare model id (`qwen/qwen3-32b`, `compound-beta`). Adding the `groq/` provider prefix to the model id at routing time breaks the call.

This affects:
- The qwen model specifically (`qwen/qwen3-32b` → bare works, `groq/qwen/qwen3-32b` → fails)
- The compound model (Samantha's own primary, `groq/compound-beta` → fails when routed as-is)
- Any future Groq model that lands in the allowlist with the `groq/` prefix prepended

**Verdict:** **Partially fixed.** The underlying provider `models` array has the right (unprefixed) ids, which is why the `groq` provider block itself is correct. But the **allowlist in `agents.defaults.models` and the agent-level model references (Samantha's `primary: "groq/compound-beta"`) carry the bad `groq/` prefix**, so when the gateway resolves a `primary` or `/model` selection it constructs `groq/<model-id>` and Groq rejects it. The fix would be to strip the `groq/` prefix from all Groq model references in `agents.defaults.models` and in each agent's `model.primary` / `model.fallbacks`.

**Specific entries to clean up:**
- `agents.defaults.models.allowlist`: drop `groq/` from `groq/qwen/qwen3-32b` → `qwen/qwen3-32b`; from `groq/compound-beta` → `compound-beta`; from `groq/llama-3.1-70b-versatile` (and consider removing or repointing per #2).
- `agents.list[].model.primary` and `model.fallbacks` for agents that use Groq: currently only Samantha (`primary: "groq/compound-beta"`).

---

## Appendix — Raw evidence

### `agents.defaults.models` allowlist (Groq entries, as found)
```
groq/qwen/qwen3-32b
groq/llama-3.1-70b-versatile
groq/compound-beta
```

### `models.providers.groq` (as found)
```json
{
  "api": "openai-completions",
  "apiKey": "${GROQ_API_KEY}",
  "baseUrl": "https://api.groq.com/openai/v1",
  "models": [
    { "id": "qwen/qwen3-32b", "maxTokens": 4096, "reasoning": true, ... },
    { "id": "llama-3.1-70b-versatile", "maxTokens": 1024, "reasoning": false, ... },
    { "id": "compound-beta", "maxTokens": 1024, "reasoning": false, ... }
  ]
}
```

### `auth.profiles` (Groq-relevant)
- No `groq:default` entry. Other providers (openai, openrouter, nvidia, ollama, opencode-go, google, lmstudio, opencode) all have `<provider>:default` entries.
- Groq auth is delivered via the embedded `${GROQ_API_KEY}` in `models.providers.groq.apiKey` instead.

### `auth.profiles` for `groq` after the audit
None. Still relying on embedded `apiKey` in the provider block.

### Live API test summary
- `compound-beta` → 200 ✅
- `groq/compound-beta` → 404 ❌
- `qwen/qwen3-32b` → 200 ✅
- `groq/qwen/qwen3-32b` → 404 ❌
- `llama-3.1-70b-versatile` → 400 ❌ (decommissioned)
- `groq/llama-3.1-70b-versatile` → 404 ❌

### Groq active model list (relevant subset from `/v1/models`)
- `groq/compound` (mapped to `compound-beta` in the user's mind — this is Samantha's model)
- `groq/compound-mini`
- `qwen/qwen3-32b`
- `qwen/qwen3.6-27b`
- `llama-3.3-70b-versatile` (replacement for 3.1-70b)
- `llama-3.1-8b-instant`
- `meta-llama/llama-4-scout-17b-16e-instruct`
- `openai/gpt-oss-20b`, `openai/gpt-oss-120b`
- `openai/gpt-oss-safeguard-20b`

### Env vars
- `GROQ_API_KEY`: SET (length 56)
- `OPENCODE_API_KEY`: SET (length 67)
- `OPENROUTER_API_KEY`: SET (length 73)
- `OPENCLAW_GATEWAY_TOKEN`: SET (length 48)

---

## Recommended next steps (for Jeff's consideration — no changes made in this audit)

1. **Remove `groq/llama-3.1-70b-versatile`** from `agents.defaults.models` (decommissioned). Optionally add `llama-3.3-70b-versatile` as a replacement.
2. **Strip the `groq/` prefix** from `groq/qwen/qwen3-32b` and `groq/compound-beta` in `agents.defaults.models` and from Samantha's `primary: "groq/compound-beta"` in `agents.list`.
3. **Optionally add a `groq:default` auth profile** for consistency with the other providers — purely cosmetic since the embedded `apiKey` already works.

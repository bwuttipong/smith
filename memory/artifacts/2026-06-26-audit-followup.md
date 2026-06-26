# System Audit Follow-up - 2026-06-26

## 1. Small Model No Sandbox (CRITICAL)
- **Status Check:** `ollama/gemma4:31b-cloud` is the default model. Sandbox is currently `off` while web tools are enabled, posing a critical security risk.
- **Analysis of Fixes:**
    - **Option A: Deny web tools for this provider** (`tools.byProvider["ollama/gemma4:31b-cloud"].deny=["group:web","browser"]`)
        - *Pros:* Immediate mitigation; keeps the model as default.
        - *Cons:* Model loses all web capabilities.
    - **Option B: Force all sandboxing** (`agents.defaults.sandbox.mode="all"`)
        - *Pros:* Comprehensive security; protects all models.
        - *Cons:* May introduce performance overhead or compatibility issues for some local tools.
    - **Option C: Change default model** (e.g., to a larger, sandboxed model)
        - *Pros:* Best performance/security balance if a suitable alternative exists.
        - *Cons:* Higher resource usage (RAM/VRAM).
- **Recommendation:** **Option B** as the baseline security policy, complemented by **Option A** if specific high-risk tools must be disabled for the 31B model.
- **Priority:** **NOW**

## 2. google-gemini-cli OAuth
- **Status Check:** `openclaw doctor` reports `google-gemini-cli:bed.wuttipong@gmail.com` is **expiring in 45 minutes** (as of 07:06 BKK).
- **Recommendation:** Re-authenticate immediately to avoid service interruption.
- **Steps:** Run `openclaw models auth login --provider google-gemini-cli`.
- **Priority:** **NOW**

## 3. xAI OAuth Expired
- **Status Check:** `openclaw doctor` reports `xai:bed.wuttipong@gmail.com` is **expiring in 6 hours**. (The audit finding mentioned "stale, ~20 days old", but the current runtime state shows a short-term expiration. Either it was recently refreshed or the "stale" finding was outdated).
- **Recommendation:** Re-authenticate now to prevent failure during the day.
- **Steps:** Run `openclaw models auth login --provider xai`.
- **Priority:** **TODAY**

## 4. Stale `openclaw-web-search` Plugin Config
- **Status Check:** `openclaw doctor --fix` was executed. However, the output shows that `openclaw-web-search` still has a **packaging issue** (missing compiled JS files) and a **stale config entry** that was ignored but not fully removed from the JSON.
- **Recommendation:** Manually remove `openclaw-web-search` from `plugins.entries` and `plugins.allow` in `~/.openclaw/openclaw.json` since the publisher has not shipped the compiled runtime.
- **Priority:** **TODAY**

## 5. Plaintext Secret Findings (41 findings)
- **Status Check:** Audit found 41 plaintext secrets (API keys, bot tokens) in config files and SQLite.
- **Risk Assessment:** **HIGH**. Any compromise of the filesystem or a rogue plugin could exfiltrate these keys.
- **Recommendation:** 
    1. **Rotation:** Immediately rotate all leaked API keys.
    2. **Migration:** Move secrets to the OpenClaw secure auth-profile SQLite store or a dedicated secret manager (e.g., 1Password via skill).
    3. **Cleanup:** Use `sed` or similar to scrub secrets from plaintext files and `DELETE` from SQLite tables.
- **Priority:** **THIS WEEK**

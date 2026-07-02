# Comparing Free Models on OpenRouter

## How to Compare

Navigate to each model's page on OpenRouter and extract:

| Spec | Where on the page | Why it matters |
|------|-------------------|----------------|
| **Parameters** (active/total) | Below model name | Active params = inference cost; total = capability ceiling |
| **Context window** | "CONTEXT" section | Determines max input size for long tasks |
| **Max output** | Model description | Important for code generation / long-form writing |
| **Latency** | Providers table → "Latency" column | Time to first token (seconds) |
| **Throughput** | Providers table → "Throughput" column | Tokens per second after first token |
| **Uptime** | Providers table → "Uptime" column | Reliability — below 95% = flaky |
| **Weekly tokens** | Badge next to model name | Community usage = proxy for quality/trust |
| **Category rankings** | Tag buttons below model name | OpenRouter's Programming/Finance/etc. rankings |
| **Privacy** | Provider row icon | "Trains" = data used for training; "Logs" = logged but not trained on |
| **Release date** | "RELEASED" section | Newer ≠ better, but indicates iteration speed |

## URL Pattern

Search: `https://openrouter.ai/models?q=<search-term>`
Direct model page: `https://openrouter.ai/<provider>/<model-slug>`
Model doesn't exist: page shows "The model X is not available" with Discord link

## Key Decision Framework

**For coding tasks:**
1. Programming ranking (lower = better)
2. Throughput (code gen needs speed)
3. Max output tokens (long code needs big output)

**For general/reasoning tasks:**
1. Context window size
2. Active parameters (more = generally smarter)
3. Category breadth (good across multiple categories = versatile)

**For reliability (unattended/cron use):**
1. Uptime (>98% preferred)
2. Latency (lower = faster failover)
3. Weekly token volume (more users = more stable infra)

## Pitfalls

- **Stale model references**: Models get removed from OpenRouter without notice. Always verify a model exists by navigating to its page before promising it to the user. A "not available" page means it's gone.
- **Free tier data privacy**: "Trains" means your inputs may be used for training. "Logs" means logged but not trained on. Both are privacy trade-offs — flag this to users who care.
- **Category rankings shift**: Rankings are relative to other models and change weekly. A #12 today might be #20 next month. Always re-check when advising.
- **Search quirks**: Some model names don't search well (e.g., "owl alpha" returns nothing). Try searching by provider name (e.g., "nousresearch") if the model name fails.

## Reference: July 2026 Snapshot

### Nemotron 3 Ultra (nvidia/nemotron-3-ultra-550b-a55b:free)
- 55B active / 550B total (MoE), Transformer-Mamba hybrid
- 1M context, released Jun 4 2026
- 2.95s latency, 15 tps, 97.60% uptime
- 882B weekly tokens (most popular)
- Rankings: Programming #50, Finance #31, Legal #38
- Best for: long-context reasoning, research, enterprise tasks

### Laguna M.1 (poolside/laguna-m.1:free)
- Large model, NVFP4 quantized, 256K context, 32K output
- Released Apr 28 2026
- 1.02s latency, 33 tps, 98.78% uptime
- 807B weekly tokens
- Rankings: Programming #12, Finance #28, Science #16, SEO #44
- Best for: agentic coding, software engineering

### North Mini Code (cohere/north-mini-code:free)
- 3B active / 30B total (MoE), 256K context, 64K output
- Released Jun 18 2026
- 0.46s latency, 63 tps, 97.59% uptime
- 152B weekly tokens
- Rankings: Programming #16, Technology #47, Science #39
- Best for: fast code gen, local inference, tool-calling agents

### Owl Alpha (nousresearch/owl-alpha)
- **Not available on OpenRouter** as of Jul 2026 — page returns "model not available"
- Previously referenced in Hermes config for coding tasks; likely deprecated or renamed
- If user's config still references `openrouter/owl-alpha`, flag it as stale and suggest Laguna M.1 or North Mini Code as replacement

### Quick Verdict (as of Jul 2026)
- **Coding**: Laguna M.1 (#12 programming, good speed, high uptime)
- **Speed**: North Mini Code (63 tps, 0.46s latency, runs locally)
- **General/Research**: Nemotron 3 Ultra (1M context, most popular)

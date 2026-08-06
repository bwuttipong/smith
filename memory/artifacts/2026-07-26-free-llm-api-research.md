# Free LLM API research — 2026-07-26 21:53 +07

## Short answer
Best practical stack for Jeff/Smith:
1. OpenRouter free models/router for broad no-cost experimentation.
2. Google Gemini API free tier for strong quality, especially Gemini 2.5 Flash / 3.5 Flash, accepting that free-tier data may be used to improve Google products.
3. Groq free/dev plan for fast inference and OpenAI-compatible API testing.
4. Cloudflare Workers AI only if already building near Cloudflare; the free daily allowance is small but reliable.
5. Hugging Face Inference Providers is useful as a gateway, but the free monthly credit is tiny.

## Findings

### OpenRouter
- Source checked: https://openrouter.ai/api/v1/models
- Live endpoint returned 18 zero-priced models.
- Notable free entries found:
  - openrouter/free — 200k context, smart free-model router.
  - google/gemma-4-26b-a4b-it:free — 262k context.
  - google/gemma-4-31b-it:free — 262k context.
  - openai/gpt-oss-20b:free — 131k context.
  - nvidia/nemotron-3-ultra-550b-a55b:free — 1M context.
  - cohere/north-mini-code:free — 256k context.
- Caveat: Jeff's memory says Gemma 4 free rejects some OpenClaw agent/tool payloads with HTTP 400, so use openrouter/free first and Gemma as fallback/test only.

### Google Gemini API
- Sources checked:
  - https://ai.google.dev/gemini-api/docs/pricing
  - https://ai.google.dev/gemini-api/docs/rate-limits
- Free tier includes free input/output tokens for certain models and Google AI Studio access.
- Pricing page explicitly showed Gemini 2.5 Flash and Gemini 3.5 Flash standard free-tier input/output as free of charge.
- Free tier content may be used to improve Google products; paid tier says no.
- Rate limits vary by model/project and are visible in AI Studio.

### Groq
- Sources checked:
  - https://console.groq.com/docs/rate-limits
  - https://console.groq.com/docs/models
- Groq documents free plan limits and OpenAI-compatible access, with limits measured by requests/tokens per minute and org-level caps.
- Exact org limits are visible on the Groq console limits page rather than hard-coded universally.
- Best use: speed tests, small apps, low-latency chat, not guaranteed free production scale.

### Cloudflare Workers AI
- Source checked: https://developers.cloudflare.com/workers-ai/platform/pricing/index.md
- Free allocation: 10,000 Neurons per day.
- Paid overage: $0.011 per 1,000 Neurons on Workers Paid.
- Best use: Cloudflare-native apps, Workers, edge demos. Not the best general-purpose free LLM API unless the app already lives on Cloudflare.

### Hugging Face Inference Providers
- Source checked: https://huggingface.co/docs/inference-providers/pricing.md
- Free users get $0.10 monthly credits, subject to change.
- PRO users get $2.00 monthly credits; Team/Enterprise get $2.00 per seat.
- Best use: model/provider experimentation under one token, not meaningful sustained free usage.

## Recommendation
Use OpenRouter as the default free aggregator, Gemini API as the quality fallback/free direct provider, and Groq for latency-sensitive tests. Avoid depending on Hugging Face free credits for anything beyond smoke tests; $0.10/month is a polite sneeze, not a budget.

## Verification
- Used live OpenRouter models API and counted zero-price entries.
- Retrieved official provider documentation pages for Google, Groq, Cloudflare, and Hugging Face.
- Confirmed local `freeride` CLI exists but `OPENROUTER_API_KEY` is not set in this shell.

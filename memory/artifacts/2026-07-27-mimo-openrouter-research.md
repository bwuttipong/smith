# MiMo-V2.5 OpenRouter Research

Timestamp: 2026-07-27 14:33 +07
Artifact: `/Users/Jeff/.agentos/apps/mimo-openrouter-usage-costs.html`

## User request
Research public usage of Xiaomi MiMo-V2.5 on OpenRouter over roughly the last 3 months, summarize daily-life use cases in 3 bullets, estimate genuine monthly costs by usage group, and build a gorgeous HTML/CSS presentation for AgentOS.

## Sources checked
- OpenRouter rankings: https://openrouter.ai/rankings
- OpenRouter MiMo-V2.5 model card: https://openrouter.ai/xiaomi/mimo-v2.5
- ChatForest builder log, published 2026-07-15: https://chatforest.com/builders-log/xiaomi-mimo-openrouter-chinese-ai-token-volume-builder-guide/
- YouTube search results for MiMo-V2.5 OpenRouter: recent videos 2 months, 1 month, 2 weeks old.
- LLMReference pricing mirror: https://www.llmreference.com/provider/openrouter/mimo-v2-5
- TypingMind OpenRouter MiMo-V2.5 guide: https://www.typingmind.com/guide/openrouter/mimo-v2.5

## Tool/source limits
- Google blocked automated search.
- Perplexity blocked with Cloudflare.
- Reddit JSON returned 403.
- last30days script returned Reddit 401 and X 400; no social API results.
- Public personal monthly invoice data was sparse, so the cost section uses transparent estimates from token pricing rather than invented bills.

## Key findings
Three practical user categories:
1. Coding agents: OpenCode/Cursor-style workflows, multi-file edits, game/app/frontend generation tests, bug fixing, long tool-call chains.
2. Daily assistant/document work: TypingMind-style chat, agents, plugins, document chat, long context summarization.
3. High-volume pipelines: structured extraction, JSON/table cleanup, repetitive batch jobs, token-heavy production routing.

Price basis:
- OpenRouter/LLMReference list price: $0.14/M input tokens, $0.28/M output tokens.
- OpenRouter page also showed effective weighted input price around $0.012/M due caching and weighted output around $0.289/M.

Monthly estimate groups:
- Few: 0.05M in + 0.02M out/day → ~$0.38/mo list, ~$0.19/mo cached effective.
- Middle: 1M in + 0.35M out/day → ~$7.14/mo list, ~$3.39/mo cached effective.
- Heavy: 20M in + 6M out/day → ~$134.40/mo list, ~$59.22/mo cached effective.
- Extreme: 100M in + 25M out/day → ~$630/mo list, ~$252.75/mo cached effective.

## Smith verdict
MiMo-V2.5 is popular because it is good, huge-context, omnimodal, and cheap enough for token-heavy agent work. It is a daily workhorse, not necessarily the premium final-judgment model.

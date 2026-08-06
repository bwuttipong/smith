# Ollama research — 2026-07-28 11:50 +07

Sources checked: official home page, docs, quickstart, cloud docs, pricing page, blog index, GitHub API.

## Verdict
Ollama is evolving from a local open-model runner into a local-first model platform: local runtime, cloud offload, CLI/API, desktop apps, agent integrations, tool calling, structured outputs, vision, embeddings, and web search. It is worth testing for Jeff's local-agent stack, but cloud usage/capacity should be treated as fallback or augmentation rather than the sole backbone.

## Key points
- Runs open models locally on macOS, Windows, and Linux.
- Cloud models can run larger hosted models while keeping local tools and workflows.
- Cloud requires `ollama signin`; direct API uses `OLLAMA_API_KEY` and `https://ollama.com` as remote host.
- Pricing checked: Free $0; Pro $20/month or $200/year; Max $100/month but new sign-ups paused; Team coming soon.
- Cloud concurrency: Free 1 model, Pro 3 models, Max 10 models.
- Pro claims 50x more cloud usage than Free; Max claims 5x more than Pro.
- Usage is infrastructure/GPU-utilisation based, not fixed token/request caps.
- Upcoming cloud retirements: `minimax-m2.5` and `kimi-k2.5` on 2026-07-31, with recommended alternatives `minimax-m2.7` and `kimi-k2.6`.

## Engineering signal
GitHub API returned:
- Repo: `ollama/ollama`
- License: MIT
- Stars: 177,053
- Forks: 17,141
- Open issues: 3,541
- Updated: 2026-07-28T04:49:54Z
- Pushed: 2026-07-28T00:29:20Z

Recent blog themes from 2026: Apple Silicon MLX acceleration, GGUF support, NVIDIA Nemotron 3 Ultra, OpenJarvis, OpenClaw setup, Claude Code subagents/web search, `ollama launch`, image generation, Anthropic API compatibility, and Codex integration.

## Recommendation
For Jeff: test Ollama as a private/local runtime for small-to-mid models and as a simple compatibility layer for local agents. Use Ollama Cloud only as optional burst capacity until pricing/usage visibility becomes less misty.

Dashboard artifact: `/Users/Jeff/.agentos/apps/ollama-research-2026-07-28.html`.

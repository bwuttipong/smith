# Nine Proxy model refresh — 2026-08-03

Command attempted:

```bash
hermes model --refresh
```

The non-interactive shell rejected it, so it was rerun in a real tmux PTY. The provider picker was navigated to **Nine Proxy** and its live model list was fetched.

Result: Nine Proxy exposes a generic `openrouter/openrouter/free` route, but no `deepseek/deepseek-v4-flash`, `deepseek-v4-flash`, or other DeepSeek Flash model. The picker was cancelled before selecting a model; no active model or config was changed.

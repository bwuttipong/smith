# Hermes → Claude Code CLI subagent

- Date: 2026-08-02
- Hermes: v0.19.1
- Claude Code: v2.1.212 at `/opt/homebrew/bin/claude`
- Hermes toolsets: `terminal`, `file`, and `delegation` enabled
- Claude Code authentication: expired; run `claude auth login`
- Recommended integration: Hermes launches Claude Code in non-interactive print mode with `claude -p`, an explicit workdir, allowed tools, turn limit, and JSON output; Hermes then independently inspects the diff and runs tests.
- Important distinction: Hermes `delegate_task` creates a Hermes child agent. Configuring it with an Anthropic model does not turn it into the Claude Code CLI.
- Interactive Claude Code work should run through tmux; bounded one-shot work should use print mode.
- Sources checked: installed CLI help, Hermes delegation documentation, local `hermes-agent` and `coding-agents` skills.

---
name: coding-agents
description: Use when delegating implementation work to an autonomous coding CLI (OpenAI Codex, Anthropic Claude Code, OpenCode). Covers CLI invocation patterns, PTY/tmux orchestration, worktree isolation, PR review workflows, verification, and provider-specific quirks. Load instead of a narrower single-CLI skill when the task is "use a coding agent" and the specific CLI is secondary to the workflow.
version: 1.0.0
license: MIT
metadata:
  hermes:
    tags: [coding-agents, codex, claude-code, opencode, autonomous-agents, pty, worktrees, code-review]
    related_skills: [systematic-debugging, python-debugpy, node-inspect-debugger]
---

# Coding Agents — Autonomous CLI Orchestration

This umbrella replaces three narrow skills (`claude-code`, `codex`, `opencode`) with a single workflow guide. The agent commands change; the *orchestration shape* (one-shot vs interactive, worktree isolation, background monitoring, PR review, verification, cleanup) is the shared class.

## Provider selection

| CLI | Auth | Best for |
|-----|------|----------|
| **Codex** (`codex`) | `OPENAI_API_KEY` or `~/.codex/auth.json` | One-shot edits, parallel worktrees, batch PR review |
| **Claude Code** (`claude`) | `ANTHROPIC_API_KEY` or OAuth | Print-mode automation, deep interactive refactors, JSON-schema extraction |
| **OpenCode** (`opencode`) | `OPENROUTER_API_KEY` or provider env | Open-source fallback, provider-agnostic sessions, parallel runs |

Use the provider the user prefers or the one available in the current environment. When in doubt, check availability with `command -v <cli>` and `cli --version`; fall back if the required CLI is missing.

## Invocation quick map

| Need | Codex | Claude Code | OpenCode |
|------|-------|-------------|----------|
| One-shot edit | `codex exec 'prompt'` | `claude -p 'prompt'` | `opencode run 'prompt'` |
| Interactive session | `codex exec --full-auto` in PTY | `claude` in PTY, usually via tmux | `opencode` in PTY |
| Background / long | `background=true, pty=true` then `process(poll/log)` | tmux session + `capture-pane` | `background=true, pty=true` + `process` |
| PR review | `codex review` or diff-prompt | `claude --from-pr <n>` | `opencode pr <n>` |
| Parallel work | Multiple `codex exec` in separate worktrees | Multiple tmux sessions | Multiple `opencode run` in separate dirs |

## Shared rules

1. **Worktree isolation.** Never run an autonomous coding CLI in the user's main dirty checkout. Create a branch/worktree. For Git repos: `git worktree add -b fix/issue-78 /tmp/issue-78 main`; run the CLI there; cherry-pick accepted commits back.
2. **PTY for interactive CLIs.** Codex, Claude Code, and OpenCode are terminal apps. Use `pty=true` in `terminal()`. For Claude Code interactive, prefer tmux because it gives `capture-pane` and `send-keys`.
3. **Verify before claiming.** Do not mark a task complete based on the agent's self-report alone. Inspect the diff (`git diff`), run canonical tests (Hermes `scripts/run_tests.sh` or the repo's documented wrapper), and only then complete/kill/cleanup.
4. **Cleanup.** Remove temporary worktrees and stop/kill background PTY sessions when the lane is accepted, rejected, or timed out. Preserve artifacts only when recording them explicitly in handoff metadata.
5. **Skill-specific quirks (see subsections).** Each CLI has its own flag conventions, auth paths, and dead-ends. Read the matching subsection before launching that CLI for the first time in a session.

## Codex (OpenAI)

- Requires Codex CLI installed: `npm install -g @openai/codex`.
- Auth: `OPENAI_API_KEY` or `~/.codex/auth.json`. Hermes `openai-codex` provider uses `~/.hermes/auth.json`.
- Must run inside a git repository; use `mktemp -d && git init` for scratch.
- `pty=true` always.
- Flags: `--full-auto` for auto-approve; `--yolo` for no sandbox.
- Background: `terminal(command="codex exec --full-auto '...'", workdir=..., background=true, pty=true)`.

## Claude Code (Anthropic)

- Install: `npm install -g @anthropic-ai/claude-code`.
- Auth: browser OAuth, `ANTHROPIC_API_KEY`, SSO.
- Two modes: print (`-p`) for automation; interactive via tmux for multi-turn.
- Print mode supports `--output-format json`, `--json-schema`, `--max-turns`, `--fallback-model`, `--bare`, `--allowedTools`.
- Interactive mode requires handling two dialogs: workspace trust (Enter) and permissions bypass (Down → Enter).
- `--max-budget-usd` minimum is ~$0.05 due to system prompt cache.

## OpenCode

- Install: `npm i -g opencode-ai@latest` or `brew install anomalyco/tap/opencode`.
- Auth: `opencode auth login` or provider env (`OPENROUTER_API_KEY`).
- `opencode run 'prompt'` is one-shot; interactive `opencode` needs PTY.
- Do NOT use `/exit` — use Ctrl+C (`\x03`) or `process(action="kill")`.
- `which -a opencode` to resolve binary collisions.

## PR review recipe

1. `git fetch` PR refs or clone to temp dir.
2. Run CLI in review mode against the PR diff.
3. Inspect CLI-reported findings; do not trust them verbatim.
4. Post results to the PR only after an independent review of the diff in Hermes.

## Parallel lanes

Launch one CLI process per lane in its own worktree. Limit concurrency to the user's hardware. Monitor via `process(action="list")` + per-lane `poll`/`log`. Collect commit SHAs, then cherry-pick/merge in a final integration step.

## When to prefer one CLI over another

- **Codex**: fastest for bounded diffs, simplest background story, OpenAI billing.
- **Claude Code**: best for JSON-structured output, large-context code review, multi-turn planning inside the agent.
- **OpenCode**: provider-agnostic, useful where OpenAI/Anthropic keys are unavailable.

## Further reading

- `references/claude-code.md` — full Claude Code flags, hooks, MCP, tmux orchestration (from `claude-code`)
- `references/codex.md` — Codex workflow patterns and background mode (from `codex`)
- `references/opencode.md` — OpenCode session/cost management and TUI notes (from `opencode`)
- `references/pr-review-merge.md` — PR review + merge recipe across CLIs

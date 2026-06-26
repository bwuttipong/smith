# Agent Lifecycle — OpenClaw

Session-derived reference for spawning / binding / inspecting agents via the `openclaw` CLI. Pairs with the SKILL.md workflow section.

## State check

```bash
openclaw agents list
```

Each agent shows a `Routing rules: N` count. **N=0 = dormant agent** (registered in `openclaw.json`, no channel routes). The "spawn" verb means wiring a channel to the agent — not creating it from scratch.

## Activation (dormant → live)

```bash
# 1. Confirm agent is dormant (Routing rules: 0)
openclaw agents list

# 2. Wire a channel to it
openclaw agents bind <agent-id> <channel[:accountId]>

# examples
openclaw agents bind samantha telegram
openclaw agents bind samantha telegram:samantha-bot   # if she has her own bot account
```

The `--bind` flag is repeatable. `accountId` is required for channels with multiple accounts (e.g. `discord:beaker`).

## First-time registration

```bash
openclaw agents add <name> \
  --workspace <dir> \
  --agent-dir <dir/agent> \
  --model <id> \
  --non-interactive
```

The workspace should already contain the persona files (`IDENTITY.md`, `SOUL.md`, `USER.md`, `AGENTS.md`) — the CLI doesn't create them.

## Pitfalls

- **`agents add` errors with "agent already exists"** when the config entry is present. Don't retry — the agent is already registered; use `agents bind` instead. (Verified 2026-06-24 with samantha.)
- **No `--bind` flag on `agents add`.** Bindings are a separate step (`agents bind`) regardless of whether you're creating a fresh agent or activating a dormant one. The `add` flow is for first-time registration; the `bind` flow is for channel wiring.
- **One telegram listener at a time.** The default `TELEGRAM_BOT_TOKEN` is bound to one agent. Re-binding it (e.g. `samantha`) will silence the previous one (e.g. `smith`) on telegram. Other channels (line, discord) can stay on smith.
- **Routing-rule count is the truth.** If `agents list` shows `Routing rules: 0`, the agent cannot receive messages regardless of how well its persona is written.

## Verification

After binding, run `openclaw agents list` and confirm `Routing rules: N` is now > 0 for the target agent. Channel-side, `openclaw channels status --probe` shows config-level status; live health needs a reachable gateway with a token.

## Session example — 2026-06-24

**Goal (Jeff's verb):** "spawn samantha" — make her a live general assistant.

**State at start:**
- `samantha` was already registered in `openclaw.json` with workspace + model set
- `~/Agents/Samantha/agent/` had full persona files (IDENTITY, SOUL, USER, AGENTS)
- 6+ memory files at `~/Smith/memory/samantha-*` showed she had already been doing real work (weather, audits, calendar, healthcheck) as a delegated subagent
- **But:** `openclaw agents list` showed `Routing rules: 0` — she was dormant for incoming messages

**Wrong move:** edit `openclaw.json` to add a `bindings` entry by hand. Risky, easy to mis-key, doesn't validate the way the CLI does.

**Right move:**
```bash
openclaw agents bind samantha telegram
```

…which wires the existing `telegram` channel to her. She comes online, smith goes silent on telegram (still alive on line/discord).

**What I did wrong first:** I gave Jeff a 4-option matrix ("A: full hand-off, B: keep smith reachable, C: both, D: full first-class") when the verb "spawn" already implied the action. He said "you don't need you just swawn her." Lesson: verbs like "spawn" / "set up" / "start" are unambiguous; act, report.

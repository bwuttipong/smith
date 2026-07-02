---
name: smith-local-stack
description: "Jeff's local runtime topology — which agent frameworks, gateways, dashboards, and daemons are running on his machine, what ports they use, and how to interact with each. Load when asked to open, start, stop, or check the status of any local web UI, gateway, dashboard, or agent runtime. Also load when confusion arises between openclaw and hermes surfaces."
version: 1.0.0
author: Smith
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [smith, topology, openclaw, hermes, gateway, dashboard, ports]
    homepage: null
---

# Smith Local Stack

The runtime topology on Jeff's Mac (verified 2026-06-24). The recurring failure mode this skill prevents: treating "openclaw" and "hermes" as the same thing, or assuming a hermes/openclaw web UI doesn't exist without checking.

## Port Map (quick reference)

| Port  | Service                  | Framework  | Notes                                                                 |
|-------|--------------------------|------------|-----------------------------------------------------------------------|
| 18789 | openclaw gateway         | openclaw   | Web control panel. Node. Always running (launchd-managed).            |
| 18790 | cloudflared forward      | openclaw   | External tunnel to 18789 (socat + cloudflared).                       |
| 9119  | hermes dashboard         | hermes     | Web control panel. Python uvicorn. **NOT running by default** — launch on demand with `hermes dashboard --port 9119`. |
| 11434 | ollama                   | ollama     | Local LLM inference.                                                 |

**Important — 9119 has two different meanings depending on context:**
- In the **default profile** (not this one), the hermes gateway itself binds 9119 (uvicorn + messaging).
- In the **smith profile**, the launchd-managed hermes gateway runs **headless with NO listening port** — it's messaging-only (telegram polling). To get a web UI on 9119, you must start `hermes dashboard` separately. The two are independent processes and don't conflict (dashboard just opens another uvicorn).

Full per-process detail (PIDs, cmdlines, last-verified timestamps) lives in `references/port-map.md`.

## Frameworks — don't conflate them

- **openclaw** — multi-platform messaging agent host. Gateway at 18789. Drives Discord, Slack, LINE, Telegram, etc. Has its own web control panel.
- **hermes-agent** — Nous Research agent framework. CLI: `hermes`. Web UI: `hermes dashboard` on 9119. Can run standalone or hosted inside an openclaw gateway.
- **ollama** — local LLM runtime. Not an agent framework; just inference. Used by the smith profile (`opencode-go/minimax-m3`).
- The smith profile is an **openclaw-hosted hermes agent** (gateway on 18789 wraps a hermes process). The hermes dashboard on 9119 is a separate web control plane for that same agent.

## Common commands

```bash
# Open the openclaw control panel (tokenized URL)
openclaw dashboard
# or visit directly: http://127.0.0.1:18789/chat?session=main

# Start the hermes dashboard (the real hermes web control)
hermes dashboard --port 9119 --skip-build --no-open
# Then open: http://127.0.0.1:9119

# Stop all running hermes dashboards
hermes dashboard --stop

# List running hermes dashboards
hermes dashboard --status

# Inspect the openclaw gateway
openclaw status
openclaw status --deep

# Restart the smith hermes gateway (launchd-managed, supervised path — USE THIS)
hermes gateway restart

# Check launchd state for both hermes services
launchctl list | grep hermes
# ai.hermes.gateway          (default profile)
# ai.hermes.gateway-smith    (smith — this is ours)
```

**"Restart the gateway" in the smith profile = `hermes gateway restart`.** Not `kill -9`, not `launchctl kickstart` (unless the supervised path is broken), not a foreground `python -m hermes_cli.main gateway run` (the supervised service will refuse with "A gateway is already running under launchd for this profile").

## Pitfalls

- **Don't say "X doesn't exist" without checking.** When the user asks about a hermes/openclaw feature, run `hermes <cmd> --help` or check `~/.hermes/hermes-agent/hermes_cli/subcommands/` first. Jeff has corrected this on 2026-06-24 (hermes dashboard).
- **Port 18789 ≠ port 9119.** Different frameworks, different web UIs. Never route a "open the hermes dashboard" request to the openclaw port or vice versa.
- **In the smith profile, the hermes gateway is HEADLESS — port 9119 is empty by default.** If `curl 127.0.0.1:9119` returns connection refused, that does NOT mean the gateway is down. The gateway is messaging-only (telegram/discord polling) and doesn't bind any port. To get a web UI on 9119, you must start `hermes dashboard` separately.
- **`hermes dashboard` needs the web build to be present.** Use `--skip-build` if `~/.hermes/hermes-agent/web/dist` exists; else run `cd ~/.hermes/hermes-agent/web && npm run build` first.
- **Background process pattern.** Use `terminal(background=true, notify_on_complete=True)` for long-running daemons like the hermes dashboard. Shell-level `nohup &` triggers Hermes' soft guard and errors out.
- **The hermes-agent skill is the canonical reference for hermes commands.** If it's loaded, consult it before declaring a hermes feature missing.
- **Never `kill -9` the hermes gateway while launchd is watching it.** It will leave the launchd label pointing at a dead PID, and the next time a new gateway tries to start, the Discord adapter fails with "Discord bot token already in use (PID XXXX)" because the old token-holding process is still being torn down. Always use `hermes gateway restart` so launchd sequences stop+start correctly.
- **Don't start a foreground `python -m hermes_cli.main gateway run` while the launchd service is alive.** The supervised service detects the conflict and refuses: "A gateway is already running under launchd for this profile." Use `--force` only if you know what you're doing.
- **Two `ai.hermes.gateway*` launchd labels exist.** `ai.hermes.gateway` is the default profile; `ai.hermes.gateway-smith` is ours. `launchctl list | grep hermes` shows both — make sure you restart the right one.
- **"Process alive" ≠ "gateway healthy".** After a restart, check `tail ~/.hermes/profiles/smith/logs/gateway.log` for "✓ telegram connected" and "Gateway running with N platform(s)" — a process with a PID can be alive but stuck mid-startup with zero platforms attached.
- **The MCP `qmd` server fails its 3 startup attempts on every gateway boot (recurring since at least 2026-06-24).** Symptom in `gateway.error.log`: "unhandled errors in a TaskGroup (1 sub-exception)". Not blocking — telegram/discord work fine without it.

### Cross-session continuity — when the user invokes "next me" (lesson from 2026-06-24)

When Jeff says things like "make sure Smith on Antigravity knows," "the next session should see this," or any explicit handoff to a future-me / different-deployment-me, the work must live in **three** places, not one:

1. **The artifact on disk** — runbook, doc, file, config. The thing itself.
2. **The cross-session `memory` tool** — durable, injected into every future turn. Use the `memory` tool, not just a daily file. The `memory` is the only thing that survives session reset and gets read in the very first turn of a new session.
3. **The daily file `~/Smith/memory/YYYY-MM-DD.md`** — the source of truth for "what happened today?" per `AGENTS.md`. Append, don't replace.

The failure mode: a runbook on disk alone is invisible to the next session that doesn't go look for it. A `memory` entry alone loses the full context. Both together is what lets the next me open up, read the first injected memory, and say "ah, here's what's going on."

**Workflow when handing off to future-me:**
1. Write the artifact to its final path (e.g. `~/Smith/docs/<topic>.md`).
2. Append a short entry to today's daily file — bullet, timestamp, pointer to the artifact.
3. Call the `memory` tool with the durable fact (project name, runbook path, key decision, next action).
4. Confirm all three before telling the user it's handed off.

This came up explicitly when Jeff asked: "did you brief that in to memory too otherwise you (Smith) on Antigravity, don't know what we're gonna be doing right now." Don't wait to be asked — if the work is project-shaped and you suspect another session will pick it up, do all three writes proactively.

## Telegram chat style (Jeff's preference, 2026-06-24)

When chatting with Jeff on telegram, **default to chat-style replies**:
- One or two short paragraphs max
- No lists, no tables, no headers, no bold-as-structure
- No "I'd be happy to help" or "great question" — no preamble
- Plain text, conversational, like texting

This is partly because of the upstream streaming-edit rendering bug (see `references/telegram-streaming-edit-bug.md`) and partly because Jeff has explicitly asked for it multiple times. **For long content (runbooks, audits, plans, research): write it to a file in `~/Smith/docs/`, `~/Smith/memory/`, or another path. Send a one-line pointer in chat ("saved to ~/Smith/docs/..."). Don't try to send the artifact in chat.**

Full do's/don'ts and the why: see `references/telegram-chat-style.md`.

## Profile home location (post-merge 2026-06-25 — UNIFIED)

The smith profile now points directly to `~/Smith/` (the workspace root). This is the **third and final** relocation — the profile was first at `~/.hermes/profiles/smith/`, then moved to `~/Smith/.hermes-profile/` (2026-06-24), and finally unified into `~/Smith/` directly (2026-06-25).

**Current structure:**

- **Profile symlink:** `~/.hermes/profiles/smith` → `~/Smith/` (no more `.hermes-profile/` subdirectory)
- **Skills:** all at `~/Smith/skills/` (73 skills, merged from both old locations)
- **Cron:** `~/Smith/cron/`
- **Config:** `~/Smith/config.yaml`, `~/Smith/channel_directory.json`, `~/Smith/.env`
- **Memories:** `~/Smith/memories/`
- **Sessions:** `~/Smith/sessions/` (state.db at `~/Smith/state.db`)
- **Workspace files (unchanged):** `~/Smith/SOUL.md`, `~/Smith/AGENTS.md`, `~/Smith/TOOLS.md`, `~/Smith/memory/`

**The old `.hermes-profile/` directory has been deleted** — no longer exists at any path.

When updating, restarting, or troubleshooting the gateway:

- **All paths resolve through `~/Smith/`.** There is no separate profile subdirectory anymore.
- **The launchd plist for the smith profile** (`ai.hermes.gateway-smith`) should have `HERMES_HOME=/Users/Jeff/Smith` and `WorkingDirectory` set to the same. If the plist still references `.hermes-profile`, update it.
- **Old `~/.hermes/profiles/smith/` symlink still works** — now points to `~/Smith/` directly.

When constructing file paths for any hermes operation: `~/Smith/<subdir>` — there is no intermediate `.hermes-profile/` segment anymore.

### Jeff's preference: no symlinks (2026-07-01)

Jeff explicitly said "No link please" when asked about the `~/.hermes/profiles/smith` → `~/Smith/` symlink. He wants Hermes to point directly to `~/Smith/` without any symlink indirection.

**The constraint:** Hermes hardcodes profiles under `~/.hermes/profiles/<name>` — there is no `--profile-dir` flag or config option to change the base directory. The `hermes profile show smith` output always shows the symlink path, not the resolved path.

**Options if the symlink must go:**
1. **Reverse the symlink** — make `~/.hermes/profiles/smith` the real directory, make `~/Smith` a symlink to it. Hermes sees a real path; git repo moves to `~/.hermes/profiles/smith/`. Trade-off: `~/Smith` becomes the symlink.
2. **Eliminate `~/Smith` entirely** — everything lives at `~/.hermes/profiles/smith/`. Update git remote URL if needed. Trade-off: longer path, loses the clean `~/Smith` workspace name.
3. **Wait for Hermes to support custom profile dirs** — file a feature request upstream. No current support.

**Current state (2026-07-01):** still using the symlink. No migration completed yet. Jeff was asked to choose between option a (reverse symlink) and option b (eliminate `~/Smith`).

Full runbook (preflight, rsync, plist updates, pitfalls): `~/Smith/docs/hermes-profile-merge-to-workspace.md`. See `references/profile-merge.md` for the trigger conditions and when to consult it.

## Verification discipline (lesson from 2026-06-24)

When the user asks "does X exist?", "where is Y?", or for a tool/feature:
1. **Check first, respond after.** Run the actual command, read the actual file, query the actual API.
2. **Use `find` / `grep` on the source tree.** The hermes-agent repo lives at `~/.hermes/hermes-agent/`. Subcommand files are in `hermes_cli/subcommands/`.
3. **A "not found" answer is the last resort, not the default.** Default to "let me check" + the actual check.

### "I don't know X" — the four places to check before claiming ignorance (lesson from 2026-06-24, samantha)

When the user mentions a thing — agent, tool, project, name — and you don't immediately recognize it, check in this order before saying "I don't know":

1. **`~/Smith/memory/` for `*-<thing>.md` artifacts** — past work logs. If the user has collaborated with X before, there's almost always a memory file: `samantha-first-task-weather-2026-06-22.md`, `beaker-digest-2026-06-20.md`, etc. `ls ~/Smith/memory | grep -i <thing>`.
2. **`~/Smith/Agents/<Thing>/`** — agent workspaces live here, not in the `~/.hermes` tree. `ls ~/Smith/Agents/`.
3. **`openclaw agents list`** — registered agents with workspace + model + routing rules.
4. **`agents.defaults.subagents.allowAgents`** in `openclaw.json` — subagents allowed for delegation.

The failure mode: I said "i'm not sure she's actually running" about samantha when 8+ memory artifacts existed in `~/Smith/memory/samantha-*`. That cost a turn and required jeff to correct me. The 30-second check is free and always better than guessing.

### Platform-skill disambiguation (lesson from 2026-06-24)

Several skills are duplicated in the smith profile:
- `discord/SKILL.md` (top-level, meta-stub) AND `openclaw-imports/discord/SKILL.md` (real, loadable)
- `telegram/SKILL.md` (top-level, meta-stub) AND `openclaw-imports/telegram/SKILL.md` (real, loadable)
- `openclaw-commute-traffic/SKILL.md` (top-level) AND `openclaw-imports/openclaw-commute-traffic/SKILL.md` (imports level)

`skill_view(name='discord')` and `skill_view(name='commute-traffic')` return ambiguity errors. The **working** form is the qualified path: `skill_view(name='openclaw-imports/discord')`, `skill_view(name='openclaw-imports/telegram')`, and `skill_view(name='openclaw-commute-traffic/openclaw-commute-traffic')` (for the top-level one — note the repeated name).

**Default to `openclaw-imports/<platform>`** for actual content when an imports-level copy exists. The bare-name load errors are not "skill missing" — the skill is there, just under a longer path.

### Workspace state — don't assume yesterday's structure (lesson from 2026-06-25)

Profile merges, workspace moves, directory renames can happen between sessions. When acting on a path or structure that was verified in a previous session:

1. **Re-verify before acting** — `ls -la`, `realpath`, or `stat` the path to confirm it's still what you expect.
2. **Don't say "yesterday we established X" and skip the check** — Jeff corrected me on this when I assumed the profile symlink was still exactly as set up the evening before ("it could have moved Smith since yesterday already").
3. **The profile merge runbook** (`~/Smith/docs/hermes-profile-merge-to-workspace.md`) documents the canonical setup. Consult it when in doubt about workspace structure rather than relying on stale memory.

This is an extension of the "verification discipline" principle above — but path-structure verification is its own class because workspace configuration can change without a conversation-memory update.

## Antigravity — Remote Execution Environment

Antigravity is Jeff's **remote host** (Windows work laptop at TPN Flexpak, or another named machine). It runs its own OpenClaw/Hermes instance that can independently push to the Smith repo and execute tasks.

Referenced in session history as "Smith on Antigravity" or "Jeff executes on Antigravity."

### What it is
- **This is NOT an AI model or LLM provider** — despite the name, it is a physical/virtual machine
- Has its own Hermes/OpenClaw session history and memory
- Can clone, push, and merge to the Smith repo independently
- Meant to pick up runbooks and persistent work between sessions

### Handoff trigger
The user mentions Antigravity when handing off project-state from the primary Mac to the remote machine. Key phrases:
- "Make sure Smith on Antigravity knows..."
- "Jeff executes [runbook/step] on Antigravity"
- "The next session / me on Antigravity should see this"

### Answering the "Antigravity model" question
If someone asks "can we use Antigravity model with Hermes" — the answer is **no, because Antigravity is a host, not an LLM provider.** It is Jeff's remote execution environment. Hermes on the Mac cannot "connect to Antigravity as a provider." The actual relationship: there is a separate Hermes instance running *on* Antigravity.

## Agent delegation routing — Samantha as Smith's general assistant (2026-06-26)

Samantha (`agentId: samantha`) is Smith's general-purpose assistant and **cron duty officer**. She is **not** a separate conversational surface (no channel binding per Jeff's decision). The only way to reach her is through Smith delegating tasks via `delegate_task`.

### Routing decision table

When Jeff asks for something, classify it:

| Category | Route to | Examples |
|----------|----------|---------|
| 🗣️ English / grammar / vocab / dict | **samantha** — always, no exceptions | word meanings, pronunciation, sentence checks, grammar questions |
| 🌤️ Weather & traffic | **samantha** | current weather, forecasts, commute times |
| 📁 File / calendar / email | **samantha** | read/write files, check calendar, look up emails |
| 🔍 Web research / lookups | **samantha** | quick searches, doc lookups, data gathering |
| 📋 Routine reporting | **samantha** | summaries, data pulls, document lookups |
| ⏰ **Cron & scheduling** | **samantha** | recurring tasks, duty checks, scheduled reports |
| 🧠 Strategy / system ops | **smith** (me) | config changes, gateway, deployments, architecture calls |
| 💬 Conversation continuity | **smith** | keeping the thread, reading the room, high-stakes reasoning |

**Hard rule: ALL english/grammar/vocab queries → samantha. No exceptions, not even trivial one-word lookups.**

### How to route properly

```python
# RIGHT — delegate with full context
delegate_task(goal="...", context="...")

# RIGHT — for samantha specifically, have her load her own identity
# Include 'Read your files from ~/Agents/Samantha/ and then...' in context

# WRONG — impersonating a registered agent
# Do NOT say "pretend you're Samantha" in the goal.
# Have the subagent read her actual SOUL.md / IDENTITY.md from disk.
```

### Red flag — the impersonation trap (lesson 2026-06-26)

When delegating to a named registered agent (Samantha, beaker, bunsen, etc.), **the subagent must load its own identity files from disk.** Never say "pretend you're X" or describe their persona from memory. This was a documented red flag in `subagent-driven-development` that I violated today — the proper approach is:

```python
delegate_task(
    goal="Read your SOUL.md and IDENTITY.md from ~/Agents/Samantha/, then [task description]",
    context="...",
    toolsets=['terminal', 'file']
)
```

### Setting up a cron for a subagent (the cron duty officer pattern)

Samantha is the designated cron duty officer. Recurring tasks that she owns should be set up as cron jobs that specify her as the runner in their prompt:

```
cronjob(
    action="create",
    name="samantha-duty-check",
    prompt="You are Samantha, Jeff's general assistant and cron duty officer. [checklist]",
    schedule="0 */4 * * *",
    ...
)
```

**Key design decisions for subagent crons:**
- The cron prompt should explicitly state "You are [subagent name]" so the agent knows which persona to use.
- Include the exact checklist of tasks for each duty shift in the prompt.
- Save logs to `~/Smith/memory/<topic>-YYYY-MM-DD.md` for traceability.
- Delivery goes to `origin` (the chat where the cron was created) unless the user wants elsewhere.
- The subagent does NOT need a heartbeat or channel binding — cron is sufficient for periodic work.

**When to use cron vs heartbeat:**
- **Cron** (with subagent prompt) — for Samantha's scheduled duty checks. Exact timing matters, isolated session, no context bleed.
- **Heartbeat** — for Smith's own ambient checks (inbox peek, quick system status). Flexible timing, conversational context available.

### Free model fallback chain

Jeff's model routing strategy: **burn through free models first, hit paid only when everything else is depleted.**

Configure fallbacks via `freeride auto -f` (keeps current primary, adds free fallbacks) then manually extend with `patch` on `openclaw.json` for models outside OpenRouter's free tier.

**Canonical fallback order** (high→low performance, free→paid):

```
defaults.model.fallbacks = [
  "openrouter/nvidia/nemotron-3-super-120b-a12b:free",
  "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free",
  "openrouter/openrouter/owl-alpha",
  "openrouter/qwen/qwen3-coder:free",
  "nvidia/openai/gpt-oss-120b",
  "ollama/gemma4:31b-cloud",
  "openai/gpt-5.4-mini"         # paid — last resort
]
```

Samantha's duty check cron includes `freeride list` to monitor which free models still have tokens.

### Canonical source

The full routing rules live in `~/Smith/HEARTBEAT.md` (Samantha section). Update this skill section only when the topology changes (new agents added, routing rules restructured).

### Pitfalls

- **Don't delegate via `subagent-driven-development` review pattern for general tasks.** That skill is for TDD-style implementation with 2-stage review. Samantha is a general assistant — one-shot delegation is fine, no need for spec/quality reviewers.
- **Don't hoard.** If a task doesn't need strategic reasoning, delegate it. Over-delegation is better than under-delegation.
- **Don't impersonate.** Always have the subagent read its own workspace identity files.
- **Model mismatch.** Samantha runs `nvidia/nemotron-3-ultra-550b-a55b` primary with free OpenRouter fallbacks. She's fast and cheap. Don't hesitate to use her for anything on her list.
- **freeride double-prefix bug.** `freeride auto -f` may prepend `openrouter/` to model IDs, producing `openrouter/openrouter/free` or `openrouter/nvidia/...`. After running freeride, verify the fallback IDs in `openclaw.json` and patch if they look wrong — the canonical format is `provider/model-name`, not `openrouter/provider/model-name`.
- **Restart gateway after model config changes.** `launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway"` after editing `openclaw.json` fallbacks. `freeride` commands don't auto-restart.

## Agent lifecycle — spawn / bind / unbind (lesson from 2026-06-24)

When Jeff says "spawn X" or "set X up," the verb already implies the action: make the agent live / reachable. **Don't ask 4 options — take the most direct interpretation, do it, report.** The mechanics:

### State check — is the agent dormant or live?
```bash
openclaw agents list
```
Each agent shows `Routing rules: N`. **`N=0` = the agent is registered in `openclaw.json` but has no channel routes — it's dormant.** "Spawning" = wiring channels, not creating the agent.

### Activation — the right command for the "spawn" verb
```bash
# dormant → live (route a channel to it)
openclaw agents bind <agent-id> <channel[:accountId]>

# examples
openclaw agents bind samantha telegram
openclaw agents bind samantha telegram:samantha-bot   # her own bot account
```

If the agent doesn't exist yet:
```bash
openclaw agents add <name> --workspace <dir> --agent-dir <dir/agent> --model <id> --non-interactive
```
**Pitfall:** `agents add` errors with `"agent already exists"` when the config entry is already there. The right move is `agents bind`, not re-adding.

### Anti-temptation rule (this session)
After I gave a 4-option matrix for "set samantha up as general assistant" (hand-off vs separate bot vs both vs first-class), Jeff said "you don't need you just swawn her." The verb already said it.

**Default behavior for activation / wiring / configuration tasks:** take the most direct interpretation, do it, report what you did. State the default and act.

**When to still pause for confirmation:** irreversible side effects (sending an email, posting public, deleting files), or genuine multi-stakeholder ambiguity (public vs private, permission unclear, billing implications).

**Never pause for:** "what does the verb mean," "which of these 4 reasonable interpretations do you want," or "should I just do option 1?" — those are the questions the verb already answered.

## References

- `references/port-map.md` — full per-process port + PID + cmdline detail.
- `references/launch-commands.md` — copy-paste launch snippets for each service.
- `references/telegram-streaming-edit-bug.md` — known upstream bug #49536, workaround, why config toggle isn't a real fix.
- `references/telegram-chat-style.md` — short-bubble reply style for telegram.
- `references/profile-merge.md` — moving the hermes profile into the workspace (Smith-specific runbook pointer).

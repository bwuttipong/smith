# Walkthrough — Profile Merge and Telegram Bind

I have completed the profile merge and agent binding tasks. Here is a summary of the accomplishments:

## Changes Made

1. **Profile Merge**:
   - Backed up the original profile directory `~/.hermes/profiles/smith` to `~/.hermes/.hermes-profile-backup-20260624-215423.tar.gz`.
   - Snapshot `~/.openclaw/openclaw.json` config.
   - Synchronized all files from `~/.hermes/profiles/smith/` to the new workspace directory `~/Smith/.hermes-profile/`.
   - Deleted the original source profile directory and created a symbolic link at `~/.hermes/profiles/smith` pointing to `~/Smith/.hermes-profile/`. This preserves the profile resolution name expected by the `hermes` CLI.

2. **Launchd Service Update**:
   - Modified `~/Library/LaunchAgents/ai.hermes.gateway-smith.plist` to point to the new location inside the workspace for `WorkingDirectory`, `StandardOutPath`, and `StandardErrorPath`.
   - Retained `HERMES_HOME` env var pointing to `~/.hermes/profiles/smith` so profile names (like `--profile smith`) resolve correctly through the symlink.
   - Reloaded the launchd agent and started the gateway.

3. **Telegram Agent Binding**:
   - Reverted Telegram binding to `smith` per user instruction, keeping `samantha` purely as a sub-agent.

## Verification

1. **Gateway Running**:
   - Verified that `launchctl list | grep ai.hermes.gateway-smith` shows the service running under PID `53564` with exit status `0`.
   - Checked `gateway.log` and verified it successfully initialized and connected to Telegram:
     ```
     2026-06-24 21:59:38,768 INFO hermes_plugins.telegram_platform.adapter: [Telegram] Connected to Telegram (polling mode)
     2026-06-24 21:59:38,770 INFO gateway.run: ✓ telegram connected
     2026-06-24 21:59:38,770 INFO gateway.run: Gateway running with 1 platform(s)
     ```

2. **Agent Routing**:
   - Ran `openclaw agents list` and verified routing rules:
     - `samantha` has routing rules: 0
     - `smith` has routing rules: 3 (Line + Discord + Telegram)

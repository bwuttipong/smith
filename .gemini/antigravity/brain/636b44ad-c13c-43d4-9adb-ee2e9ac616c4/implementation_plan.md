# Merge Hermes smith Profile & Bind Telegram

This plan outlines the steps to merge the Hermes profile `smith` (`~/.hermes/profiles/smith`) into the workspace directory under `~/Smith/.hermes-profile/`, update the `launchd` plist file, verify the migration, and bind the `samantha` agent to Telegram.

## User Review Required

> [!WARNING]
> This operation will restart the Hermes gateway service, causing a brief downtime of a few seconds.

## Open Questions

None. The runbook is detailed and we have all the required steps.

## Proposed Changes

### Configuration & Relocation

#### [MODIFY] [ai.hermes.gateway-smith.plist](file:///Users/Jeff/Library/LaunchAgents/ai.hermes.gateway-smith.plist)
Modify the `HERMES_HOME`, `WorkingDirectory`, `StandardOutPath`, and `StandardErrorPath` keys in the plist to point to the new location under `~/Smith/.hermes-profile`.

#### [NEW] [.hermes-profile](file:///Users/Jeff/Smith/.hermes-profile)
The entire contents of the profile from `~/.hermes/profiles/smith` will be moved here.

## Verification Plan

### Manual Verification
1. Verify `launchctl list | grep ai.hermes.gateway-smith` shows the service running with a valid PID.
2. Verify `~/Smith/.hermes-profile/logs/gateway.log` shows clean startup.
3. Test that the bot responds to commands on Telegram.
4. Bind `samantha` to telegram using `openclaw agents bind samantha telegram` and verify.

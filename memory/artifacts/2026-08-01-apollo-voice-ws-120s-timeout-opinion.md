# Apollo voice/WS 120-second timeout — opinion

- **Timestamp:** 2026-08-01 23:30:36 +07
- **Question:** How to deal with `[voice/WS path] the turn exceeded the 120s limit...`

## Evidence checked

- `src/server/apollo-ws.ts` defines `HERMES_TIMEOUT_MS = 120_000`.
- The timer starts at turn submission and is never reset when Hermes produces meaningful activity.
- `lastActivityAt` is updated for tool steps, initialization, reply chunks, and forwarded prose, but is only used to decorate the timeout error with `quiet for...`; it does not affect whether the process is killed.
- Therefore the current limit is a 120-second absolute wall-clock cap, not a 120-second inactivity detector.
- The WS path launches Hermes with `gpt-5.6-luna` through `openai-codex`; valid tool-heavy turns can exceed two minutes.
- Hermes' current documentation lists much longer provider defaults (`HERMES_API_TIMEOUT=1800s`) and a separate stale-call default (`HERMES_API_CALL_STALE_TIMEOUT=90s`), reinforcing that total-runtime and inactivity limits should be separate concepts.
- Live AgentOS processes were running on ports 3737/3738; WS PID 52895 started at 23:15:02 +07 and is executing the current 120-second constant.

## Opinion

The 120-second absolute kill is the wrong control. It fixed the 15-minute silent-wedge complaint by replacing it with premature termination of legitimate long turns. Keep fast failure, but base it on inactivity.

Recommended policy:

1. **Idle timeout:** stop only after 120 seconds with no meaningful Hermes output/activity.
2. **Hard ceiling:** retain a 10–15 minute absolute cap as the final safety net.
3. **Progress:** keep the 30/60/90-second notices, but report elapsed and idle time separately.
4. **Voice UX:** for genuinely long work, acknowledge quickly and continue in background rather than forcing the whole task into a conversational response window.

Short-term workaround: retry with a smaller request or use the build/HTTP path for long jobs. Correct fix: replace the single absolute timer with separate sliding-idle and hard-cap timers.

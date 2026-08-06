# Apollo Voice Reliability Space

**Created:** 2026-08-02  
**Project:** AgentOS / Apollo  
**Status:** Conditional pass; implementation and final QA complete

## Objective

Make Apollo's free Microsoft Edge TTS path reliable during intermittent network, provider, process, and browser conditions without introducing paid TTS or delaying the user unnecessarily.

## Current baseline

- AgentOS calls `POST /api/tts/hermes-edge`.
- The server reads the Hermes TTS configuration and invokes `edge-tts`.
- Current voice: `en-GB-RyanNeural`.
- Current process timeout: 30 seconds.
- Current client behavior: Edge audio first; browser `speechSynthesis` fallback after failure.
- The live endpoint currently returns valid MP3 audio.

## Enhancement scope

### P0 — Reliability

- Add bounded retries for transient Edge TTS failures and timeouts.
- Use a configurable per-attempt timeout and strict overall deadline.
- Add bounded exponential backoff with jitter.
- Do not retry invalid input, invalid configuration, or unsupported voice errors.
- Guarantee timed-out child-process cleanup before retry or final failure.

### P0 — Playback correctness

- Keep browser fallback deterministic and invoke it only after Edge has definitively failed.
- Ensure one request can produce at most one audible result.
- Ignore stale Edge responses, retry callbacks, and fallback callbacks.
- Preserve the existing text and browser-voice behavior.

### P1 — Cancellation and lifecycle

- Cancel obsolete client fetches and pending retries.
- Treat cancellation separately from provider failure.
- Stop active audio and browser speech when a newer request starts or the panel closes.

### P1 — Diagnostics

- Log request ID, voice, text length, attempt, duration, and outcome.
- Never log the complete spoken text in normal production logs.
- Distinguish success, retry, timeout, permanent failure, cancellation, and browser fallback.

### P1 — User feedback

- Expose clear internal states: starting, retrying, falling back, playing, cancelled, and failed.
- Do not make the user wait through an unbounded retry sequence.

## Fallback strategy

- **Plan A:** Microsoft Edge TTS using `en-GB-RyanNeural`.
- **Plan B:** Browser-native `speechSynthesis`, already present in Apollo.
- **Plan C:** Local macOS/Piper TTS if both online Edge TTS and browser speech are unavailable or unreliable.

Plan C is deliberately not part of the first change unless QA shows that Plans A and B are insufficient; it keeps the first release small while preserving a fully offline escape route.

## Acceptance criteria

- A transient first-attempt failure can recover on a later attempt.
- Final failure falls back to browser speech exactly once.
- Invalid input/configuration fails immediately without retrying.
- No orphaned `edge-tts` processes remain after success, timeout, cancellation, or failure.
- A late response from an older request never plays audio or triggers fallback.
- Existing successful Edge TTS requests still return and play `audio/mpeg`.
- Focused lint, type checks, functional checks, and adversarial checks pass.

## Delivery topology

1. **BA** — requirements and acceptance criteria: complete.
2. **Development** — implement the smallest safe change in Apollo TTS files: in progress.
3. **QA** — exercise success, timeout/retry, invalid input, cancellation, fallback, and duplicate-playback paths.
4. **Adversary** — attack process cleanup, race conditions, request-size limits, portability, and silent fallback failures.
5. **Close** — verify independently, record commands/results, and update this document.

## Constraints

- Do not touch `e2e/`.
- Do not reset or overwrite unrelated uncommitted AgentOS work.
- Keep the free-only voice path; no ElevenLabs or paid provider call path.
- Preserve the existing AgentOS dashboard and Apollo interaction model.

## Delivered

- Bounded Edge TTS retries: up to 3 attempts, 10-second attempt timeout, 30-second overall budget, capped jittered backoff.
- Permanent runtime/configuration failures are not retried.
- Timeout cleanup is idempotent with SIGTERM → SIGKILL escalation.
- Abort listeners and retry timers are cleaned up.
- Apollo keeps request ownership through response-body reading and playback, reducing stale-audio races.
- Config and executable discovery now supports explicit Hermes paths, active profiles, PATH installs, and the current `~/Smith/.hermes` layout.
- Automatic discovery skips invalid existing configs and selects the first valid Edge TTS profile.
- Browser `speechSynthesis` fallback remains available.

## Final verification — 2026-08-02

- Focused ESLint: passed.
- TypeScript (`npx tsc --noEmit`): passed.
- Reliability and config regression scripts: passed.
- Production build: passed; one non-blocking Turbopack NFT tracing warning remains because runtime filesystem discovery is dynamic.
- Live homepage: HTTP 200.
- Live repeated TTS requests: HTTP 200, `audio/mpeg`, valid 24 kHz mono MP3.
- Invalid JSON/empty input: HTTP 400.
- Oversized request/text: HTTP 413.
- No lingering `edge-tts` processes after live requests.
- Full lint remains conditional because of two unrelated pre-existing hook errors in `CreationsGallery.tsx:705` and `useApolloVocab.ts:55`.

## Known verification limits

Forced provider failure, real retry timing/SIGKILL escalation, browser cancellation during fetch/blob playback, and browser autoplay/user-gesture behavior were not fault-injected. The implementation is therefore a conditional pass, not a claim of perfect failure-path proof.

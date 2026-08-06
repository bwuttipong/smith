# Apollo Hermes Edge TTS integration

- completed: 2026-08-01T13:43:52Z
- project: `/Users/Jeff/Workspaces/agentos/source`
- outcome: Apollo prefers a same-origin server bridge at `/api/tts/hermes-edge`, reading Hermes' configured Edge voice (`en-GB-RyanNeural`) and invoking the local Hermes Edge TTS runtime. Browser Daniel/en-GB speech remains the fallback.
- files: `src/app/api/tts/hermes-edge/route.ts`, `src/lib/hermes-edge-tts.ts`, `src/components/apollo/voice.ts`, `src/hooks/useApolloVoice.ts`, `scripts/verify-hermes-edge-tts.mjs`
- security: voice/provider are server-controlled; no Hermes config or credentials are sent to the browser; input capped at 4096 characters; malformed and non-object JSON returns HTTP 400; runtime failures return generic HTTP 503.
- QA evidence: valid requests returned HTTP 200 `audio/mpeg` with valid MPEG audio; empty, malformed, scalar, array, and missing-text bodies returned HTTP 400 JSON; browser harness showed Edge preferred, browser fallback on fetch failure, and interruption generation ownership preserved; `npx tsc --noEmit` passed; changed-file ESLint passed.
- adversary: found and repaired a scalar JSON 500 defect; final adversarial retest found no new issue.
- known baseline: full `npm run lint` remains red only on pre-existing errors at `src/components/apollo/CreationsGallery.tsx:705` and `src/hooks/useApolloVocab.ts:55`.

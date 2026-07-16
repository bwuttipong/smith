# Xiaomi MiMo — Provider Reference

## API Details

- **Base URL:** `https://token-plan-sgp.xiaomimimo.com/v1` (profile-specific)
- **Plugin base URL:** `https://api.xiaomimimo.com/v1` (may differ from profile)
- **API key:** `XIAOMI_API_KEY` in `~/.openclaw/.env`
- **Key format:** `tp-...` (token plan)

## Available Models

```json
{
  "models": [
    "mimo-v2.5",
    "mimo-v2.5-asr",
    "mimo-v2.5-pro",
    "mimo-v2.5-tts",
    "mimo-v2.5-tts-voiceclone",
    "mimo-v2.5-tts-voicedesign"
  ]
}
```

## Credits/Balance

**No credits endpoint exists.** All attempts return 404:
- `/v1/credits` → 404
- `/v1/user/info` → 404
- `/v1/usage` → 404

User must check balance manually at xiaomimimo.com portal.

## Debugging Path

1. Plugin config shows `base_url="https://api.xiaomimimo.com/v1"`
2. Profile config shows `base_url: https://token-plan-sgp.xiaomimimo.com/v1`
3. Profile config takes precedence — always check both
4. Test connectivity: `curl -s "<base_url>/v1/models" -H "Authorization: Bearer <key>"`
5. If models list returns, API key is valid
6. If credits endpoint 404s, provider doesn't expose it

## Notes

- The `tp-` prefix suggests a "token plan" billing structure
- Provider supports vision (mimo-v2-omni) but not vision tool messages
- Health check not supported (models endpoint returns 401 even with valid key on some endpoints)

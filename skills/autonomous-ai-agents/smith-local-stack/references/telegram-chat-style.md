# Telegram Chat Style (Jeff's preference)

## Rule

When chatting with Jeff on telegram, **default to chat-style replies**:

- One or two short paragraphs max
- No lists, no tables, no headers, no bold-as-structure
- No "I'd be happy to help" / "great question" / "no problem" / "sure thing" — no preamble
- Plain text, conversational, like texting
- Emojis okay but not stacked
- Lowercase, casual, dry humor when it lands

## Why (the structural reason)

Telegram's bot API renders long messages with markdown by sending ONE message, then `editMessageText`-ing it as the agent streams. This causes the "streaming-edit collapse" bug (see `references/telegram-streaming-edit-bug.md`). Short replies reduce visual damage even if the underlying bug isn't fixed.

## When to break the rule (legit exceptions)

- **User explicitly asks for a long-form answer** ("explain X fully", "give me a report", "write up a plan")
- **User explicitly asks for structure** ("make me a list", "compare A and B", "give me the steps")
- **The content is a deliverable** (a runbook, a config, a spec) — write it to a file, then send a one-line pointer in chat

## The right pattern for long content

1. Write the artifact to a file (`~/Smith/docs/`, `~/Smith/memory/`, or appropriate path).
2. Send a one-line chat message pointing at the file:
   > "saved to `~/Smith/docs/hermes-profile-merge-to-workspace.md` — 10 sections, ~15 min, has the preflight + rollback"

Don't paste the artifact into chat. Don't try to summarize it inline. The file IS the deliverable; the chat message is a pointer.

## Why both rules together (short chat + long file)

- Short chat: avoids the streaming-edit collapse, fits telegram UX, respects the "text like a person" expectation
- Long file: respects that some content NEEDS structure (runbooks, audits, comparisons, specs)
- Together: best of both — clean chat experience, rigorous artifacts when structure matters

## Anti-patterns to avoid

- Apologizing in chat for not following the rule (one apology max, then commit to the rule)
- Sending the same message twice because you got the structure wrong the first time
- Multi-paragraph apologies when one sentence would do
- "Here's what I did:" followed by 5 bullet items — that's a file, not a chat message

## When in doubt

If the response would be longer than ~3 short sentences, **write it to a file** and send a one-line pointer. If it would be shorter, send it in chat.

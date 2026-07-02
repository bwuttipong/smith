# MEMORY - Log to Today's Daily Memory File

Append an entry to today's memory file with timestamp.

## Usage
```
/memory <entry>
```

## Description
Logs significant events, decisions, learnings, or context to `memory/YYYY-MM-DD.md`. Creates the file and `memory/` directory if they don't exist.

## Examples
```
/memory Decided to use PostgreSQL over Mongo for the user service — ACID compliance needed for billing
/memory Bug found in payment webhook: idempotency key not validated, fixed in PR #342
/memory Learned: Kilo's .kilo/command dir is for project-specific slash commands
```
# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---


## [LRN-20250609-001] correction

**Logged**: 2025-06-09T15:14:00+07:00
**Priority**: high
**Status**: promoted
**Area**: docs

### Summary
LINE strips markdown code blocks — commands wrapped in triple backticks get eaten entirely

### Details
When sending shell commands, code snippets, or anything wrapped in markdown code fences through the LINE channel, LINE strips the content, leaving only the surrounding text. The recipient sees placeholder text but the actual code is blank.

This happened repeatedly in the 2026-06-09 session while sending nuget install instructions. The user had to correct me several times.

### Suggested Action
For LINE messages, NEVER use markdown code fences. Instead:
- Write commands as plain text on their own line
- Keep commands unformatted for visibility
- Never wrap in ``` fences — LINE eats them

### Metadata
- Source: user_feedback
- Tags: line, formatting, code_blocks

---

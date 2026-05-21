# Working Buffer (Danger Zone Log)

> **Purpose:** Capture EVERY exchange when context > 60% — survives compaction, prevents context loss.
> **Status:** ACTIVE when context is in danger zone. Read this FIRST on session resume.

---

**Status:** STANDBY
**Started:** —
**Last Entry:** —

---

## Entries

<!-- Format:
## [timestamp] Human
[their message]

## [timestamp] Agent (summary)
[1-2 sentence summary + key details]
-->

---

## Recovery Checklist (for after compaction)

- [ ] Read this buffer first
- [ ] Extract key context → SESSION-STATE.md
- [ ] Check if decisions/corrections need logging
- [ ] Clear buffer after successful recovery
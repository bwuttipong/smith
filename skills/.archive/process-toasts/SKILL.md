---
name: process-toasts
description: Write background process state to AgentOS toast system. Use when spawning any background process (terminal background, delegate_task, cronjob).
---

# Process Toasts — AgentOS Integration

When running background processes, write state to `~/.agentos/processes/active.json` so AgentOS displays live toast notifications with progress bars.

## When to write

- **On start**: `terminal(background=true)` or `delegate_task` spawns a process
- **On complete**: process finishes successfully
- **On fail**: process exits with error

## State file

`~/.agentos/processes/active.json`

```json
{
  "processes": [
    {
      "id": "unique-id",
      "name": "Human readable name",
      "command": "the command or task description",
      "status": "running" | "completed" | "failed",
      "startedAt": "ISO timestamp",
      "endedAt": "ISO timestamp or null",
      "output": "last few lines of error output (for failed)"
    }
  ]
}
```

## Workflow

1. **Before spawning**: Write process entry with status `running`
2. **On completion**: Update status to `completed`, set `endedAt`
3. **On failure**: Update status to `failed`, set `endedAt`, include error in `output`
4. **Cleanup**: Remove completed/failed entries after 30 seconds

## Example (Python)

```python
import json, os, time
from datetime import datetime, timezone

STATE_FILE = os.path.expanduser("~/.agentos/processes/active.json")

def write_state(processes):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"processes": processes}, f, indent=2)

def read_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f).get("processes", [])
    except:
        return []

# On start
procs = read_state()
procs.append({
    "id": "qmd-embed-001",
    "name": "qmd embed",
    "command": "qmd embed",
    "status": "running",
    "startedAt": datetime.now(timezone.utc).isoformat(),
    "endedAt": None
})
write_state(procs)

# On complete
for p in procs:
    if p["id"] == "qmd-embed-001":
        p["status"] = "completed"
        p["endedAt"] = datetime.now(timezone.utc).isoformat()
write_state(procs)
```

## Notes
- AgentOS polls `/api/processes` every 3 seconds
- Running toasts show animated progress bar with percentage
- Failed toasts persist until manually dismissed, show error output + retry button
- Completed toasts auto-dismiss after 5 seconds
- All toasts are draggable (grab anywhere on the card)

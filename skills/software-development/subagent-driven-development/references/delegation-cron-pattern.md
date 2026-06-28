# Delegation + Cron: Subagent Duty Officer Pattern

## When to Use

When a cron job needs to be run by a specific subagent rather than the main
session agent. Common cases:

- A general assistant (e.g. Samantha) owns recurring checks instead of Smith
- A subagent has a different model, toolset, or workspace for the task
- You want to keep the main agent's context clean of routine check output

## Pattern

Create a cron job whose prompt explicitly instructs the session agent to
delegate the work to the target subagent:

```
cronjob(
    action="create",
    name="samantha-duty-check",
    prompt="You are the duty dispatcher. Delegate the following tasks to
    [subagent name] via delegate_task. Wait for their result, then deliver
    it to Jeff. Keep it brief.",
    schedule="0 */4 * * *",
    ...
)
```

## Key Details

- **The cron runs the main session agent (e.g. Smith).** The prompt tells it
  to delegate to the target subagent. The main agent then acts as dispatcher
  and delivery relay.
- **Subagent must have no channel binding** to be reachable only via delegation.
  This is the correct pattern for non-public agents (like Samantha).
- **Keep cron prompts self-contained.** Don't reference chat context — it won't
  exist in the cron session.

## Example: Samantha Duty Check

The cron job `samantha-duty-check` (every 4h):
1. Runs as Smith (default session agent)
2. Delegates to Samantha via `delegate_task`
3. Samantha runs `freeride list`, checks system health
4. Result comes back to the cron session
5. Smith relays it to Jeff's chat

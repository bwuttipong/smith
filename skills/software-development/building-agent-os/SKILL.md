---
name: building-agent-os
description: "Build local AI agent dashboards with Next.js — wire real agent connections, status polling, Obsidian sync."
platforms: [macos, linux]
---

# Building Agent OS Dashboards

When the user wants to build a local AI agent dashboard (mission control), follow this workflow.

## Stack
- Next.js 16 (App Router) + TypeScript
- Tailwind CSS + clsx + twMerge
- Framer Motion (animations)
- Lucide React (icons)

## Agent Connection Pattern

Each agent has a different connection method. Use switch/case dispatch:

| Agent | Method | Port | API |
|-------|--------|------|-----|
| Hermes | OpenClaw CLI | 9120 | `openclaw agent -m "..." --json` |
| OpenClaw | OpenClaw CLI | 18789 | `openclaw agent -m "..." --json` |
| Ollama | Direct API | 11434 | `curl http://localhost:11434/api/chat` |
| ZCode/Codex | Not wired | 3001 | Return 501 |
| Claude Code | Not wired | 3002 | Return 501 |
| Paperclip | Not wired | 3100 | Return 501 |

## API Routes to Build

1. **`/api/agents/health`** — GET, pings all agents, returns status array
2. **`/api/chat`** — POST, sends message to agent, returns reply
3. **`/api/obsidian`** — POST (save), GET (list), syncs to vault

## Health Check Pattern

```typescript
const controller = new AbortController();
const timeout = setTimeout(() => controller.abort(), 3000);
const res = await fetch(agent.url, { signal: controller.signal });
clearTimeout(timeout);
```

## Obsidian Vault Path

Default: `~/Library/CloudStorage/OneDrive-Personal/Apps/remotely-save/Wuttipong Vault/Agent OS/`

Save format: `YYYY-MM-DD.md` with `## AgentName — HH:MM` sections.

## Dashboard Component Structure

- Sidebar with agent list + status badges
- ChatPanel per agent with message history
- Voice input (browser SpeechRecognition)
- Save to Obsidian button
- Status polling every 30 seconds

## Adding New Feature Panels (Multi-File Pattern)

When adding a new feature (e.g., Process Toasts, new panel), follow this exact file order. Each step depends on the previous — don't reorder.

1. **`src/types/index.ts`** — Add types. Insert before the Vault section if possible (Vault is the last major section). Use the `// ── Section ──────────` comment style.
2. **`src/app/api/<feature>/route.ts`** — API route. Server-side only, reads from disk or external source. Use `NextResponse.json()`. Wrap in try/catch, return empty defaults on missing file.
3. **`src/lib/api.ts`** — Service method. Import new types into the existing import block. Use the `http<T>()` helper for responses. Add a new section with the `// ── Section ──────────` header.
4. **`src/hooks/use<Feature>.ts`** — Client hook. Use `"use client"`. Poll or fetch data. Always use `alive` flag pattern for cleanup.
5. **`src/components/<Feature>.tsx`** — Component. Use `"use client"`, framer-motion for animations, clsx for classes, lucide-react for icons.
6. **`src/components/Dashboard.tsx`** — Integration. Import and render. Place at the appropriate location in the JSX tree.

## Shared JSON File Pattern

For features where an external process (Hermes) writes state that AgentOS reads:

- **Write side**: Hermes writes to `~/.agentos/<feature>/active.json`
- **Read side**: API route reads with `fs.readFile`, try/catch, returns `{ items: [] }` on missing
- **Client**: Hook polls every 3s with `{ cache: "no-store" }`
- **Directory**: Create with `mkdir -p ~/.agentos/<feature>/` before first use
- **Test data**: Write a sample JSON file so the UI renders on first load

See `references/shared-json-feature.md` for the full template.

## Polling Hook Pattern

```typescript
"use client";
import { useEffect, useState } from "react";

const POLL_MS = 3000;

export function useThings(): Thing[] {
  const [things, setThings] = useState<Thing[]>([]);
  useEffect(() => {
    let alive = true;
    const load = async () => {
      try {
        const data = await api.list();
        if (alive) setThings(data);
      } catch { /* transient */ }
    };
    load();
    const t = setInterval(load, POLL_MS);
    return () => { alive = false; clearInterval(t); };
  }, []);
  return things;
}
```

## Floating Toast Pattern

For bottom-right floating notifications (process toasts, background task alerts):
- `fixed bottom-4 right-4 z-50` container — do NOT use `pointer-events-none` (breaks drag)
- `AnimatePresence` wrapping `motion.div` cards with spring transition
- Max visible limit, newest on top (reverse or flex-col with newest appended)
- Dark theme: `bg-zinc-900/90 border-zinc-800/80 backdrop-blur-md shadow-lg shadow-black/30`

### Draggable Toasts (whole card)
- Add `drag`, `dragMomentum={false}`, `dragConstraints` to the outer `motion.div`
- Add `whileDrag={{ scale: 1.02, zIndex: 100, boxShadow: "0 8px 32px rgba(0,0,0,0.5)" }}`
- Add `cursor-grab active:cursor-grabbing` to className
- Buttons (dismiss, retry) MUST use `e.stopPropagation()` to avoid triggering drag on click

### Progress Bar with Percentage
Use a `RunningProgressBar` helper component with `requestAnimationFrame` for a smooth 0→100% counter that loops. The animated bar uses framer-motion `animate={{ width: "100%" }}` with `repeat: Infinity`. The percentage text uses `tabular-nums` for stable digit width.

```tsx
function RunningProgressBar() {
  const [pct, setPct] = useState(0);
  useEffect(() => {
    const start = Date.now();
    const DURATION = 3000;
    let raf: number;
    const tick = () => {
      const elapsed = Date.now() - start;
      setPct(Math.min(100, Math.round((elapsed % DURATION) / DURATION * 100)));
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);
  // Render: "Progress" label left, "{pct}%" right, then the animated bar
}
```

### Failed Toast Pattern
- Failed toasts do NOT auto-dismiss — persist until manually dismissed
- Show error output as `<pre>` block: `text-[10px] text-red-400/80 bg-red-500/5 rounded p-1.5 max-h-16 overflow-y-auto font-mono whitespace-pre-wrap`
- Retry button: `RotateCw` icon (or `Loader2` with `animate-spin` while retrying), POSTs to API to reset process status
- Dismiss X button: absolute top-right, `stopPropagation` on click

## Pitfalls

- Hermes runs on port 9120 (not 9119 as some docs say)
- OpenClaw gateway is on 18789 (not 4444)
- `openclaw agent` requires the gateway to be running
- Ollama model names must match exactly (e.g., `gemma4:12b-mlx`)
- Voice recognition only works in Chrome/Safari
- **`patch` tool hunk markers must match file content exactly.** If the context hint in `@@` doesn't match a unique location in the file, the patch fails silently or modifies wrong lines. When multi-file patches fail, fall back to individual `replace` operations with unique `old_string` matches. Use `read_file` first to see exact current content.
- **Unused imports cause ESLint warnings.** If you import a type only for documentation/annotation and don't reference it as a value in the component, remove it. Use `void` prefix on fire-and-forget calls like `setTimeout` to avoid unused variable warnings.
- **`npx next lint` in Next.js 16 may fail** with "Invalid project directory". Run `npx eslint <files>` directly instead.
- **Hermes chat timeout too short causes SIGTERM kills.** The `/api/chat` route for Hermes (`hermes -z`) defaults to 180s timeout. Complex queries often exceed this. Bump to 300000 (5 min) in `src/app/api/chat/route.ts`: `{ timeout: 300000, maxBuffer: 1024 * 1024 }`.
- **Node version mismatch in different shells.** If `qmd` or other native modules were compiled against a different NODE_MODULE_VERSION than the shell running them, operations fail silently with ~70% error rate. Check `node --version` in the target shell before running embed/index operations.

## References

- See `references/agent-ports.md` for current port mapping
- See `references/obsidian-sync.md` for vault integration details
- See `references/shared-json-feature.md` for the shared JSON file feature template

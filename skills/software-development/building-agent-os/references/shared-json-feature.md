# Shared JSON File Feature Template

Pattern for features where an external process writes state and AgentOS reads it.

## Directory Structure

```
~/.agentos/<feature>/active.json     ← external process writes here
src/app/api/<feature>/route.ts       ← reads the JSON file
src/lib/api.ts                       ← client service method
src/hooks/use<Feature>.ts            ← polling hook
src/components/<Feature>.tsx         ← UI component
```

## active.json Schema

```json
{
  "items": [
    {
      "id": "unique-id",
      "name": "Human-readable name",
      "command": "the command that was run",
      "status": "running" | "completed" | "failed",
      "startedAt": "ISO-8601",
      "endedAt": null | "ISO-8601",
      "output": "optional last lines"
    }
  ]
}
```

## API Route (src/app/api/<feature>/route.ts)

```typescript
import { NextResponse } from "next/server";
import fs from "fs/promises";
import path from "path";
import os from "os";

const STATE_FILE = path.join(os.homedir(), ".agentos", "<feature>", "active.json");

export async function GET() {
  try {
    const raw = await fs.readFile(STATE_FILE, "utf-8");
    const data = JSON.parse(raw);
    return NextResponse.json(data);
  } catch {
    return NextResponse.json({ items: [] });
  }
}
```

## Types (src/types/index.ts — before Vault section)

```typescript
// ── <Feature> ──────────────────────────────────────────────────────
export type ItemStatus = "running" | "completed" | "failed";

export interface ItemInfo {
  id: string;
  name: string;
  command: string;
  status: ItemStatus;
  startedAt: string;
  endedAt: string | null;
  output?: string;
}

export interface ItemsResponse {
  items: ItemInfo[];
}
```

## Service Method (src/lib/api.ts — append after last section)

```typescript
// Add ItemInfo, ItemsResponse to existing import block

// ── <Feature> ──────────────────────────────────────────────────────
export const itemsApi = {
  async list(): Promise<ItemInfo[]> {
    const res = await fetch("/api/<feature>", { cache: "no-store" });
    const data = await http<ItemsResponse>(res);
    return data.items ?? [];
  },
};
```

## Polling Hook (src/hooks/use<Feature>.ts)

```typescript
"use client";
import { useEffect, useState } from "react";
import { itemsApi } from "@/lib/api";
import type { ItemInfo } from "@/types";

const POLL_MS = 3000;

export function useItems(): ItemInfo[] {
  const [items, setItems] = useState<ItemInfo[]>([]);
  useEffect(() => {
    let alive = true;
    const load = async () => {
      try {
        const data = await itemsApi.list();
        if (alive) setItems(data);
      } catch { /* transient */ }
    };
    load();
    const t = setInterval(load, POLL_MS);
    return () => { alive = false; clearInterval(t); };
  }, []);
  return items;
}
```

## Integration (Dashboard.tsx)

```tsx
import { FeatureComponent } from "./FeatureComponent";
// In JSX, after ambient-glow:
<div className="ambient-glow" />
<FeatureComponent />
```

## Setup Commands

```bash
mkdir -p ~/.agentos/<feature>/
```

## Verification

```bash
cd /Users/Jeff/Workspaces/agentos/source
npx tsc --noEmit
npx eslint src/app/api/<feature>/route.ts src/hooks/use<Feature>.ts src/components/<Feature>.tsx
```

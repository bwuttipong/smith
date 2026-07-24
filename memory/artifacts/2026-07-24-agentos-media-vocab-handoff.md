# AgentOS Media Vocab — Handoff

**Date:** 2026-07-24
**Repo:** `/Users/Jeff/Workspaces/agentos/source`
**Branch:** `feature/media-vocab-extractor`
**Commit:** `d891271` — feat(media-vocab): text ingest endpoint, manual paste, accurate new-word counts

---

## The headline

The plan assumed today was "audit, repair, verify." The audit's finding was
that the feature was **further along than the plan believed** — 5 commits
deep, including a lightbox and AI captioning that the plan's "current known
state" didn't mention. The OCR → vocab diff → Recall pipeline already worked
end to end. Today's real work was the missing text path plus two counting
bugs.

Also worth correcting for tomorrow: the plan said port 3737 was free and
nothing was listening. Something *was* on 3737 — Claude Desktop's network
helper — but it wasn't an AgentOS server, so `preview_start` claimed the port
without a fight. Don't kill PIDs on 3737 reflexively.

---

## What was verified working (not just present)

Driven against the live dev server, not read from source:

- **Image drop → OCR.** A generated 4-sentence test image OCR'd at 100%
  accuracy. tesseract runs `eng+tha` in-browser; nothing uploaded.
- **Persistence.** `~/.agentos/media-vocab/assets.json` + original +
  300w WebP thumbnail all written. Survives page reload.
- **Thumbnails serve through the API route** (`/api/media-vocab/file?path=`),
  not a broken `file://` — confirmed `naturalWidth` 300 in the DOM.
- **Vocab diff + Thai gloss.** 15 candidates, all 15 glossed
  (`breathtaking น่าทึ่ง`, `resilience ความยืดหยุ่น`, `meticulous พิถีพิถัน`).
- **Add to Recall.** Deck 2859 → 2874. Cards carry `source:"media"`,
  `origin:"Media Vocab"`, Thai gloss as `back`, sentence as `note`.
- **Duplicate guard.** Re-POSTing the same words returns `added: 0`;
  deck size unchanged, `breathtaking` count stays 1.
- **Recall API round trip.** `GET /api/english/recall` returns all 16 media
  cards (cards live under `state.cards`, not `cards` — noted because it cost
  me a wrong lookup).
- **No browser console errors** at any point.

---

## What changed today

### New: `POST /api/media-vocab/ingest`
The LINE → AgentOS bridge. One local HTTP call:

```bash
curl -s -X POST http://localhost:3737/api/media-vocab/ingest \
  -H 'Content-Type: application/json' \
  -d '{"text":"Her tenacity eventually prevailed.","sourceType":"line"}'
```

Returns `{ asset, candidates }`. Text-only by design — it never accepts a
path, so there's no file-read surface. Guards verified: missing text 400,
empty 400, >20k chars 413, malformed JSON 400, disallowed `sourceType`
coerced to `line`, `javascript:` sourceUrl dropped.

### New: manual paste box
Backed by the same ingest endpoint so the manual and LINE paths can't drift.
A Facebook post that returns text but no image now **pre-fills this box**
rather than telling you to go screenshot it yourself.

### Fixed: new-word counts were wrong
Badges and the header counted only `existsInCatalogue` — a snapshot from
extraction time that never updates. A capture read "+15 new" forever after
those 15 were added, and the header disagreed with the cards below it. Both
now also exclude `addedToRecall`. Header went from a nonsense "1" to a
correct "13" (7 + 6 + 0).

### Fixed: every upload saved as `.jpg`
`extFromMime` read the *request's* content-type (always
`multipart/form-data`) instead of the uploaded file's. Now uses `file.type`.

### Also
Cards get `tags:["media"]`, and uploads with no external link get
`originUrl: "media-vocab:<assetId>"` so a card traces back to its screenshot.

---

## What is still rough

1. **Mobile is broken app-wide.** At 375px the fixed sidebar eats the
   viewport and content overflows horizontally. This is the **dashboard
   shell**, not Media Vocab — every panel has it. Prompt 5 asked for a
   usable narrow viewport; I did not do it, because fixing it means
   rearchitecting the global shell (drawer/hamburger), which "polish without
   changing architecture" explicitly ruled out. Flagging rather than
   half-doing it. **This is the biggest open item.**

2. **Facebook scraping is untested against a live URL.** No public post was
   on hand. The code path is unchanged from before today; the *fallback* is
   what I made reliable. Assume FB blocks it and lean on paste/screenshot.

3. **Two lint errors remain in media-vocab files** — `useMediaVocab.ts:27`
   and `MediaAssetDetail.tsx:72`, both `react-hooks/set-state-in-effect`.
   Left deliberately: every other hook in the repo (`useRecall`, `useMoa`,
   `useOracle`, `useGoalMode`…) has the identical error. Fixing only these
   two would diverge from repo convention for a stylistic rule. The repo has
   **58 lint problems total**, all pre-existing.

4. **`git stash` was used mid-session** to typecheck the staged subset in
   isolation. It was popped and the tree verified restored — but that's why
   there's no stash entry; don't go looking for one.

5. **Image ingest via the endpoint** (`{imagePath}`) was not built — the plan
   said text-only unless image was easy, and it isn't (bytes vs. path).

---

## Commit scope — read this before your next commit

The repo has **65 untracked files** and a pile of modified ones from earlier
sessions (whole panels, hooks, `recall-store`, `src/server/`). This is
pre-existing, not from today.

My commit had to include `src/types/index.ts` and `src/lib/api.ts` because the
media-vocab code **does not compile without them** — verified by stashing and
running `tsc`. Jeff chose to include them, so that commit's diffstat for those
two files (686 and 716 lines) is mostly **earlier sessions' work**, not
today's. Today's actual edits there are the `MediaSourceType` union
(+`"text"`, +`"line"`) and the `ingestText` client method.

Everything else remains uncommitted and untouched.

---

## Commands for tomorrow

Start the dashboard (never `next dev` via raw bash — use the preview tool, or):

```bash
cd /Users/Jeff/Workspaces/agentos/source && npm run dev
```

Verify the LINE bridge end to end:

```bash
curl -s -X POST http://localhost:3737/api/media-vocab/ingest -H 'Content-Type: application/json' -d '{"text":"The proposal was surprisingly cogent.","sourceType":"line"}'
```

Check what the deck actually got:

```bash
python3 -c "import json,os;c=json.load(open(os.path.expanduser('~/.agentos/english/cards.json')))['cards'];m=[x for x in c if x.get('source')=='media'];print(len(c),'cards |',len(m),'from media')"
```

Build + lint:

```bash
cd /Users/Jeff/Workspaces/agentos/source && npm run build && npm run lint
```

---

## Suggested next move

Mobile shell, or wire Smith's LINE handler to actually POST the ingest
endpoint. The second one is smaller and is the thing that makes this feel
like Jeff's system rather than another dashboard tab — the endpoint is live
and waiting; nothing calls it yet.

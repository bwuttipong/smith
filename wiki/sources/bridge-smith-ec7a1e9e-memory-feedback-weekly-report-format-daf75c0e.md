---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-feedback-weekly-report-format-daf75c0e
title: "Memory Bridge (smith): feedback_weekly_report_format"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/feedback_weekly_report_format.md
bridgeRelativePath: memory/feedback_weekly_report_format.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-05-27T09:05:07.753Z
---

# Memory Bridge (smith): feedback_weekly_report_format

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/feedback_weekly_report_format.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-05-27T09:05:07.753Z

## Content
````markdown
---
name: Weekly MRP Report — Format & Process
description: Exact format and process for Wuttipong's weekly MRP report — Gmail draft, Slack Canvas update, bilingual structure
type: feedback
originSessionId: 637897f0-e7e1-4d8b-90fb-c27314cd996b
---
Never use Slack emoji shortcodes (`:large_green_circle:`) or Markdown asterisks (`*bold*`) in Gmail drafts — they render as literal text. Always use HTML with `<strong>` tags and Unicode emoji (🟢, ✅, 📋, etc.).

**Why:** User reviewed draft and found it unreadable — asterisks and Slack codes showed as plain text in Gmail.

**How to apply:** Always use `--body-html` with `gog gmail draft create`. Never `--body` for styled weekly reports.

---

## Weekly Report Process (MRP — Infor Food Packaging)

**Step 1 — Pull from Notion**
- API key: `~/.config/notion/api_key`
- Page: `3680da1b1be6807b9d22ce2a5a212ad0`
- Fetch page + child pages (Phase 2: `3680da1b-1be6-80ee-a99f-dcbe1097a1bd`, Phase 3: `3680da1b-1be6-8052-86b4-e0f454ae4bbd`)

**Step 2 — Update Slack Canvas**
- Canvas file ID: `F0AMYHAAS3Y` (titled "Weekly")
- API: `POST https://slack.com/api/canvases.edit`
- Token: `$SLACK_BOT_TOKEN` (env var, not in config file)
- Use `operation: "replace"` with `type: "markdown"`

**Step 3 — Create Gmail Draft**
- `gog gmail draft create --to wuttipong.t@flexpak.co.th --subject "..." --body-html "..." --no-input`
- Subject format: `[Weekly Update] MRP (Infor Food Packaging) | Week Ending, May DD, YYYY / [อัฟเดทประจำสัปดาห์] MRP (Infor Food Packaging) | DD พฤษภาคม YYYY`
- Do NOT send — create draft only, let user review first

---

## Email Body Structure (HTML)

```
📋 [Weekly Update] MRP (Infor Food Packaging)
Week Ending: Saturday, [date] | Draft generated: [date] at HH:MM (ICT)
---

🟢 Status
🟢 On Track

📋 Executive Summary
📌 [date range] — [narrative]

🚀 This Week
• ✅ item
• ✅ item
🔎 Pending: [items]

🥅 Next Week
• [ ] item

🔥 Notes to Self
• note
---
[Full Thai translation]
---
Thanks a ton.
Kind regards,
Wuttipong
Project: MRP — Infor Food Packaging
```

**Thai numerals:** Use ๑๒๓ style for dates in Thai section.
**Completed items:** `• ✅ item` (no strikethrough needed in HTML body)
**Next week items:** `• [ ] item`

````

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

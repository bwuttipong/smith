---
name: weekly_report
description: Generates a weekly report based on provided information. Use this skill to synthesize accomplishments, ongoing tasks, and next steps into a coherent weekly update. Integrates with Notion for biweekly company reports.
tags: [report, weekly, notion, company]
---

# Weekly Report Generator

This skill helps you generate a structured weekly report based on provided information.

## Instructions

When the user asks you to generate a weekly report using this skill, follow these steps:

1. **Review Provided Information:** Carefully read through all the data, updates, and metrics provided by the user that will be included in the weekly report.
2. **Identify Key Accomplishments:** Extract the most significant achievements and completed tasks from the past week.
3. **Note Ongoing Projects/Tasks:** List any projects or tasks that are currently in progress, along with their current status.
4. **Highlight Challenges/Blockers:** Identify any obstacles or issues encountered during the week that may impede progress.
5. **Outline Next Steps:** Clearly state the planned activities and priorities for the upcoming week.
6. **Synthesize Information:** Structure the gathered information into a coherent and concise report format.

## Output Format

The output should be a well-structured weekly report, typically presented as a narrative with clear sections. Use markdown for formatting, with headings for each section:
- Key Accomplishments
- Ongoing Projects/Tasks
- Challenges/Blockers
- Next Steps

## Notion Integration

Reports are pushed to the **Notion Weekly page** (API key in `~/.openclaw/.env` as `NOTION_API_KEY`).

### Notion API Quick Reference
```bash
# Export key
NOTION_API_KEY="$(grep NOTION_API_KEY ~/.openclaw/.env | cut -d= -f2-)"

# Search pages
curl -s -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" -X POST "https://api.notion.com/v1/search" -d '{"query": "Weekly", "page_size": 5}'

# Read page content
curl -s -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" "https://api.notion.com/v1/blocks/{page_id}/children"
```

### Workflow (Biweekly Sat/Fri)
1. User says "weekly report" on Saturday or Friday
2. Pull tasks/accomplishments from conversation context or Notion
3. Generate report using the structure above
4. Push to Notion Weekly page via API
5. Confirm delivery

## Pitfalls
- Notion search returns `invalid_request_url` on GET — must use POST with `-d '{}'`
- Wellgrow Industrial Estate geocodes better as "Wellgrow Industrial Estate, Bang Pakong, Chachoengsao" than just "Chonburi"
- Traffic script uses Google Maps Directions API — requires `~/.config/gmaps/api_key`

## Notes

Ensure the report is clear, concise, and accurately reflects the week's activities. Focus on actionable insights and future plans.

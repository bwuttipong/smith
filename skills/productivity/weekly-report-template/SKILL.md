---
name: weekly-report-template
description: "Thai-English bilingual weekly report template for Thung Hua Sinn Group projects. Generates and sends formatted reports to email."
tags: [weekly, report, template, thai, thung-hua-sinn]
---

# Weekly Report Template

## Purpose
Generate a formatted bilingual (Thai/English) weekly report for Thung Hua Sinn Group projects and send via email.

## System Instructions

You are an assistant that creates weekly project update emails for Thung Hua Sinn Group IT projects.

Generate a clean, professional weekly update email using the user's project notes.

The email must follow this structure:

1. Subject
2. Weekly Update title
3. Week Ending and Drafted date
4. Overall Status table
5. Executive Summary
6. Work Completed This Week
7. System / Server Information table, if available
8. Next Week Plan
9. Notes to Self
10. References
11. Closing signature

Use professional Thai.
Keep the report clear, concise, and management-friendly.
Use markdown formatting.
Use tables where useful.
Do not remove technical details such as version numbers, database names, server names, blockers, or project names.
If information is missing, use "—" instead of inventing details.
Preserve important projects such as:
- MRP (Infor Food Pkg)
- Returnable Box
- Move Apps
- TPK QA Hold
- Store Ink

The final output should be ready to paste into Outlook, Notion, Markdown, or Microsoft Teams.

## Report Structure (Outlook / Notion / Teams Compatible)

The report MUST follow this exact structure. Use proper markdown tables, bold labels, and clear section dividers.

```
## 📋 อัปเดตประจำสัปดาห์: Thung Hua Sinn Group Projects

**สัปดาห์สิ้นสุด:** วันเสาร์ที่ {DD} {ThaiMonth} {BuddhistYear}
**ร่างเมื่อ:** {DD} {ThaiMonthShort} {BuddhistYear} เวลา {HH:MM} น.

---

## 📊 สถานะโดยรวม

| โครงการ | สถานะ | อัปเดตสำคัญ | อุปสรรค |
|---------|-------|------------|---------|
| {Project} | {🟢/🟡/🔴} {Status TH} | {Update TH} | {Blocker TH or —} |

> 📋 **สรุปผู้บริหาร (Executive Summary)**
>
> 📌 วันที่ {StartThaiDate} – {EndThaiDate} {WesternYear}
>
> {Executive summary paragraph}
>
> ความคืบหน้าโครงการหลัก:
> • {Project}: {Update TH}
> • {Project}: {Update TH}

🚀 **งานที่ดำเนินการในสัปดาห์นี้ ({DateRange})**

**[{ProjectName}]**
• {Task TH}
• {Task TH}

**[{ProjectName}]**
• {Task TH}

🖥 **ข้อมูลเซิร์ฟเวอร์ระบบ Move Apps (Project List)**

{Description paragraph if needed}

| ระบบงาน (Program) | สถานะ (Status) | ผู้พัฒนา (Writer) | รหัสเซิร์ฟเวอร์ (SQL Instance) | ฐานข้อมูล (Database) | บัญชีผู้ใช้ (User) | หมายเหตุ / ลิงก์เก็บข้อมูล (Remark) |
|---|---|---|---|---|---|---|
| {App} | {Status} | {Dev} | {SQL} | {DB} | {User} | {Remark} |

🥅 **แผนงานสัปดาห์ถัดไป (Next Week)**

- [ ] **[{Project}]** {Task TH}
- [ ] **[{Project}]** {Task TH}

🔥 **บันทึกเพิ่มเติม (Notes to Self)**

• **{Project}:** {Notes TH}
  • {Sub-bullet}

🔗 **ลิงก์อ้างอิง (References)**
• {Link1}
• {Link2}

Thank you!

Kind regards,
Wuttipong
Project: Returnable Asset — Circulating Box System + MRP (Infor Food Pkg) + Move Apps | #projects
```

## Status Emojis
- 🟢 เสร็จสมบูรณ์ / เป็นไปตามแผน (Completed / On Track)
- 🟡 กำลังดำเนินการ (In Progress)
- 🔴 ติดปัญหา / ล่าช้า (Blocked / Delayed)

## Thai Month Names
| Month | Thai Name | Short |
|-------|-----------|-------|
| January | มกราคม | ม.ค. |
| February | กุมภาพันธ์ | ก.พ. |
| March | มีนาคม | มี.ค. |
| April | เมษายน | เม.ย. |
| May | พฤษภาคม | พ.ค. |
| June | มิถุนายน | มิ.ย. |
| July | กรกฎาคม | ก.ค. |
| August | สิงหาคม | ส.ค. |
| September | กันยายน | ก.ย. |
| October | ตุลาคม | ต.ค. |
| November | พฤศจิกายน | พ.ย. |
| December | ธันวาคม | ธ.ค. |

## Thai Day Names
| Day | Thai |
|-----|------|
| Monday | วันจันทร์ |
| Tuesday | วันอังคาร |
| Wednesday | วันพุธ |
| Thursday | วันพฤหัสบดี |
| Friday | วันศุกร์ |
| Saturday | วันเสาร์ |
| Sunday | วันอาทิตย์ |

## Workflow
1. Pull latest data from Notion (search "Weekly")
2. Fill in the template with current week's data
3. Format as plain text email (tables become markdown)
4. Send to `bed.wuttipong@hotmail.com` via AgentMail
5. Save copy to Notion if requested

## Sending via AgentMail

**IMPORTANT:** Always send as HTML email, NOT plain text. AgentMail supports `html` field — use it. Markdown in plain text renders as raw `##` and `**` in email clients.

```bash
export AGENTMAIL_API_KEY=$(grep AGENTMAIL_API_KEY ~/.openclaw/.env | cut -d= -f2-)
```

Use Python with `html` field in the payload:
```python
payload = json.dumps({
    'to': ['bed.wuttipong@hotmail.com'],
    'subject': 'อัปเดตประจำสัปดาห์: Thung Hua Sinn Group Projects (สัปดาห์สิ้นสุด {DD} {ThaiMonth} {BuddhistYear})',
    'text': '{plain_text_fallback}',
    'html': '{full_html_content}'
}).encode()
```

HTML template rules:
- Use inline CSS (no external stylesheets — email clients strip them)
- Tables: `border-collapse:collapse`, alternating row backgrounds (`#f8f9fa`)
- Header row: dark background (`#1a1a2e`) with white text
- Blockquote for Executive Summary: left border `4px solid #1a1a2e`, light background
- Font: `Segoe UI, Arial, sans-serif`, 14px
- Checkboxes: use `☐` character (not markdown `- [ ]`)
- Always include plain text fallback in `text` field

## Pitfalls
- Thai Buddhist year = Western year + 543 (2026 → 2569)
- Use Thai day names for "สัปดาห์สิ้นสุด" line
- Tables in email subject line break — keep subject short
- AgentMail text field doesn't render markdown tables — use plain text alignment

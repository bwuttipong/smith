# Circulating_Box (Returnable Box)

## Quick Facts

| Field | Value |
|-------|-------|
| **Location** | `C:\Users\Wuttipong.t\Workspaces\Circulating_Box` |
| **Status** | 🟢 Active |
| **Solution** | `CirculatingBox\CirculatingBox.slnx` (.slnx format) |
| **Framework** | .NET 9 (modern) |
| **Deploy** | `\\192.168.95.200\TPKShare\IT\Box\` |
| **Slack Channel** | `#projects` (Canvas `F0AMYHAAS3Y`) |

## Solution Structure

```
Circulating_Box/
├── CirculatingBox/
│   ├── CirculatingBox/          — main app
│   ├── AuditCheckApp/           — audit verification tool
│   ├── NotificationHub/         — SignalR real-time notifications
│   ├── TestConsole/             — test harness
│   ├── SQL/                     — database scripts
│   └── Icons/                   — UI icons
├── Circulating Box - User Manual v1.0.*.pdf
├── Circulating Box User Manual.docx
└── OverrideTest.json
```

## Sub-Projects

| Project | Purpose |
|---------|---------|
| `CirculatingBox` | Main box tracking app |
| `AuditCheckApp` | Audit verification — checks box status |
| `NotificationHub` | SignalR server — real-time push to clients |
| `TestConsole` | Test harness / dev tooling |

## Key Features

- **Box tracking** — location, FIFO management, Receiving–Issuing
- **BOXSOFT material numbers** — barcode system
- **SignalR notifications** — real-time updates to shop floor
- **Audit checking** — verification workflow

## Core Tables (from MEMORY.md)

- `StockLayer` — inventory tracking
- `Box` — box master data
- `tbl_box_rec` — receiving transactions
- `tbl_box_issu_in_out` — issuing in/out transactions

## Deployment

| Script | Purpose |
|--------|---------|
| `Publish-To-Desktop.bat` | Local desktop deploy |
| `One-click modern deployment.txt` | Modern deployment guide |
| `Deploy cmd.txt` | Deploy commands |

## Prior AI Work

This project was previously worked on by other AIs:
- `AGENTS.md` — agent instructions (check for context)
- `CLAUDE.md` — Claude-specific instructions
- `QWEN.md` — Qwen-specific instructions

**Read these before making changes** — they may contain important conventions.

## Documentation

- `SIGNALR_*.md` — SignalR implementation docs
- `NOTIFICATION_HUB_SERVER_SETUP.md` — server setup guide
- `README_SIGNALR.md` — SignalR overview
- `Circulating Box - User Manual v1.0.3.pdf` — latest user manual

## Recent Fix (2026-06-26)

- ClickOnce deployment crash — fixed with `<PublishSingleFile>True</PublishSingleFile>` + `<IncludeNativeLibrariesForSelfExtract>True</IncludeNativeLibrariesForSelfExtract>`
- Version bumped to 3.1.0.31

---

*Last updated: 2026-07-03*

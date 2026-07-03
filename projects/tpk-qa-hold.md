# TPK QA Hold (TPNShopFloor)

## Quick Facts

| Field | Value |
|-------|-------|
| **Location** | `C:\Users\Wuttipong.t\Workspaces\TPK QA Hold` |
| **Status** | 🟢 Active |
| **Solution** | `TPNShopFloor.sln` |
| **Project** | `TPNShopFloor\TPNShopFloor.csproj` |
| **Framework** | .NET Framework 4.7.2 (WinForms) |
| **Assembly** | `TPK-QA Hold.exe` |
| **Excel** | ClosedXML 0.105.0 |
| **Namespace** | `TPN_Shop_Floor` |

## Architecture — Clean Architecture ✅

```
TPNShopFloor/
├── Core/
│   ├── Domain/
│   │   ├── HoldRecord.cs      — QA hold transaction model
│   │   ├── JobDetails.cs      — ERP job data model
│   │   ├── Department.cs      — Department reference
│   │   └── Operator.cs        — Operator reference
│   └── Interfaces/
│       ├── IHoldRepository.cs      — hold data access contract
│       ├── IErpJobRepository.cs    — ERP job read contract
│       ├── IExcelExporter.cs       — Excel export contract
│       └── IQAlertImageService.cs  — alert image contract
├── Infrastructure/
│   ├── Data/
│   │   ├── SqlHoldRepository.cs     — raw SQL hold CRUD
│   │   └── SqlErpJobRepository.cs   — raw SQL ERP reads
│   └── Services/
│       ├── ClosedXmlExcelExporter.cs — Excel reporting
│       └── UNCAlertImageService.cs   — alert images from UNC path
├── Presentation/
│   ├── frmMain.cs / .Data.cs / .Operations.cs — main form (split files)
│   ├── frmQAlert.cs             — QA alert popup
│   └── FormModernizer.cs        — UI modernization helpers
└── Program.cs
```

## Databases

| Database | Server | Access | Purpose |
|----------|--------|--------|---------|
| `csgwin-tpk` | `192.168.95.150` | Read-only | ERP job details source |
| `QA` | `192.168.95.100\SQLEXPRESS` | Read/Write | Hold transactions (`HoldData` table) |

**No DbContext** — uses raw ADO.NET via `SqlHoldRepository` and `SqlErpJobRepository`.

## NuGet Packages

- ClosedXML 0.105.0 + ClosedXML.Parser 2.0.0
- DocumentFormat.OpenXml 3.1.1
- RBush.Signed 4.0.0 (spatial indexing?)
- SixLabors.Fonts 1.0.0

## Key Forms

| Form | Purpose |
|------|---------|
| `frmMain` | Dashboard — hold entry, search, reporting |
| `frmQAlert` | QA alert popup |

## Notes

- Clean Architecture is well-structured — rare for a WinForms app
- `frmMain` is split into 3 partial classes (UI, data, operations) — good separation
- Legacy .NET Framework — would need significant work to migrate to .NET 9
- `FormModernizer.cs` suggests UI modernization effort in progress

---

*Last updated: 2026-07-03*

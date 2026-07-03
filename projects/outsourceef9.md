# OutsourceEF9 (tpn-outsource)

## Quick Facts

| Field | Value |
|-------|-------|
| **Location** | `C:\Users\Wuttipong.t\Workspaces\OutsourceEF9` |
| **Status** | 🟢 Active |
| **Solution** | `OutsourceEF9.sln` |
| **Project** | `OutsourceEF9\OutsourceEF9.csproj` |
| **Framework** | .NET 9.0-windows (WinForms) |
| **Assembly** | `Outsource.exe` |
| **ORM** | EF Core 9.0.0 + SqlServer |
| **Excel** | ClosedXML 0.105.0 |
| **Deploy** | `\\192.168.95.200\TPKShare\IT\Outsource\OutsourceEF9\` |

## Architecture

- **Pattern**: WinForms monolith (single Form1.cs)
- **Config**: `DbConfigHelper.cs` — resolves DB connection dynamically
  1. `OUTSOURCE_CONFIG_PATH` env var
  2. Fallback: `\\192.168.95.200\TPKShare\IT\Outsource\config.json`

## DbContext Classes (4 total)

| Context | Purpose | Tables |
|---------|---------|--------|
| `TpndbContext` | Main database | Core TPN data |
| `TpnJoborderContext` | Job orders | Pickup, job tracking |
| `TpnprintingContext` | Printing system | Print jobs, labels |
| `TpnLiveContext` | Live views | `V_Item_Cust_Name` (customer items) |

All in `OutsourceEF9\Models\` directory.

## Key Files

| File | Purpose |
|------|---------|
| `Form1.cs` | Main UI (3141+ lines — large monolith) |
| `Configs.cs` | Configuration constants |
| `DbConfigHelper.cs` | Dynamic DB config resolver |
| `Models/*.cs` | EF Core DbContext classes |

## Deploy

```powershell
./publish.ps1
# Builds and copies ClickOnce setup files to network share
```

## Notes

- Monolithic Form1.cs — consider extracting services if adding features
- 4 separate DbContexts suggest multiple databases or schemas
- TpnLiveContext uses `TpndbContext` options (possible shared connection)

---

*Last updated: 2026-07-03*

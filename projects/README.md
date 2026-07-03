# Projects Registry

Cross-project context for Smith. Each project has its own context file with architecture, conventions, and active tasks.

## Active Projects

| Project | Status | Location | Stack |
|---------|--------|----------|-------|
| [OutsourceEF9](outsourceef9.md) | 🟢 Active | `Workspaces\OutsourceEF9` | .NET 9, WinForms, EF Core (4 DbContexts) |
| [TPK QA Hold](tpk-qa-hold.md) | 🟢 Active | `Workspaces\TPK QA Hold` | .NET 4.7.2, WinForms, Clean Architecture, raw SQL |
| [CirculatingBox](circulatingbox.md) | 🟢 Active | `Workspaces\Circulating_Box` | .NET 9, WinForms, SignalR, multi-project |

## How to Use

1. When a project is copied to this machine, update its context file with the actual path
2. Run initial scan: `Get-ChildItem -Recurse *.sln,*.csproj` in the project dir
3. Update status from 🟡 to 🟢

## Conventions

- All projects are WinForms + SQL Server (TPN standard)
- Deploy to `\\192.168.95.200\TPKShare\IT\`
- ClickOnce deployment preferred
- Git for source control (no remote for most)

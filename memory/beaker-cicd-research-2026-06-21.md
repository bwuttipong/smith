# CI/CD + DevOps Research Brief: VB.NET / .NET 9 WinForms + SQL Server + ClickOnce

**Date:** 2026-06-21  
**Target Stack:** VB.NET WinForms (.NET 9) + SQL Server + ClickOnce deployment  
**Prepared for:** Jeff

---

## 1. CI/CD Comparison: GitHub Actions vs Azure DevOps vs GitLab CI

### Quick Verdict: **GitHub Actions wins** for this stack.

| Factor | GitHub Actions | Azure DevOps | GitLab CI |
|--------|----------------|--------------|-----------|
| **WinForms/.NET Desktop support** | ✅ First-class via `windows-latest` runners; Microsoft-maintained starter workflows & `github-actions-for-desktop-apps` repo | ✅ Native Windows agents; mature ClickOnce tasks | ⚠️ Works via Docker-in-Docker; no native Windows runners on SaaS |
| **ClickOnce automation** | ✅ Native MSBuild + `microsoft/setup-msbuild`; Cake.ClickOnce.Recipe; MSIX/AppInstaller support | ✅ Dedicated ClickOnce tasks; mature but legacy-feeling | ❌ Manual scripting required |
| **SQL Server / EF Core migrations** | ✅ `dotnet-ef` bundles; Azure SQL deploy actions; GitHub Environments for approval gates | ✅ Built-in SQL DACPAC deploy; release gates | ✅ Good via templates; less .NET-specific |
| **Cost (OSS/small team)** | ✅ Free for public; generous private minutes | ⚠️ Free tier limited (1800 min/mo) | ✅ Generous free tier (400 CI min/mo) |
| **Secret management** | ✅ Repository/Environment secrets; OIDC to Azure | ✅ Variable groups; Key Vault integration | ✅ CI/CD variables; Vault integration |
| **VB.NET friendliness** | ✅ `dotnet build`/`msbuild` agnostic | ✅ MSBuild-first | ✅ MSBuild via Docker |
| **Ecosystem momentum** | ✅ High (.NET 9 samples, MSFT investment) | ⚠️ Stable but legacy perception | ⚠️ Strong but Linux-first |

### Why GitHub Actions Wins
1. **Microsoft owns it** — .NET 9 desktop workflows are maintained by MSFT (`actions/starter-workflows`, `microsoft/github-actions-for-desktop-apps`)
2. **Windows runners are free** — `windows-latest` gives you a real Windows VM with VS Build Tools pre-installed
3. **ClickOnce is a solved problem** — See Cake.ClickOnce.Recipe (devlead) + GitHub Actions sample; MSIX/AppInstaller is the modern path
4. **SQL Server integration** — `azure/sql-action`, EF Core migration bundles, Environment protection rules for DB approvals
5. **VB.NET is just another MSBuild target** — no language-specific gaps

### When to pick Azure DevOps instead
- Already on Azure DevOps Server (on-prem)
- Need TFVC or complex release pipelines with manual approvals across many environments
- Heavy investment in Azure Artifacts/Boards/Test Plans

### When to pick GitLab CI instead
- Self-hosted runners on Windows (you manage the VMs)
- Single platform for everything (repo + CI + registry + security)
- Kubernetes-first backend deployments

---

## 2. Docker Reality Check: Can WinForms Be Containerized?

### Short Answer: **Yes, but not for the UI tier.** Containerize backend services only.

### The Hard Truth About WinForms in Containers

| Scenario | Feasibility | Reality |
|----------|-------------|---------|
| **Run WinForms GUI inside Linux container** | ❌ Impossible | WinForms = Windows-only UI stack (GDI+/USER32). No X11/Wayland support. |
| **Run WinForms GUI inside Windows container (process isolation)** | ⚠️ Technically possible | Requires Windows Server host (not Win10/11 for prod). Session 0 isolation = no interactive desktop. Users **cannot see or interact** with the UI. |
| **Run WinForms GUI inside Windows container (Hyper-V isolation)** | ⚠️ Possible | True VM-level isolation. Still **no interactive GUI access** for end users. |
| **Package WinForms as MSIX/AppInstaller in container** | ✅ Works great | Build/publish in container → output MSIX/ClickOnce artifacts → distribute to real Windows machines. |

### What *Actually* Works in Containers (Backend Tier)

| Component | Containerization | Notes |
|-----------|------------------|-------|
| **ASP.NET Core Web API / Minimal APIs** | ✅ First-class | Linux containers, `mcr.microsoft.com/dotnet/aspnet:9.0` |
| **EF Core / SQL Server** | ✅ First-class | Run migrations via init containers or migration bundles |
| **Background workers / hosted services** | ✅ First-class | Generic host, Linux containers |
| **gRPC services** | ✅ First-class | HTTP/2, Linux containers |
| **Azure Functions / Container Apps** | ✅ First-class | Deploy the same container image |

### Recommended Architecture: **Hybrid**

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions CI/CD                     │
├─────────────────────┬───────────────────────────────────────┤
│   WinForms Client   │           Backend Services            │
│   (ClickOnce/MSIX)  │         (Linux Docker Containers)     │
├─────────────────────┼───────────────────────────────────────┤
│ • Build on          │ • ASP.NET Core 9 Web API              │
│   windows-latest    │ • EF Core 9 + SQL Server              │
│ • Sign + publish    │ • Build → linux/amd64 image           │
│   ClickOnce/MSIX    │ • Deploy to Azure Container Apps /    │
│ • Artifact →        │   AKS / App Service                   │
│   GitHub Releases   │ • gMSA for SQL auth (Windows nodes)   │
│   or Azure Blob     │                                       │
└─────────────────────┴────────────────────────────────────────┘
```

### Key Windows Container Gotchas (if you *must* containerize the backend on Windows)
- **Base images are large** — `mcr.microsoft.com/dotnet/framework/sdk:4.8-windowsservercore-ltsc2022` ≈ 6–8 GB
- **Licensing** — Windows Server Core containers require licensed Windows Server host (Datacenter for unlimited)
- **gMSA** — Required for domain auth (SQL integrated auth) — see [Microsoft gMSA docs](https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/gmsa-run-container)
- **Process vs Hyper-V isolation** — Process = density; Hyper-V = security. [FAQ](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/faq)

---

## 3. Migration Path: 5 Concrete Steps (Ordered by Difficulty)

| Step | Difficulty | Timeline | What to Do | Why |
|------|------------|----------|------------|-----|
| **1. Add GitHub Actions CI** | 🟢 Easy | **This week** | Add `.github/workflows/ci.yml` using `dotnet-desktop.yml` starter. Build, test, publish ClickOnce artifacts on every PR. | Zero infrastructure. Immediate PR validation. Catches build breaks instantly. |
| **2. Automate ClickOnce publish to Azure Blob / GitHub Releases** | 🟢 Easy | **This week** | Use Cake.ClickOnce.Recipe or MSBuild `/t:Publish` + `actions/upload-artifact` → release on tag. Store certs in GitHub Secrets. | Eliminates manual "Publish" wizard. Versioning via Nerdbank.GitVersioning. |
| **3. Extract backend → ASP.NET Core 9 + containerize** | 🟡 Medium | **2–4 weeks** | Move SQL logic, business rules, auth to Web API. `dotnet new webapi` → Dockerfile → `docker buildx` → GHCR/Azure Container Registry. | Enables real CI/CD for server logic. Scales independently. Linux containers = cheap/fast. |
| **4. Add DB migration gates + environments** | 🟡 Medium | **4–6 weeks** | EF Core migration bundles → GitHub Environment `staging` (auto) → `production` (manual approval). Backup before prod. | Safe schema changes. Audit trail. Rollback plan. |
| **5. Modernize client delivery → MSIX / AppInstaller** | 🔴 Hard | **3–6 months** | Migrate ClickOnce → MSIX (Windows Application Packaging Project). Sideload + Store channels. Auto-update via AppInstaller. | ClickOnce is legacy. MSIX = modern, sandboxed, Store-ready, per-machine/per-user. |

---

## 4. Quick Wins: 3 Things to Do This Week (No Breaking Changes)

| # | Action | Time | How |
|---|--------|------|-----|
| **1** | **Add CI workflow** | 30 min | Copy `dotnet-desktop.yml` → `.github/workflows/ci.yml`. Update `Solution_Name`, `Test_Project_Path`. Push. Watch green checks. |
| **2** | **Store signing cert + password as GitHub Secrets** | 15 min | `Settings → Secrets → Actions → New repository secret`: `Base64_Encoded_Pfx` (base64 `.pfx`), `Pfx_Key` (password). Enables signed ClickOnce/MSIX from CI. |
| **3** | **Enable Nerdbank.GitVersioning** | 20 min | `dotnet add package Nerdbank.GitVersioning` → add `version.json` → add `uses: aarnott/nbgv@master` step in workflow. Every build gets semantic version (e.g., `1.2.159.47562`) auto-injected into `AssemblyInfo` + ClickOnce manifest. |

---

## 📋 Summary Cheat-Sheet

| Topic | Decision / Action |
|-------|-------------------|
| **CI/CD Platform** | **GitHub Actions** — free Windows runners, MSFT-maintained desktop workflows, ClickOnce/MSIX native |
| **WinForms in Docker** | **Don't.** Build/publish in CI → ship ClickOnce/MSIX to real Windows machines. Containerize *backend only* (Linux). |
| **ClickOnce → Modern** | Use **Cake.ClickOnce.Recipe** now; plan **MSIX + AppInstaller** migration (6–12 mo horizon). |
| **SQL Server in CI** | EF Core migration bundles + GitHub Environment protection rules (staging auto, prod manual). |
| **Versioning** | **Nerdbank.GitVersioning** — zero config, git-height-based, feeds AssemblyVersion/FileVersion/ClickOnce. |
| **Secrets** | GitHub Secrets for certs/connection strings; OIDC to Azure for deploy (no long-lived secrets). |
| **First PR** | Add `ci.yml` + `Base64_Encoded_Pfx` + `Pfx_Key` + `version.json` = **fully automated signed builds today**. |

---

## 🔗 Key Sources

- [GitHub Actions starter workflow: dotnet-desktop.yml](https://github.com/actions/starter-workflows/blob/main/ci/dotnet-desktop.yml) — official .NET desktop CI template
- [microsoft/github-actions-for-desktop-apps](https://github.com/microsoft/github-actions-for-desktop-apps) — WPF/WinForms CI/CD reference implementation (MSIX, signing, channels)
- [Cake.ClickOnce.Recipe (devlead)](https://github.com/devlead/Cake.ClickOnce.Recipe) — ClickOnce automation via Cake + GitHub Actions → Azure Blob
- [Nerdbank.GitVersioning](https://github.com/AArnott/Nerdbank.GitVersioning) — automatic semantic versioning from git history
- [Windows Containers FAQ](https://learn.microsoft.com/en-us/virtualization/windowscontainers/about/faq) — licensing, isolation, gMSA, process vs Hyper-V
- [Streamlining .NET 9 Deployment with GitHub Actions and Azure](https://www.milanjovanovic.tech/blog/streamlining-dotnet-9-deployment-with-github-actions-and-azure) — complete pipeline with DB migrations, environments, coverage
- [Building .NET using GitLab CI/CD](https://b.j4.lc/2025/01/15/building-net-using-gitlab-ci-cd/) — GitLab .NET 9 Docker + NuGet registry approach
- [Azure DevOps ClickOnce Pipeline 2025](https://programming.gonevis.com/azure-devops-pipeline-for-clickonce-deployment-in-2025/) — Azure Pipelines YAML for ClickOnce

---

**Bottom line:** Start with GitHub Actions CI today. It costs nothing, runs on real Windows, and the Microsoft desktop team maintains the templates. Containerize the SQL/backend tier on Linux. Keep WinForms native — ship MSIX/ClickOnce artifacts to users. Modernize the installer (MSIX) on your own timeline.
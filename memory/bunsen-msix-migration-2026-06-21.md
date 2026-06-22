# Research Report: Modernize TPN Flexpak ClickOnce Deployment to MSIX with CI Pipeline

**Date:** 2026-06-21
**Author:** Dr. Bunsen Honeydew (Bunsen), Senior Research Lead
**Client:** Jeff (Wuttipong Thongmon), TPN Flexpak
**Status:** Complete — actionable findings ready

---

## Executive Summary

TPN Flexpak's two VB.NET WinForms apps (OutsourceEF9 and TPK QA Hold) currently deploy via ClickOnce using `publish.ps1` to a network share at `\\192.168.95.200\TPKShare\`. This report evaluates migrating to MSIX packaging with a GitHub Actions CI pipeline. **Recommendation: Proceed with phased migration.** MSIX provides cleaner install/uninstall, enterprise management, and CI/CD integration. The primary investment is a code signing certificate (~$150–300/yr) and the time to set up the packaging project and pipeline. Quick wins are achievable this week.

---

## 1. Why MSIX Over ClickOnce

### Comparison at a Glance

| Criterion | ClickOnce | MSIX |
|-----------|-----------|------|
| Clean uninstall | Partial (some artifacts remain) | Full (containerized, removes everything) |
| Package identity | ❌ No | ✅ Yes (enables AppLocker, GP, etc.) |
| Update model | Built-in, simple | App Installer with force-update, downgrade, channels |
| Enterprise management | Limited | Intune, ConfigMgr, DISM, Group Policy |
| CI/CD integration | Manual (publish.ps1) | Native (GitHub Actions, Azure Pipelines) |
| OS requirements | Windows (any) | Windows 10/11 |
| Code signing | Not required* | Required |
| Per-user install | ✅ Yes | ✅ Yes |
| Per-machine install | ❌ No | ✅ Yes |
| Air-gapped / offline | ✅ Good | ✅ Good |
| Implementation cost | Already done | New setup effort |

*\*ClickOnce can use signing but doesn't require it for internal deployment.*

### Pros of MSIX for TPN Flexpak

1. **Deterministic uninstall** — No leftover registry entries or files after removal. Critical for shop floor machines where app hygiene matters.

2. **Enterprise management** — Group Policy can control installs, AppLocker can restrict execution, updates can be forced. If TPN ever adopts Intune or ConfigMgr, MSIX is ready.

3. **CI/CD friendly** — MSIX packages can be produced and signed entirely in an automated pipeline. No more manual `publish.ps1` on a developer's machine.

4. **Package identity** — Enables Windows features that ClickOnce can't use, like AppLocker rules by publisher, and cleaner integration with Windows Security.

5. **Update control** — The App Installer file lets you force critical updates (`UpdateBlocksActivation`), support downgrades (`ForceUpdateFromAnyVersion`), and schedule update checks.

### Cons / Risks

1. **Code signing is mandatory** — Unsigned MSIX packages cannot be installed. This adds ~$150–300/yr or ~$10/mo for a signing solution.

2. **Learning curve** — Windows Application Packaging Project, manifest editing, and signing setup take time to learn.

3. **App Installer protocol disabled** — The `ms-appinstaller:` URI (one-click web install) has been disabled by default since Dec 2023. Enterprise IT can re-enable via Group Policy, but it's an extra step.

4. **Prerequisites need explicit handling** — If your app depends on the .NET runtime or other components, MSIX requires declaring them as dependencies rather than bundling them.

### Verdict for TPN Flexpak

**MSIX is the right direction.** ClickOnce still works, but it's a legacy technology with no future investment from Microsoft. MSIX aligns with Jeff's DevOps career goal, enables CI/CD, and gives TPN Flexpak a modern deployment story. The risks are manageable.

---

## 2. Packaging Workflow: Converting ClickOnce Apps to MSIX

There are two paths. Since Jeff has source code in Visual Studio, **Path A (Developer approach)** is recommended.

### Path A: Windows Application Packaging Project (Recommended)

**Best for:** Developers with source code access.

**Steps:**

1. **Open the solution** in Visual Studio 2022+
2. **Right-click solution → Add → New Project → Search "Windows Application Packaging Project"**
   - Select "Windows Application Packaging Project" (`.wapproj`)
   - Name it e.g., `OutsourceEF9.Package`
3. **In the Packaging Project, right-click Applications → Add Reference**
   - Select your existing VB.NET WinForms project (OutsourceEF9 or TPK QA Hold)
4. **Configure the Package.appxmanifest**
   - Set Display name, Publisher name, etc.
   - Publisher must match the certificate's subject
5. **Build the Packaging Project**
   - Output: `.msix` file in `AppPackages\` folder
6. **For .NET 9 apps**, the packaging project will bundle the framework-dependent app. If you want self-contained, configure in the .csproj/.vbproj.

**Why this works for VB.NET WinForms:**
- Windows Application Packaging Projects support any desktop app that can be built by MSBuild, including VB.NET projects
- The packaging project acts as a wrapper; your VB.NET code doesn't change
- Full-trust apps run with the `runFullTrust` capability in the manifest

### Path B: MSIX Packaging Tool (Fallback)

**Best for:** When source code isn't available, or for initial experimentation.

**Steps:**

1. **Install the MSIX Packaging Tool** from Microsoft Store
2. **Run the tool**
3. **Select "Application package" → "Create package on this computer"**
4. **Choose the installer type:** ClickOnce
5. **Specify the ClickOnce deployment manifest** (or run the setup manually)
6. **Let the tool monitor installation** — it captures all file system and registry changes
7. **Configure package info** — name, publisher, version
8. **Sign the package** (or defer signing)

**Usage for TPN Flexpak:**
- Use this for an initial proof-of-concept without modifying the solution
- Run the existing ClickOnce installer, have the tool capture it, produce an MSIX
- Then move to Path A for the real pipeline

### Key Considerations for VB.NET + .NET 9

- .NET 9 WinForms apps package without issues in a WAP project
- Set `<TargetFramework>net9.0-windows10.0.19041.0</TargetFramework>` if you need specific Windows API support
- For EF Core 9 with SQL Server, ensure the connection string is accessible — consider using `Windows.Data.Xml.Dom.AppSettings` or an external config file
- **No code changes** are required for VB.NET → MSIX conversion in most cases

---

## 3. Code Signing Requirements

MSIX packages **must** be signed. Here are the options for TPN Flexpak, ranked by suitability.

### Option A: Self-Signed Certificate (Dev/Test) — Free

| Detail | Value |
|--------|-------|
| Cost | Free |
| Trust | ❌ Not trusted by Windows by default |
| Use case | Local testing, initial development |

**How to create:**
```powershell
New-SelfSignedCertificate -Type Custom -Subject "CN=TPN Flexpak, O=TPN Flexpak, C=TH" `
  -KeyUsage DigitalSignature -FriendlyName "TPN Flexpak Code Signing" `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")
```

**For enterprise distribution:** Deploy the self-signed .cer to the Trusted Root store via Group Policy. Once trusted, MSIX packages signed with it install without warnings.

### Option B: OV Certificate — $150–300/year ✅ RECOMMENDED

| Detail | Value |
|--------|-------|
| Cost | $150–300/year |
| CA examples | DigiCert, Sectigo, GlobalSign |
| Validation | Organization identity (days to approve) |
| SmartScreen | Reputation builds over time |
| Availability | 🌍 Worldwide (no geographic restrictions) |

**Important for Jeff in Thailand:**
- Azure Artifact Signing (~$9.99/mo) is the cheaper option, but it's **not available in Thailand** (only USA, Canada, EU, UK for orgs; USA/Canada for individuals).
- An OV certificate from a traditional CA is the **best option** for TPN Flexpak.
- As of June 2023, CA/B Forum requires OV certificate private keys to be stored on an HSM or hardware token. Most CAs provide a USB token or cloud HSM.
- DigiCert and Sectigo both support code signing certificate delivery to Thailand.

### Option C: EV Certificate — $400+/year ❌ NOT RECOMMENDED

- Lost its SmartScreen bypass advantage in 2024
- Now behaves identically to OV for SmartScreen
- Only useful if enterprise procurement specifically requires EV

### Signing in CI/CD

**For automated pipelines:**

1. **Import the PFX to Azure Key Vault** (or store as a GitHub secret)
2. **Use AzureSignTool** (open source, works in GitHub Actions)
   ```bash
   dotnet tool install --global AzureSignTool
   AzureSignTool sign -kvu "<keyvault-url>" -kvi "<app-id>" -kvs "<secret>" \
     -kvc "<cert-name>" -tr http://timestamp.digicert.com -v app.msix
   ```
3. **Or use the standard SignTool** with the PFX decoded from a GitHub secret
   ```yaml
   - name: Sign the package
     run: |
       & "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" sign `
         /fd SHA256 /a /f "$env:USERPROFILE\cert.pfx" /p "${{ secrets.PFX_PASSWORD }}" `
         /tr http://timestamp.digicert.com /td SHA256 `
         "$(Build.ArtifactStagingDirectory)\app.msix"
   ```

### Recommendation for TPN Flexpak

| Phase | Signing Method | Cost |
|-------|---------------|------|
| Week 1-2 (Dev/Test) | Self-signed certificate | Free |
| Week 3+ (Production) | OV certificate (DigiCert/Sectigo) | ~$200/year |
| CI/CD | Store PFX as GitHub secret + Azure Key Vault | Included |

---

## 4. CI Pipeline Design (GitHub Actions)

### Architecture

```
Git Push → GitHub Actions (windows-latest) → Build → Package → Sign → Deploy to Network Share
```

### Concrete Workflow YAML

```yaml
# .github/workflows/build-and-deploy.yml
name: Build, Package & Deploy MSIX

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'src/**'
      - '!src/**/*.md'
  pull_request:
    branches: [ main ]
  workflow_dispatch:      # Allow manual trigger
    inputs:
      environment:
        description: 'Target environment'
        type: choice
        options:
          - dev
          - prod
        default: dev

env:
  DOTNET_VERSION: '9.0.x'
  NETWORK_SHARE: '\\192.168.95.200\TPKShare\MSIX\'
  APPS:
    - OutsourceEF9
    - TPKQAHold

jobs:
  build-and-package:
    runs-on: windows-latest

    strategy:
      matrix:
        app: [OutsourceEF9, TPKQAHold]
      fail-fast: false

    steps:
    - name: Checkout
      uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Setup .NET ${{ env.DOTNET_VERSION }}
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: ${{ env.DOTNET_VERSION }}

    - name: Setup MSBuild
      uses: microsoft/setup-msbuild@v2

    - name: Restore NuGet packages
      run: dotnet restore src/${{ matrix.app }}/${{ matrix.app }}.vbproj

    - name: Build application
      run: dotnet build src/${{ matrix.app }}/${{ matrix.app }}.vbproj `
        --configuration Release `
        --no-restore

    - name: Run unit tests
      run: dotnet test src/${{ matrix.app }}.Tests/${{ matrix.app }}.Tests.vbproj `
        --configuration Release `
        --no-build `
        --logger trx `
        --results-directory "${{ runner.temp }}/TestResults"
      continue-on-error: true

    - name: Build Windows Application Packaging Project
      run: msbuild src/${{ matrix.app }}.Package/${{ matrix.app }}.Package.wapproj `
        /p:Configuration=Release `
        /p:AppxPackage=true `
        /p:AppxBundle=Never `
        /p:UapAppxPackageBuildMode=CI `
        /p:AppxPackageDir="${{ runner.temp }}\AppPackages\${{ matrix.app }}\"

    - name: Decode signing certificate
      if: github.ref == 'refs/heads/main'
      run: |
        $pfxBytes = [System.Convert]::FromBase64String("${{ secrets.MSIX_SIGNING_PFX_BASE64 }}")
        [System.IO.File]::WriteAllBytes("${{ runner.temp }}\cert.pfx", $pfxBytes)

    - name: Sign the MSIX package
      if: github.ref == 'refs/heads/main'
      run: |
        & "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" sign `
          /fd SHA256 `
          /f "${{ runner.temp }}\cert.pfx" `
          /p "${{ secrets.MSIX_SIGNING_PFX_PASSWORD }}" `
          /tr http://timestamp.digicert.com `
          /td SHA256 `
          "${{ runner.temp }}\AppPackages\${{ matrix.app }}\*${{ matrix.app }}*.msix"

    - name: Clean up certificate
      if: always()
      run: Remove-Item -Path "${{ runner.temp }}\cert.pfx" -Force -ErrorAction SilentlyContinue

    - name: Upload MSIX as build artifact
      uses: actions/upload-artifact@v4
      with:
        name: ${{ matrix.app }}-msix
        path: ${{ runner.temp }}\AppPackages\${{ matrix.app }}\*.msix
        retention-days: 30

    - name: Deploy to network share (main branch only)
      if: github.ref == 'refs/heads/main'
      shell: pwsh
      run: |
        $sharePath = Join-Path $env:NETWORK_SHARE "${{ matrix.app }}\"
        # Map network drive
        net use T: $env:NETWORK_SHARE /user:${{ secrets.NETWORK_DOMAIN }}\${{ secrets.NETWORK_USER }} `
          "${{ secrets.NETWORK_PASSWORD }}"
        Copy-Item "${{ runner.temp }}\AppPackages\${{ matrix.app }}\*.msix" `
          -Destination "T:\${{ matrix.app }}\" -Force
        Copy-Item "${{ runner.temp }}\AppPackages\${{ matrix.app }}\*.appinstaller" `
          -Destination "T:\${{ matrix.app }}\" -Force -ErrorAction SilentlyContinue
        net use T: /delete
      env:
        NETWORK_SHARE: ${{ env.NETWORK_SHARE }}

    - name: Notify on failure
      if: failure()
      uses: slackapi/slack-github-action@v2
      with:
        webhook: ${{ secrets.SLACK_WEBHOOK }}
        webhook-type: incoming-webhook
        payload: |
          text: "❌ MSIX build failed for ${{ matrix.app }}: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
```

### Required GitHub Secrets

| Secret Name | Description |
|-------------|-------------|
| `MSIX_SIGNING_PFX_BASE64` | Base64-encoded PFX certificate file |
| `MSIX_SIGNING_PFX_PASSWORD` | Password for the PFX |
| `NETWORK_USER` | Domain user for network share access |
| `NETWORK_DOMAIN` | Network domain (e.g., `TPK`) |
| `NETWORK_PASSWORD` | Network share password |
| `SLACK_WEBHOOK` | (Optional) Slack notification webhook |

### Self-Hosted Runner Consideration

Since TPN Flexpak is on an internal network, you have two options:
1. **GitHub-hosted runner + VPN/site-to-site** — simplest if VPN exists
2. **Self-hosted runner on a Windows machine inside the network** — use `runs-on: self-hosted` with the `windows` label. This avoids credential exposure for the network share. See [GitHub docs on self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners).

**Recommendation:** Start with a self-hosted runner on a VM or the build server. It eliminates the credential problem for the internal file share and gives you full control.

---

## 5. Distribution Strategy (Internal Network)

TPN Flexpak's shop floor machines are on the same internal network as `\\192.168.95.200\TPKShare\`. Here's how to deliver MSIX packages to them.

### Option A: Network Share + PowerShell (Simplest) ⭐ Recommended

**How it works:**
- GitHub Actions pushes MSIX to the existing network share
- Shop floor machines install via PowerShell

**Install command:**
```powershell
# One-time: trust the signing certificate
Import-Certificate -FilePath "\\192.168.95.200\TPKShare\Certificates\tpk-root.cer" `
  -CertStoreLocation "Cert:\LocalMachine\TrustedPeople"

# Install or update the app
Add-AppxPackage -Path "\\192.168.95.200\TPKShare\MSIX\OutsourceEF9\OutsourceEF9_1.0.0.0_x64.msix"
```

**Auto-update:**
Create a scheduled task on each machine that runs daily:
```powershell
# daily-update.ps1
$latest = Get-ChildItem "\\192.168.95.200\TPKShare\MSIX\OutsourceEF9\*.msix" | 
  Sort-Object LastWriteTime -Descending | Select-Object -First 1
$current = Get-AppxPackage -Name "OutsourceEF9"
if ($current.Version -lt $latest.Version) {
    Add-AppxPackage -Path $latest.FullName
}
```

### Option B: App Installer File (For Managed Updates)

Create an `.appinstaller` file on the network share:

```xml
<!-- OutsourceEF9.appinstaller -->
<?xml version="1.0" encoding="utf-8"?>
<AppInstaller xmlns="http://schemas.microsoft.com/appx/appinstaller/2021">
  <MainPackage 
    Name="TPNFlexpak.OutsourceEF9"
    Publisher="CN=TPN Flexpak, O=TPN Flexpak, C=TH"
    Version="1.0.0.0"
    ProcessorArchitecture="x64"
    Uri="\\192.168.95.200\TPKShare\MSIX\OutsourceEF9\OutsourceEF9.msix" />
  <UpdateSettings>
    <OnLaunch HoursBetweenUpdateChecks="24" 
              UpdateBlocksActivation="true" />
  </UpdateSettings>
</AppInstaller>
```

Users double-click the `.appinstaller` file or install via:
```powershell
Add-AppxPackage -AppInstallerFile "\\192.168.95.200\TPKShare\MSIX\OutsourceEF9\OutsourceEF9.appinstaller"
```

### Option C: Group Policy Software Installation

If TPN Flexpak has Active Directory and Group Policy management:
1. Deploy the signing certificate via Group Policy to Trusted Root store
2. Use Group Policy Software Installation to assign MSIX packages
3. This gives you silent install across all domain-joined machines

### Option D: PDQ / SCCM / Intune (If Available)

- MSIX is natively supported by Microsoft Configuration Manager (SCCM)
- If TPN ever adopts Intune, MSIX apps can be deployed as line-of-business apps
- Third-party tools like PDQ Deploy also support MSIX

### Recommendation for TPN Flexpak

| Phase | Method | Effort | 
|-------|--------|--------|
| Pilot | PowerShell from network share | Low |
| Rollout | Add scheduled task for auto-updates | Medium |
| Mature | Group Policy for cert + MSIX deployment | Medium-High |

The network share approach directly replaces the current ClickOnce flow — same `\\192.168.95.200\TPKShare\`, just MSIX files instead of ClickOnce manifests.

---

## 6. Migration Timeline: Phased Approach

### Phase 0: Foundation (This Week) — Quick Wins

| Day | Task | Deliverable |
|-----|------|-------------|
| **Mon** | Install MSIX Packaging Tool on dev machine | Tool ready |
| **Mon** | Create a self-signed cert for testing | cert.pfx + cert.cer |
| **Tue** | Manually package OutsourceEF9 via Path A (WAP project) | Working .msix on desktop |
| **Tue** | Install the .msix on dev machine (double-click) | Verification it works |
| **Wed** | Create GitHub repo, push code (if not already) | Repo with secrets configured |
| **Wed** | Set up GitHub Actions starter workflow | Workflow runs, produces .msix |
| **Thu** | Test signing with self-signed cert in CI | Signed .msix from pipeline |
| **Fri** | Push .msix to dev network share folder | Pilot-ready package |

**Effort:** ~8 hours total

### Phase 1: Pilot (Week 2-3)

| Week | Task |
|------|------|
| W2 | Refine App Installer file for auto-updates |
| W2 | Install first MSIX on one shop floor QA machine |
| W3 | Monitor: does the app work identically? Any file access issues? |
| W3 | Test the update flow (push new version, verify it updates) |

**Success criteria:** App runs on a shop floor machine, update works from network share.

### Phase 2: Productionize (Week 4-6)

| Week | Task |
|------|------|
| W4 | Purchase OV code signing certificate from DigiCert or Sectigo |
| W4 | Replace self-signed cert with OV cert in pipeline |
| W5 | Deploy OV certificate via Group Policy to all shop floor machines |
| W5 | Package TPK QA Hold (second app) using the same pipeline |
| W6 | Create deployment script / scheduled task for auto-update |
| W6 | Document the process for future maintenance |

### Phase 3: Rollout (Week 7-10)

| Week | Task |
|------|------|
| W7 | Roll OutsourceEF9 MSIX to all contractor management users |
| W8 | Roll TPK QA Hold MSIX to all shop floor QA machines |
| W9 | Retire ClickOnce manifests; keep as fallback |
| W10 | Full cutover — ClickOnce disabled, MSIX is default |

### Risk Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| App doesn't work as MSIX (file access, registry) | Medium | High | Test thoroughly on one machine first; keep ClickOnce as fallback |
| Network share auth in CI pipeline | Medium | Medium | Use self-hosted runner to avoid credential exposure |
| Signing certificate expires | Low | High | Set up calendar reminder 60 days before; use timestamp server |
| Shop floor machines don't support MSIX | Low | High | Verify Windows version (requires Windows 10 1809+) |
| App Installer protocol blocked | Medium | Medium | Use PowerShell `Add-AppxPackage` instead, or re-enable via GP |
| .NET 9 bundled size large | Low | Low | Use framework-dependent deployment; .NET 9 is already on target machines? |

### Rollback Plan

If MSIX causes issues:
1. ClickOnce manifests remain on the network share during Phase 0-2
2. Users can reinstall ClickOnce version until MSIX is stable
3. After Phase 3, keep older MSIX versions available for downgrade (MSIX supports `ForceUpdateFromAnyVersion`)

---

## 7. Quick Wins: What to Do This Week

This is actionable right now, with zero budget and a dev machine:

### ✅ Quick Win 1: Create a self-signed code signing certificate

```powershell
# Run on dev machine as Administrator
$cert = New-SelfSignedCertificate -Type Custom `
  -Subject "CN=TPN Flexpak Dev, O=TPN Flexpak, C=TH" `
  -KeyUsage DigitalSignature `
  -FriendlyName "TPN Flexpak Dev Code Signing" `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

# Export as PFX (with password) and CER (public)
$pwd = ConvertTo-SecureString -String "YourPassword123!" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "C:\Certs\tpk-dev.pfx" -Password $pwd
Export-Certificate -Cert $cert -FilePath "C:\Certs\tpk-dev.cer"
```

### ✅ Quick Win 2: Manually package OutsourceEF9

1. Open solution in VS 2022+
2. Right-click solution → Add → New Project → "Windows Application Packaging Project"
3. Name: `OutsourceEF9.Package`
4. Right-click Applications → Add → Reference → select OutsourceEF9 project
5. Open `Package.appxmanifest`, set basic publisher info
6. Build → produces `.msix` in `OutsourceEF9.Package\AppPackages\`
7. Double-click to install on dev machine

### ✅ Quick Win 3: Install and test the MSIX

```powershell
# Install
Add-AppxPackage -Path ".\OutsourceEF9.Package\AppPackages\OutsourceEF9_1.0.0.0_x64_Debug.msix"

# Verify
Get-AppxPackage -Name "*OutsourceEF9*"

# Uninstall (clean — no leftovers!)
Get-AppxPackage -Name "*OutsourceEF9*" | Remove-AppxPackage
```

### ✅ Quick Win 4: Set up the GitHub repo and starter workflow

1. Push code to new GitHub repo (if not already)
2. Create `.github/workflows/build-and-deploy.yml` with the YAML above
3. Add the self-signed PFX as `MSIX_SIGNING_PFX_BASE64` secret
4. Trigger the workflow — watch it build and sign
5. Download the artifact, install on dev machine

### ✅ Quick Win 5: Benchmark the difference

| Metric | ClickOnce | MSIX (estimate) |
|--------|-----------|-----------------|
| Install time | ~30s | ~5s |
| Build-to-deploy time | Manual, ~15min | Automated, ~3min |
| Uninstall | Partial cleanup | Total cleanup |
| Audit trail | None | AppLocker logs |

---

## Appendix A: Key Terms

| Term | Definition |
|------|------------|
| **MSIX** | Modern Windows app packaging format (replacement for MSI, ClickOnce, App-V) |
| **WAP Project** | Windows Application Packaging Project — MSBuild project that wraps existing desktop apps into MSIX |
| **App Installer** | Windows component that handles .msix installation and auto-updates |
| **AppInstaller file** | XML file (.appinstaller) that describes the package and update settings |
| **OV Certificate** | Organization Validated code signing certificate ($150-300/yr) |
| **AzureSignTool** | Open-source tool for signing with Azure Key Vault certificates in CI/CD |
| **SmartScreen** | Windows Defender SmartScreen — reputation-based security check for downloaded files |

## Appendix B: Resources

- [Microsoft: Create MSIX from any installer](https://learn.microsoft.com/en-us/windows/msix/packaging-tool/create-app-package)
- [Microsoft: Code signing options](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options)
- [Microsoft: CI/CD with GitHub Actions](https://learn.microsoft.com/en-us/windows/msix/desktop/cicd-overview)
- [Microsoft: Enterprise MSIX distribution](https://learn.microsoft.com/en-us/windows/msix/desktop/managing-your-msix-deployment-enterprise)
- [Microsoft: Sign MSIX package guide](https://learn.microsoft.com/en-us/windows/msix/package/sign-msix-package-guide)
- [GitHub: dotnet-desktop starter workflow](https://github.com/actions/starter-workflows/blob/main/ci/dotnet-desktop.yml)
- [Advanced Installer: Replace ClickOnce with MSIX](https://www.advancedinstaller.com/how-to-replace-clickonce-with-msix.html)
- [KomuraSoft: Deployment model decision table](https://comcomponent.com/en/blog/2026/03/20/000-windows-app-deployment-msi-msix-clickonce-xcopy-custom-updater/)
- [AzureSignTool GitHub](https://github.com/vcsjones/AzureSignTool)

---

## Confidence Assessment

| Finding | Confidence | Source |
|---------|-----------|--------|
| MSIX is the right long-term direction | 90% | Microsoft docs + industry trends |
| WAP Project works for VB.NET WinForms | 85% | MS docs confirm full-trust desktop app support |
| OV cert is best for Thailand-based deployment | 90% | Azure Artifact Signing geo restrictions confirmed |
| GitHub Actions pipeline is achievable | 85% | Starter workflow + CI/CD docs are clear |
| Network share distribution works | 95% | `Add-AppxPackage` from UNC paths is documented |
| Self-signed cert + Group Policy for internal use | 80% | Requires IT to deploy cert via GP |

---

*Report prepared by Dr. Bunsen Honeydew 🔬 — Research complete, findings synthesized, next steps are yours, Jeff.*

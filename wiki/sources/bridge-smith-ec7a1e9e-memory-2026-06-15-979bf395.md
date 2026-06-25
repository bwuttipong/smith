---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-06-15-979bf395
title: "Memory Bridge (smith): 2026-06-15"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-06-15.md
bridgeRelativePath: memory/2026-06-15.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-06-17T12:17:34.875Z
---

# Memory Bridge (smith): 2026-06-15

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-06-15.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-06-17T12:17:34.875Z

## Content
```markdown
# 2026-06-15 — Monday

## Session Start 🎩
- started session with jeff.
- compiled morning briefing (weather, market status, slack tasks).
- set Smith workspace memory guidance to use local memory/YYYY-MM-DD.md files.
- vault memory lives at C:\Users\Wuttipong.t\OneDrive\Apps\remotely-save\Memory Vault.
- reviewed and fixed NotificationListControl text overlapping issue (due to DPI scaling, hardcoded offsets, and z-order docking) by implementing dynamic text centering and resize invalidation.

## Session Updates 📦
- resolved dotnet MSBuild conflict by excluding duplicate `Consumable.Navigation.resx` in `CirculatingBox.vbproj`.
- injected `INotificationService` into `IssueOrderOpenControl` constructor.
- implemented real-time SignalR and native Windows Toast notifications in Thai within `btnSubmit_Click` in `IssueOrderOpenControl.vb`.
- wired up the `picForklift` image in `IssueOrderOpenControl` to trigger random test notifications when clicked.
- added `builder.Host.UseWindowsService()` to the `NotificationHub` project and configured port `5085` under `"Urls"` in `appsettings.json`.
- compiled and published `NotificationHub` in Release mode.
- authored a comprehensive server deployment guide (`NOTIFICATION_HUB_SERVER_SETUP.md`) for hosting the hub as a Windows background service.
- fixed `SingleFileProfile.pubxml` and `ClickOnceProfile.pubxml` target frameworks from `net8.0-windows` to `net8.0-windows10.0.17763.0` to resolve `ToastContentBuilder.Show` compilation errors.
- created `Publish-To-Desktop.bat` to compile, package, and deploy the test build to the local Desktop folder (`C:\Users\Wuttipong.t\Desktop\CirculatingBox_Test`).
- investigated and fixed a major ClickOnce deployment bug where the application crashed on startup because data and configuration files (`appsettings.json`, `sites.json`, `CirculatingBoxApps.config`) were nested in a subfolder and couldn't be located.
- implemented `Config.BasePath` to dynamically discover the application root directory during startup by scanning current and sub-directories.
- refactored `DatabaseBootstrap`, `SiteService`, `ReportViewerForm`, and `LanguageService` to use `Config.BasePath` instead of strict/hardcoded directories like `AppDomain.CurrentDomain.BaseDirectory` or `AppContext.BaseDirectory`, successfully resolving missing translation keys and startup crashes on client machines.
- added request logging middleware to `NotificationHub/Program.cs` to help debug SignalR client connection attempts.

```

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

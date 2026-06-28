# Antigravity Migration — Company Laptop (Windows)
# Run this from PowerShell as Admin (or with Developer Mode enabled)
# Target: Move Antigravity workspace into ~/Smith/.gemini/ with a junction back

$ErrorActionPreference = "Stop"
$oldPath = "$env:USERPROFILE\.gemini"
$newPath = "$env:USERPROFILE\Smith\.gemini"
$backupPath = "$env:USERPROFILE\.gemini-backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "=== Antigravity Migration ===" -ForegroundColor Cyan
Write-Host "From: $oldPath"
Write-Host "To:   $newPath"
Write-Host ""

# Step 1 — Check source exists
if (-not (Test-Path $oldPath)) {
    Write-Host "❌ Source not found at $oldPath" -ForegroundColor Red
    exit 1
}

# Step 2 — Create backup
Write-Host "⑴ Creating backup..." -ForegroundColor Yellow
Copy-Item -Recurse $oldPath $backupPath
Write-Host "   ✅ Backup at $backupPath"

# Step 3 — Ensure target directory exists
Write-Host "⑵ Ensuring target directory..." -ForegroundColor Yellow
if (-not (Test-Path "$env:USERPROFILE\Smith")) {
    New-Item -ItemType Directory -Path "$env:USERPROFILE\Smith" | Out-Null
}

# Step 4 — Move .gemini into workspace
Write-Host "⑶ Moving .gemini into workspace..." -ForegroundColor Yellow
if (Test-Path $newPath) {
    Write-Host "   ⚠️  Target already exists — skipping move, will re-link" -ForegroundColor Magenta
} else {
    Move-Item $oldPath $newPath
    Write-Host "   ✅ Moved to $newPath"
}

# Step 5 — Create junction (symlink alternative for Windows)
Write-Host "⑷ Creating junction at $oldPath → $newPath..." -ForegroundColor Yellow
# Remove any residual at the old path (the MoveItem already did, but double-check)
if (Test-Path $oldPath) {
    Remove-Item $oldPath -Force
}
cmd /c "mklink /J `"$oldPath`" `"$newPath`"" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ Junction created"
} else {
    Write-Host "   ❌ Junction failed — try running as Admin or enable Developer Mode" -ForegroundColor Red
    Write-Host "      Settings → Privacy & Security → For Developers → Developer Mode ON"
    exit 1
}

# Step 6 — Verify
Write-Host "⑸ Verifying..." -ForegroundColor Yellow
$testPath = "$oldPath\antigravity"
if (Test-Path $testPath) {
    Write-Host "   ✅ Antigravity resolves through junction" -ForegroundColor Green
    $children = Get-ChildItem $testPath -Directory | Select-Object -ExpandProperty Name
    Write-Host "   📁 Contains: $($children -join ', ')"
} else {
    Write-Host "   ⚠️  antigravity/ not found — check paths" -ForegroundColor Red
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Cyan
Write-Host "Backup saved at: $backupPath"
Write-Host "To roll back: Remove-Item $oldPath -Force; Move-Item $newPath $oldPath"

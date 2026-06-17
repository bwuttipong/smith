param(
    [Parameter(Mandatory=$true)]
    [string]$text
)

$ErrorActionPreference = "Stop"

Write-Host "Copying text to clipboard..."
Set-Clipboard -Value $text

Write-Host "Launching OneNote Sticky Notes..."
$oneNotePath = "C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE"
if (Test-Path $oneNotePath) {
    Start-Process $oneNotePath -ArgumentList "/stickynotes"
} else {
    # Fallback to classic Windows UWP Sticky Notes
    Start-Process "explorer.exe" -ArgumentList "shell:AppsFolder\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App"
}

Start-Sleep -Seconds 5

Write-Host "Simulating keystrokes (Ctrl+N, Ctrl+V)..."
$wshell = New-Object -ComObject Wscript.Shell
$wshell.SendKeys("^n")
Start-Sleep -Seconds 1
$wshell.SendKeys("^v")

Write-Host "Sticky note created successfully! 🎩" -ForegroundColor Green

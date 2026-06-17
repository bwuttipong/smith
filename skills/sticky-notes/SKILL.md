---
name: sticky-notes
description: >-
  Launches the OneNote Sticky Notes application on Windows, copies the provided
  text to the clipboard, and simulates keyboard shortcuts to paste the text into
  a new note.
---

# Sticky Notes

## Overview
This skill automates the creation of a new Windows/OneNote Sticky Note containing a specified text block (e.g. daily session summaries, reminders). It copies the input text to the Windows Clipboard, launches the OneNote Sticky Notes app, and simulates `Ctrl+N` followed by `Ctrl+V` to paste the content.

## Quick Start
To write a summary to Sticky Notes:
```powershell
powershell -File "skills/sticky-notes/scripts/sticky.ps1" -text "your note here"
```

## Utility Scripts
- **`scripts/sticky.ps1`**: PowerShell script to handle clipboard copy, application launch, and keyboard paste simulation.

## Common Mistakes
- **Focus Issues**: The simulated keystrokes depend on the OneNote Sticky Notes window gaining focus. If it does not focus within 5 seconds, the script will create the note but you may need to manually press `Ctrl+V` to paste the clipboard contents.

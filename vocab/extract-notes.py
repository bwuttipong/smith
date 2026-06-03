#!/usr/bin/env python3
"""Extract all notes from 🇬🇧 English folder in Apple Notes to JSON."""
import subprocess, json, re, html, sys
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

def strip_html(html_text):
    s = MLStripper()
    s.feed(html_text)
    return s.get_data().strip()

script = '''
tell application "Notes"
    set allNotes to {}
    repeat with f in folders
        if name of f is "🇬🇧 English" then
            repeat with sf in folders of f
                set folderName to name of sf
                repeat with n in notes of sf
                    set noteTitle to name of n
                    set noteBody to body of n
                    set end of allNotes to {folderName, noteTitle, noteBody}
                end repeat
            end repeat
        end if
    end repeat
    return allNotes
end tell
'''

result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=30)
raw = result.stdout.strip()

# Parse the osascript output format: comma-separated records
notes = []
lines = raw.split('\n')
i = 0
while i < len(raw):
    # Find the start of a note (comma, tab, or newline separated)
    # Actually osascript returns items separated by comma and space: item, item, item
    pass

# Better approach: rebuild from individual field extraction
# osascript returns: folder, title, body, folder, title, body, ...
# But body can span multiple lines with HTML

# Let me use a delimiter approach
delim = "|||NOTE_BOUNDARY|||"
script2 = f'''
tell application "Notes"
    set output to ""
    repeat with f in folders
        if name of f is "🇬🇧 English" then
            repeat with sf in folders of f
                set folderName to name of sf
                repeat with n in notes of sf
                    set noteTitle to name of n
                    set noteBody to body of n
                    set output to output & folderName & "|||FIELD|||" & noteTitle & "|||FIELD|||" & noteBody & "{delim}"
                end repeat
            end repeat
        end if
    end repeat
    return output
end tell
'''

result2 = subprocess.run(['osascript', '-e', script2], capture_output=True, text=True, timeout=60)
output = result2.stdout

notes = []
for block in output.split(delim):
    block = block.strip()
    if not block:
        continue
    parts = block.split('|||FIELD|||', 2)
    if len(parts) == 3:
        folder, title, body_html = [p.strip() for p in parts]
        body_text = strip_html(body_html)
        # Shorten body for storage - keep first 500 chars
        notes.append({
            "folder": folder,
            "title": title,
            "body": body_text[:1000] if body_text else ""
        })

with open('/Users/Jeff/Smith/vocab/apple-notes.json', 'w') as f:
    json.dump(notes, f, ensure_ascii=False, indent=2)

print(f"✅ Extracted {len(notes)} notes from 🇬🇧 English folder")
# Show note counts per folder
from collections import Counter
folder_counts = Counter(n["folder"] for n in notes)
for folder, count in sorted(folder_counts.items(), key=lambda x: -x[1]):
    print(f"   {folder}: {count} notes")
print(f"\nSaved to ~/Smith/vocab/apple-notes.json")

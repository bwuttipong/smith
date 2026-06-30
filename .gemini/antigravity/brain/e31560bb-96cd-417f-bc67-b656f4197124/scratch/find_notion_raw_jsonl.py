import os
import json

search_dir = "/Users/Jeff/Smith"
print("Scanning workspace for raw session transcripts...")

matches = []
for root, dirs, files in os.walk(search_dir):
    # skip standard ignore folders
    if "site-packages" in root or "node_modules" in root or ".git" in root or "cache" in root:
        continue
    for file in files:
        if file.endswith((".jsonl", ".json", ".md")):
            file_path = os.path.join(root, file)
            # check if file path has 'session' in it
            if "session" in file_path.lower() or "log" in file_path.lower():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if "ntn" in line or "npm install -g ntn" in line or "api_key" in line:
                                matches.append({
                                    "file": file_path,
                                    "line": line_num,
                                    "content": line.strip()
                                })
                except Exception as e:
                    pass

print(f"Found {len(matches)} matches:")
for m in matches:
    print(f"File: {m['file']}:{m['line']}")
    # print up to 500 chars
    print(f"  Snippet: {m['content'][:500]}")
    print("-" * 50)

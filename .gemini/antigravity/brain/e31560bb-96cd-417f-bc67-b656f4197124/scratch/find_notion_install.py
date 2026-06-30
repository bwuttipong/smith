import os
import json

search_dirs = [
    "/Users/Jeff/.gemini/antigravity/brain",
]

print("Starting scan...")
for root_dir in search_dirs:
    for root, dirs, files in os.walk(root_dir):
        # exclude site-packages and node_modules
        if "site-packages" in root or "node_modules" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith((".jsonl", ".json")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            if "notion" in line.lower() and ("install" in line.lower() or "npm" in line.lower() or "setup" in line.lower() or "cli" in line.lower() or "laptop" in line.lower() or "wuttipong" in line.lower()):
                                # print the match
                                print(f"File: {file_path}:{line_num}")
                                # print a snippet of the line
                                print(f"  Snippet: {line[:500].strip()}")
                                print("-" * 40)
                except Exception as e:
                    pass
print("Scan finished.")

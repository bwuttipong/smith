import os
import json

brain_dir = "/Users/Jeff/.gemini/antigravity/brain"
current_conv = "e31560bb-96cd-417f-bc67-b656f4197124"
results = []

for folder in os.listdir(brain_dir):
    if folder == current_conv:
        continue
    folder_path = os.path.join(brain_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    
    for root, dirs, files in os.walk(folder_path):
        if "site-packages" in root or "node_modules" in root or ".git" in root:
            continue
        for file in files:
            if file.endswith((".jsonl", ".json")):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line_num, line in enumerate(f, 1):
                            line_lower = line.lower()
                            if "notion" in line_lower and ("install" in line_lower or "npm" in line_lower or "setup" in line_lower or "cli" in line_lower or "laptop" in line_lower or "wuttipong" in line_lower):
                                step = json.loads(line)
                                # Let's only list it if it contains user interaction
                                if step.get("type") in ("USER_INPUT", "USER_EXPLICIT"):
                                    results.append({
                                        "file": file_path,
                                        "line": line_num,
                                        "created_at": step.get("created_at"),
                                        "content": step.get("content", "")
                                    })
                except Exception as e:
                    pass

results.sort(key=lambda x: x.get("created_at") or "")
for r in results:
    print(f"File: {r['file']}:{r['line']}")
    print(f"Date: {r['created_at']}")
    print(f"Content: {r['content'][:1000]}")
    print("-" * 50)
print(f"Total results: {len(results)}")

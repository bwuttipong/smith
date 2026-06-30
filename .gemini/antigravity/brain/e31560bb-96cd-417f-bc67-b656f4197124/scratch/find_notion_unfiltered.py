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
    
    for file in [
        "transcript.jsonl",
        "transcript_full.jsonl"
    ]:
        file_path = os.path.join(folder_path, ".system_generated", "logs", file)
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    if "notion" in line.lower():
                        step = json.loads(line)
                        if step.get("type") == "USER_INPUT":
                            results.append({
                                "file": file_path,
                                "line": line_num,
                                "created_at": step.get("created_at"),
                                "content": step.get("content", "")
                            })
        except Exception as e:
            pass

# deduplicate by created_at and content
unique_results = {}
for r in results:
    key = (r['created_at'], r['content'])
    if key not in unique_results:
        unique_results[key] = r

sorted_results = list(unique_results.values())
sorted_results.sort(key=lambda x: x.get("created_at") or "")

for r in sorted_results:
    print(f"File: {r['file']}")
    print(f"Date: {r['created_at']}")
    print(f"Content: {r['content']}")
    print("-" * 50)
print(f"Total results: {len(sorted_results)}")

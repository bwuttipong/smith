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
                        results.append({
                            "folder": folder,
                            "file": file,
                            "line": line_num,
                            "step_index": step.get("step_index"),
                            "type": step.get("type"),
                            "source": step.get("source"),
                            "created_at": step.get("created_at"),
                            "content": step.get("content", "")
                        })
        except Exception as e:
            pass

# Sort by created_at
results.sort(key=lambda x: x.get("created_at") or "")

print(f"Total raw matches: {len(results)}")
# print summaries
unique_steps = set()
for r in results:
    step_key = (r['folder'], r['file'], r['step_index'])
    if step_key in unique_steps:
        continue
    unique_steps.add(step_key)
    print(f"Folder: {r['folder']} ({r['file']}) | Step: {r['step_index']} | Type: {r['type']} | Source: {r['source']} | Date: {r['created_at']}")
    # If the content contains the word notion in a user request or assistant reasoning, let's print a small snippet
    content_str = str(r['content'])
    if "notion" in content_str.lower():
        snippet = content_str[:200].replace("\n", " ").strip()
        print(f"  Content: {snippet}...")

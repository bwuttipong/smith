import os
import json

brain_dir = "/Users/Jeff/.gemini/antigravity/brain"
print("Scanning brain directory:", brain_dir)

for folder in os.listdir(brain_dir):
    folder_path = os.path.join(brain_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    
    logs_dir = os.path.join(folder_path, ".system_generated", "logs")
    if os.path.exists(logs_dir):
        for file in os.listdir(logs_dir):
            if file.endswith(".jsonl"):
                file_path = os.path.join(logs_dir, file)
                print(f"Checking {file_path}")
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        for line in f:
                            if "notion" in line.lower():
                                step = json.loads(line)
                                if step.get("type") in ("USER_INPUT", "USER_EXPLICIT", "PLANNER_RESPONSE"):
                                    # print first 200 chars of step content or prompt
                                    print(f"  Match in {file}: index {step.get('step_index')}, type {step.get('type')}")
                                    print(f"  Content snippet: {str(step.get('content'))[:300]}")
                except Exception as e:
                    print(f"  Error reading {file_path}: {e}")

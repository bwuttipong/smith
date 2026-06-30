import os
import json

brain_dir = "/Users/Jeff/.gemini/antigravity/brain"
results = []

for folder in os.listdir(brain_dir):
    folder_path = os.path.join(brain_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    
    transcript_path = os.path.join(folder_path, ".system_generated", "logs", "transcript.jsonl")
    if not os.path.exists(transcript_path):
        # try transcript_full.jsonl
        transcript_path = os.path.join(folder_path, ".system_generated", "logs", "transcript_full.jsonl")
        if not os.path.exists(transcript_path):
            continue
            
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                step = json.loads(line)
                if step.get("type") == "USER_INPUT":
                    content = step.get("content", "")
                    if "notion" in content.lower():
                        results.append({
                            "conversation_id": folder,
                            "created_at": step.get("created_at"),
                            "content": content
                        })
    except Exception as e:
        print(f"Error reading {transcript_path}: {e}")

# Sort by created_at
results.sort(key=lambda x: x.get("created_at") or "")

for r in results:
    print(f"Conversation: {r['conversation_id']}")
    print(f"Date: {r['created_at']}")
    print(f"Prompt: {r['content']}")
    print("-" * 50)

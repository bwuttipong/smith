import json
import urllib.request
import os

with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
    notion_key = f.read().strip()

headers = {
    "Authorization": f"Bearer {notion_key}",
    "Notion-Version": "2025-09-03"
}

parent_id = "3680da1b-1be6-807b-9d22-ce2a5a212ad0"

# List child blocks of parent
req_children = urllib.request.Request(f"https://api.notion.com/v1/blocks/{parent_id}/children", headers=headers, method='GET')
try:
    with urllib.request.urlopen(req_children) as r:
        res = json.loads(r.read().decode('utf-8'))
        print("Total child blocks fetched:", len(res.get('results', [])))
        for block in res.get('results', []):
            if block['type'] == 'child_page':
                title = block['child_page']['title']
                print(f"Child Page: {title.encode('ascii', errors='replace').decode()} | ID: {block['id']}")
except Exception as e:
    print(f"Error fetching children: {e}")

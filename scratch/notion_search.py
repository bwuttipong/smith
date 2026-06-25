import json
import urllib.request
import os

with open(os.path.expanduser('~/.config/notion/api_key'), 'r') as f:
    notion_key = f.read().strip()

url = "https://api.notion.com/v1/search"
headers = {
    "Authorization": f"Bearer {notion_key}",
    "Notion-Version": "2025-09-03",
    "Content-Type": "application/json"
}

data = {
    "query": "Weekly",
    "filter": {
        "property": "object",
        "value": "page"
    }
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers=headers, method='POST')

try:
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode('utf-8'))
        print(json.dumps(res, indent=2))
except Exception as e:
    print(f"Error: {e}")

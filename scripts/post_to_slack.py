import urllib.request
import json
import sys
import os

def post_message(filepath):
    token = "xoxb-10733190954023-11007119797409-bvdNvd4DHktaostusaMP8fvd"
    channel = "D0AV4PTTKDK"
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return False
        
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
        
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    
    # We can split message if it's too long, but Slack supports up to 40000 characters.
    # We will format it as a markdown text block.
    payload = {
        "channel": channel,
        "text": text
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(payload).encode("utf-8"), 
        headers=headers, 
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            res_json = json.loads(res_data)
            if res_json.get("ok"):
                print("Message posted successfully!")
                return True
            else:
                print("Error posting message:", res_json.get("error"))
                return False
    except Exception as e:
        print("HTTP request failed:", e)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python post_to_slack.py <filepath>")
        sys.exit(1)
    post_message(sys.argv[1])

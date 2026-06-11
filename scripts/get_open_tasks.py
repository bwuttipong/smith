import urllib.request
import json
import sys
from datetime import datetime

def get_open_tasks():
    token = "xoxb-10733190954023-11007119797409-bvdNvd4DHktaostusaMP8fvd"
    url = "https://slack.com/api/files.info?file=F0AQ9CED5MF"
    
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {token}")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            data = json.loads(res_data)
            
            if not data.get("ok"):
                print("Error fetching list:", data.get("error"))
                return
                
            file_obj = data.get("file", {})
            download_url = file_obj.get("url_private_download") or file_obj.get("url_private")
            if not download_url:
                print("No download URL found")
                return
                
            req_dl = urllib.request.Request(download_url)
            req_dl.add_header("Authorization", f"Bearer {token}")
            with urllib.request.urlopen(req_dl) as dl_res:
                content = dl_res.read().decode("utf-8")
                content_json = json.loads(content)
                
                # Column mapping
                col_map = {
                    "Col0AQ9CEP48H": "task",
                    "Col00": "completed",
                    "Col01": "assignee",
                    "Col02": "due_date",
                    "Col0APT389FNH": "priority",
                    "Col0AQQPES7GQ": "status",
                    "Col0APUDDDFV4": "description"
                }

                status_labels = {
                    "Opt7MNHB19N": "Not started",
                    "OptXBPNOYKC": "In progress",
                    "OptEY5M00J3": "Blocked",
                    "OptTR35W8NA": "Done"
                }

                records = content_json.get("list_records", [])
                all_open_tasks = []

                for rec in records:
                    fields = rec.get("fields", [])
                    task_info = {
                        "task": "",
                        "completed": False,
                        "assignee": "",
                        "due_date": "",
                        "priority": 0,
                        "status": "Not started",
                        "description": ""
                    }
                    
                    for f in fields:
                        col_id = f.get("column_id")
                        key = col_map.get(col_id)
                        if not key:
                            continue
                            
                        val = f.get("value")
                        
                        if key == "task":
                            task_info["task"] = f.get("text") or val
                        elif key == "completed":
                            task_info["completed"] = bool(val)
                        elif key == "assignee":
                            task_info["assignee"] = val
                        elif key == "due_date":
                            task_info["due_date"] = val
                        elif key == "priority":
                            task_info["priority"] = val
                        elif key == "status":
                            task_info["status"] = status_labels.get(val, val)
                        elif key == "description":
                            task_info["description"] = f.get("text") or val
                            
                    if not task_info["completed"] and task_info["status"] != "Done":
                        all_open_tasks.append(task_info)
                
                # Filter for "In progress" tasks first
                in_progress_tasks = [t for t in all_open_tasks if t["status"] == "In progress"]
                
                # If we don't have enough "In progress" tasks, we'll top up with others
                other_tasks = [t for t in all_open_tasks if t["status"] != "In progress"]
                
                # Sort function:
                # - due_date empty should go to the end
                # - sort by due_date ascending (overdue/earlier first)
                # - then sort by priority descending (P3, P2, P1)
                def sort_key(t):
                    due = t["due_date"]
                    # If no due date, set to a far future date so it sorts last
                    due_val = due if due else "9999-12-31"
                    # Priority is numeric (e.g. 3, 2, 1). To sort descending, we negate it.
                    prio_val = -t["priority"]
                    return (due_val, prio_val)
                
                in_progress_tasks.sort(key=sort_key)
                other_tasks.sort(key=sort_key)
                
                # Select top 3 tasks from In Progress first, then fallback to others if needed
                selected_tasks = in_progress_tasks[:3]
                if len(selected_tasks) < 3:
                    selected_tasks.extend(other_tasks[:(3 - len(selected_tasks))])
                
                print(f"Total Open Tasks: {len(all_open_tasks)} | Showing Top 3 Priority/Due Items:")
                for idx, t in enumerate(selected_tasks, 1):
                    p_str = "P" + str(t["priority"]) if t["priority"] else "No priority"
                    due = t["due_date"] if t["due_date"] else "No due date"
                    assignee = t["assignee"] if t["assignee"] else "Unassigned"
                    
                    # Safe print
                    task_clean = t["task"].encode("ascii", "ignore").decode("ascii")
                    desc_clean = t["description"].encode("ascii", "ignore").decode("ascii") if t["description"] else ""
                    
                    print(f"{idx}. [{t['status']}] {task_clean} | Priority: {p_str} | Due: {due} | Assignee: {assignee}")
                    if desc_clean:
                        print(f"   Description: {desc_clean}")
                        
    except Exception as e:
        print("Failed to load list:", e)

if __name__ == "__main__":
    get_open_tasks()

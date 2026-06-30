import sqlite3
import datetime

db_path = "/Users/Jeff/.hermes/state.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

query = """
SELECT session_id, role, content, timestamp 
FROM messages 
WHERE (content LIKE '%notion%' OR content LIKE '%ntn%')
  AND length(content) < 1000
ORDER BY timestamp ASC
"""

cursor.execute(query)
rows = cursor.fetchall()

print(f"Total matching messages: {len(rows)}")
print("=" * 60)
for session_id, role, content, timestamp in rows:
    content_lower = content.lower()
    # Exclude system configs or logs that are not useful
    if "allow" in content_lower and "deny" in content_lower:
        continue
    if "provider" in content_lower and "model" in content_lower:
        continue
    
    dt = datetime.datetime.fromtimestamp(timestamp)
    print(f"Session ID: {session_id}")
    print(f"Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Role: {role}")
    print(f"Content:\n{content}")
    print("=" * 60)
conn.close()

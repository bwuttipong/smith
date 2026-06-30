import os
import sqlite3

search_dirs = [
    "/Users/Jeff/.hermes",
    "/Users/Jeff/Smith",
]

print("Scanning for SQLite databases...")
for root_dir in search_dirs:
    for root, dirs, files in os.walk(root_dir):
        # Skip some huge folders or irrelevant ones
        if "site-packages" in root or "node_modules" in root or ".git" in root or "cache" in root:
            continue
        for file in files:
            if file.endswith((".db", ".sqlite")):
                db_path = os.path.join(root, file)
                try:
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()
                    # Check if 'messages' table exists
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
                    if cursor.fetchone():
                        # We have a messages database! Search for notion in it
                        cursor.execute("SELECT count(*) FROM messages WHERE content LIKE '%notion%'")
                        cnt = cursor.fetchone()[0]
                        if cnt > 0:
                            print(f"Database: {db_path} has {cnt} notion matches!")
                            # Query matching rows
                            cursor.execute("SELECT session_id, role, content, timestamp FROM messages WHERE content LIKE '%notion%'")
                            rows = cursor.fetchall()
                            for session_id, role, content, timestamp in rows:
                                content_lower = content.lower()
                                if 'install' in content_lower or 'npm' in content_lower or 'cli' in content_lower or 'setup' in content_lower or 'laptop' in content_lower or 'access' in content_lower or 'pc' in content_lower:
                                    import datetime
                                    dt = datetime.datetime.fromtimestamp(timestamp)
                                    print(f"  Session ID: {session_id}")
                                    print(f"  Time: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                                    print(f"  Role: {role}")
                                    print(f"  Content:\n{content[:600]}")
                                    print("  " + "-" * 40)
                    conn.close()
                except Exception as e:
                    pass

print("Scan complete.")

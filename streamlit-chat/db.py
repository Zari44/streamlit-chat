## NAIVE COPY FROM BACKEND DB
import json
import sqlite3

DB_PATH = "chat_sessions.db"


def get_session(session_id: str) -> dict:
    """Retrieves config by session ID"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT config FROM sessions WHERE id = ?", (session_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return {}

import json
import sqlite3
import uuid

DB_PATH = "chat_sessions.db"


def init_db():
    """Initialize the database and create tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Create table if not exists
    c.execute("""CREATE TABLE IF NOT EXISTS sessions
                 (id TEXT PRIMARY KEY, config JSON)""")
    conn.commit()
    conn.close()


def create_session(config: dict) -> str:
    """Saves config and returns a session ID"""
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sessions (id, config) VALUES (?, ?)", (session_id, json.dumps(config)))
    conn.commit()
    conn.close()
    return session_id


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

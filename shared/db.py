import json
import sqlite3

from backend.app.models.chat_config import ChatConfig

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


def create_session(config: ChatConfig) -> str:
    """Saves config and returns the domain"""
    domain = config.get("domain")
    if not domain:
        raise ValueError("Domain is required")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO sessions (id, config) VALUES (?, ?)", (config.domain, json.dumps(config)))
    conn.commit()
    conn.close()
    return domain


def get_session(domain: str) -> ChatConfig:
    """Retrieves config by domain"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT config FROM sessions WHERE id = ?", (domain,))
    row = c.fetchone()
    conn.close()
    if row:
        return ChatConfig(json.loads(row[0]))
    return {}

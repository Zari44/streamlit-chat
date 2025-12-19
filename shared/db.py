import os
import sqlite3

from shared.chat_config import ChatConfig

DB_PATH = "/data/chat_sessions.db"


def init_db():
    """Initialize the database and create tables if they don't exist"""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Create new table schema with separate columns for each ChatConfig field
        c.execute("""CREATE TABLE IF NOT EXISTS chat_configs
                        (domain TEXT PRIMARY KEY,
                        title TEXT NOT NULL,
                        bot_aim TEXT NOT NULL,
                        password TEXT NOT NULL,
                        user TEXT,
                        bot_audience TEXT,
                        bot_tone TEXT)""")
        conn.commit()


def create_session(config: ChatConfig) -> str:
    """Saves config and returns the domain"""
    domain = config.domain
    if not domain:
        raise ValueError("Domain is required")
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            """INSERT OR REPLACE INTO chat_configs
                    (domain, title, bot_aim, password, user, bot_audience, bot_tone)
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                config.domain,
                config.title,
                config.bot_aim,
                config.password,
                config.user,
                config.bot_audience,
                config.bot_tone,
            ),
        )
        conn.commit()
    return domain


def get_session(domain: str) -> ChatConfig | None:
    """Retrieves config by domain"""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            """SELECT domain, title, bot_aim, password, user, bot_audience, bot_tone
                    FROM chat_configs WHERE domain = ?""",
            (domain,),
        )
        row = c.fetchone()

    if not row:
        return None

    return ChatConfig(
        domain=row[0], title=row[1], bot_aim=row[2], password=row[3], user=row[4], bot_audience=row[5], bot_tone=row[6]
    )

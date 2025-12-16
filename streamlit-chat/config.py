import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from shared.db import get_session

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


load_dotenv()

TITLE = os.getenv("TITLE", "title")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
PASSWORD = os.getenv("PASSWORD", "password")


def get_config(session_id: str | None) -> dict[str, str]:
    if not session_id:
        return {
            "title": os.getenv("TITLE", TITLE),
            "system_prompt": SYSTEM_PROMPT,
            "password": PASSWORD,
        }

    loaded_config = get_session(session_id)
    if loaded_config:
        return loaded_config
    else:
        st.error("Session not found or expired.")
        st.stop()
        raise AssertionError("terminate all hope")

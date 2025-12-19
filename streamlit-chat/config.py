import logging
import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("streamlit_chat.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

logger.info("=== config.py: Starting module initialization ===")

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.chat_config import ChatConfig
from shared.db import get_session  # type: ignore

load_dotenv()

TITLE = os.getenv("TITLE", "G.O.A.T. Bot")
PASSWORD = os.getenv("PASSWORD", "pass")


def get_config(domain: str | None) -> ChatConfig:
    if not domain:
        return ChatConfig(
            domain="",
            title=TITLE,
            bot_aim="To help user. To make him happy and help him with his problems.",
            password=PASSWORD,
            user=None,
            bot_audience="General audience",
            bot_tone="Playful, funny and friendly!",
        )

    loaded_config = get_session(domain)
    if loaded_config:
        return loaded_config
    else:
        st.error("Session not found or expired.")
        st.stop()
        raise AssertionError("terminate all hope")

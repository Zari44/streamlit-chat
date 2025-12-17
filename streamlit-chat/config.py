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
logger.info(f"Line 19: Added project root to path: {project_root}")

from shared.db import get_session  # type: ignore

logger.info("Line 21: Imported get_session from shared.db")

load_dotenv()
logger.info("Line 23: Environment variables loaded")

TITLE = os.getenv("TITLE", "title")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.")
PASSWORD = os.getenv("PASSWORD", "password")
logger.info(f"Line 24-26: Default config values loaded - TITLE={TITLE}, PASSWORD={'*' * len(PASSWORD)}")


def get_config(domain: str | None) -> dict[str, str]:
    logger.info(f"Line 29: get_config called with domain={domain}")
    if not domain:
        logger.info("Line 30: No domain provided, using default config")
        config = {
            "title": os.getenv("TITLE", TITLE),
            "system_prompt": SYSTEM_PROMPT,
            "password": PASSWORD,
        }
        logger.info(f"Line 31-35: Returning default config with title={config['title']}")
        return config

    logger.info(f"Line 37: Domain provided, attempting to load session: {domain}")
    loaded_config = get_session(domain)
    logger.info(f"Line 38: get_session returned: {loaded_config is not None}")
    if loaded_config:
        logger.info(f"Line 39: Session config loaded successfully for domain {domain}")
        return loaded_config
    else:
        logger.error(f"Line 41: Session not found or expired for domain {domain}")
        st.error("Session not found or expired.")
        st.stop()
        raise AssertionError("terminate all hope")

import os

from fastapi import APIRouter

from backend.app.models.chat_config import ChatConfig
from shared.db import create_session

router = APIRouter()


STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")


@router.post("/start")
def start_chat(config: ChatConfig):
    # 1. Save the config to DB

    domain = create_session(config.model_dump())
    # 2. Return the link to Streamlit
    # Assuming Streamlit runs on port 8501
    chat_url = f"{STREAMLIT_URL}/?domain={domain}"

    return {"message": "Session created", "domain": domain, "url": chat_url}

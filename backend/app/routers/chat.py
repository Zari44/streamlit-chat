import os

from fastapi import APIRouter

from backend.app.models.chat_config import ChatConfig
from shared.db import create_session

router = APIRouter()


STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")


@router.post("/start")
def start_chat(config: ChatConfig):
    domain = create_session(config.model_dump())
    return {"message": "New chatbot created", "domain": domain, "redirect_url": f"/chats/{domain}"}

import os

from fastapi import APIRouter

from backend.app.models.chat_config import ChatConfig
from shared.db import create_session

router = APIRouter()


STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")

DOMAIN_URL = os.getenv("DOMAIN_URL", "goatbot.localhost")


@router.post("/start")
def start_chat(config: ChatConfig):
    domain = create_session(config.model_dump())
    return {"message": "New chatbot created", "redirect_url": f"http://{domain}.{DOMAIN_URL}"}

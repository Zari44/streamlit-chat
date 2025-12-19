import os

from fastapi import APIRouter, HTTPException

from shared.chat_config import ChatConfig
from shared.db import create_session

router = APIRouter()


STREAMLIT_URL = os.getenv("STREAMLIT_URL", "http://localhost:8501")

DOMAIN_URL = os.getenv("DOMAIN_URL", "goatbot.localhost")


@router.post("/start")
def start_chat(config: ChatConfig):
    try:
        domain = create_session(config)
        return {"message": "New chatbot created", "redirect_url": f"http://{domain}.{DOMAIN_URL}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create bot") from e

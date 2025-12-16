from fastapi import APIRouter

from backend.app.routers import example, health
from backend.app.routers import chat

api_router = APIRouter()

# Include individual routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(example.router, prefix="/example", tags=["example"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

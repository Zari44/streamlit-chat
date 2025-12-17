from fastapi import APIRouter

from backend.app.routers import chat, health

api_router = APIRouter(prefix="/api")

# Include individual routers
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(health.router, tags=["health"])

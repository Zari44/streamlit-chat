from fastapi import APIRouter

from app.routers import example, health

api_router = APIRouter()

# Include individual routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(example.router, prefix="/example", tags=["example"])

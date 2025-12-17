from fastapi import APIRouter

router = APIRouter(prefix="/health")


@router.get("/")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "goatbot-api"}

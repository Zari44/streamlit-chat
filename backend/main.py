from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db.db import init_db
from backend.app.routers import api_router, root

app = FastAPI(title="GoatBot API", description="FastAPI backend for GoatBot", version="1.0.0")
init_db()

# CORS middleware
app.add_middleware(
    CORSMiddleware,  # type: ignore[invalid-argument-type]
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api")
app.include_router(root.router)

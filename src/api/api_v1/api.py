from fastapi import APIRouter

from src.api.api_v1.endpoints import location, business
from src.api.api_v1 import sqlite_s3_backup

# Create FastAPI app and include routers
api_router = APIRouter()
api_router.include_router(location.router)
api_router.include_router(sqlite_s3_backup.router)

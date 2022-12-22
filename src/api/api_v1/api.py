from fastapi import APIRouter

from src.api.api_v1.endpoints import location, business

# Create FastAPI app and include routers
api_router = APIRouter()
api_router.include_router(location.router)

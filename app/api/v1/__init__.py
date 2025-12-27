"""API v1 router"""
from fastapi import APIRouter

api_router = APIRouter()


# Import and include sub-routers here
# from app.api.v1.endpoints import health, trunk, branches
# api_router.include_router(health.router, tags=["health"])
# api_router.include_router(trunk.router, prefix="/trunk", tags=["trunk"])
# api_router.include_router(branches.router, prefix="/branches", tags=["branches"])


@api_router.get("/status")
async def api_status():
    """API status endpoint"""
    return {
        "api_version": "v1",
        "status": "operational",
        "layers": {
            "roots": "Infrastructure & Data Layer",
            "trunk": "Core Business Logic",
            "branches": "Domain Modules",
            "leaves": "User Interfaces",
            "atmosphere": "Integration Layer",
            "nervous_system": "AI Agents"
        }
    }

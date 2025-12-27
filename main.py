"""
Tree of Life System - Main Application Entry Point
A scalable AI business automation platform following the Tree of Life architecture
"""
import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
import uvicorn

from app import __version__, __title__, __description__
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import api_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("🌳 Tree of Life System starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"API Version: {settings.API_VERSION}")
    yield
    logger.info("🌳 Tree of Life System shutting down...")


# Create FastAPI application
app = FastAPI(
    title=__title__,
    description=__description__,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API routes
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": __title__,
        "description": __description__,
        "version": __version__,
        "status": "operational",
        "architecture": {
            "roots": "Blockchain & Core Infrastructure",
            "trunk": "Core Business Logic & Integration",
            "branches": "Domain-specific Modules",
            "leaves": "User Applications & Interfaces",
            "atmosphere": "API & Service Integration",
            "nervous_system": "AI Agent Network",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": __version__
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )

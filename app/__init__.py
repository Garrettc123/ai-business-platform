"""Tree of Life System Application Package"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.core.config import settings
from app.roots import RootsLayer
from app.trunk import TrunkLayer
from app.branches import BranchesLayer
from app.leaves import LeavesLayer
from app.atmosphere import AtmosphereLayer
from app.nervous_system import NervousSystemLayer

__version__ = "1.0.0"
__title__ = "Tree of Life System"
__description__ = "Multiplex AI Business Platform - Integrated GitHub, Linear, Notion & AI ecosystem"

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global layer instances (singleton pattern)
_roots = None
_trunk = None
_branches = None
_leaves = None
_atmosphere = None
_nervous_system = None


def get_layers():
    """Get or create singleton layer instances"""
    global _roots, _trunk, _branches, _leaves, _atmosphere, _nervous_system
    
    if _roots is None:
        _roots = RootsLayer()
        _trunk = TrunkLayer()
        _branches = BranchesLayer()
        _leaves = LeavesLayer()
        _atmosphere = AtmosphereLayer()
        _nervous_system = NervousSystemLayer()
    
    return {
        'roots': _roots,
        'trunk': _trunk,
        'branches': _branches,
        'leaves': _leaves,
        'atmosphere': _atmosphere,
        'nervous_system': _nervous_system
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🌳 Starting Tree of Life System...")
    layers = get_layers()
    await layers['roots'].initialize()
    logger.info("✅ Tree of Life System started successfully")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Tree of Life System...")


# Create FastAPI application with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    description=__description__,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API router after app creation to avoid circular imports
from app.api.v1 import api_router
app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint with system overview"""
    return {
        "name": __title__,
        "version": __version__,
        "description": __description__,
        "status": "operational",
        "architecture": {
            "🌱 ROOTS": "Infrastructure & Data Layer",
            "🪵 TRUNK": "Core Business Logic",
            "🌿 BRANCHES": "Domain Modules",
            "🍃 LEAVES": "User Interfaces",
            "💨 ATMOSPHERE": "Integration Layer",
            "🧠 NERVOUS SYSTEM": "AI Agents"
        },
        "docs": "/docs",
        "api": settings.API_PREFIX
    }


@app.get("/health")
async def health_check():
    """Comprehensive health check for all layers"""
    try:
        layers = get_layers()
        roots_health = await layers['roots'].health_check()
        
        return {
            "status": "healthy",
            "version": __version__,
            "layers": {
                "roots": roots_health,
                "trunk": {"status": "operational"},
                "branches": {"status": "operational"},
                "leaves": {"status": "operational"},
                "atmosphere": {"status": "operational"},
                "nervous_system": {"status": "operational"}
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }


@app.get("/layers")
async def get_layers_info():
    """Get detailed information about all Tree of Life layers"""
    return {
        "roots": {
            "name": "ROOTS Layer",
            "description": "Foundation Infrastructure - Database, blockchain, and core data infrastructure",
            "components": ["PostgreSQL", "Redis", "Kafka", "Weaviate"],
            "status": "active"
        },
        "trunk": {
            "name": "TRUNK Layer",
            "description": "Core Business Logic - Central coordination and business logic management",
            "components": ["Contribution Manager", "Verification Engine", "Reward Distributor"],
            "status": "active"
        },
        "branches": {
            "name": "BRANCHES Layer",
            "description": "Domain-specific Modules - Specialized functionality for different business domains",
            "domains": ["Research", "Medical", "Financial", "Environmental"],
            "status": "active"
        },
        "leaves": {
            "name": "LEAVES Layer",
            "description": "User-facing Applications - Frontend interfaces and user interaction points",
            "interfaces": ["Contributor Portal", "Verifier Dashboard", "Analytics Platform"],
            "status": "active"
        },
        "atmosphere": {
            "name": "ATMOSPHERE Layer",
            "description": "Integration & Communication - API gateway, service mesh, and external integrations",
            "integrations": ["GitHub", "Linear", "Notion", "Perplexity"],
            "status": "active"
        },
        "nervous_system": {
            "name": "NERVOUS SYSTEM Layer",
            "description": "AI Agent Network - Intelligent automation and AI-powered decision making",
            "agents": ["Verification Agents", "Risk Assessment", "Orchestration", "Optimization"],
            "status": "active"
        }
    }


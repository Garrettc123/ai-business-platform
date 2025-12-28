"""API v1 router"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from app.roots import RootsLayer
from app.trunk import TrunkLayer
from app.branches import BranchesLayer
from app.leaves import LeavesLayer
from app.atmosphere import AtmosphereLayer
from app.nervous_system import NervousSystemLayer

api_router = APIRouter()

# Initialize layers for API access
roots = RootsLayer()
trunk = TrunkLayer()
branches = BranchesLayer()
leaves = LeavesLayer()
atmosphere = AtmosphereLayer()
nervous_system = NervousSystemLayer()


# Pydantic models for request validation
class ContributionCreate(BaseModel):
    """Model for creating a contribution"""
    title: str
    content: str
    domain: str


class DomainRequest(BaseModel):
    """Model for domain-specific requests"""
    domain: str
    data: Dict[str, Any]


class UserContribution(BaseModel):
    """Model for user contribution submission"""
    user_id: str
    title: str
    content: str


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


# ROOTS Layer Endpoints
@api_router.get("/roots/health", tags=["roots"])
async def roots_health():
    """Check health of infrastructure components"""
    return await roots.health_check()


# TRUNK Layer Endpoints
@api_router.post("/trunk/contributions", tags=["trunk"])
async def create_contribution(contribution: ContributionCreate):
    """Process a new contribution through the trunk layer"""
    result = await trunk.process_contribution(contribution.dict())
    return result


@api_router.get("/trunk/contributions/{contribution_id}/verify", tags=["trunk"])
async def verify_contribution(contribution_id: str):
    """Verify a specific contribution"""
    result = await trunk.verify_contribution(contribution_id)
    return result


# BRANCHES Layer Endpoints
@api_router.get("/branches/domains", tags=["branches"])
async def list_domains():
    """Get list of available domain modules"""
    return await branches.get_available_domains()


@api_router.post("/branches/process", tags=["branches"])
async def process_domain_request(request: DomainRequest):
    """Process a domain-specific request"""
    result = await branches.process_domain_request(request.domain, request.data)
    return result


# LEAVES Layer Endpoints
@api_router.get("/leaves/dashboard/{user_id}", tags=["leaves"])
async def get_user_dashboard(user_id: str):
    """Get user dashboard data"""
    return await leaves.get_user_dashboard(user_id)


@api_router.post("/leaves/contributions", tags=["leaves"])
async def submit_user_contribution(contribution: UserContribution):
    """Submit a user contribution through the leaves layer"""
    result = await leaves.submit_contribution(
        contribution.user_id,
        {"title": contribution.title, "content": contribution.content}
    )
    return result


# ATMOSPHERE Layer Endpoints
@api_router.post("/atmosphere/github/sync", tags=["atmosphere"])
async def sync_github(repo: str):
    """Sync with GitHub repository"""
    result = await atmosphere.sync_with_github(repo)
    return result


@api_router.post("/atmosphere/linear/sync", tags=["atmosphere"])
async def sync_linear(project_id: str):
    """Sync with Linear project"""
    result = await atmosphere.sync_with_linear(project_id)
    return result


@api_router.post("/atmosphere/notion/sync", tags=["atmosphere"])
async def sync_notion(database_id: str):
    """Sync with Notion database"""
    result = await atmosphere.sync_with_notion(database_id)
    return result


@api_router.post("/atmosphere/perplexity/query", tags=["atmosphere"])
async def query_perplexity(query: str):
    """Query Perplexity AI"""
    result = await atmosphere.query_perplexity(query)
    return result


# NERVOUS SYSTEM Layer Endpoints
@api_router.post("/nervous-system/verify/{contribution_id}", tags=["nervous_system"])
async def ai_verify_contribution(contribution_id: str):
    """Run AI verification on a contribution"""
    result = await nervous_system.run_verification_agent(contribution_id)
    return result


@api_router.post("/nervous-system/risk-assessment", tags=["nervous_system"])
async def assess_risk(data: Dict[str, Any]):
    """Run AI risk assessment"""
    result = await nervous_system.run_risk_assessment(data)
    return result


@api_router.post("/nervous-system/orchestrate/{workflow_id}", tags=["nervous_system"])
async def orchestrate_workflow(workflow_id: str):
    """Orchestrate a complex workflow using AI"""
    result = await nervous_system.orchestrate_workflow(workflow_id)
    return result

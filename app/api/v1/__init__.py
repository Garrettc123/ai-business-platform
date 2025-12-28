"""API v1 router"""
from fastapi import APIRouter
from typing import Dict, Any
from pydantic import BaseModel, Field, field_validator

api_router = APIRouter()


# Pydantic models for request validation
class ContributionCreate(BaseModel):
    """Model for creating a contribution"""
    title: str = Field(..., min_length=1, max_length=200, description="Contribution title")
    content: str = Field(..., min_length=1, description="Contribution content")
    domain: str = Field(..., description="Domain for the contribution")


class DomainRequest(BaseModel):
    """Model for domain-specific requests"""
    domain: str = Field(..., description="Target domain")
    data: Dict[str, Any] = Field(..., description="Domain-specific data")


class UserContribution(BaseModel):
    """Model for user contribution submission"""
    user_id: str = Field(..., description="User identifier")
    title: str = Field(..., min_length=1, max_length=200, description="Contribution title")
    content: str = Field(..., min_length=1, description="Contribution content")


class GitHubSyncRequest(BaseModel):
    """Model for GitHub sync request"""
    repo: str = Field(..., description="Repository in format 'owner/repo'")
    
    @field_validator('repo')
    @classmethod
    def validate_repo_format(cls, v: str) -> str:
        """Validate repository format"""
        if '/' not in v or v.count('/') != 1:
            raise ValueError('Repository must be in format "owner/repo"')
        owner, repo = v.split('/')
        if not owner or not repo:
            raise ValueError('Owner and repo name cannot be empty')
        return v


class LinearSyncRequest(BaseModel):
    """Model for Linear sync request"""
    project_id: str = Field(..., min_length=1, description="Linear project identifier")


class NotionSyncRequest(BaseModel):
    """Model for Notion sync request"""
    database_id: str = Field(..., min_length=1, description="Notion database identifier")


class PerplexityQueryRequest(BaseModel):
    """Model for Perplexity query request"""
    query: str = Field(..., min_length=1, max_length=1000, description="Query text")


class RiskAssessmentRequest(BaseModel):
    """Model for risk assessment request"""
    data: Dict[str, Any] = Field(..., description="Data to assess for risk")
    context: str = Field(default="", description="Optional context for risk assessment")


def get_layers():
    """Get singleton layer instances from main app"""
    from app import get_layers as get_app_layers
    return get_app_layers()


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
    layers = get_layers()
    return await layers['roots'].health_check()


# TRUNK Layer Endpoints
@api_router.post("/trunk/contributions", tags=["trunk"])
async def create_contribution(contribution: ContributionCreate):
    """Process a new contribution through the trunk layer"""
    layers = get_layers()
    result = await layers['trunk'].process_contribution(contribution.model_dump())
    return result


@api_router.get("/trunk/contributions/{contribution_id}/verify", tags=["trunk"])
async def verify_contribution(contribution_id: str):
    """Verify a specific contribution"""
    layers = get_layers()
    result = await layers['trunk'].verify_contribution(contribution_id)
    return result


# BRANCHES Layer Endpoints
@api_router.get("/branches/domains", tags=["branches"])
async def list_domains():
    """Get list of available domain modules"""
    layers = get_layers()
    return await layers['branches'].get_available_domains()


@api_router.post("/branches/process", tags=["branches"])
async def process_domain_request(request: DomainRequest):
    """Process a domain-specific request"""
    layers = get_layers()
    result = await layers['branches'].process_domain_request(request.domain, request.data)
    return result


# LEAVES Layer Endpoints
@api_router.get("/leaves/dashboard/{user_id}", tags=["leaves"])
async def get_user_dashboard(user_id: str):
    """Get user dashboard data"""
    layers = get_layers()
    return await layers['leaves'].get_user_dashboard(user_id)


@api_router.post("/leaves/contributions", tags=["leaves"])
async def submit_user_contribution(contribution: UserContribution):
    """Submit a user contribution through the leaves layer"""
    layers = get_layers()
    result = await layers['leaves'].submit_contribution(
        contribution.user_id,
        {"title": contribution.title, "content": contribution.content}
    )
    return result


# ATMOSPHERE Layer Endpoints
@api_router.post("/atmosphere/github/sync", tags=["atmosphere"])
async def sync_github(request: GitHubSyncRequest):
    """Sync with GitHub repository"""
    layers = get_layers()
    result = await layers['atmosphere'].sync_with_github(request.repo)
    return result


@api_router.post("/atmosphere/linear/sync", tags=["atmosphere"])
async def sync_linear(request: LinearSyncRequest):
    """Sync with Linear project"""
    layers = get_layers()
    result = await layers['atmosphere'].sync_with_linear(request.project_id)
    return result


@api_router.post("/atmosphere/notion/sync", tags=["atmosphere"])
async def sync_notion(request: NotionSyncRequest):
    """Sync with Notion database"""
    layers = get_layers()
    result = await layers['atmosphere'].sync_with_notion(request.database_id)
    return result


@api_router.post("/atmosphere/perplexity/query", tags=["atmosphere"])
async def query_perplexity(request: PerplexityQueryRequest):
    """Query Perplexity AI"""
    layers = get_layers()
    result = await layers['atmosphere'].query_perplexity(request.query)
    return result


# NERVOUS SYSTEM Layer Endpoints
@api_router.post("/nervous-system/verify/{contribution_id}", tags=["nervous_system"])
async def ai_verify_contribution(contribution_id: str):
    """Run AI verification on a contribution"""
    layers = get_layers()
    result = await layers['nervous_system'].run_verification_agent(contribution_id)
    return result


@api_router.post("/nervous-system/risk-assessment", tags=["nervous_system"])
async def assess_risk(request: RiskAssessmentRequest):
    """Run AI risk assessment"""
    layers = get_layers()
    result = await layers['nervous_system'].run_risk_assessment(
        request.data,
        request.context
    )
    return result


@api_router.post("/nervous-system/orchestrate/{workflow_id}", tags=["nervous_system"])
async def orchestrate_workflow(workflow_id: str):
    """Orchestrate a complex workflow using AI"""
    layers = get_layers()
    result = await layers['nervous_system'].orchestrate_workflow(workflow_id)
    return result

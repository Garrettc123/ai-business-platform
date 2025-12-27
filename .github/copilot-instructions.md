# Tree of Life AI Business Platform - GitHub Copilot Instructions

## Project Overview

This is an enterprise-grade AI business automation platform built with Python and FastAPI, following the **Tree of Life** architectural pattern. The system integrates multiple AI agents, vector databases, and external services (GitHub, Linear, Notion, Perplexity) into a scalable, production-ready platform.

### Architecture Components

The Tree of Life architecture consists of:
- **🌱 ROOTS**: Blockchain foundation & core infrastructure
- **🪵 TRUNK**: Core business logic & integration management
- **🌿 BRANCHES**: Domain-specific modules (Research, Medical, Financial, Environmental)
- **🍃 LEAVES**: User-facing applications and interfaces
- **💨 ATMOSPHERE**: Integration layer (GitHub, Linear, Notion, Perplexity APIs)
- **🧠 NERVOUS SYSTEM**: AI agent network for intelligent automation

## Python Coding Standards

### General Guidelines

- Use Python 3.10+ features and type hints
- Follow PEP 8 style guide with Black formatter
- Use snake_case for variables and functions, PascalCase for classes
- Maximum line length: 100 characters (Black default)
- Use docstrings for all public modules, functions, classes, and methods
- Prefer explicit over implicit code
- Use type hints for function parameters and return values

### Code Style Examples

```python
# Good: Type hints and clear docstring
def process_agent_task(
    agent_id: str,
    task_data: dict[str, Any],
    timeout: int = 30
) -> TaskResult:
    """
    Process a task for a specific AI agent.
    
    Args:
        agent_id: Unique identifier for the agent
        task_data: Dictionary containing task parameters
        timeout: Maximum time in seconds for task execution
        
    Returns:
        TaskResult object containing execution status and output
    """
    # Implementation here
    pass
```

### Import Organization

Order imports using isort with Black-compatible settings:
1. Standard library imports
2. Third-party imports (separated by blank line)
3. Local application imports (separated by blank line)

```python
import os
import logging
from typing import Any

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from app.core.config import settings
from app.api.v1 import api_router
```

## FastAPI Best Practices

### API Endpoint Structure

- Place all API endpoints in `app/api/v1/` directory
- Use FastAPI router pattern for modularity
- Always include proper response models using Pydantic
- Use dependency injection for database sessions and authentication
- Include proper HTTP status codes
- Add comprehensive docstrings for OpenAPI documentation

```python
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/agents", tags=["AI Agents"])

class AgentResponse(BaseModel):
    """Response model for agent operations"""
    id: str
    name: str
    status: str

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str) -> AgentResponse:
    """
    Retrieve agent information by ID.
    
    Returns agent status and configuration details.
    """
    # Implementation
    pass
```

### Error Handling

- Always use FastAPI's HTTPException for API errors
- Include meaningful error messages
- Use appropriate HTTP status codes
- Log errors with proper context

```python
from fastapi import HTTPException, status

if not agent_exists:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Agent with ID {agent_id} not found"
    )
```

## Tree of Life Architecture Patterns

### Module Organization

Follow the Tree of Life component structure when adding new features:

- **roots/** - Infrastructure, blockchain, database models
- **trunk/** - Core business logic, shared services
- **branches/** - Domain-specific features (research, medical, finance)
- **leaves/** - User interfaces, frontend integrations
- **atmosphere/** - External API integrations (GitHub, Linear, Notion, Perplexity)
- **nervous_system/** - AI agent coordination and orchestration

### Service Layer Pattern

- Separate business logic from API endpoints
- Create service classes in appropriate component directories
- Use dependency injection for service initialization

```python
# app/trunk/services/contribution_service.py
class ContributionService:
    """Core service for managing user contributions"""
    
    def __init__(self, db: Database):
        self.db = db
    
    async def create_contribution(self, data: ContributionCreate) -> Contribution:
        """Create a new contribution record"""
        # Implementation
        pass
```

## AI Agent Development

### Multi-Agent Orchestration

When working with AI agents (CrewAI, LangChain, AutoGen):

- Keep agent definitions modular and reusable
- Use structured output formats (Pydantic models)
- Implement proper error handling and retries
- Add logging for agent actions and decisions
- Use async/await for concurrent agent operations

```python
from crewai import Agent, Task, Crew
from langchain.tools import Tool

class ResearchAgent:
    """AI agent specialized in research tasks"""
    
    def __init__(self):
        self.agent = Agent(
            role="Research Specialist",
            goal="Conduct thorough research and analysis",
            backstory="Expert researcher with access to multiple data sources",
            tools=[self._get_tools()],
            verbose=True
        )
    
    def _get_tools(self) -> list[Tool]:
        """Define tools available to the agent"""
        # Return list of tools
        pass
```

## Database and Data Models

### SQLAlchemy Models

- Place models in `app/roots/models/`
- Use descriptive table names with proper schema
- Include created_at and updated_at timestamps
- Add proper indexes for query optimization
- Use Alembic for database migrations

```python
from sqlalchemy import Column, String, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Contribution(Base):
    """Database model for user contributions"""
    __tablename__ = "contributions"
    __table_args__ = {'schema': 'trunk'}
    
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_contributions_user_created', 'user_id', 'created_at'),
    )
```

### Pydantic Schemas

- Create Pydantic models for request/response validation
- Use separate models for Create, Update, and Response operations
- Leverage Pydantic v2 features (validators, computed fields)

## Testing Requirements

### Test Structure

- Use pytest for all tests
- Place tests in `tests/` directory mirroring the `app/` structure
- Use meaningful test names: `test_<function_name>_<scenario>_<expected_result>`
- Mock external dependencies (APIs, databases)
- Achieve minimum 80% code coverage for new features

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_agent_returns_201_on_success():
    """Test that creating an agent returns 201 status code"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/agents", json={
            "name": "Test Agent",
            "role": "research"
        })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Agent"
```

### Test Fixtures

- Use pytest fixtures for common setup
- Place shared fixtures in `tests/conftest.py`
- Use factory-boy for test data generation

## Security Best Practices

### Authentication & Authorization

- Use JWT tokens for API authentication
- Implement proper role-based access control (RBAC)
- Never hardcode API keys or secrets
- Use environment variables for sensitive configuration
- Validate all user inputs

### API Security

- Implement rate limiting on endpoints
- Use HTTPS in production
- Add CORS middleware with appropriate origins
- Sanitize all user inputs to prevent injection attacks
- Use parameterized queries for database operations

```python
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Security(security)):
    """Verify JWT token and extract user information"""
    try:
        # Token verification logic
        pass
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Integration with External Services

### Atmosphere Layer (External APIs)

When integrating with GitHub, Linear, Notion, or Perplexity:

- Use async HTTP clients (httpx)
- Implement retry logic with exponential backoff
- Add proper error handling for API failures
- Cache responses when appropriate
- Use environment variables for API keys

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

class GitHubIntegration:
    """Integration with GitHub API"""
    
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30.0
        )
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_repository(self, owner: str, repo: str) -> dict:
        """Fetch repository information from GitHub"""
        response = await self.client.get(f"https://api.github.com/repos/{owner}/{repo}")
        response.raise_for_status()
        return response.json()
```

## Logging and Monitoring

### Structured Logging

- Use structlog for structured logging
- Include context in log messages (user_id, request_id, etc.)
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Add correlation IDs for request tracing

```python
import structlog

logger = structlog.get_logger()

async def process_task(task_id: str, user_id: str):
    """Process a user task"""
    logger.info(
        "task_processing_started",
        task_id=task_id,
        user_id=user_id
    )
    try:
        # Process task
        logger.info("task_processing_completed", task_id=task_id)
    except Exception as e:
        logger.error(
            "task_processing_failed",
            task_id=task_id,
            error=str(e),
            exc_info=True
        )
        raise
```

### Observability

- Add OpenTelemetry instrumentation for distributed tracing
- Use Prometheus metrics for monitoring
- Include health check endpoints

## Documentation Requirements

### Code Documentation

- Write docstrings for all public functions, classes, and modules
- Use Google-style or NumPy-style docstrings
- Include parameter types, return types, and examples
- Document exceptions that may be raised

### API Documentation

- FastAPI automatically generates OpenAPI docs
- Add comprehensive descriptions to endpoints
- Include example requests and responses
- Document all possible status codes

## Development Workflow

### Code Quality Tools

Before committing code, ensure:
- Code is formatted with Black: `black .`
- Imports are sorted with isort: `isort .`
- Code passes flake8 linting: `flake8 .`
- Type checking passes with mypy: `mypy .`
- Tests pass: `pytest`
- Security scan passes: `bandit -r app/`

### Git Commit Messages

- Use conventional commits format: `<type>(<scope>): <subject>`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep subject line under 72 characters
- Include detailed description in body if needed

Examples:
- `feat(agents): add multi-agent orchestration support`
- `fix(api): resolve authentication token validation issue`
- `docs(readme): update deployment instructions`

### Environment Configuration

- Always use `.env` file for local development (never commit it)
- Reference `.env.example` for required variables
- Use Pydantic Settings for configuration management
- Validate environment variables on application startup

## Docker and Kubernetes

### Docker Best Practices

- Use multi-stage builds to reduce image size
- Run containers as non-root user
- Use specific version tags, not `latest`
- Minimize number of layers
- Use .dockerignore to exclude unnecessary files

### Kubernetes Deployments

- Use resource limits and requests
- Implement liveness and readiness probes
- Use ConfigMaps for configuration
- Store secrets in Kubernetes Secrets
- Use Horizontal Pod Autoscaler (HPA) for scaling

## Performance Optimization

- Use async/await for I/O-bound operations
- Implement caching with Redis for frequently accessed data
- Use connection pooling for databases
- Optimize database queries with proper indexes
- Use pagination for large result sets
- Implement request batching where appropriate

## Code Review Guidelines

When reviewing pull requests:
- Verify adherence to coding standards
- Check for proper error handling
- Ensure tests are included and passing
- Review security implications
- Verify documentation is updated
- Check for performance considerations
- Ensure Tree of Life architecture principles are followed

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Tree of Life Architecture](./README.md)

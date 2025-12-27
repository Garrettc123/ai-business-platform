# Tree of Life System Integration Guide

## Overview

This Python platform (`ai-business-platform`) implements the **Tree of Life architectural pattern** and can integrate with the separate Node.js-based [Tree of Life System](https://github.com/Garrettc123/tree-of-life-system) (TITAN).

## Architecture Relationship

### This Repository (Python Platform)
- **Purpose**: Enterprise-scale AI business automation infrastructure
- **Stack**: Python, FastAPI, PostgreSQL, Redis, Kafka, Weaviate
- **Focus**: Backend services, ML pipelines, data processing
- **Deployment**: Kubernetes, Docker, Cloud-native

### Tree of Life System (Node.js Platform)
- **Purpose**: Multiplex AI business automation with external integrations
- **Stack**: Node.js, Express, GitHub/Linear/Notion/Perplexity APIs
- **Focus**: External service orchestration, webhooks, real-time sync
- **Deployment**: Vercel, Railway, Heroku

## Integration Patterns

### Pattern 1: Standalone Deployment
Deploy each system independently and integrate via REST APIs.

```
┌─────────────────────┐         ┌─────────────────────┐
│  Python Platform    │   API   │  Node.js TITAN      │
│  (This Repo)        │ ◄─────► │  (tree-of-life)     │
│  - ML Processing    │         │  - GitHub/Linear    │
│  - Data Pipeline    │         │  - Notion/Perplexity│
└─────────────────────┘         └─────────────────────┘
```

### Pattern 2: Microservices Architecture
Deploy both as microservices behind an API gateway.

```
                    ┌─────────────────┐
                    │  API Gateway    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼──────────────────┐
         │                   │                  │
┌────────▼────────┐  ┌──────▼──────┐  ┌───────▼────────┐
│ Python Platform │  │ Node TITAN  │  │ Other Services │
└─────────────────┘  └─────────────┘  └────────────────┘
```

### Pattern 3: Hybrid Deployment
Python for heavy processing, Node.js for external integrations.

```
┌────────────────────────────────────────────────┐
│              Python Platform                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ ML Model │  │   Data   │  │  Vector  │    │
│  │ Serving  │  │Processing│  │   DB     │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │              │          │
│       └─────────────┼──────────────┘          │
│                     │                         │
└─────────────────────┼─────────────────────────┘
                      │ Integration Layer
┌─────────────────────▼─────────────────────────┐
│           Node.js TITAN System                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │  GitHub  │  │  Linear  │  │  Notion  │    │
│  │  Sync    │  │  Sync    │  │  Sync    │    │
│  └──────────┘  └──────────┘  └──────────┘    │
└────────────────────────────────────────────────┘
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+ (if integrating with TITAN)
- Docker & Kubernetes (optional)

### Step 1: Deploy Python Platform

```bash
# Clone this repository
git clone https://github.com/Garrettc123/ai-business-platform.git
cd ai-business-platform

# Install dependencies
pip install -r requirements-app.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run the application
python main.py
```

The Python platform will be available at http://localhost:8000

### Step 2: Deploy Tree of Life System (Optional)

```bash
# Clone TITAN repository
git clone https://github.com/Garrettc123/tree-of-life-system.git
cd tree-of-life-system

# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with GitHub, Linear, Notion, Perplexity API keys

# Run the application
npm start
```

The Node.js TITAN system will be available at http://localhost:3000

### Step 3: Configure Integration

Add to your Python platform `.env`:

```bash
# Tree of Life System Integration
TREE_OF_LIFE_URL=http://localhost:3000
```

### Step 4: Verify Integration

```bash
# Test Python platform
curl http://localhost:8000/health

# Test TITAN system (if deployed)
curl http://localhost:3000/api/status

# Test integration (from Python platform)
python -c "
from app.atmosphere.tree_of_life_integration import get_integration
import asyncio

async def test():
    integration = get_integration()
    status = await integration.get_system_status()
    print(status)
    await integration.close()

asyncio.run(test())
"
```

## Using the Integration

### From Python Code

```python
from app.atmosphere.tree_of_life_integration import get_integration

async def sync_with_github():
    integration = get_integration()
    
    # Sync GitHub repository data
    result = await integration.sync_github_data("owner/repo")
    print(f"Sync result: {result}")
    
    # Sync Linear project
    result = await integration.sync_linear_data("project-123")
    print(f"Linear sync: {result}")
    
    # Sync Notion database
    result = await integration.sync_notion_data("database-456")
    print(f"Notion sync: {result}")
```

### From FastAPI Endpoints

```python
from fastapi import APIRouter
from app.atmosphere.tree_of_life_integration import get_integration

router = APIRouter()

@router.post("/sync/github")
async def sync_github(repo: str):
    integration = get_integration()
    return await integration.sync_github_data(repo)
```

## Deployment Options

### Option 1: Docker Compose (Both Systems)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  python-platform:
    build: ./ai-business-platform
    ports:
      - "8000:8000"
    environment:
      - TREE_OF_LIFE_URL=http://titan-system:3000
    depends_on:
      - postgres
      - redis
  
  titan-system:
    build: ./tree-of-life-system
    ports:
      - "3000:3000"
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - LINEAR_API_KEY=${LINEAR_API_KEY}
```

### Option 2: Kubernetes

Deploy both systems in Kubernetes cluster with service discovery.

### Option 3: Cloud Native

- Python Platform → AWS ECS/EKS, Google Cloud Run, Azure Container Apps
- TITAN System → Vercel, Railway, Heroku

## Benefits of This Architecture

1. **Separation of Concerns**: Python for heavy ML/data, Node.js for API integrations
2. **Scalability**: Scale each component independently
3. **Technology Fit**: Best tool for each job
4. **Flexibility**: Can be deployed together or separately
5. **Resilience**: Failure in one doesn't affect the other

## Vercel Deployment Reference

The Tree of Life System is deployed on Vercel. The problem statement references:
```
https://vercel.com/garrett-carrols-projects/tree-of-life-system-dp1d/GNfKY86885yjXHWBXrj1MN2Rjvjt
```

This Python platform can integrate with that deployment by setting:
```bash
TREE_OF_LIFE_URL=https://your-vercel-deployment.vercel.app
```

## Troubleshooting

### Connection Issues
- Ensure both services are running
- Check firewall rules
- Verify URLs and ports in `.env`

### API Authentication
- Configure API keys in both systems
- Ensure tokens have necessary permissions

### Network Issues
- Check service discovery in Kubernetes
- Verify DNS resolution
- Test with `curl` or `httpx`

## Support

- Python Platform Issues: https://github.com/Garrettc123/ai-business-platform/issues
- TITAN System Issues: https://github.com/Garrettc123/tree-of-life-system/issues

# Tree of Life System - API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### Root Endpoints

#### GET /
Get system information and architecture overview.

**Response:**
```json
{
  "name": "Tree of Life System",
  "description": "Multiplex AI Business Platform",
  "version": "1.0.0",
  "status": "operational",
  "architecture": {
    "roots": "Blockchain & Core Infrastructure",
    "trunk": "Core Business Logic & Integration",
    "branches": "Domain-specific Modules",
    "leaves": "User Applications & Interfaces",
    "atmosphere": "API & Service Integration",
    "nervous_system": "AI Agent Network"
  }
}
```

#### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "environment": "production",
  "version": "1.0.0"
}
```

### API v1 Endpoints

#### GET /api/v1/status
Get API version and layer status.

**Response:**
```json
{
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
```

## Interactive Documentation

When the application is running, you can access interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Tree of Life Architecture Layers

### 🌱 ROOTS Layer
Infrastructure and data foundation
- Database connections
- Message queues
- Vector databases

### 🪵 TRUNK Layer
Core business logic
- Contribution management
- Verification engine
- Reward distribution

### 🌿 BRANCHES Layer
Domain-specific modules
- Research
- Medical
- Financial
- Environmental

### 🍃 LEAVES Layer
User-facing applications
- Contributor portal
- Verifier dashboard
- Analytics platform

### 💨 ATMOSPHERE Layer
Integration and communication
- GitHub integration
- Linear integration
- Notion integration
- Perplexity AI integration

### 🧠 NERVOUS SYSTEM Layer
AI agent network
- Verification agents
- Risk assessment agents
- Orchestration agents
- Optimization agents

## Authentication

Authentication endpoints will be added in future releases. Currently, the API is open for development purposes.

## Rate Limiting

Rate limiting will be implemented in production deployments.

## Support

For issues and questions, please visit: https://github.com/Garrettc123/ai-business-platform/issues

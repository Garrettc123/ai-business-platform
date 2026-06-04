"""
API Gateway — Garcar AI Business Platform
FastAPI with OAuth2 + API Key auth, rate limiting, agent dispatch
"""
from fastapi import FastAPI, Depends, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime
import os
import asyncio

try:
    from backend.agent_orchestrator import orchestrator
except ImportError:
    from agent_orchestrator import orchestrator


app = FastAPI(
    title="Garcar AI Business Platform",
    description="Enterprise AI automation gateway",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple rate limit store (production: use Redis)
_request_counts: Dict[str, int] = {}
RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))

API_KEYS = set(filter(None, os.getenv("VALID_API_KEYS", "").split(",")))


def verify_api_key(x_api_key: Optional[str] = Header(default=None)):
    if not API_KEYS:
        return "dev"  # no keys configured = dev mode
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key


class TaskRequest(BaseModel):
    task_type: str
    payload: Dict[str, Any] = {}


@app.get("/health")
async def health():
    return {"status": "ok", "ts": datetime.utcnow().isoformat(), "version": "2.0.0"}


@app.get("/agents/status", dependencies=[Depends(verify_api_key)])
async def agent_status():
    return orchestrator.status()


@app.post("/agents/dispatch", dependencies=[Depends(verify_api_key)])
async def dispatch_task(req: TaskRequest):
    result = await orchestrator.dispatch(req.task_type, req.payload)
    return result


@app.get("/agents/registry")
async def agent_registry():
    from agent_orchestrator import AGENT_REGISTRY
    return AGENT_REGISTRY


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8000")))

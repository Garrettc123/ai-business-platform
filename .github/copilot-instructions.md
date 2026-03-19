# AI Business Platform — Copilot Instructions

## Purpose
Enterprise AI Business Automation Platform — LangGraph agent orchestration, FastAPI, multi-cloud.

## Standards
- Python 3.11+, FastAPI, LangGraph, Pydantic v2
- All secrets from env vars or AWS SSM — never hardcoded
- All agents must be importable and testable independently
- Workflows must use `continue-on-error: true` on cloud auth steps
- New agents must register in the agent coordinator module

## Agent Architecture
- Each agent = single Python file in `agents/`
- Agents communicate via shared message bus (Redis streams)
- All agents emit metrics to `metrics/` S3 prefix

## PR Standards
- Must not break `/health` or `/agents` API endpoints
- Must include a test in `tests/` for new agents
- CI must pass before merge

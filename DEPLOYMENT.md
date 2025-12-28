# 🚀 Deployment Guide

## Quick Deploy to Vercel

### Option 1: One-Command Deploy
```bash
npm install -g vercel
vercel --prod
```

### Option 2: Git Integration (Recommended)
```bash
git push origin main
```
Auto-deploys on every push!

## Local Development

```bash
# Standard Python
python main.py

# Using UV (faster)
uv run main.py

# Development with hot reload
uvicorn app:app --reload
```

## Environment Variables

Create `.env` file:
```
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Vercel Setup

1. Install Vercel CLI: `npm install -g vercel`
2. Login: `vercel login`
3. Deploy: `vercel --prod`

## Endpoints

- `/` - Root health check
- `/health` - Health status
- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation

## Status

✅ Ready to deploy
✅ All files configured
✅ FastAPI entrypoint ready

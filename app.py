"""FastAPI application entrypoint for Vercel deployment."""
# Import the integrated FastAPI app from the app package
from app import app

# Export app for Vercel
__all__ = ["app"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

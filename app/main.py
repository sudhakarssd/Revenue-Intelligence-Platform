from fastapi import FastAPI
from app.api.v1.router import api_router
from app.shared.logger import get_logger
from app.infrastructure.config import settings

# Initialize logging on entry
logger = get_logger("app.main")

app = FastAPI(
    title="Revenue Intelligence Platform API",
    description="Enterprise AI Platform for Revenue Intelligence, Sales Analytics, and Executive Decision Support.",
    version="1.0.0"
)

# Register API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint to monitor application and default config status."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "default_provider": settings.default_provider,
        "default_model": settings.default_model
    }

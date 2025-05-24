"""Main application module."""
import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import admin, rag, webhook
from app.core.config import settings
from app.services.monitoring import setup_monitoring

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
try:
    app.include_router(admin.router, prefix="/admin", tags=["admin"])
    app.include_router(rag.router, prefix="/rag", tags=["rag"])
    app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])
    logger.info("All routers included successfully")
except Exception as e:
    logger.error(f"Error including routers: {e}")
    # Don't re-raise, allow app to start even if some routers fail

# Set up monitoring
try:
    setup_monitoring(app)
    logger.info("Monitoring setup complete")
except Exception as e:
    logger.error(f"Error setting up monitoring: {e}")
    # Don't re-raise, allow app to start even if monitoring setup fails

@app.on_event("startup")
async def startup():
    """Run startup tasks."""
    logger.info("Application startup initiated")
    # Note: We don't create tables here anymore - that's handled by Alembic migrations
    # This prevents conflicts between direct SQLAlchemy table creation and migrations
    logger.info("Application startup complete")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Lumi API",
        "docs": "/docs",
        "version": settings.PROJECT_VERSION,
        "status": "active",
    }

@app.get("/ping")
async def ping():
    """Simple ping endpoint to verify the service is running."""
    return {"status": "ok", "message": "pong"}

if __name__ == "__main__":
    import hypercorn
    port = int(os.getenv("PORT", "8000"))
    logger.info(f"Starting Hypercorn server on port {port}")
    hypercorn.run("main:app", host="0.0.0.0", port=port, reload=True)

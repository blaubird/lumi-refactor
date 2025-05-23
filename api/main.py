"""Main application module."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import admin, rag, webhook
from app.core.config import settings
from app.core.database import Base, engine
from app.services.monitoring import setup_monitoring

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

# Set up monitoring
setup_monitoring(app)

# Include routers
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(rag.router, prefix="/rag", tags=["rag"])
app.include_router(webhook.router, prefix="/webhook", tags=["webhook"])


@app.on_event("startup")
async def startup():
    """Run startup tasks."""
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Lumi API",
        "docs": "/docs",
        "version": settings.PROJECT_VERSION,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

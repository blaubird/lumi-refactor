from fastapi import FastAPI, Depends, HTTPException, Request, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from app.api.endpoints import webhook
from app.core.database import get_db
from app.core.logging import logging as logger

# Create FastAPI app
app = FastAPI(title="LuminiteQ API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(webhook.router, tags=["webhook"])

# Root endpoint
@app.get("/")
def read_root():
    return {"status": "ok", "message": "LuminiteQ API is running"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

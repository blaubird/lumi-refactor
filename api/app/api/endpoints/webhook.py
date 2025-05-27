from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.logging import logging as logger
from app.api.deps import get_db
import os

router = APIRouter()

@router.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    """Handler for webhook verification from Meta"""
    if hub_mode == "subscribe" and hub_verify_token == os.getenv("WH_TOKEN"):
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/webhook")
def webhook_handler(request: Request, db: Session = Depends(get_db)):
    """Handler for webhooks from WhatsApp"""
    try:
        # Log webhook receipt
        logger.info("Received webhook request")
        
        # Return successful response
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error in webhook handler: {str(e)}")
        return {"status": "error", "message": str(e)}

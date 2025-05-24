"""Enhanced webhook handler for WhatsApp integration."""

import json
import os
from typing import Dict, Optional

from app.api.deps import get_db
from app.core.logging import logging as logger
from app.models.message import Message
from app.services.ai import get_rag_response
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

# Import the WhatsApp client
from app.services.whatsapp import WhatsAppClient

router = APIRouter()
whatsapp_client = None

# Initialize WhatsApp client
try:
    whatsapp_client = WhatsAppClient()
    logger.info("WhatsApp client initialized")
except Exception as e:
    logger.error(f"Failed to initialize WhatsApp client: {e}")


@router.get("/webhook")
def verify_webhook(
    hub_mode: str = None, hub_verify_token: str = None, hub_challenge: str = None
):
    """Handler for webhook verification from Meta"""
    verify_token = os.getenv("WH_TOKEN")
    if not verify_token:
        logger.error("WH_TOKEN environment variable not set")
        raise HTTPException(status_code=500, detail="Webhook token not configured")
        
    if hub_mode == "subscribe" and hub_verify_token == verify_token:
        logger.info("Webhook verification successful")
        return int(hub_challenge)
    
    logger.warning(f"Webhook verification failed. Expected: {verify_token}, Got: {hub_verify_token}")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/webhook")
async def webhook_handler(request: Request, db: Session = Depends(get_db)):
    """Handler for webhooks from WhatsApp"""
    try:
        # Parse request body
        body = await request.json()
        logger.info(f"Received webhook: {json.dumps(body)[:200]}...")
        
        # Check if WhatsApp client is initialized
        if not whatsapp_client:
            logger.error("WhatsApp client not initialized")
            return {"status": "error", "message": "WhatsApp client not initialized"}
        
        # Parse the message
        message_data = whatsapp_client.parse_webhook_message(body)
        if not message_data:
            logger.warning("No valid message found in webhook")
            return {"status": "ok", "message": "No valid message found"}
        
        # Extract message details
        from_number = message_data.get("from")
        message_content = message_data.get("content")
        message_type = message_data.get("type")
        
        # Only process text messages
        if message_type != "text" or not message_content:
            logger.info(f"Skipping non-text message of type: {message_type}")
            return {"status": "ok", "message": "Non-text message received"}
        
        # Store the message
        tenant_id = "default"  # Use default tenant or extract from context
        db_message = Message(
            tenant_id=tenant_id,
            user_id=from_number,
            content=message_content,
            role="user"
        )
        db.add(db_message)
        db.commit()
        
        # Generate AI response
        logger.info(f"Generating response for: {message_content[:50]}...")
        ai_response = await get_rag_response(
            db=db,
            tenant_id=tenant_id,
            query=message_content
        )
        
        # Store AI response
        ai_db_message = Message(
            tenant_id=tenant_id,
            user_id="system",
            content=ai_response,
            role="assistant"
        )
        db.add(ai_db_message)
        db.commit()
        
        # Send response back to user
        logger.info(f"Sending response to {from_number}")
        send_result = await whatsapp_client.send_text_message(
            to=from_number,
            text=ai_response
        )
        
        if "error" in send_result:
            logger.error(f"Failed to send response: {send_result}")
            return {"status": "error", "message": "Failed to send response"}
        
        return {"status": "ok", "message": "Message processed successfully"}
        
    except Exception as e:
        logger.error(f"Error in webhook handler: {str(e)}")
        return {"status": "error", "message": str(e)}

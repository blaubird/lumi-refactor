"""WhatsApp client module for interacting with WhatsApp Business API."""

import json
import logging
import os
from typing import Dict, List, Optional, Union

import httpx
from app.core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class WhatsAppClient:
    """Client for WhatsApp Business API."""
    
    def __init__(self, phone_number_id: str = None, token: str = None):
        """Initialize WhatsApp client.
        
        Args:
            phone_number_id: WhatsApp phone number ID
            token: WhatsApp API token
        """
        self.phone_number_id = phone_number_id or os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.token = token or os.getenv("WHATSAPP_API_TOKEN")
        self.api_version = "v17.0"  # Current WhatsApp API version
        self.base_url = f"https://graph.facebook.com/{self.api_version}/{self.phone_number_id}"
        
        if not self.phone_number_id or not self.token:
            logger.warning("WhatsApp credentials not configured properly")
    
    async def send_text_message(self, to: str, text: str) -> Dict:
        """Send a text message to a WhatsApp user.
        
        Args:
            to: Recipient's phone number
            text: Message content
            
        Returns:
            API response
        """
        try:
            url = f"{self.base_url}/messages"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "text",
                "text": {"body": text}
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    headers=headers, 
                    json=payload, 
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Message sent successfully to {to}")
                    return response.json()
                else:
                    logger.error(f"Failed to send message: {response.text}")
                    return {"error": response.text, "status_code": response.status_code}
                    
        except Exception as e:
            logger.error(f"Error sending WhatsApp message: {str(e)}")
            return {"error": str(e)}
    
    async def send_template_message(
        self, 
        to: str, 
        template_name: str, 
        language_code: str = "en_US",
        components: Optional[List[Dict]] = None
    ) -> Dict:
        """Send a template message to a WhatsApp user.
        
        Args:
            to: Recipient's phone number
            template_name: Name of the template
            language_code: Language code for the template
            components: Template components (header, body, buttons)
            
        Returns:
            API response
        """
        try:
            url = f"{self.base_url}/messages"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.token}"
            }
            
            template = {
                "name": template_name,
                "language": {"code": language_code}
            }
            
            if components:
                template["components"] = components
                
            payload = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "template",
                "template": template
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url, 
                    headers=headers, 
                    json=payload,
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    logger.info(f"Template message sent successfully to {to}")
                    return response.json()
                else:
                    logger.error(f"Failed to send template message: {response.text}")
                    return {"error": response.text, "status_code": response.status_code}
                    
        except Exception as e:
            logger.error(f"Error sending WhatsApp template message: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def parse_webhook_message(body: Dict) -> Optional[Dict]:
        """Parse WhatsApp webhook message.
        
        Args:
            body: Webhook request body
            
        Returns:
            Parsed message or None if invalid
        """
        try:
            # Extract entry and changes
            entry = body.get("entry", [])
            if not entry or not isinstance(entry, list):
                return None
                
            changes = entry[0].get("changes", [])
            if not changes or not isinstance(changes, list):
                return None
                
            # Extract value
            value = changes[0].get("value", {})
            if not value:
                return None
                
            # Extract messages
            messages = value.get("messages", [])
            if not messages or not isinstance(messages, list):
                return None
                
            # Extract first message
            message = messages[0]
            if not message:
                return None
                
            # Extract message details
            message_id = message.get("id")
            from_number = message.get("from")
            timestamp = message.get("timestamp")
            
            # Extract message content based on type
            message_type = message.get("type")
            content = None
            
            if message_type == "text":
                text_obj = message.get("text", {})
                content = text_obj.get("body") if text_obj else None
            elif message_type == "image":
                image_obj = message.get("image", {})
                content = image_obj.get("id") if image_obj else None
            elif message_type == "audio":
                audio_obj = message.get("audio", {})
                content = audio_obj.get("id") if audio_obj else None
            elif message_type == "document":
                document_obj = message.get("document", {})
                content = document_obj.get("id") if document_obj else None
            
            # Return parsed message
            return {
                "message_id": message_id,
                "from": from_number,
                "timestamp": timestamp,
                "type": message_type,
                "content": content
            }
            
        except Exception as e:
            logger.error(f"Error parsing webhook message: {str(e)}")
            return None

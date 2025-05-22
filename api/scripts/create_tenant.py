#!/usr/bin/env python3
import os
import argparse
from sqlalchemy.orm import Session
from app.models.tenant import Tenant
from app.core.database import SessionLocal
from app.core.logging import logger

def create_tenant(phone_id: str, wh_token: str, system_prompt: str = None):
    """Create a new tenant in the database"""
    db = SessionLocal()
    try:
        # Generate tenant ID from phone_id
        tenant_id = f"tenant_{phone_id.replace('+', '')}"
        
        # Set default system prompt if not provided
        if not system_prompt:
            system_prompt = "You are a helpful assistant."
        
        # Create tenant object
        tenant = Tenant(
            id=tenant_id,
            phone_id=phone_id,
            wh_token=wh_token,
            system_prompt=system_prompt
        )
        
        # Add to database
        db.add(tenant)
        db.commit()
        
        logger.info(f"Created tenant: {tenant_id}")
        return tenant
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating tenant: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a new tenant")
    parser.add_argument("--phone_id", required=True, help="Phone ID for the tenant")
    parser.add_argument("--wh_token", required=True, help="Webhook token for the tenant")
    parser.add_argument("--system_prompt", help="System prompt for the tenant")
    
    args = parser.parse_args()
    
    create_tenant(args.phone_id, args.wh_token, args.system_prompt)

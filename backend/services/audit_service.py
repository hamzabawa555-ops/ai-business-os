"""Audit Service"""

import logging
from typing import Optional, Any, Dict
from sqlalchemy.orm import Session
from backend.models.models import AuditLog
from datetime import datetime

logger = logging.getLogger(__name__)

class AuditService:
    """Audit Service for logging user actions"""
    
    @staticmethod
    def log_action(
        db: Session,
        user_id: Optional[str],
        action: str,
        resource_type: str,
        resource_id: str,
        changes: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Optional[AuditLog]:
        """Log an action to audit log"""
        try:
            audit_log = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                changes=changes or {},
                ip_address=ip_address,
                user_agent=user_agent
            )
            
            db.add(audit_log)
            db.commit()
            db.refresh(audit_log)
            
            logger.info(
                f"Audit log created: action={action}, resource={resource_type}/{resource_id}, user={user_id}"
            )
            return audit_log
        except Exception as e:
            db.rollback()
            logger.error(f"Audit logging error: {str(e)}")
            return None
    
    @staticmethod
    def get_audit_logs(
        db: Session,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> list:
        """Get audit logs with optional filters"""
        try:
            query = db.query(AuditLog)
            
            if user_id:
                query = query.filter(AuditLog.user_id == user_id)
            if resource_type:
                query = query.filter(AuditLog.resource_type == resource_type)
            
            return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Get audit logs error: {str(e)}")
            return []

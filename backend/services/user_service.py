"""User Service"""

import logging
from datetime import datetime
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from backend.models.models import User

logger = logging.getLogger(__name__)

class UserService:
    """User Service"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            return db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Get user error: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            logger.error(f"Get user by email error: {str(e)}")
            return None
    
    @staticmethod
    def update_user(
        db: Session,
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        company_name: Optional[str] = None
    ) -> Tuple[Optional[User], Optional[str]]:
        """Update user information"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None, "User not found"
            
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if company_name is not None:
                user.company_name = company_name
            
            user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(user)
            
            logger.info(f"User updated: {user_id}")
            return user, None
        except Exception as e:
            db.rollback()
            logger.error(f"User update error: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def deactivate_user(db: Session, user_id: str) -> Tuple[bool, Optional[str]]:
        """Deactivate user account"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found"
            
            user.is_active = False
            db.commit()
            
            logger.info(f"User deactivated: {user_id}")
            return True, None
        except Exception as e:
            db.rollback()
            logger.error(f"User deactivation error: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def verify_user(db: Session, user_id: str) -> Tuple[bool, Optional[str]]:
        """Verify user email"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found"
            
            user.is_verified = True
            db.commit()
            
            logger.info(f"User verified: {user_id}")
            return True, None
        except Exception as e:
            db.rollback()
            logger.error(f"User verification error: {str(e)}")
            return False, str(e)

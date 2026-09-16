"""User Service"""

import logging
from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.user import User, UserRole
from backend.schemas.user import UserCreate, UserUpdate, UserResponse
from backend.utils.security import hash_password, verify_password
from typing import Optional

logger = logging.getLogger(__name__)

class UserService:
    """User business logic service"""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user
        """
        logger.info(f"Creating new user with email: {user_data.email}")
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            logger.warning(f"User with email {user_data.email} already exists")
            raise ValueError(f"User with email {user_data.email} already exists")
        
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Create user
        db_user = User(
            email=user_data.email,
            password_hash=password_hash,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            company_name=user_data.company_name,
            role=UserRole.USER,
            is_active=True,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(f"User {db_user.id} created successfully")
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user with email and password
        """
        logger.info(f"Authenticating user: {email}")
        
        user = UserService.get_user_by_email(db, email)
        if not user:
            logger.warning(f"User {email} not found")
            return None
        
        if not user.is_active:
            logger.warning(f"User {email} is inactive")
            return None
        
        if not verify_password(password, user.password_hash):
            logger.warning(f"Invalid password for user {email}")
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()
        
        logger.info(f"User {email} authenticated successfully")
        return user

    @staticmethod
    def update_user(db: Session, user_id: str, user_data: UserUpdate) -> Optional[User]:
        """
        Update user information
        """
        logger.info(f"Updating user: {user_id}")
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return None
        
        # Update fields
        if user_data.first_name:
            user.first_name = user_data.first_name
        if user_data.last_name:
            user.last_name = user_data.last_name
        if user_data.company_name is not None:
            user.company_name = user_data.company_name
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        logger.info(f"User {user_id} updated successfully")
        return user

    @staticmethod
    def change_password(db: Session, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password
        """
        logger.info(f"Changing password for user: {user_id}")
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return False
        
        # Verify current password
        if not verify_password(current_password, user.password_hash):
            logger.warning(f"Invalid current password for user {user_id}")
            return False
        
        # Hash and set new password
        user.password_hash = hash_password(new_password)
        user.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"Password changed for user {user_id}")
        return True

    @staticmethod
    def deactivate_user(db: Session, user_id: str) -> bool:
        """
        Deactivate user account
        """
        logger.info(f"Deactivating user: {user_id}")
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        db.commit()
        
        logger.info(f"User {user_id} deactivated")
        return True

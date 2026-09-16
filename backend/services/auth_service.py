"""Authentication Service"""

from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.config import settings
from backend.models.models import User
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthenticationError(Exception):
    """Custom authentication error"""
    pass

class AuthService:
    """Authentication Service"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password"""
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters")
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Password verification error: {str(e)}")
            return False
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        
        to_encode.update({"exp": expire})
        
        try:
            encoded_jwt = jwt.encode(
                to_encode,
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM
            )
            return encoded_jwt
        except Exception as e:
            logger.error(f"Token creation error: {str(e)}")
            raise AuthenticationError("Failed to create token")
    
    @staticmethod
    def decode_access_token(token: str) -> dict:
        """Decode and verify JWT access token"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.error(f"Token decode error: {str(e)}")
            raise AuthenticationError("Invalid token")
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user by email and password"""
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                logger.warning(f"Login attempt for non-existent user: {email}")
                return None
            
            if not user.is_active:
                logger.warning(f"Login attempt for inactive user: {email}")
                return None
            
            if not AuthService.verify_password(password, user.password_hash):
                logger.warning(f"Failed login attempt for user: {email}")
                return None
            
            # Update last login
            user.last_login = datetime.utcnow()
            db.commit()
            
            logger.info(f"User logged in: {email}")
            return user
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return None
    
    @staticmethod
    def create_user(
        db: Session,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        company_name: Optional[str] = None
    ) -> Tuple[User, Optional[str]]:
        """Create new user"""
        try:
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                return None, "Email already registered"
            
            # Hash password
            password_hash = AuthService.hash_password(password)
            
            # Create user
            user = User(
                email=email,
                password_hash=password_hash,
                first_name=first_name,
                last_name=last_name,
                company_name=company_name
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info(f"User created: {email}")
            return user, None
        except Exception as e:
            db.rollback()
            logger.error(f"User creation error: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            return db.query(User).filter(User.id == user_id).first()
        except Exception as e:
            logger.error(f"Get user error: {str(e)}")
            return None
    
    @staticmethod
    def change_password(
        db: Session,
        user_id: str,
        current_password: str,
        new_password: str
    ) -> Tuple[bool, Optional[str]]:
        """Change user password"""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False, "User not found"
            
            # Verify current password
            if not AuthService.verify_password(current_password, user.password_hash):
                return False, "Current password is incorrect"
            
            # Hash new password
            user.password_hash = AuthService.hash_password(new_password)
            db.commit()
            
            logger.info(f"Password changed for user: {user.email}")
            return True, None
        except Exception as e:
            db.rollback()
            logger.error(f"Password change error: {str(e)}")
            return False, str(e)

"""Security Utilities"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from backend.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    # TODO: Implement JWT token creation
    # This is a placeholder implementation
    return "placeholder_token"

def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT access token"""
    # TODO: Implement JWT token decoding
    # This is a placeholder implementation
    return {}

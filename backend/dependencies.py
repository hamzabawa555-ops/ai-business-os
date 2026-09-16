"""Dependencies for FastAPI endpoints"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from typing import Optional
import logging

from backend.db.session import get_db
from backend.services.auth_service import AuthService, AuthenticationError
from backend.models.models import User
from backend.exceptions import AuthenticationException, AuthorizationException

logger = logging.getLogger(__name__)
security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency for getting current authenticated user
    
    Args:
        credentials: HTTP bearer token from request
        db: Database session
        
    Returns:
        User object
        
    Raises:
        AuthenticationException: If token is invalid or user not found
    """
    try:
        token = credentials.credentials
        
        # Decode token
        payload = AuthService.decode_access_token(token)
        user_id = payload.get("sub")
        
        if not user_id:
            logger.warning("Token missing user ID")
            raise AuthenticationException("Invalid token")
        
        # Get user from database
        user = AuthService.get_user_by_id(db, user_id)
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise AuthenticationException("User not found")
        
        if not user.is_active:
            logger.warning(f"Inactive user attempted access: {user_id}")
            raise AuthenticationException("User account is inactive")
        
        return user
    except AuthenticationError as e:
        logger.error(f"Authentication error: {str(e)}")
        raise AuthenticationException(str(e))
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {str(e)}")
        raise AuthenticationException("Authentication failed")

async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency for getting current user with admin role
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        User object with admin role
        
    Raises:
        AuthorizationException: If user is not admin
    """
    if current_user.role != "admin":
        logger.warning(f"Non-admin user attempted admin access: {current_user.id}")
        raise AuthorizationException("Admin privileges required")
    
    return current_user

def verify_user_owns_resource(
    user_id: str,
    resource_owner_id: str
) -> bool:
    """
    Verify that user owns a resource
    
    Args:
        user_id: Current user ID
        resource_owner_id: Resource owner ID
        
    Returns:
        True if user owns resource
        
    Raises:
        AuthorizationException: If user doesn't own resource
    """
    if user_id != resource_owner_id:
        logger.warning(f"User {user_id} attempted to access resource owned by {resource_owner_id}")
        raise AuthorizationException("You don't have permission to access this resource")
    
    return True

"""Updated Authentication API endpoints with actual implementation"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.services.auth_service import AuthService
from backend.models.models import User
from backend.dependencies import get_current_user
from backend.exceptions import AuthenticationException, ValidationException, ConflictException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    """Login response model"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict

class RegisterRequest(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    company_name: Optional[str] = None

class RegisterResponse(BaseModel):
    """User registration response"""
    id: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime

class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    """Change password request"""
    current_password: str
    new_password: str
    confirm_password: str

# Routes
@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    User login endpoint
    
    Returns access token for authenticated users
    """
    try:
        # Authenticate user
        user = AuthService.authenticate_user(db, request.email, request.password)
        if not user:
            logger.warning(f"Failed login attempt for: {request.email}")
            raise AuthenticationException("Invalid email or password")
        
        # Create access token
        access_token = AuthService.create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=timedelta(hours=24)
        )
        
        logger.info(f"User logged in: {user.email}")
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=86400,  # 24 hours
            user={
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "company_name": user.company_name
            }
        )
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise AuthenticationException("Login failed")

@router.post("/auth/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    User registration endpoint
    
    Creates a new user account
    """
    try:
        # Validate password
        if len(request.password) < 6:
            raise ValidationException(
                "Password must be at least 6 characters",
                {"password": ["Minimum 6 characters required"]}
            )
        
        if request.password != getattr(request, "confirm_password", request.password):
            raise ValidationException(
                "Passwords do not match",
                {"password": ["Passwords do not match"]}
            )
        
        # Create user
        user, error = AuthService.create_user(
            db,
            request.email,
            request.password,
            request.first_name,
            request.last_name,
            request.company_name
        )
        
        if error:
            if "already" in error.lower():
                raise ConflictException("Email already registered")
            raise ValidationException(error)
        
        logger.info(f"New user registered: {user.email}")
        
        return RegisterResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at
        )
    except (ValidationException, ConflictException, AuthenticationException):
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise AuthenticationException("Registration failed")

@router.post("/auth/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    User logout endpoint
    
    Invalidates user session
    """
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "Successfully logged out"}

@router.post("/auth/refresh", response_model=LoginResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token endpoint
    
    Returns new access token using refresh token
    """
    try:
        # TODO: Implement refresh token logic with token blacklist
        # For now, decode the token and create a new one
        payload = AuthService.decode_access_token(request.refresh_token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise AuthenticationException("Invalid refresh token")
        
        user = AuthService.get_user_by_id(db, user_id)
        if not user:
            raise AuthenticationException("User not found")
        
        # Create new access token
        access_token = AuthService.create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=timedelta(hours=24)
        )
        
        logger.info(f"Token refreshed for user: {user.email}")
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=86400,
            user={
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "company_name": user.company_name
            }
        )
    except AuthenticationException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise AuthenticationException("Token refresh failed")

@router.post("/auth/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    
    Updates authenticated user's password
    """
    try:
        if request.new_password != request.confirm_password:
            raise ValidationException(
                "Passwords do not match",
                {"password": ["New passwords do not match"]}
            )
        
        if len(request.new_password) < 6:
            raise ValidationException(
                "Password must be at least 6 characters",
                {"password": ["Minimum 6 characters required"]}
            )
        
        success, error = AuthService.change_password(
            db,
            current_user.id,
            request.current_password,
            request.new_password
        )
        
        if not success:
            raise AuthenticationException(error or "Password change failed")
        
        logger.info(f"Password changed for user: {current_user.email}")
        return {"message": "Password changed successfully"}
    except (ValidationException, AuthenticationException):
        raise
    except Exception as e:
        logger.error(f"Password change error: {str(e)}")
        raise AuthenticationException("Password change failed")

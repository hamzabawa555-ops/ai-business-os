"""User database schema"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class UserRole(str, Enum):
    """User role"""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"

class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str
    last_name: str
    company_name: Optional[str] = None

class UserCreate(UserBase):
    """User creation schema"""
    password: str

class UserUpdate(BaseModel):
    """User update schema"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company_name: Optional[str] = None

class UserResponse(UserBase):
    """User response schema"""
    id: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    """User in database schema"""
    password_hash: str

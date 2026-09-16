"""Exception Classes and Error Handlers"""

import logging
from fastapi import HTTPException, status
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AppException(Exception):
    """Base application exception"""
    def __init__(self, message: str, status_code: int = 500, details: Dict[str, Any] = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class AuthenticationException(AppException):
    """Authentication error"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)

class AuthorizationException(AppException):
    """Authorization error"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)

class ValidationException(AppException):
    """Validation error"""
    def __init__(self, message: str = "Validation failed", details: Dict[str, Any] = None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, details)

class ResourceNotFoundException(AppException):
    """Resource not found error"""
    def __init__(self, resource: str, resource_id: str = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(message, status.HTTP_404_NOT_FOUND)

class ConflictException(AppException):
    """Resource conflict error"""
    def __init__(self, message: str = "Resource conflict"):
        super().__init__(message, status.HTTP_409_CONFLICT)

class RateLimitException(AppException):
    """Rate limit exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS)

def create_error_response(exception: AppException) -> Dict[str, Any]:
    """Create standardized error response"""
    response = {
        "error": {
            "message": exception.message,
            "status_code": exception.status_code,
        }
    }
    if exception.details:
        response["error"]["details"] = exception.details
    return response

def log_exception(exc: Exception, context: Dict[str, Any] = None) -> None:
    """Log exception with context"""
    context_str = ""
    if context:
        context_str = f" | Context: {context}"
    logger.error(f"Exception: {str(exc)}{context_str}", exc_info=True)

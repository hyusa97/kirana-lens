"""
Rate limiting middleware using slowapi
"""
import time
from typing import Optional

from fastapi import HTTPException, Request, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from starlette.responses import JSONResponse

from app.dependencies import get_current_user_optional


def get_user_id_or_ip(request: Request) -> str:
    """
    Get user ID for authenticated requests, IP address for unauthenticated.
    This allows per-user rate limiting for authenticated endpoints.
    """
    try:
        # Try to get user from request state (set by auth middleware)
        user = getattr(request.state, 'user', None)
        if user:
            return f"user:{user.id}"
    except Exception:
        pass
    
    # Fall back to IP address
    return f"ip:{get_remote_address(request)}"


def get_ip_address(request: Request) -> str:
    """Get IP address for IP-based rate limiting."""
    return get_remote_address(request)


# Create limiter instance
limiter = Limiter(
    key_func=get_ip_address,  # Default to IP-based limiting
    default_limits=["1000 per hour"]  # Global fallback limit
)


def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    """
    Custom rate limit exceeded handler that returns structured JSON response.
    """
    retry_after = int(exc.retry_after) if exc.retry_after else 60
    
    response = JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Rate limit exceeded",
            "retry_after_seconds": retry_after,
            "limit": str(exc.detail).split(" ")[0] if exc.detail else "unknown"
        }
    )
    
    # Add Retry-After header
    response.headers["Retry-After"] = str(retry_after)
    
    return response


# Rate limiting decorators for different endpoint types
def rate_limit_auth_login():
    """Rate limit for login endpoint: 10 requests/minute per IP"""
    return limiter.limit("10/minute", key_func=get_ip_address)


def rate_limit_auth_register():
    """Rate limit for register endpoint: 5 requests/minute per IP"""
    return limiter.limit("5/minute", key_func=get_ip_address)


def rate_limit_assessments():
    """Rate limit for assessment creation: 30 requests/hour per authenticated user"""
    return limiter.limit("30/hour", key_func=get_user_id_or_ip)


def rate_limit_get_endpoints():
    """Rate limit for GET endpoints: 100 requests/minute per IP"""
    return limiter.limit("100/minute", key_func=get_ip_address)


def rate_limit_general():
    """General rate limit for other endpoints: 200 requests/hour per IP"""
    return limiter.limit("200/hour", key_func=get_ip_address)


# Export the limiter and handler for use in main.py
__all__ = [
    "limiter",
    "custom_rate_limit_handler",
    "rate_limit_auth_login",
    "rate_limit_auth_register", 
    "rate_limit_assessments",
    "rate_limit_get_endpoints",
    "rate_limit_general"
]
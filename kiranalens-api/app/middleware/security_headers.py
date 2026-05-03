"""
Security headers middleware for enhanced security
"""
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    
    Headers added:
    - X-Content-Type-Options: Prevents MIME type sniffing
    - X-Frame-Options: Prevents clickjacking attacks
    - X-XSS-Protection: Enables XSS filtering in browsers
    - Referrer-Policy: Controls referrer information
    - Content-Security-Policy: Prevents XSS and data injection
    - Strict-Transport-Security: Enforces HTTPS (production only)
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.is_production = settings.ENVIRONMENT == "production"
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers to response
        self._add_security_headers(response)
        
        return response
    
    def _add_security_headers(self, response: Response):
        """Add all security headers to the response."""
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking by denying framing
        response.headers["X-Frame-Options"] = "DENY"
        
        # Enable XSS protection in browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Control referrer information
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Content Security Policy - restrictive but functional for API
        csp_directives = [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self' 'unsafe-inline'",  # Allow inline styles for API docs
            "img-src 'self' data: https:",  # Allow images from HTTPS and data URLs
            "font-src 'self'",
            "connect-src 'self'",
            "frame-ancestors 'none'",  # Equivalent to X-Frame-Options: DENY
            "base-uri 'self'",
            "form-action 'self'"
        ]
        response.headers["Content-Security-Policy"] = "; ".join(csp_directives)
        
        # Strict Transport Security (HTTPS only, production only)
        if self.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Additional security headers
        
        # Prevent browsers from inferring content type
        response.headers["X-Download-Options"] = "noopen"
        
        # Control DNS prefetching
        response.headers["X-DNS-Prefetch-Control"] = "off"
        
        # Disable Adobe Flash cross-domain requests
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        
        # Remove server information
        if "server" in response.headers:
            del response.headers["server"]
        
        # Add custom API version header
        response.headers["X-API-Version"] = "1.0.0"
        
        # Add security policy information
        response.headers["X-Security-Policy"] = "KiranaLens API Security Policy v1.0"


# Export for use in main.py
__all__ = ["SecurityHeadersMiddleware"]
"""
KiranaLens API - Main application entry point
"""
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import SQLAlchemyError

from app.config import settings
from app.database import engine, test_db_connection
from app.middleware.request_logging import RequestLoggingMiddleware, configure_logging
from app.middleware.rate_limit import limiter, custom_rate_limit_handler
from app.middleware.security_headers import SecurityHeadersMiddleware
from app.middleware.validation import InputValidationMiddleware
from app.routers import auth, assessments, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("[START] Starting KiranaLens API...")
    
    # Configure structured logging
    configure_logging()
    
    # Test database connection (optional for development)
    try:
        await test_db_connection()
        print("[OK] Database connection successful")
    except Exception as e:
        print(f"[WARN] Database connection failed: {e}")
        print("[INFO] Continuing without database for development...")
    
    yield
    
    # Shutdown
    print("[STOP] Shutting down KiranaLens API...")
    try:
        await engine.dispose()
    except Exception as e:
        print(f"[WARN] Error during engine disposal: {e}")


# Create FastAPI application
app = FastAPI(
    title="KiranaLens API",
    version="1.0.0",
    description="AI-powered kirana store cash flow underwriting platform",
    lifespan=lifespan,
)

# Add rate limiter state
app.state.limiter = limiter

# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with request ID"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "request_id": request_id
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with detailed field information"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Format validation errors
    errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field_path,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors,
            "request_id": request_id
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors without exposing sensitive information"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Log the full error for debugging
    import structlog
    logger = structlog.get_logger("kiranalens.database")
    logger.error(
        "Database error occurred",
        request_id=request_id,
        error=str(exc),
        exc_info=True
    )
    
    # Return generic error to client
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred",
            "request_id": request_id
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    # Log the full error for debugging
    import structlog
    logger = structlog.get_logger("kiranalens.errors")
    logger.error(
        "Unhandled exception occurred",
        request_id=request_id,
        error=str(exc),
        exc_info=True
    )
    
    # Return generic error to client (never expose stack traces in production)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "request_id": request_id
        }
    )


# Rate limit exception handler
app.add_exception_handler(RateLimitExceeded, custom_rate_limit_handler)

# Add middleware in correct order (order matters!)
# 1. Security headers (outermost)
app.add_middleware(SecurityHeadersMiddleware)

# 2. Request logging (must wrap rate limiter to capture 429s)
app.add_middleware(RequestLoggingMiddleware)

# 3. Input validation
app.add_middleware(InputValidationMiddleware)

# 4. GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 5. CORS (innermost, closest to routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"] + (settings.ALLOWED_ORIGINS if settings.ALLOWED_ORIGINS != ["http://localhost:3000"] else []),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],  # Allow all headers for development
    expose_headers=["*"],
)

# Mount routers under /api/v1 prefix
app.include_router(auth.router, prefix="/api/v1")
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["Assessments"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])


@app.get("/")
async def root():
    """API information endpoint"""
    return {
        "name": "KiranaLens API",
        "version": "1.0.0",
        "description": "AI-powered kirana store cash flow underwriting platform",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint.
    
    Returns:
        dict: Health status with detailed checks
    """
    health_status = {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "db_connected": False,
        "checks": {
            "database": "unknown",
            "storage": "unknown"
        }
    }
    
    # Test database connection
    try:
        from app.database import engine
        from sqlalchemy import text
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        health_status["db_connected"] = True
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"error: {str(e)}"
    
    # Test Supabase storage connection
    try:
        from app.services.storage_service import StorageService
        storage_service = StorageService()
        
        # Try to list buckets (simple connectivity test)
        response = storage_service.supabase.storage.list_buckets()
        if response:
            health_status["checks"]["storage"] = "healthy"
        else:
            health_status["checks"]["storage"] = "error: unable to list buckets"
    except Exception as e:
        health_status["checks"]["storage"] = f"error: {str(e)}"
    
    # Determine overall status — DB is the critical dependency; storage is optional
    if health_status["db_connected"]:
        health_status["status"] = "ok"
    else:
        health_status["status"] = "unhealthy"
    
    # Return 200 as long as DB is up; only 503 if DB is completely down
    status_code = 200 if health_status["db_connected"] else 503
    
    return JSONResponse(
        status_code=status_code,
        content=health_status
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )

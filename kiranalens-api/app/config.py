"""
Application configuration using Pydantic Settings
"""
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database
    DATABASE_URL: str = Field(
        ...,
        description="PostgreSQL database URL with asyncpg driver"
    )
    
    # Security
    SECRET_KEY: str = Field(
        ...,
        description="Secret key for JWT token generation"
    )
    ALGORITHM: str = Field(
        default="HS256",
        description="JWT algorithm"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60,
        description="Access token expiration time in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    
    # AI Services
    AI_PROVIDER: str = Field(
        default="groq",
        description="AI provider to use (groq, openai, anthropic)"
    )
    GROQ_API_KEY: str = Field(
        default="",
        description="Groq API key for Llama models"
    )
    OPENAI_API_KEY: str = Field(
        default="",
        description="OpenAI API key for GPT models"
    )
    ANTHROPIC_API_KEY: str = Field(
        default="",
        description="Anthropic API key for Claude"
    )
    
    # Google Maps
    GOOGLE_MAPS_API_KEY: str = Field(
        default="",
        description="Google Maps API key for geocoding"
    )
    
    # OpenStreetMap Nominatim (Free alternative)
    USE_NOMINATIM: bool = Field(
        default=True,
        description="Use OpenStreetMap Nominatim instead of Google Maps (free)"
    )
    
    # Supabase Storage
    SUPABASE_URL: str = Field(
        ...,
        description="Supabase project URL"
    )
    SUPABASE_KEY: str = Field(
        ...,
        description="Supabase anon/service key"
    )
    SUPABASE_BUCKET: str = Field(
        default="kirana-images",
        description="Supabase storage bucket name"
    )
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins"
    )
    
    # File Upload
    MAX_IMAGE_SIZE_MB: int = Field(
        default=10,
        description="Maximum image size in MB"
    )
    MIN_IMAGES: int = Field(
        default=3,
        description="Minimum number of images required"
    )
    MAX_IMAGES: int = Field(
        default=5,
        description="Maximum number of images allowed"
    )
    
    # Environment
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment name (development, staging, production)"
    )
    
    # Internal API Key for admin operations
    INTERNAL_API_KEY: str = Field(
        ...,
        description="Internal API key for admin operations"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create global settings instance
settings = Settings()

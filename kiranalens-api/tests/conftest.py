"""
Test configuration and shared fixtures for KiranaLens test suite.

Sets dummy environment variables before any imports so that pydantic-settings
does not raise validation errors for required fields that are not needed for
pure unit/integration tests of the utility modules.
"""
import os

# Provide stub values for required settings so app.config.Settings can be
# instantiated without a real .env file. These are never used during the
# utility unit tests but must be present for the import chain to succeed.
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-unit-tests-only")
os.environ.setdefault("SUPABASE_URL", "https://example.supabase.co")
os.environ.setdefault("SUPABASE_KEY", "test-supabase-key")
os.environ.setdefault("INTERNAL_API_KEY", "test-internal-api-key")

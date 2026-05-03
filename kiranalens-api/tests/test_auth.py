"""
Authentication tests
"""
import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest
from app.services.auth_service import AuthService
from main import app

client = TestClient(app)


class TestAuthService:
    """Test AuthService methods"""
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        
        assert hashed != password
        assert AuthService.verify_password(password, hashed)
        assert not AuthService.verify_password("wrongpassword", hashed)
    
    def test_create_access_token(self):
        """Test access token creation"""
        data = {"sub": "test-user-id", "email": "test@example.com"}
        token = AuthService.create_access_token(data)
        
        # Decode token to verify
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        assert payload["sub"] == "test-user-id"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
        assert "exp" in payload
    
    def test_create_refresh_token(self):
        """Test refresh token creation"""
        data = {"sub": "test-user-id", "email": "test@example.com"}
        token = AuthService.create_refresh_token(data)
        
        # Decode token to verify
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        assert payload["sub"] == "test-user-id"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "refresh"
        assert "exp" in payload
    
    def test_decode_valid_token(self):
        """Test decoding valid token"""
        data = {"sub": "test-user-id", "email": "test@example.com"}
        token = AuthService.create_access_token(data)
        
        payload = AuthService.decode_token(token)
        
        assert payload["sub"] == "test-user-id"
        assert payload["email"] == "test@example.com"
    
    def test_decode_invalid_token(self):
        """Test decoding invalid token raises exception"""
        with pytest.raises(Exception):  # Should raise HTTPException
            AuthService.decode_token("invalid-token")
    
    def test_decode_expired_token(self):
        """Test decoding expired token raises exception"""
        # Create token that expires immediately
        data = {"sub": "test-user-id", "exp": datetime.utcnow() - timedelta(minutes=1)}
        expired_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        with pytest.raises(Exception):  # Should raise HTTPException
            AuthService.decode_token(expired_token)


class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_register_success(self):
        """Test successful user registration"""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "organisation": "Test Org",
            "password": "testpassword123",
            "role": "credit_officer"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"
        assert data["organisation"] == "Test Org"
        assert data["role"] == "credit_officer"
        assert "id" in data
        assert "created_at" in data
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email returns 409"""
        user_data = {
            "name": "Test User",
            "email": "duplicate@example.com",
            "password": "testpassword123",
            "role": "credit_officer"
        }
        
        # First registration should succeed
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same email should fail
        response2 = client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 409
        assert "Email already registered" in response2.json()["detail"]
    
    def test_register_invalid_data(self):
        """Test registration with invalid data returns 422"""
        # Missing required fields
        response = client.post("/api/v1/auth/register", json={})
        assert response.status_code == 422
        
        # Invalid email
        user_data = {
            "name": "Test User",
            "email": "invalid-email",
            "password": "testpassword123"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
        
        # Password too short
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "short"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422
    
    def test_login_success(self):
        """Test successful login"""
        # First register a user
        user_data = {
            "name": "Login Test User",
            "email": "login@example.com",
            "password": "testpassword123",
            "role": "credit_officer"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Then login
        login_data = {
            "email": "login@example.com",
            "password": "testpassword123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == "login@example.com"
    
    def test_login_wrong_password(self):
        """Test login with wrong password returns 401"""
        # First register a user
        user_data = {
            "name": "Wrong Password User",
            "email": "wrongpass@example.com",
            "password": "correctpassword123",
            "role": "credit_officer"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Try login with wrong password
        login_data = {
            "email": "wrongpass@example.com",
            "password": "wrongpassword123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self):
        """Test login with non-existent user returns 401"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "testpassword123"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        assert "Incorrect email or password" in response.json()["detail"]
    
    def test_oauth2_login_success(self):
        """Test OAuth2 compatible login endpoint"""
        # First register a user
        user_data = {
            "name": "OAuth2 Test User",
            "email": "oauth2@example.com",
            "password": "testpassword123",
            "role": "credit_officer"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Login using OAuth2 form data
        form_data = {
            "username": "oauth2@example.com",  # OAuth2 uses 'username' field
            "password": "testpassword123"
        }
        response = client.post("/api/v1/auth/token", data=form_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    def test_refresh_token_success(self):
        """Test successful token refresh"""
        # Register and login to get tokens
        user_data = {
            "name": "Refresh Test User",
            "email": "refresh@example.com",
            "password": "testpassword123",
            "role": "credit_officer"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": "refresh@example.com",
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        refresh_token = login_response.json()["refresh_token"]
        
        # Use refresh token to get new access token
        refresh_data = {"refresh_token": refresh_token}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_refresh_token_invalid(self):
        """Test refresh with invalid token returns 401"""
        refresh_data = {"refresh_token": "invalid-refresh-token"}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
    
    def test_refresh_token_wrong_type(self):
        """Test refresh with access token (wrong type) returns 401"""
        # Register and login to get tokens
        user_data = {
            "name": "Wrong Type Test User",
            "email": "wrongtype@example.com",
            "password": "testpassword123",
            "role": "credit_officer"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": "wrongtype@example.com",
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Try to use access token as refresh token
        refresh_data = {"refresh_token": access_token}
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        assert response.status_code == 401
        assert "Invalid token type" in response.json()["detail"]
    
    def test_get_current_user_success(self):
        """Test getting current user info with valid token"""
        # Register and login to get token
        user_data = {
            "name": "Current User Test",
            "email": "current@example.com",
            "password": "testpassword123",
            "role": "branch_manager"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": "current@example.com",
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Get current user info
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "current@example.com"
        assert data["name"] == "Current User Test"
        assert data["role"] == "branch_manager"
    
    def test_get_current_user_no_token(self):
        """Test getting current user without token returns 401"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self):
        """Test getting current user with invalid token returns 401"""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_get_current_user_expired_token(self):
        """Test getting current user with expired token returns 401"""
        # Create expired token
        data = {"sub": "test-user-id", "exp": datetime.utcnow() - timedelta(minutes=1)}
        expired_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/v1/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_logout_success(self):
        """Test successful logout"""
        # Register and login to get token
        user_data = {
            "name": "Logout Test User",
            "email": "logout@example.com",
            "password": "testpassword123",
            "role": "credit_officer"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        login_data = {
            "email": "logout@example.com",
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/auth/login", json=login_data)
        access_token = login_response.json()["access_token"]
        
        # Logout
        headers = {"Authorization": f"Bearer {access_token}"}
        response = client.post("/api/v1/auth/logout", headers=headers)
        
        assert response.status_code == 200
        assert "Logged out successfully" in response.json()["message"]
    
    def test_logout_no_token(self):
        """Test logout without token returns 401"""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 401


# Fixtures for database testing (if using a test database)
@pytest.fixture
async def test_user(db_session: AsyncSession):
    """Create a test user"""
    user_data = RegisterRequest(
        name="Test User",
        email="testuser@example.com",
        password="testpassword123",
        role=UserRole.CREDIT_OFFICER
    )
    
    user = await AuthService.register_user(db_session, user_data)
    return user


@pytest.fixture
def auth_headers(test_user: User):
    """Create authorization headers for test user"""
    token_data = {"sub": str(test_user.id), "email": test_user.email}
    access_token = AuthService.create_access_token(token_data)
    return {"Authorization": f"Bearer {access_token}"}


class TestAuthIntegration:
    """Integration tests with database"""
    
    @pytest.mark.asyncio
    async def test_register_user_database(self, db_session: AsyncSession):
        """Test user registration creates database record"""
        request = RegisterRequest(
            name="DB Test User",
            email="dbtest@example.com",
            password="testpassword123",
            role=UserRole.ADMIN
        )
        
        user = await AuthService.register_user(db_session, request)
        
        assert user.id is not None
        assert user.email == "dbtest@example.com"
        assert user.name == "DB Test User"
        assert user.role == UserRole.ADMIN
        assert user.is_active is True
        assert user.created_at is not None
        assert user.last_login is None
        
        # Verify password is hashed
        assert user.hashed_password != "testpassword123"
        assert AuthService.verify_password("testpassword123", user.hashed_password)
    
    @pytest.mark.asyncio
    async def test_login_updates_last_login(self, db_session: AsyncSession):
        """Test login updates last_login timestamp"""
        # Register user
        request = RegisterRequest(
            name="Login Time Test",
            email="logintime@example.com",
            password="testpassword123",
            role=UserRole.CREDIT_OFFICER
        )
        user = await AuthService.register_user(db_session, request)
        
        # Verify last_login is initially None
        assert user.last_login is None
        
        # Login
        token_response = await AuthService.login_user(
            db_session, "logintime@example.com", "testpassword123"
        )
        
        # Refresh user from database
        await db_session.refresh(user)
        
        # Verify last_login is updated
        assert user.last_login is not None
        assert isinstance(user.last_login, datetime)
        
        # Verify token response
        assert token_response.access_token is not None
        assert token_response.refresh_token is not None
        assert token_response.user.email == "logintime@example.com"
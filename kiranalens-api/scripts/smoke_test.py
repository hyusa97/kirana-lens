#!/usr/bin/env python3
"""
Smoke test script for KiranaLens API

Runs sequential HTTP tests to verify core API functionality:
- Health check
- User registration and login
- Authentication verification
- Assessment retrieval
- Error handling

Usage:
    python scripts/smoke_test.py
"""
import asyncio
import sys
from pathlib import Path
from typing import Dict, Optional
from uuid import uuid4

import httpx
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_EMAIL = f"smoketest_{uuid4().hex[:8]}@test.com"
TEST_USER_PASSWORD = "SmokeTest@123"
TIMEOUT = 30.0


class SmokeTestRunner:
    """Smoke test runner with colored output"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.access_token: Optional[str] = None
        self.demo_assessment_id: Optional[str] = None
    
    def print_test_result(self, test_name: str, passed: bool, details: str = ""):
        """Print colored test result"""
        if passed:
            print(f"{Fore.GREEN}[PASS]{Style.RESET_ALL} {test_name}")
            if details:
                print(f"       {Fore.CYAN}{details}{Style.RESET_ALL}")
            self.passed += 1
        else:
            print(f"{Fore.RED}[FAIL]{Style.RESET_ALL} {test_name}")
            if details:
                print(f"       {Fore.YELLOW}{details}{Style.RESET_ALL}")
            self.failed += 1
    
    def print_summary(self):
        """Print final test summary"""
        total = self.passed + self.failed
        if self.failed == 0:
            color = Fore.GREEN
            status = "ALL TESTS PASSED! 🎉"
        else:
            color = Fore.RED
            status = "SOME TESTS FAILED ❌"
        
        print(f"\n{color}{'='*50}{Style.RESET_ALL}")
        print(f"{color}{status}{Style.RESET_ALL}")
        print(f"{color}{self.passed}/{total} tests passed{Style.RESET_ALL}")
        print(f"{color}{'='*50}{Style.RESET_ALL}")
    
    async def test_health_check(self, client: httpx.AsyncClient):
        """Test GET /health"""
        try:
            response = await client.get(f"{BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    self.print_test_result(
                        "GET /health → 200, status='ok'", 
                        True, 
                        f"Status: {data.get('status')}, DB: {data.get('db_connected', 'unknown')}"
                    )
                else:
                    self.print_test_result(
                        "GET /health → 200, status='ok'", 
                        False, 
                        f"Expected status='ok', got '{data.get('status')}'"
                    )
            else:
                self.print_test_result(
                    "GET /health → 200, status='ok'", 
                    False, 
                    f"Expected 200, got {response.status_code}"
                )
        except Exception as e:
            self.print_test_result(
                "GET /health → 200, status='ok'", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_user_registration(self, client: httpx.AsyncClient):
        """Test POST /api/v1/auth/register"""
        try:
            payload = {
                "name": "Smoke Test User",
                "email": TEST_USER_EMAIL,
                "organisation": "Test Org",
                "password": TEST_USER_PASSWORD,
                "role": "credit_officer"
            }
            
            response = await client.post(f"{BASE_URL}/api/v1/auth/register", json=payload)
            
            if response.status_code == 201:
                data = response.json()
                if data.get("email") == TEST_USER_EMAIL:
                    self.print_test_result(
                        "POST /api/v1/auth/register → 201", 
                        True, 
                        f"Created user: {data.get('email')}"
                    )
                else:
                    self.print_test_result(
                        "POST /api/v1/auth/register → 201", 
                        False, 
                        f"Email mismatch: expected {TEST_USER_EMAIL}, got {data.get('email')}"
                    )
            else:
                error_detail = response.json().get("detail", "Unknown error") if response.status_code != 500 else "Server error"
                self.print_test_result(
                    "POST /api/v1/auth/register → 201", 
                    False, 
                    f"Expected 201, got {response.status_code}: {error_detail}"
                )
        except Exception as e:
            self.print_test_result(
                "POST /api/v1/auth/register → 201", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_user_login(self, client: httpx.AsyncClient):
        """Test POST /api/v1/auth/login"""
        try:
            payload = {
                "email": TEST_USER_EMAIL,
                "password": TEST_USER_PASSWORD
            }
            
            response = await client.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access_token")
                if access_token:
                    self.access_token = access_token
                    self.print_test_result(
                        "POST /api/v1/auth/login → 200, has access_token", 
                        True, 
                        f"Token type: {data.get('token_type', 'unknown')}"
                    )
                else:
                    self.print_test_result(
                        "POST /api/v1/auth/login → 200, has access_token", 
                        False, 
                        "No access_token in response"
                    )
            else:
                error_detail = response.json().get("detail", "Unknown error") if response.status_code != 500 else "Server error"
                self.print_test_result(
                    "POST /api/v1/auth/login → 200, has access_token", 
                    False, 
                    f"Expected 200, got {response.status_code}: {error_detail}"
                )
        except Exception as e:
            self.print_test_result(
                "POST /api/v1/auth/login → 200, has access_token", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_get_current_user(self, client: httpx.AsyncClient):
        """Test GET /api/v1/auth/me"""
        if not self.access_token:
            self.print_test_result(
                "GET /api/v1/auth/me → 200, correct email", 
                False, 
                "No access token available"
            )
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await client.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("email") == TEST_USER_EMAIL:
                    self.print_test_result(
                        "GET /api/v1/auth/me → 200, correct email", 
                        True, 
                        f"User: {data.get('name')} ({data.get('role')})"
                    )
                else:
                    self.print_test_result(
                        "GET /api/v1/auth/me → 200, correct email", 
                        False, 
                        f"Email mismatch: expected {TEST_USER_EMAIL}, got {data.get('email')}"
                    )
            else:
                error_detail = response.json().get("detail", "Unknown error") if response.status_code != 500 else "Server error"
                self.print_test_result(
                    "GET /api/v1/auth/me → 200, correct email", 
                    False, 
                    f"Expected 200, got {response.status_code}: {error_detail}"
                )
        except Exception as e:
            self.print_test_result(
                "GET /api/v1/auth/me → 200, correct email", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_get_assessments(self, client: httpx.AsyncClient):
        """Test GET /api/v1/assessments"""
        if not self.access_token:
            self.print_test_result(
                "GET /api/v1/assessments → 200, list with total", 
                False, 
                "No access token available"
            )
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await client.get(f"{BASE_URL}/api/v1/assessments", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if "items" in data and "total" in data:
                    # Try to find a demo assessment for next test
                    items = data.get("items", [])
                    for item in items:
                        if item.get("store_name") == "Sharma General Store":
                            self.demo_assessment_id = item.get("id")
                            break
                    
                    self.print_test_result(
                        "GET /api/v1/assessments → 200, list with total", 
                        True, 
                        f"Found {data.get('total', 0)} assessments"
                    )
                else:
                    self.print_test_result(
                        "GET /api/v1/assessments → 200, list with total", 
                        False, 
                        "Missing 'items' or 'total' in response"
                    )
            else:
                error_detail = response.json().get("detail", "Unknown error") if response.status_code != 500 else "Server error"
                self.print_test_result(
                    "GET /api/v1/assessments → 200, list with total", 
                    False, 
                    f"Expected 200, got {response.status_code}: {error_detail}"
                )
        except Exception as e:
            self.print_test_result(
                "GET /api/v1/assessments → 200, list with total", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_get_specific_assessment(self, client: httpx.AsyncClient):
        """Test GET /api/v1/assessments/{demo_id_1}"""
        if not self.access_token:
            self.print_test_result(
                "GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1", 
                False, 
                "No access token available"
            )
            return
        
        if not self.demo_assessment_id:
            self.print_test_result(
                "GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1", 
                False, 
                "No demo assessment ID found (run seed_demo_data.py first)"
            )
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await client.get(
                f"{BASE_URL}/api/v1/assessments/{self.demo_assessment_id}", 
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                csqs = float(data.get("csqs", 0))
                if abs(csqs - 82.1) < 0.1:  # Allow small floating point differences
                    self.print_test_result(
                        "GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1", 
                        True, 
                        f"CSQS: {csqs}, Store: {data.get('store_name')}"
                    )
                else:
                    self.print_test_result(
                        "GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1", 
                        False, 
                        f"Expected CSQS ~82.1, got {csqs}"
                    )
            else:
                error_detail = response.json().get("detail", "Unknown error") if response.status_code != 500 else "Server error"
                self.print_test_result(
                    "GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1", 
                    False, 
                    f"Expected 200, got {response.status_code}: {error_detail}"
                )
        except Exception as e:
            self.print_test_result(
                "GET /api/v1/assessments/{demo_id_1} → 200, csqs=82.1", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_get_assessment_status(self, client: httpx.AsyncClient):
        """Test GET /api/v1/assessments/{demo_id_1}/status"""
        if not self.access_token:
            self.print_test_result(
                "GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'", 
                False, 
                "No access token available"
            )
            return
        
        if not self.demo_assessment_id:
            self.print_test_result(
                "GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'", 
                False, 
                "No demo assessment ID found"
            )
            return
        
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = await client.get(
                f"{BASE_URL}/api/v1/assessments/{self.demo_assessment_id}/status", 
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "complete":
                    self.print_test_result(
                        "GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'", 
                        True, 
                        f"Status: {data.get('status')}"
                    )
                else:
                    self.print_test_result(
                        "GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'", 
                        False, 
                        f"Expected status='complete', got '{data.get('status')}'"
                    )
            else:
                error_detail = response.json().get("detail", "Unknown error") if response.status_code != 500 else "Server error"
                self.print_test_result(
                    "GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'", 
                    False, 
                    f"Expected 200, got {response.status_code}: {error_detail}"
                )
        except Exception as e:
            self.print_test_result(
                "GET /api/v1/assessments/{demo_id_1}/status → 200, status='complete'", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_login_wrong_password(self, client: httpx.AsyncClient):
        """Test POST /api/v1/auth/login (wrong password)"""
        try:
            payload = {
                "email": TEST_USER_EMAIL,
                "password": "WrongPassword123"
            }
            
            response = await client.post(f"{BASE_URL}/api/v1/auth/login", json=payload)
            
            if response.status_code == 401:
                self.print_test_result(
                    "POST /api/v1/auth/login (wrong password) → 401", 
                    True, 
                    "Correctly rejected invalid credentials"
                )
            else:
                self.print_test_result(
                    "POST /api/v1/auth/login (wrong password) → 401", 
                    False, 
                    f"Expected 401, got {response.status_code}"
                )
        except Exception as e:
            self.print_test_result(
                "POST /api/v1/auth/login (wrong password) → 401", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def test_get_assessments_no_token(self, client: httpx.AsyncClient):
        """Test GET /api/v1/assessments (no token)"""
        try:
            response = await client.get(f"{BASE_URL}/api/v1/assessments")
            
            if response.status_code == 401:
                self.print_test_result(
                    "GET /api/v1/assessments (no token) → 401", 
                    True, 
                    "Correctly rejected unauthenticated request"
                )
            else:
                self.print_test_result(
                    "GET /api/v1/assessments (no token) → 401", 
                    False, 
                    f"Expected 401, got {response.status_code}"
                )
        except Exception as e:
            self.print_test_result(
                "GET /api/v1/assessments (no token) → 401", 
                False, 
                f"Exception: {str(e)}"
            )
    
    async def run_all_tests(self):
        """Run all smoke tests"""
        print(f"{Fore.CYAN}🧪 Starting KiranaLens API Smoke Tests{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Target: {BASE_URL}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}\n")
        
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Run tests in sequence
            await self.test_health_check(client)
            await self.test_user_registration(client)
            await self.test_user_login(client)
            await self.test_get_current_user(client)
            await self.test_get_assessments(client)
            await self.test_get_specific_assessment(client)
            await self.test_get_assessment_status(client)
            await self.test_login_wrong_password(client)
            await self.test_get_assessments_no_token(client)
        
        # Print summary
        self.print_summary()
        
        # Return exit code
        return 0 if self.failed == 0 else 1


async def main():
    """Main function"""
    try:
        runner = SmokeTestRunner()
        exit_code = await runner.run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrupted by user{Style.RESET_ALL}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    # Check if colorama is available
    try:
        import colorama
    except ImportError:
        print("Installing colorama for colored output...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
        import colorama
        colorama.init(autoreset=True)
    
    # Check if httpx is available
    try:
        import httpx
    except ImportError:
        print("Installing httpx for HTTP client...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "httpx"])
        import httpx
    
    asyncio.run(main())
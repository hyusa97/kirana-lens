#!/usr/bin/env python3
"""
Comprehensive API Testing Script for KiranaLens
Tests all major endpoints and functionality
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = 'http://localhost:8000'
API_URL = f'{BASE_URL}/api/v1'

# ANSI color codes for pretty output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    print(f"{RED}❌ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ️  {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠️  {message}{RESET}")

def print_header(message):
    print(f"\n{BLUE}{'='*60}")
    print(f"  {message}")
    print(f"{'='*60}{RESET}\n")

# Test results tracking
tests_passed = 0
tests_failed = 0

def run_test(test_name, test_func):
    """Run a test and track results"""
    global tests_passed, tests_failed
    try:
        print_info(f"Running: {test_name}")
        test_func()
        tests_passed += 1
        print_success(f"PASSED: {test_name}\n")
    except AssertionError as e:
        tests_failed += 1
        print_error(f"FAILED: {test_name}")
        print_error(f"Reason: {str(e)}\n")
    except Exception as e:
        tests_failed += 1
        print_error(f"ERROR: {test_name}")
        print_error(f"Exception: {str(e)}\n")

# Global token storage
auth_token = None
test_assessment_id = None

def test_health_check():
    """Test API health endpoint"""
    response = requests.get(f'{BASE_URL}/health')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    print(f"   Status: {data['status']}")
    print(f"   Database: {data['checks']['database']}")
    print(f"   Storage: {data['checks']['storage']}")
    
    assert data['status'] in ['ok', 'unhealthy'], "Invalid status"
    assert data['db_connected'] == True, "Database not connected"

def test_login():
    """Test user login"""
    global auth_token
    
    response = requests.post(f'{API_URL}/auth/login', json={
        'email': 'demo@kiranalens.com',
        'password': 'Demo@1234'
    })
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert 'access_token' in data, "No access token in response"
    assert 'user' in data, "No user data in response"
    
    auth_token = data['access_token']
    user = data['user']
    
    print(f"   User: {user['name']}")
    print(f"   Email: {user['email']}")
    print(f"   Role: {user['role']}")
    print(f"   Token: {auth_token[:30]}...")

def test_get_current_user():
    """Test getting current user info"""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    response = requests.get(f'{API_URL}/auth/me', headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    user = response.json()
    print(f"   Name: {user['name']}")
    print(f"   Organisation: {user.get('organisation', 'N/A')}")

def test_get_assessments():
    """Test fetching all assessments"""
    global test_assessment_id
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    response = requests.get(f'{API_URL}/assessments', headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert 'items' in data, "No items in response"
    assert 'total' in data, "No total in response"
    
    print(f"   Total assessments: {data['total']}")
    print(f"   Items in page: {len(data['items'])}")
    print(f"   Current page: {data['page']}")
    print(f"   Total pages: {data['pages']}")
    
    if data['items']:
        test_assessment_id = data['items'][0]['id']
        print(f"   First assessment: {data['items'][0]['store_name']}")

def test_get_single_assessment():
    """Test fetching a single assessment"""
    if not test_assessment_id:
        print_warning("Skipping: No assessment ID available")
        return
    
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    response = requests.get(f'{API_URL}/assessments/{test_assessment_id}', headers=headers)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    assessment = response.json()
    print(f"   Store: {assessment['store_name']}")
    print(f"   Address: {assessment['address']}")
    print(f"   CSQS: {assessment['csqs']}")
    print(f"   Tier: {assessment['store_tier']}")
    print(f"   Recommendation: {assessment['recommendation']}")
    print(f"   Status: {assessment['status']}")

def test_filter_by_recommendation():
    """Test filtering assessments by recommendation"""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    for recommendation in ['pre_approve', 'needs_verification', 'reject']:
        response = requests.get(
            f'{API_URL}/assessments',
            headers=headers,
            params={'recommendation': recommendation}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        print(f"   {recommendation}: {len(data['items'])} assessments")

def test_filter_by_tier():
    """Test filtering assessments by store tier"""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    for tier in ['A', 'B', 'C', 'D', 'E']:
        response = requests.get(
            f'{API_URL}/assessments',
            headers=headers,
            params={'store_tier': tier}
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        data = response.json()
        if data['items']:
            print(f"   Tier {tier}: {len(data['items'])} assessments")

def test_pagination():
    """Test assessment pagination"""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # Test page 1 with limit 2
    response = requests.get(
        f'{API_URL}/assessments',
        headers=headers,
        params={'page': 1, 'limit': 2}
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    print(f"   Page 1: {len(data['items'])} items (limit: 2)")
    print(f"   Total pages: {data['pages']}")

def test_unauthorized_access():
    """Test accessing protected endpoint without token"""
    response = requests.get(f'{API_URL}/assessments')
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print(f"   Correctly rejected unauthorized request")

def test_invalid_token():
    """Test accessing with invalid token"""
    headers = {'Authorization': 'Bearer invalid_token_here'}
    
    response = requests.get(f'{API_URL}/assessments', headers=headers)
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    print(f"   Correctly rejected invalid token")

def test_cors_headers():
    """Test CORS headers are present"""
    response = requests.options(f'{API_URL}/auth/login', headers={
        'Origin': 'http://localhost:3001',
        'Access-Control-Request-Method': 'POST'
    })
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    headers = response.headers
    assert 'access-control-allow-origin' in headers, "Missing CORS origin header"
    assert 'access-control-allow-methods' in headers, "Missing CORS methods header"
    
    print(f"   CORS Origin: {headers.get('access-control-allow-origin')}")
    print(f"   CORS Methods: {headers.get('access-control-allow-methods')}")

def test_rate_limiting():
    """Test rate limiting (informational only)"""
    headers = {'Authorization': f'Bearer {auth_token}'}
    
    # Make multiple requests quickly
    for i in range(5):
        response = requests.get(f'{API_URL}/assessments', headers=headers)
        if response.status_code == 429:
            print(f"   Rate limit hit after {i+1} requests")
            return
    
    print(f"   Made 5 requests without hitting rate limit")

def main():
    """Run all tests"""
    print_header("KiranaLens API Test Suite")
    print(f"Testing API at: {BASE_URL}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Test Suite
    run_test("Health Check", test_health_check)
    run_test("User Login", test_login)
    run_test("Get Current User", test_get_current_user)
    run_test("Get All Assessments", test_get_assessments)
    run_test("Get Single Assessment", test_get_single_assessment)
    run_test("Filter by Recommendation", test_filter_by_recommendation)
    run_test("Filter by Tier", test_filter_by_tier)
    run_test("Pagination", test_pagination)
    run_test("Unauthorized Access", test_unauthorized_access)
    run_test("Invalid Token", test_invalid_token)
    run_test("CORS Headers", test_cors_headers)
    run_test("Rate Limiting", test_rate_limiting)
    
    # Summary
    print_header("Test Summary")
    total_tests = tests_passed + tests_failed
    pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print_success(f"Passed: {tests_passed}")
    if tests_failed > 0:
        print_error(f"Failed: {tests_failed}")
    print(f"Pass Rate: {pass_rate:.1f}%\n")
    
    if tests_failed == 0:
        print_success("🎉 All tests passed!")
    else:
        print_warning(f"⚠️  {tests_failed} test(s) failed")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nTests interrupted by user")
    except Exception as e:
        print_error(f"\n\nUnexpected error: {str(e)}")

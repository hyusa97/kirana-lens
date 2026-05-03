"""
Quick test to verify Supabase storage is working with new credentials
"""
import requests
import json

# Test configuration
API_URL = "http://localhost:8000"
LOGIN_EMAIL = "demo@kiranalens.com"
LOGIN_PASSWORD = "Demo@1234"

def test_supabase_connection():
    """Test if we can create an assessment with Supabase storage"""
    
    print("=" * 60)
    print("SUPABASE STORAGE TEST")
    print("=" * 60)
    
    # Step 1: Login to get token
    print("\n1. Logging in...")
    login_response = requests.post(
        f"{API_URL}/api/v1/auth/login",
        json={
            "email": LOGIN_EMAIL,
            "password": LOGIN_PASSWORD
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return False
    
    token = login_response.json()["access_token"]
    print(f"✅ Login successful! Token: {token[:20]}...")
    
    # Step 2: Create a test image file
    print("\n2. Creating test image...")
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # Step 3: Try to create assessment
    print("\n3. Creating assessment with Supabase storage...")
    
    files = [
        ('files', ('test1.png', test_image_data, 'image/png')),
        ('files', ('test2.png', test_image_data, 'image/png')),
        ('files', ('test3.png', test_image_data, 'image/png')),
    ]
    
    data = {
        'lat': 28.6139,
        'lng': 77.2090,
        'store_name': 'Supabase Test Store',
        'gps_accuracy_metres': 10.0
    }
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/v1/assessments",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {response.text[:500]}")
        
        if response.status_code == 201:
            print("\n✅ SUCCESS! Assessment created with Supabase storage!")
            result = response.json()
            print(f"   Assessment ID: {result['id']}")
            print(f"   Status: {result['status']}")
            print(f"   Image URLs: {len(result.get('image_urls', []))} images uploaded")
            if result.get('image_urls'):
                print(f"   First image URL: {result['image_urls'][0][:80]}...")
            return True
        else:
            print(f"\n❌ FAILED! Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ SUPABASE STORAGE IS WORKING!")
        print("You can now create assessments through the UI.")
    else:
        print("❌ SUPABASE STORAGE TEST FAILED")
        print("Check the error messages above for details.")
    print("=" * 60)

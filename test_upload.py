import requests
import io

# Login first
login_response = requests.post('http://localhost:8000/api/v1/auth/login', json={
    'email': 'demo@kiranalens.com',
    'password': 'Demo@1234'
})
token = login_response.json()['access_token']
print(f"✅ Logged in, token: {token[:30]}...")

# Create a fake image file
fake_image = io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 1000)
fake_image.name = 'test.png'

# Try to create assessment
files = [
    ('images', ('test1.png', fake_image, 'image/png')),
    ('images', ('test2.png', io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 1000), 'image/png')),
    ('images', ('test3.png', io.BytesIO(b'\x89PNG\r\n\x1a\n' + b'\x00' * 1000), 'image/png')),
]

data = {
    'lat': '19.1136',
    'lng': '72.8697',
    'store_name': 'Test Store'
}

headers = {'Authorization': f'Bearer {token}'}

print("\n📤 Attempting to create assessment...")
try:
    response = requests.post(
        'http://localhost:8000/api/v1/assessments',
        files=files,
        data=data,
        headers=headers,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
except Exception as e:
    print(f"❌ Error: {e}")

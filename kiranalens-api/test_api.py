import requests

# Login
login_response = requests.post('http://localhost:8000/api/v1/auth/login', json={
    'email': 'demo@kiranalens.com',
    'password': 'Demo@1234'
})
token = login_response.json()['access_token']
print(f"Token: {token[:50]}...")

# Get assessments
assessments_response = requests.get(
    'http://localhost:8000/api/v1/assessments',
    headers={'Authorization': f'Bearer {token}'}
)
print(f"Status: {assessments_response.status_code}")
if assessments_response.status_code == 200:
    data = assessments_response.json()
    print(f"Items: {len(data.get('items', []))}")
    if data.get('items'):
        print(f"First assessment: {data['items'][0]['store_name']}")
else:
    print(f"Error: {assessments_response.text}")

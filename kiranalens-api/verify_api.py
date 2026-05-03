import urllib.request, json

# Login
req = urllib.request.Request(
    'http://localhost:8000/api/v1/auth/login',
    data=json.dumps({'email': 'demo@kiranalens.com', 'password': 'Demo@1234'}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read())
token = data['access_token']
print('Login OK, user:', data['user']['name'], '| role:', data['user']['role'])

# Get assessments
req2 = urllib.request.Request(
    'http://localhost:8000/api/v1/assessments',
    headers={'Authorization': 'Bearer ' + token}
)
resp2 = urllib.request.urlopen(req2)
data2 = json.loads(resp2.read())
print('Assessments total:', data2['total'])
for a in data2['items']:
    print('  -', a['store_name'], '| CSQS:', a['csqs'], '| Tier:', a['store_tier'], '| Rec:', a['recommendation'])

print('\nAll checks passed!')

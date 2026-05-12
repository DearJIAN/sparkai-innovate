import requests
import sys

BASE = 'http://127.0.0.1:5000'

# Login
r = requests.post(f'{BASE}/api/auth/login',
    json={'username': 'student1', 'password': '123456'},
    timeout=10)
print(f'Login: {r.status_code}')
if r.status_code != 200:
    print(f'Login failed: {r.text[:300]}')
    sys.exit(1)

data = r.json()
token = data.get('data', {}).get('token', '')
print(f'Token: {token[:30]}...')

# Test PDF download WITHOUT refresh first (use cached)
headers = {'Authorization': f'Bearer {token}'}
url = f'{BASE}/api/material-evaluation/reports/8/pdf?refresh=1'
print(f'\nGET {url}')
r2 = requests.get(url, headers=headers, timeout=120)
print(f'Status: {r2.status_code}')
print(f'Content-Type: {r2.headers.get("Content-Type", "")}')
print(f'Content-Length: {r2.headers.get("Content-Length", "N/A")}')

if r2.status_code == 200:
    print(f'PDF size: {len(r2.content)} bytes')
    with open('test_pdf_result.pdf', 'wb') as f:
        f.write(r2.content)
    print('Saved to test_pdf_result.pdf')
    if len(r2.content) > 5:
        print(f'PDF header (valid): {r2.content[:5]}')
else:
    print(f'Error body: {r2.text[:2000]}')
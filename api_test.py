import requests
import json
import os
import sys

BASE_URL = 'http://localhost:5000/api'
USERS = {
    'student': {'username': 'student1', 'password': 'student123'},
    'teacher': {'username': 'teacher1', 'password': 'teacher123'},
    'judge': {'username': 'judge1', 'password': 'judge123'},
    'admin': {'username': 'admin', 'password': 'admin123'}
}

tokens = {}
results = []

def record(role, feature, expected, actual, status):
    results.append({
        'Role': role,
        'Feature': feature,
        'Expected': expected,
        'Actual': actual,
        'Status': status
    })

def login():
    for role, creds in USERS.items():
        try:
            r = requests.post(f"{BASE_URL}/auth/login", json=creds, timeout=2)
            if r.status_code == 200:
                data = r.json()
                if data.get('code') == 200:
                    tokens[role] = data['data']['token']
                    record(role, 'Login', '200 OK', '200 OK', 'PASS')
                else:
                    record(role, 'Login', '200 OK', f"Failed: {data.get('message')}", 'FAIL')
            else:
                record(role, 'Login', '200 OK', f"HTTP {r.status_code}", 'FAIL')
        except Exception as e:
            record(role, 'Login', '200 OK', f"Exception: {str(e)}", 'FAIL')

def test_api():
    login()
    
    headers = lambda role: {'Authorization': f"Bearer {tokens.get(role, '')}"}
    
    # 1. Projects API
    for role in USERS.keys():
        if role not in tokens: continue
        r = requests.get(f"{BASE_URL}/projects", headers=headers(role))
        if r.status_code == 200 and r.json().get('code') == 200:
            count = len(r.json().get('data', {}).get('list', []))
            record(role, 'GET /projects', '200 OK (Returns list)', f'200 OK ({count} items)', 'PASS')
        else:
            record(role, 'GET /projects', '200 OK', f'HTTP {r.status_code}', 'FAIL')
            
    # 2. Agent AI API Boundaries
    # Mock defense (should only work for student, teacher, admin)
    for role in USERS.keys():
        if role not in tokens: continue
        r = requests.post(f"{BASE_URL}/agent/mock-defense", json={"project_id": 1}, headers=headers(role))
        json_resp = r.json() if r.status_code == 200 else {}
        if role == 'judge':
            if json_resp.get('code') in (403, 401) or r.status_code == 403:
                record(role, 'Mock Defense (Unauthorized)', '403 Forbidden', 'Blocked correctly', 'PASS')
            else:
                record(role, 'Mock Defense (Unauthorized)', '403 Forbidden', f"Not blocked: {r.status_code} {json_resp.get('message')}", 'FAIL')
        else:
            if json_resp.get('code') == 200 or json_resp.get('code') == 404: # 404 means project not found, but access check passed
                record(role, 'Mock Defense (Authorized)', '200/404', f"Code: {json_resp.get('code')}", 'PASS')
            else:
                record(role, 'Mock Defense (Authorized)', '200/404', f"Code: {json_resp.get('code')} msg: {json_resp.get('message')}", 'FAIL')

    # Project Idea (should only work for student, admin)
    for role in USERS.keys():
        if role not in tokens: continue
        r = requests.post(f"{BASE_URL}/agent/project-idea", json={"industry": "AI"}, headers=headers(role))
        json_resp = r.json() if r.status_code == 200 else {}
        if role in ('teacher', 'judge'):
            if json_resp.get('code') in (403, 401) or r.status_code == 403:
                record(role, 'Project Idea (Unauthorized)', '403 Forbidden', 'Blocked correctly', 'PASS')
            else:
                record(role, 'Project Idea (Unauthorized)', '403 Forbidden', f"Not blocked: {r.status_code} {json_resp.get('message')}", 'FAIL')
        else:
            if json_resp.get('code') == 200:
                record(role, 'Project Idea (Authorized)', '200 OK', f"Code: {json_resp.get('code')}", 'PASS')
            else:
                record(role, 'Project Idea (Authorized)', '200 OK', f"Code: {json_resp.get('code')} msg: {json_resp.get('message')}", 'FAIL')

    # Review Assist (teacher, judge, admin)
    for role in USERS.keys():
        if role not in tokens: continue
        r = requests.post(f"{BASE_URL}/agent/review-assist", json={"project_id": 1}, headers=headers(role))
        json_resp = r.json() if r.status_code == 200 else {}
        if role == 'student':
            if json_resp.get('code') in (403, 401) or r.status_code == 403:
                record(role, 'Review Assist (Unauthorized)', '403 Forbidden', 'Blocked correctly', 'PASS')
            else:
                record(role, 'Review Assist (Unauthorized)', '403 Forbidden', f"Not blocked: {r.status_code} {json_resp.get('message')}", 'FAIL')
        else:
            # For authorized, it might be 404 (project missing) or 403 (project access denied for that specific user)
            # This is expected behavior for project_access check, so long as it's not the capability check blocking it
            if json_resp.get('message') != '评审辅助仅限教师、评委和管理员使用':
                record(role, 'Review Assist (Authorized)', 'Pass Capability Check', f"Msg: {json_resp.get('message', 'OK')}", 'PASS')
            else:
                record(role, 'Review Assist (Authorized)', 'Pass Capability Check', f"Blocked by capability check", 'FAIL')

    with open('test_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    test_api()

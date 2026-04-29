#!/usr/bin/env python3
"""
全链路 API 测试
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

results = []

def test(name, method, url, **kwargs):
    """测试单个接口"""
    try:
        res = method(f"{BASE_URL}{url}", **kwargs)
        ok = res.status_code in [200, 201]
        results.append((name, ok, res.status_code, res.json() if ok else None))
        print(f"{'✅' if ok else '❌'} {name} - {res.status_code}")
        return res
    except Exception as e:
        results.append((name, False, 0, str(e)))
        print(f"❌ {name} - ERROR: {e}")
        return None

def login(username, password):
    """登录获取 token"""
    res = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
    if res.status_code == 200:
        return res.json().get("data", {}).get("token")
    return None

print("=" * 60)
print("全链路 API 测试")
print("=" * 60)

# 1. 测试各角色登录
print("\n【1. 登录测试】")
admin_token = login("admin", "admin123")
student_token = login("student1", "student123")
teacher_token = login("teacher1", "teacher123")
judge_token = login("judge1", "judge123")

for name, token in [("admin", admin_token), ("student", student_token), ("teacher", teacher_token), ("judge", judge_token)]:
    print(f"{'✅' if token else '❌'} {name} 登录 - {'成功' if token else '失败'}")

# 2. 学生功能测试
print("\n【2. 学生功能测试】")
headers = {"Authorization": f"Bearer {student_token}"}
# 先获取项目列表，找到学生有权限的项目
res = requests.get(f"{BASE_URL}/projects", headers=headers)
if res.status_code == 200:
    projects = res.json().get("data", {}).get("projects", [])
    if projects:
        project_id = projects[0]["id"]
        test("获取项目列表", requests.get, "/projects", headers=headers)
        test("获取项目详情", requests.get, f"/projects/{project_id}", headers=headers)
        test("获取项目任务", requests.get, f"/projects/{project_id}/tasks", headers=headers)
        test("获取项目文件", requests.get, f"/projects/{project_id}/files", headers=headers)
        test("获取项目评审", requests.get, f"/projects/{project_id}/reviews", headers=headers)
    else:
        print("  学生没有项目，跳过项目相关测试")
else:
    test("获取项目列表", requests.get, "/projects", headers=headers)

# 3. 教师功能测试
print("\n【3. 教师功能测试】")
headers = {"Authorization": f"Bearer {teacher_token}"}
test("教师获取项目列表", requests.get, "/projects", headers=headers)

# 4. 评委功能测试
print("\n【4. 评委功能测试】")
headers = {"Authorization": f"Bearer {judge_token}"}
test("获取待评审项目", requests.get, "/reviews/projects", headers=headers)
test("获取项目评审详情", requests.get, "/reviews/projects/1", headers=headers)
test("获取我的评审记录", requests.get, "/reviews/my", headers=headers)

# 5. 管理员功能测试
print("\n【5. 管理员功能测试】")
headers = {"Authorization": f"Bearer {admin_token}"}
test("管理员看板统计", requests.get, "/dashboard/stats", headers=headers)
test("管理员最近数据", requests.get, "/dashboard/recent", headers=headers)
test("获取用户列表", requests.get, "/users", headers=headers)
test("获取比赛列表", requests.get, "/competitions", headers=headers)

# 6. AI 功能测试
print("\n【6. AI 功能测试】")
headers = {"Authorization": f"Bearer {student_token}"}
test("AI 生成项目简介", requests.post, "/ai/project-summary",
     headers={**headers, "Content-Type": "application/json"},
     json={"project_name": "测试项目", "description": "这是一个测试项目"})
test("AI 获取历史记录", requests.get, "/ai/records", headers=headers)

# 7. 权限测试
print("\n【7. 权限测试】")
# 学生访问管理员接口
headers = {"Authorization": f"Bearer {student_token}"}
res = requests.get(f"{BASE_URL}/dashboard/stats", headers=headers)
print(f"{'✅' if res.status_code == 403 else '❌'} 学生访问管理员接口 - {res.status_code} (期望 403)")

# 总结
print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)
passed = sum(1 for _, ok, _, _ in results if ok)
total = len(results)
print(f"通过: {passed}/{total}")
for name, ok, code, _ in results:
    if not ok:
        print(f"  ❌ {name} - {code}")

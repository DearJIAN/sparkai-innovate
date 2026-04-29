#!/usr/bin/env python3
"""
测试任务管理 API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

# 1. 登录
print("=" * 50)
print("1. 登录")
print("=" * 50)
login_res = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
login_data = login_res.json()
token = login_data.get("data", {}).get("token")
headers = {"Authorization": f"Bearer {token}"}
print(f"✅ 登录成功")

# 2. 获取项目列表
print("\n" + "=" * 50)
print("2. 获取项目列表")
print("=" * 50)
projects_res = requests.get(f"{BASE_URL}/projects", headers=headers)
projects = projects_res.json().get("data", {}).get("projects", [])
if not projects:
    print("❌ 没有项目")
    exit(1)
project_id = projects[0]["id"]
print(f"✅ 项目 ID: {project_id}")

# 3. 获取任务列表（应该为空）
print("\n" + "=" * 50)
print("3. 获取任务列表")
print("=" * 50)
tasks_res = requests.get(f"{BASE_URL}/projects/{project_id}/tasks", headers=headers)
tasks_data = tasks_res.json()
print(f"状态码: {tasks_res.status_code}")
print(f"统计: {json.dumps(tasks_data.get('data', {}).get('stats', {}), indent=2, ensure_ascii=False)}")

# 4. 创建任务
print("\n" + "=" * 50)
print("4. 创建任务")
print("=" * 50)
create_res = requests.post(
    f"{BASE_URL}/projects/{project_id}/tasks",
    headers={**headers, "Content-Type": "application/json"},
    json={
        "title": "完成项目需求分析",
        "description": "分析创新创业比赛的项目需求，确定核心功能模块",
        "priority": "high",
        "status": "doing"
    }
)
print(f"状态码: {create_res.status_code}")
create_data = create_res.json()
print(f"响应: {json.dumps(create_data, indent=2, ensure_ascii=False)}")
task_id = create_data.get("data", {}).get("task", {}).get("id")
print(f"✅ 任务创建成功，ID: {task_id}")

# 5. 再创建几个任务
print("\n" + "=" * 50)
print("5. 创建更多任务")
print("=" * 50)
for i, (title, status, priority) in enumerate([
    ("设计数据库模型", "done", "high"),
    ("实现后端 API", "doing", "high"),
    ("搭建前端框架", "todo", "medium"),
    ("编写测试用例", "todo", "low"),
]):
    res = requests.post(
        f"{BASE_URL}/projects/{project_id}/tasks",
        headers={**headers, "Content-Type": "application/json"},
        json={"title": title, "status": status, "priority": priority}
    )
    print(f"  任务 {i+1}: {title} - {res.status_code}")

# 6. 获取任务列表（应该有5个）
print("\n" + "=" * 50)
print("6. 获取任务列表（含统计）")
print("=" * 50)
tasks_res2 = requests.get(f"{BASE_URL}/projects/{project_id}/tasks", headers=headers)
tasks_data2 = tasks_res2.json()
print(f"状态码: {tasks_res2.status_code}")
print(f"统计: {json.dumps(tasks_data2.get('data', {}).get('stats', {}), indent=2, ensure_ascii=False)}")
print(f"任务数: {len(tasks_data2.get('data', {}).get('tasks', []))}")

# 7. 更新任务状态为 done
print("\n" + "=" * 50)
print("7. 更新任务状态为 done")
print("=" * 50)
update_res = requests.put(
    f"{BASE_URL}/tasks/{task_id}",
    headers={**headers, "Content-Type": "application/json"},
    json={"status": "done"}
)
print(f"状态码: {update_res.status_code}")
print(f"响应: {json.dumps(update_res.json(), indent=2, ensure_ascii=False)}")

# 8. 按状态筛选
print("\n" + "=" * 50)
print("8. 按状态筛选 (done)")
print("=" * 50)
filter_res = requests.get(f"{BASE_URL}/projects/{project_id}/tasks?status=done", headers=headers)
filter_data = filter_res.json()
print(f"状态码: {filter_res.status_code}")
print(f"已完成任务数: {len(filter_data.get('data', {}).get('tasks', []))}")

# 9. 删除一个任务
print("\n" + "=" * 50)
print("9. 删除任务")
print("=" * 50)
# 先获取一个任务ID
tasks = tasks_data2.get("data", {}).get("tasks", [])
if len(tasks) > 1:
    delete_id = tasks[1]["id"]
    delete_res = requests.delete(f"{BASE_URL}/tasks/{delete_id}", headers=headers)
    print(f"状态码: {delete_res.status_code}")
    print(f"响应: {json.dumps(delete_res.json(), indent=2, ensure_ascii=False)}")

# 10. 最终统计
print("\n" + "=" * 50)
print("10. 最终任务统计")
print("=" * 50)
final_res = requests.get(f"{BASE_URL}/projects/{project_id}/tasks", headers=headers)
final_data = final_res.json()
print(f"统计: {json.dumps(final_data.get('data', {}).get('stats', {}), indent=2, ensure_ascii=False)}")

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)

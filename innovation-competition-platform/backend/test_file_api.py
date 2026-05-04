#!/usr/bin/env python3
"""
测试文件上传下载 API
"""
import requests
import os
import json

BASE_URL = "http://127.0.0.1:5000/api"

# 1. 登录获取 token
print("=" * 50)
print("1. 登录获取 JWT Token")
print("=" * 50)
login_res = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "admin123"
})
print(f"状态码: {login_res.status_code}")
login_data = login_res.json()
print(f"响应: {json.dumps(login_data, indent=2, ensure_ascii=False)}")

token = login_data.get("data", {}).get("token")
if not token:
    print("❌ 登录失败，无法获取 token")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}
print(f"✅ 登录成功，获取到 token")

# 2. 获取项目列表
print("\n" + "=" * 50)
print("2. 获取项目列表")
print("=" * 50)
projects_res = requests.get(f"{BASE_URL}/projects", headers=headers)
print(f"状态码: {projects_res.status_code}")
projects_data = projects_res.json()
projects = projects_data.get("data", {}).get("projects", [])
print(f"项目数量: {len(projects)}")

if not projects:
    print("❌ 没有项目，无法测试文件上传")
    exit(1)

project = projects[0]
project_id = project["id"]
print(f"✅ 使用项目 ID: {project_id}, 名称: {project['name']}")

# 3. 获取项目文件列表（当前应该为空）
print("\n" + "=" * 50)
print("3. 获取项目文件列表")
print("=" * 50)
files_res = requests.get(f"{BASE_URL}/projects/{project_id}/files", headers=headers)
print(f"状态码: {files_res.status_code}")
files_data = files_res.json()
print(f"响应: {json.dumps(files_data, indent=2, ensure_ascii=False)}")

# 4. 创建一个测试文件并上传
print("\n" + "=" * 50)
print("4. 上传测试文件")
print("=" * 50)

# 创建测试文件
test_file_path = os.path.join(os.path.dirname(__file__), "test_upload.txt")
with open(test_file_path, "w", encoding="utf-8") as f:
    f.write("这是一个测试文件，用于测试项目材料上传功能。\n")
    f.write("项目名称: 火花智创 SparkAI Innovate\n")
    f.write("测试时间: 2026-04-29\n")

print(f"创建测试文件: {test_file_path}")

with open(test_file_path, "rb") as f:
    upload_res = requests.post(
        f"{BASE_URL}/projects/{project_id}/files",
        headers=headers,
        files={"file": ("测试文档.txt", f, "text/plain")},
        data={"material_type": "调研报告"}
    )

print(f"状态码: {upload_res.status_code}")
upload_data = upload_res.json()
print(f"响应: {json.dumps(upload_data, indent=2, ensure_ascii=False)}")

if upload_res.status_code == 201:
    print("✅ 文件上传成功")
    file_id = upload_data["data"]["file"]["id"]
else:
    print("❌ 文件上传失败")
    file_id = None

# 5. 再次获取文件列表
print("\n" + "=" * 50)
print("5. 再次获取项目文件列表")
print("=" * 50)
files_res2 = requests.get(f"{BASE_URL}/projects/{project_id}/files", headers=headers)
print(f"状态码: {files_res2.status_code}")
files_data2 = files_res2.json()
print(f"文件数量: {files_data2.get('data', {}).get('total', 0)}")
print(f"文件列表: {json.dumps(files_data2, indent=2, ensure_ascii=False)}")

# 6. 下载文件
if file_id:
    print("\n" + "=" * 50)
    print("6. 下载文件")
    print("=" * 50)
    download_res = requests.get(f"{BASE_URL}/files/{file_id}/download", headers=headers)
    print(f"状态码: {download_res.status_code}")
    print(f"Content-Type: {download_res.headers.get('Content-Type')}")
    print(f"Content-Disposition: {download_res.headers.get('Content-Disposition')}")
    print(f"文件大小: {len(download_res.content)} bytes")
    
    # 保存下载的文件
    download_path = os.path.join(os.path.dirname(__file__), "test_download.txt")
    with open(download_path, "wb") as f:
        f.write(download_res.content)
    print(f"✅ 文件已保存到: {download_path}")
    
    # 验证内容
    with open(download_path, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"文件内容:\n{content}")

# 7. 删除文件
if file_id:
    print("\n" + "=" * 50)
    print("7. 删除文件")
    print("=" * 50)
    delete_res = requests.delete(f"{BASE_URL}/files/{file_id}", headers=headers)
    print(f"状态码: {delete_res.status_code}")
    delete_data = delete_res.json()
    print(f"响应: {json.dumps(delete_data, indent=2, ensure_ascii=False)}")

# 8. 清理测试文件
print("\n" + "=" * 50)
print("8. 清理测试文件")
print("=" * 50)
for path in [test_file_path, download_path]:
    if os.path.exists(path):
        os.remove(path)
        print(f"✅ 已删除: {path}")

print("\n" + "=" * 50)
print("测试完成！")
print("=" * 50)

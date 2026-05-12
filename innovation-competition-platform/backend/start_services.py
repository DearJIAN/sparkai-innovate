import subprocess
import os
import time
import socket

backend_dir = r"E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\backend"
frontend_dir = r"E:\LEAR-CODE-NEW\软件工程\my-keshe\innovation-competition-platform\frontend"
python_exe = r"D:\TOOLS\anaconda\envs\newyolo\python.exe"

env = os.environ.copy()
env["FLASK_ENV"] = "development"
env["FLASK_APP"] = "app.py"
env["FLASK_DEBUG"] = "0"

DETACHED = 0x00000008 | 0x00000200

proc_backend = subprocess.Popen(
    [python_exe, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--no-debugger", "--no-reload"],
    cwd=backend_dir, env=env, creationflags=DETACHED, close_fds=True
)
print(f"Backend: PID {proc_backend.pid}")

proc_frontend = subprocess.Popen(
    ["cmd", "/c", "start", "npm", "run", "dev"],
    cwd=frontend_dir, creationflags=DETACHED, close_fds=True
)
print(f"Frontend: PID {proc_frontend.pid}")

time.sleep(8)

for name, port in [("Backend", 5000), ("Frontend", 5173)]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    r = s.connect_ex(('127.0.0.1', port))
    print(f"{name} port {port}: {'OPEN' if r == 0 else 'CLOSED'}")
    s.close()
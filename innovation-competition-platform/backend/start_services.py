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

DETACHED_PROCESS = 0x00000008
CREATE_NEW_PROCESS_GROUP = 0x00000200
flags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP

proc_backend = subprocess.Popen(
    [python_exe, "-m", "flask", "run", "--host=0.0.0.0", "--port=5000", "--no-debugger", "--no-reload"],
    cwd=backend_dir,
    env=env,
    creationflags=flags,
    close_fds=True
)

time.sleep(1)

proc_frontend = subprocess.Popen(
    ["cmd", "/c", "npm", "run", "dev"],
    cwd=frontend_dir,
    creationflags=flags,
    close_fds=True
)

print(f"Backend PID: {proc_backend.pid}")
print(f"Frontend PID: {proc_frontend.pid}")
time.sleep(5)

s = socket.socket()
try:
    s.settimeout(3)
    s.connect(("127.0.0.1", 5000))
    print("Port 5000: OPEN - Backend OK")
    s.close()
except Exception as e:
    print(f"Port 5000: CLOSED ({e})")

s2 = socket.socket()
try:
    s2.settimeout(3)
    s2.connect(("127.0.0.1", 5173))
    print("Port 5173: OPEN - Frontend OK")
    s2.close()
except Exception as e:
    print(f"Port 5173: CLOSED ({e})")

print("Done - services running in background")
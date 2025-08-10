import subprocess
import sys
import os

# Path to your virtual env python exe
venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")

print("Running stress runner...")
subprocess.run([venv_python, "stress_runner.py"], check=True)

print("Launching dashboard (this will keep running)...")
proc = subprocess.Popen([venv_python, "dashboard.py"])

import time
import webbrowser
time.sleep(3)
url = "http://127.0.0.1:8050"
print(f"Dashboard is running at {url}")
webbrowser.open(url)

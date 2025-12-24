import subprocess
import time
import requests

BASE = "http://localhost:5000"

def wait_ready(path: str, expected: int, timeout: int = 30):
    last_status = None
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}{path}", timeout=1)
            last_status = r.status_code
            if last_status == expected:
                return 
        except requests.RequestException as e:
            last_status = f"error: {e}"
        time.sleep(1)
    raise RuntimeError(f"{path}: expected {expected}, get {last_status}")

def test_sigterm_graceful_shutdown():
    
        wait_ready("/health/ready", 200)

        subprocess.run(
            ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
            check=True,
        )

        wait_ready("/health/ready", 503)

        wait_ready("/health/live", 200)
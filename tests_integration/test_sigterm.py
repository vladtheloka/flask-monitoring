import subprocess
import time
import requests

BASE = "http://localhost:5000"

def wait_ready(expected: int = 200, timeout: int = 20):
    last_status = None
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/health/ready", timeout=1)
            last_status = r.status_code
            if last_status == expected:
                return "http"
        except requests.exceptions.ConnectionError:
            if expected == 503:
                return "conn_refused"

        time.sleep(1)
    raise RuntimeError(f"Expected {expected}, but last status was {last_status}")

def test_sigterm_graceful_shutdown():
    proc = subprocess.Popen(
        [
            "docker", "run", "--rm",
            "-p", "5000:5000",
            "--name", "restmon_sigterm_test",
            "restmon:latest",
        ]
    )

    try:
 
        wait_ready(200)

        r = requests.get(f"{BASE}/health/live", timeout=1)
        assert r.status_code == 200

        subprocess.run(
            ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
            check=True,
        )

        result = wait_ready(503)
        assert result in ("http", "conn_refused")

    finally:
        proc.wait(timeout=30)
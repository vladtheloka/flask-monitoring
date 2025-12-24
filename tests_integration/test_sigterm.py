import subprocess
import time
import requests
import pytest
import shutil

BASE = "http://localhost:5000"

pytestmark = pytest.mark.skipif(
    shutil.which('docker') is None,
    reason = 'Docker CLI not avaliable',
)

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
    proc = subprocess.Popen(
        [
            "docker", "run", "--rm",
            "-p", "5000:5000",
            "--name", "restmon_sigterm_test",
            "restmon:latest",
        ]
    )

    try:
 
        wait_ready("/hetalth/ready", 200)

        subprocess.run(
            ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
            check=True,
        )

        wait_ready("/health/ready", 503)

        wait_ready("/health/live", 200)

    finally:
        proc.wait(timeout=30)
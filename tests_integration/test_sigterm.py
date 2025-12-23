import subprocess
import time
import requests
import pytest
import shutil

BASE = "http://localhost:5000"

docker_available = shutil.which("docker") is not None

pytestmark = pytest.mark.skipif(
    not docker_available,
    reason="Docker CLI not available",
)

def wait_not_ready(timeout: int = 20):
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/health/ready", timeout=1)
            if r.status_code == 503:
                return
        except requests.exceptions.RequestException:
            return
        time.sleep(1)

    raise RuntimeError("Service did not transition to not-ready state")

def wait_ready(expected: int = 200, timeout: int = 20):
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/health/ready", timeout=1)
            if r.status_code == expected:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    raise RuntimeError("Service did not become ready")


def test_sigterm_graceful_shutdown():
    # старт контейнера
    proc = subprocess.Popen(
        [
            "docker", "run", "--rm",
            "-p", "5000:5000",
            "--name", "restmon_sigterm_test",
            "restmon:latest",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        wait_ready(200)
        # отправляем SIGTERM
        subprocess.run(
            ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
            check=True,
        )

        # readiness должен упасть
        wait_not_ready()

        try:
            r = requests.get(f"{BASE}/health/live", timeout = 1)
            assert r.status_code == 200
        except requests.exceptions.RequestException:
            pass

    finally:
        proc.wait(timeout=30)
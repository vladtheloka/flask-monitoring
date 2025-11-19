# tests_integration/conftest.py
import subprocess
import time
import requests
import pytest
import os

COMPOSE_FILE = "docker-compose.test.yml"
COMPOSE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_URL = "http://localhost:5001/platform"
START_TIMEOUT = 30  # секунд

@pytest.fixture(scope="session", autouse=True)
def run_compose():
    print("[+] Starting integration services...")
    subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "up", "-d", "--build"],
        cwd=COMPOSE_DIR,
        check=True
    )

    for _ in range(START_TIMEOUT):
        try:
            r = requests.get(SERVICE_URL, timeout=1)
            if r.status_code == 200:
                print("[+] Service is ready")
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        subprocess.run(
            ["docker", "compose", "-f", COMPOSE_FILE, "logs"],
            cwd=COMPOSE_DIR
        )
        raise RuntimeError("Service did not start!")

    yield

    print("[+] Stopping integration services...")
    subprocess.run(
        ["docker", "compose", "-f", COMPOSE_FILE, "down", "-v"],
        cwd=COMPOSE_DIR,
        check=True
    )
    print("[+] Integration services stopped.")
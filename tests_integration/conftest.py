import subprocess
import time
import requests
import pytest


@pytest.fixture(scope="session", autouse=True)
def run_compose():
    # поднять compose
    subprocess.run(["docker", " compose", "up", "-d", "--build"], cwd="tests_integration")

    # ждать готовности сервиса
    url = "http://localhost:5001/platform"
    for _ in range(30):
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise RuntimeError("Service did not start!")

    yield

    # остановить compose
    subprocess.run(["docker", "compose", "down", "-v"], cwd="tests_integration")

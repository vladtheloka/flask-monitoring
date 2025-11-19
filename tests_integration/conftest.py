import subprocess
import time
import requests
import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def run_compose():
    compose_dir = os.path.join(os.getcwd(), "tests_integration")

    subprocess.run(
        ["docker", "compose", "up", "-d", "--build"],
        cwd=compose_dir,
        check=True
    )

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

    subprocess.run(
        ["docker", "compose", "down", "-v"],
        cwd=compose_dir
    )
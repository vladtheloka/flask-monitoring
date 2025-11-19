import time
import subprocess
import requests
import pytest


COMPOSE_FILE = "docker-compose.test.yml"
SERVICE_URL = "http://localhost:5001/platform"


def wait_for_service(url: str, timeout: int = 30):
    """Ждём пока сервис поднимется."""
    for _ in range(timeout):
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Service did not start!")


@pytest.fixture(scope="session", autouse=True)
def run_compose():
    """Поднимает docker-compose перед тестами, затем останавливает."""

    # up
    subprocess.run(
        ["docker", "compose",
         "-f", COMPOSE_FILE,
         "up", "-d", "--build"],
        cwd="tests_integration",
        check=True
    )

    wait_for_service(SERVICE_URL)

    yield

    # down
    subprocess.run(
        ["docker", "compose",
         "-f", COMPOSE_FILE,
         "down", "-v"],
        cwd="tests_integration",
        check=True
    )

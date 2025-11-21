import subprocess
import time
import pytest
import requests

APP_CONTAINER_NAME = "restmon_test"
APP_IMAGE = "restmon:latest"
NETWORK_NAME = "restmon_test_net"
APP_PORT = 5000
BASE_URL = f"http://{APP_CONTAINER_NAME}:{APP_PORT}"


@pytest.fixture(scope="session", autouse=True)
def start_app_container():
    # создаем сеть, если не существует
    subprocess.run(
        ["docker", "network", "create", NETWORK_NAME],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # запускаем контейнер приложения
    subprocess.run([
        "docker", "run", "-d",
        "--name", APP_CONTAINER_NAME,
        "--network", NETWORK_NAME,
        "-p", f"{APP_PORT}:{APP_PORT}",
        APP_IMAGE
    ], check=True)

    # ждем, пока сервис поднимется
    for _ in range(30):
        try:
            r = requests.get(f"{BASE_URL}/platform", timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise RuntimeError("Service did not start!")

    yield BASE_URL

    # остановка и удаление контейнера
    subprocess.run(["docker", "rm", "-f", APP_CONTAINER_NAME])
    # оставим сеть, может быть использована повторно
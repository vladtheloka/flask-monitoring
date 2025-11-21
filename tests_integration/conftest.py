import subprocess
import time
import requests
import pytest
import os

@pytest.fixture(scope="session", autouse=True)
def run_container():
    # Порт, на котором сервис будет доступен снаружи
    port = os.getenv("PORT", "5000")
    base_url = f"http://localhost:{port}"
    
    # Запускаем контейнер с нужным портом
    subprocess.run([
        "docker", "run", "--rm", "-d",
        "-p", f"{port}:{port}",
        "--name", "restmon_test",
        "restmon:latest"
    ], check=True)

    # Ждём, пока сервис станет доступен
    for _ in range(30):
        try:
            r = requests.get(f"{base_url}/platform", timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        raise RuntimeError("Service did not start!")

    yield base_url  # передаём тестам URL

    # Останавливаем контейнер
    subprocess.run(["docker", "stop", "restmon_test"], check=True)
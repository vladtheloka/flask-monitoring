import pytest
import requests
import time
import subprocess

@pytest.fixture(scope="session")
def base_url():
    """Запускаем контейнер с приложением и возвращаем base_url для тестов."""
    image_name = "restmon:latest"
    container_name = "restmon_test"
    port = 5001

    # Запуск контейнера в фоне с пробросом порта
    subprocess.run([
        "docker", "run", "-d",
        "--name", container_name,
        "-p", f"{port}:5001",
        image_name
    ], check=True)

    url = f"http://localhost:{port}"

    # Ждём готовности сервиса
    for _ in range(30):
        try:
            r = requests.get(f"{url}/platform", timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(1)
    else:
        # если не поднялся
        subprocess.run(["docker", "logs", container_name])
        subprocess.run(["docker", "rm", "-f", container_name])
        raise RuntimeError("Service did not start!")

    yield url  # base_url для тестов

    # После тестов контейнер останавливаем и удаляем
    subprocess.run(["docker", "rm", "-f", container_name])
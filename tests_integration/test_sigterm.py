import subprocess
import time
import requests

BASE = "http://localhost:5000"


def wait_ready(expected=200, timeout=20):
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/health/ready")
            if r.status_code == expected:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Service not in expected state")


def test_sigterm_graceful_shutdown():
    # старт контейнера
    proc = subprocess.Popen(
        [
            "docker", "run", "--rm",
            "-p", "5000:5000",
            "--name", "restmon_sigterm_test",
            "restmon:latest",
        ]
    )

    try:
        # ждём readiness = 200
        wait_ready(200)

        # отправляем SIGTERM
        subprocess.run(
            ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
            check=True,
        )

        # readiness должен упасть
        wait_ready(503)

        # liveness остаётся OK
        r = requests.get(f"{BASE}/health/live")
        assert r.status_code == 200

    finally:
        proc.wait(timeout=20)
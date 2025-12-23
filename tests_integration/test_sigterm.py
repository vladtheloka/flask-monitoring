import subprocess
import time
import requests

BASE = "http://localhost:5000"


def wait_live(timeout: int = 20):
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/health/live", timeout=1)
            if r.status_code == 200:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    raise RuntimeError("Service did not become live")

def wait_ready(expected: int = 200, timeout: int = 20):
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}/health/ready", timeout=1)
            if r.status_code == expected:
                return
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    raise RuntimeError("Service did not reach expected readiness")

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
        # 1️⃣ дождались, что сервис жив
        wait_live()

        # 2️⃣ дождались readiness = OK
        wait_ready(200)

        # 3️⃣ шлём SIGTERM
        subprocess.run(
            ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
            check=True,
        )

        # 4️⃣ readiness падает
        wait_ready(503)

        # 5️⃣ liveness может ещё отвечать (grace period)
        r = requests.get(f"{BASE}/health/live", timeout=1)
        assert r.status_code == 200

    finally:
        proc.wait(timeout=30)
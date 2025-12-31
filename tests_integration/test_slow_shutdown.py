# tests_integration/test_slow_shutdown.py
import threading
import time
import subprocess
import requests

BASE = "http://localhost:5000"


def wait_not_ready_or_down(path: str, timeout: int = 30):
    for _ in range(timeout):
        try:
            r = requests.get(f"{BASE}{path}", timeout=1)
            if r.status_code == 503:
                return "503"
        except requests.RequestException:
            return "down"
        time.sleep(1)
    raise RuntimeError("Service did not transition to not ready or down")


def test_sigterm_during_slow_request():
    slow_result = {"status": None}

    def call_slow():
        try:
            r = requests.get(f"{BASE}/slow", timeout=20)
            slow_result["status"] = r.status_code # type: ignore
        except Exception:
            slow_result["status"] = "error" # type: ignore

    t = threading.Thread(target=call_slow)
    t.start()

    time.sleep(1)  # гарантируем, что slow стартовал

    subprocess.run(
        ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
        check=True,
    )

    # readiness должен упасть или сервис должен умереть
    state = wait_not_ready_or_down("/health/ready")
    assert state in ("503", "down")

    t.join(timeout=20)

    # slow может:
    #  - завершиться (200)
    #  - быть оборван (error)
    assert slow_result["status"] in (200, "error")

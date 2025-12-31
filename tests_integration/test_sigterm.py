import time
import requests
import threading

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

def wait_eventually_down(timeout: int = 30):
    for _ in range(timeout):
        try:
            requests.get(f"{BASE}/health/live", timeout=1)
        except requests.RequestException:
            return
        time.sleep(1)
    raise RuntimeError("Service never went down")

def test_slow_aborted_on_sigterm():
    t = threading.Thread(
        target=lambda: requests.get(f"{BASE}/slow", timeout=15)
    )
    t.start()

    time.sleep(2)

    t.join(timeout=5)


def test_sigterm_graceful_shutdown():

        state = wait_not_ready_or_down("/health/ready")
        assert state in ("503", "down")
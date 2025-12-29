import time
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

def test_sigterm_graceful_shutdown():

        state = wait_not_ready_or_down("/health/ready")
        assert state in ("503", "down")
        wait_not_ready_or_down("/health/live")
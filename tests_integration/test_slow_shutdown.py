import requests
import time
import threading

BASE = "http://localhost:5000"

def wait_eventually_down(timeout: int = 30):
    for _ in range(timeout):
        try:
            requests.get(f"{BASE}/health/live", timeout=1)
        except requests.RequestException:
            return
        time.sleep(1)
    raise RuntimeError("Service never went down")

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

    time.sleep(1)

    state = wait_not_ready_or_down("/health/ready")
    assert state in ("503", "down")

    t.join(timeout=20)
    assert slow_result["status"] in ("error", 200, 503)

    wait_eventually_down()
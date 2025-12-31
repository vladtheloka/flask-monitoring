import requests, time, subprocess
import threading

BASE = "http://localhost:5000"


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

    subprocess.run(
        ["docker", "kill", "--signal=SIGTERM", "restmon_sigterm_test"],
        check=True,
    )

    state = wait_not_ready_or_down("/health/ready")
    assert state in ("503", "down")

    t.join(timeout=20)
    assert slow_result["status"] in ("error", 200)

    wait_eventually_down()
import time
import requests

BASE_URL = "http://localhost:5000/system_info"


def wait_for_service(timeout: int = 30):
    """Ждём когда API поднимется в контейнере."""
    for _ in range(timeout):
        try:
            r = requests.get(BASE_URL)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Service did not start within timeout!")


def test_system_info_status_ok():
    wait_for_service()

    resp = requests.get(BASE_URL)
    assert resp.status_code == 200
    assert resp.headers["Content-Type"].startswith("application/json")


def test_system_info_contains_fields():
    wait_for_service()

    resp = requests.get(BASE_URL)
    data = resp.json()

    expected_keys = {
        "os_details",
        "cpu_usage",
        "memory_usage",
        "storage_usage",
        "network_usage",
        "system_uptime",
    }

    assert set(data.keys()) == expected_keys


def test_system_info_values_types():
    wait_for_service()

    data = requests.get(BASE_URL).json()

    assert isinstance(data["os_details"], dict)
    assert isinstance(data["cpu_usage"], (float, int))
    assert isinstance(data["memory_usage"], dict)
    assert isinstance(data["storage_usage"], dict)
    assert isinstance(data["network_usage"], dict)
    assert isinstance(data["system_uptime"], (int, float))
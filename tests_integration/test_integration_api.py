import time
import requests


BASE_URL = "http://localhost:5001"


def wait_for_service(timeout=20): # type: ignore
    """Ждём пока контейнер поднимется"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{BASE_URL}/platform")
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(1)
    raise TimeoutError("Service did not start in time")


def test_front_page():
    wait_for_service()
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert r.json() == {"Hello": "World"}


def test_platform():
    wait_for_service()
    r = requests.get(f"{BASE_URL}/platform")
    assert r.status_code == 200
    j = r.json()
    assert "kernelversion" in j
    assert "operatingsystem" in j
    assert "hostname" in j
    assert "architecture" in j


def test_memory():
    r = requests.get(f"{BASE_URL}/memory")
    assert r.status_code == 200
    j = r.json()
    assert "totalMemory" in j
    assert "availableMemory" in j
    assert "freeMemory" in j


def test_cpu():
    r = requests.get(f"{BASE_URL}/cpu")
    assert r.status_code == 200
    j = r.json()
    assert "cpuuser" in j
    assert "cpusystem" in j
    assert "cpuidle" in j
    assert "cpuiowait" in j


def test_storage():
    r = requests.get(f"{BASE_URL}/storage")
    assert r.status_code == 200
    j = r.json()
    assert "roottotal" in j
    assert "rootused" in j
    assert "rootfree" in j
    assert "rootfreepercent" in j

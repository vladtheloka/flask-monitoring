import requests


def test_front_page(start_app_container: str):
    base_url = start_app_container
    r = requests.get(f"{base_url}/")
    assert r.status_code == 200
    assert r.json().get("Hello") == "World"


def test_platform(start_app_container: str):
    base_url = start_app_container
    r = requests.get(f"{base_url}/platform")
    assert r.status_code == 200
    data = r.json()

    assert "kernelversion" in data
    assert "operatingsystem" in data
    assert "hostname" in data
    assert "architecture" in data


def test_memory(start_app_container: str):
    base_url = start_app_container
    r = requests.get(f"{base_url}/memory")
    assert r.status_code == 200
    data = r.json()

    assert "totalMemory" in data
    assert "availableMemory" in data
    assert "freeMemory" in data


def test_cpu(start_app_container: str):
    base_url = start_app_container
    r = requests.get(f"{base_url}/cpu")
    assert r.status_code == 200
    data = r.json()

    assert "cpuuser" in data
    assert "cpusystem" in data
    assert "cpuidle" in data
    assert "cpuiowait" in data


def test_storage(start_app_container: str):
    base_url = start_app_container
    r = requests.get(f"{base_url}/storage")
    assert r.status_code == 200
    data = r.json()

    assert "roottotal" in data
    assert "rootused" in data
    assert "rootfree" in data
    assert "rootfreepercent" in data

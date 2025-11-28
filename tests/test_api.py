import restmon.api as api
import pytest
from flask.testing import FlaskClient

class FakeResources:
    @staticmethod
    def get_os_details():
        return {"name": "TestOS", "version": "1.0"}

    @staticmethod
    def get_cpu_usage():
        return 12.5

    @staticmethod
    def get_memory_usage():
        return {"total": 4096, "used": 1024}

    @staticmethod
    def get_storage_usage():
        return {"root": {"total": 100000, "used": 50000}}

    @staticmethod
    def get_network_usage() -> list[dict[str, int | str]]:
        return [{"iface": "eth0", "rx": 1000, "tx": 2000}]

    @staticmethod
    def get_system_uptime():
        return 3600

def test_system_info_get_returns_expected_json(monkeypatch: pytest.MonkeyPatch, client: FlaskClient):
    monkeypatch.setattr(api, "SystemResources", FakeResources)
    resp = client.get("/system_info")

    assert resp.status_code == 200
    assert resp.content_type.startswith("application/json")

    data = resp.get_json()
    assert data["os_details"] == FakeResources.get_os_details()
    assert data["cpu_usage"] == FakeResources.get_cpu_usage()
    assert data["memory_usage"] == FakeResources.get_memory_usage()
    assert data["storage_usage"] == FakeResources.get_storage_usage()
    assert data["network_usage"] == FakeResources.get_network_usage()
    assert data["system_uptime"] == FakeResources.get_system_uptime()


def test_system_info_contains_all_keys(monkeypatch: pytest.MonkeyPatch, client: FlaskClient):
    monkeypatch.setattr(api, "SystemResources", FakeResources)
    data = client.get("/system_info").get_json()

    expected = {
        "os_details",
        "cpu_usage",
        "memory_usage",
        "storage_usage",
        "network_usage",
        "system_uptime",
    }

    assert set(data.keys()) == expected


def test_system_info_post_method_not_allowed(monkeypatch: pytest.MonkeyPatch, client: FlaskClient):
    monkeypatch.setattr(api, "SystemResources", FakeResources)
    resp = client.post("/system_info")
    assert resp.status_code == 405

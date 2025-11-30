import pytest
import restmon.resources as res


def test_get_os_details(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(res.platform, "system", lambda: "LinuxTest")
    monkeypatch.setattr(res.os, "uname", lambda: type("U", (), {
        "release": "5.15-test",
        "version": "v1",
        "machine": "x86-test"
    })())

    result = res.SystemResources.get_os_details()
    assert result["platform"] == "LinuxTest"
    assert result["release"] == "5.15-test"
    assert result["machine"] == "x86-test"


def test_cpu_usage(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(res.psutil, "cpu_percent", lambda interval=1: 55.5)
    assert res.SystemResources.get_cpu_usage() == 55.5


def test_memory_usage(monkeypatch: pytest.MonkeyPatch):
    Fake = type("Mem", (), {"total": 100, "available": 50, "used": 40, "percent": 60})
    monkeypatch.setattr(res.psutil, "virtual_memory", lambda: Fake)

    result = res.SystemResources.get_memory_usage()
    assert result == {"total": 100, "available": 50, "used": 40, "percent": 60}


def test_storage_usage(monkeypatch: pytest.MonkeyPatch):
    Fake = type("D", (), {"total": 200, "used": 100, "free": 50, "percent": 90})
    monkeypatch.setattr(res.psutil, "disk_usage", lambda path: Fake) # type: ignore

    result = res.SystemResources.get_storage_usage()
    assert result == {"total": 200, "used": 100, "free": 50, "percent": 90}


def test_network_usage(monkeypatch: pytest.MonkeyPatch):
    Fake = type("N", (), {
        "bytes_sent": 10, "bytes_recv": 20,
        "packets_sent": 3, "packets_recv": 4
    })
    monkeypatch.setattr(res.psutil, "net_io_counters", lambda: Fake)

    result = res.SystemResources.get_network_usage()
    assert result == {
        "bytes_sent": 10,
        "bytes_recv": 20,
        "packets_sent": 3,
        "packets_recv": 4,
    }


def test_system_uptime(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(res.psutil, "boot_time", lambda: 123456789)
    assert res.SystemResources.get_system_uptime() == 123456789


def test_process_count(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(res.psutil, "pids", lambda: [1, 2, 3, 4])
    assert res.SystemResources.get_process_count() == 4
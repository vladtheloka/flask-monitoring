# tests/test_health.py
from restmon.api import create_app
from flask.testing import FlaskClient
import pytest

@pytest.fixture
def client() -> FlaskClient:
    app = create_app()
    return app.test_client()


def test_live_ok(client : FlaskClient):
    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.get_json() == {"status": "alive"}


def test_ready_ok(monkeypatch : pytest.MonkeyPatch, client : FlaskClient):
    class FakeSR:
        @staticmethod
        def get_system_uptime():
            return 12345

    monkeypatch.setattr("restmon.health.SystemResources", FakeSR)
    r = client.get("/health/ready")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ready"}


def test_ready_not_ok(monkeypatch : pytest.MonkeyPatch, client : FlaskClient):
    class FakeSR:
        @staticmethod
        def get_system_uptime():
            raise RuntimeError("fail")

    monkeypatch.setattr("restmon.health.SystemResources", FakeSR)
    r = client.get("/health/ready")
    assert r.status_code == 503
    assert r.get_json() == {"status": "not_ready"}
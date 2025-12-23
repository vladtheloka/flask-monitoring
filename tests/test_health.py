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
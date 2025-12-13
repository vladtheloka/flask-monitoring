# tests/test_health_contract.py
from flask.testing import FlaskClient


def test_health_live_contract(client: FlaskClient):
    r = client.get("/health/live")

    assert r.status_code == 200
    data = r.get_json()

    assert isinstance(data, dict)
    assert set(data.keys()) == {"status"} # type: ignore
    assert isinstance(data["status"], str)


def test_health_ready_contract(client: FlaskClient):
    r = client.get("/health/ready")

    assert r.status_code in (200, 503)
    data = r.get_json()

    assert isinstance(data, dict)
    assert set(data.keys()) == {"status"} # type: ignore
    assert data["status"] in {"ready", "not_ready"}
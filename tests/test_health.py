# tests/test_health.py
from flask.testing import FlaskClient
from restmon.state import (
    shutdown_event,
    reset_shutdown_state,
)

def test_live_always_200(client: FlaskClient):
    reset_shutdown_state()

    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.json["status"] == "alive" # type: ignore


def test_ready_initially_200(client: FlaskClient):
    reset_shutdown_state()

    r = client.get("/health/ready")
    assert r.status_code == 200
    assert r.json["status"] == "ready" # type: ignore


def test_ready_returns_503_on_shutdown(client: FlaskClient):
    reset_shutdown_state()

    shutdown_event.set()

    r = client.get("/health/ready")
    assert r.status_code == 503
    assert r.json["status"] == "shutting_down" # type: ignore


def test_live_ignores_shutdown(client: FlaskClient):
    reset_shutdown_state()

    shutdown_event.set()

    r = client.get("/health/live")
    assert r.status_code == 200
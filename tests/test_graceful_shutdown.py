import signal
import pytest
from restmon.state import mark_shutting_down
from flask.testing import FlaskClient
from restmon.lifecycle import _handle_sigterm # type: ignore
from restmon.state import is_shutting_down

def test_ready_turns_not_ready_on_shutdown(
        client: FlaskClient,
        monkeypatch: pytest.MonkeyPatch, 
        ):

    # force system healty
    class FakeSR:
        @staticmethod
        def get_system_uptime():
            return 123


    monkeypatch.setattr(
        "restmon.health.SystemResources",
        FakeSR
    )

    # initially ready
    r1 = client.get("/health/ready")
    assert r1.status_code == 200

    # simulate SIGTERM
    mark_shutting_down()

    r2 = client.get("/health/ready")
    assert r2.status_code == 503
    assert r2.get_json()["status"] == "not_ready"


def test_live_stays_alive_on_shutdown(client: FlaskClient):
    mark_shutting_down()

    r = client.get("/health/live")
    assert r.status_code == 200
    assert r.get_json()["status"] == "alive"

def test_sigterm_handler():

    _handle_sigterm(signal.SIGTERM, None)
    assert is_shutting_down() is True
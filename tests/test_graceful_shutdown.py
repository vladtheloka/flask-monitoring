from restmon.state import shutdown_event, reset_shutdown_state
from flask.testing import FlaskClient


def test_ready_respects_shutdown_flag(client: FlaskClient):

    reset_shutdown_state()

    r1 = client.get("/health/ready")
    assert r1.status_code == 200

    shutdown_event.set()

    r2 = client.get("/health/ready")
    assert r2.status_code == 503

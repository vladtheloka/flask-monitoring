from restmon.state import mark_shutting_down, reset_shutdown_state
from flask.testing import FlaskClient


def test_ready_respects_shutdown_flag(client: FlaskClient):

    reset_shutdown_state()

    r1 = client.get("/health/ready")
    assert r1.status_code == 200

    mark_shutting_down()

    r2 = client.get("/health/ready")
    assert r2.status_code == 503

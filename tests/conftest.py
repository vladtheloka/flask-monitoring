import pytest
from restmon.api import create_app
from restmon.state import reset_shutdown_state

@pytest.fixture
def client():
    reset_shutdown_state()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

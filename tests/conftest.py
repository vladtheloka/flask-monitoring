import pytest
from restmon.api import create_app
from flask import Flask
from restmon import state


@pytest.fixture
def app() -> Flask:
    return create_app()


@pytest.fixture
def client(app: Flask):
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_state():
    state.reset_shutdown_state()
    state.shutdown_event.clear()
    yield
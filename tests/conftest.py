import pytest
from restmon.api import create_app
from flask import Flask
from restmon.state import reset_shutdown_state


@pytest.fixture
def app() -> Flask:
    return create_app()


@pytest.fixture
def client(app: Flask):
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_shutdown():
    reset_shutdown_state()
    yield
    reset_shutdown_state()
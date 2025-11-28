import pytest
from restmon.api import create_app
from flask import Flask


@pytest.fixture
def app() -> Flask:
    return create_app()


@pytest.fixture
def client(app: Flask):
    return app.test_client()
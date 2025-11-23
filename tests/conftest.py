import pytest
from restmon.api import create_app
from flask import Flask
from flask.testing import FlaskClient

@pytest.fixture
def app() -> Flask:
    """Возвращает Flask app для тестов."""
    app = create_app()
    app.testing = True
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Возвращает тестовый клиент Flask."""
    return app.test_client()

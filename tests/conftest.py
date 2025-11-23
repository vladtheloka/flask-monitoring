import pytest
from flask.testing import FlaskClient
from flask import Flask

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    app.testing = True
    return app.test_client()

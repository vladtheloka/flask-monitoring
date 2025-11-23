from __future__ import annotations

from flask import Flask
from flask_restful import Api

from restmon.resources import FrontPage


def create_app() -> Flask:
    """
    Creates and configures Flask application.
    """
    app = Flask(__name__)
    api = Api(app)

    register_resources(api)

    return app


def register_resources(api: Api) -> None:
    """
    Register all API resources here.
    Pylance understands types thanks to Protocol.
    """
    api.add_resource(FrontPage, "/")  # type: ignore[arg-type]
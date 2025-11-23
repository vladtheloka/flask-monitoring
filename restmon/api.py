from __future__ import annotations

from flask import Flask
from flask_restful import Api

from restmon.resources import FrontPage, GetMemory, GetCPU, GetCPUPercent, GetStorage
from restmon.os_platform import platform


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
    api.add_resource(FrontPage, "/") # type: ignore[arg-type]
    api.add_resource(GetMemory, "/memory") # type: ignore[arg-type]
    api.add_resource(GetCPU, "/cpu") # type: ignore[arg-type]
    api.add_resource(GetCPUPercent, "/cpu/percent") # type: ignore[arg-type]
    api.add_resource(GetStorage, "/storage") # type: ignore[arg-type]
    api.add_resource(platform.system, "/platform") # type: ignore[arg-type]

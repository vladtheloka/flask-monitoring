from flask import Flask
from flask_restful import Api, Resource
from typing import Any, Dict
from restmon.resources import SystemResources


def create_app() -> Flask:
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(SystemInfo, "/system_info") # type: ignore

    return app

class SystemInfo(Resource):
    """REST endpoint returning system information."""

    def get(self) -> Dict[str, Any]:
        return {
            "os_details": SystemResources.get_os_details(),
            "cpu_usage": SystemResources.get_cpu_usage(),
            "memory_usage": SystemResources.get_memory_usage(),
            "storage_usage": SystemResources.get_storage_usage(),
            "network_usage": SystemResources.get_network_usage(),
            "system_uptime": SystemResources.get_system_uptime(),
        }
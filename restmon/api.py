from flask import Flask
from flask_restful import Api, Resource
from flask_wtf.csrf import CSRFProtect
from typing import Any, Dict
from restmon.resources import SystemResources
from restmon.health import Live, Ready
from restmon.metrics import Metrics
from restmon.lifecycle import setup_signal_handlers
from restmon.shutdown_middleware import shutdown_middleware

def create_app() -> Flask:
    app = Flask(__name__)
    setup_signal_handlers()
    csrf = CSRFProtect()
    csrf.init_app(app) # type: ignore
    app.before_request(shutdown_middleware)
    api = Api(app)

    api.add_resource(SystemInfo, "/system_info") # type: ignore
    api.add_resource(Live, "/health/live") # type: ignore
    api.add_resource(Ready, "/health/ready") # type: ignore
    api.add_resource(Metrics, "/metrics") # type: ignore
    
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
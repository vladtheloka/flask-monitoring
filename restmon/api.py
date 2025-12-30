from flask_restful import Resource
from flask_wtf.csrf import CSRFProtect
from typing import Any, Dict
from restmon.resources import SystemResources
from restmon.health import Live, Ready
from restmon.metrics import Metrics
from restmon.lifecycle import setup_signal_handlers
import time
from restmon.state import shutdown_event
from fastapi import HTTPException
from restmon.middleware import shutdown_middleware
from fastapi import FastAPI

def create_app():
    app = FastAPI()
    setup_signal_handlers()
    csrf = CSRFProtect()
    csrf.init_app(app) # type: ignore
    
    app.middleware("http")(shutdown_middleware)
    api.add_resource(SystemInfo, "/system_info") # type: ignore
    api.add_resource(Live, "/health/live") # type: ignore
    api.add_resource(Ready, "/health/ready") # type: ignore
    api.add_resource(Metrics, "/metrics") # type: ignore

    @app.get("/slow")
    def slow() -> Dict[str, str]:  # type: ignore
        for _ in range(10):
            if shutdown_event.is_set():
                raise HTTPException(
                    status_code=503,
                    detail="Shutting down"
                )
        time.sleep(1)
        
        return {"status": "finished"}
    
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
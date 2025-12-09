# restmon/health.py
from flask_restful import Resource
from typing import Dict
from restmon.resources import SystemResources


class Live(Resource):
    """Liveness probe - simple server alive check."""
    def get(self) -> Dict[str, str]:
        return {"status": "alive"}


class Ready(Resource):
    """Readiness probe - checks essential dependencies."""

    def get(self):
        try:
            # простая быстрая проверка: psutil/boot_time доступен
            uptime = SystemResources.get_system_uptime()
            # если uptime реально число > 0 — считаем ready
            if isinstance(uptime, (int, float)) and uptime > 0: # type: ignore
                return {"status": "ready"}, 200
            return {"status": "not_ready"}, 503
        except Exception:
            return {"status": "not_ready"}, 503
from flask_restful import Resource
from typing import Dict
from restmon.resources import SystemResources
from restmon.state import is_ready


class Live(Resource):
    def get(self) -> Dict[str, str]:
        return {"status": "alive"}


class Ready(Resource):
    def get(self):
        if not is_ready():
            return {"status": "not_ready"}, 503

        try:
            uptime = SystemResources.get_system_uptime()
            if isinstance(uptime, (int, float)) and uptime > 0: # type: ignore
                return {"status": "ready"}, 200
            return {"status": "not_ready"}, 503
        except Exception:
            return {"status": "not_ready"}, 503
from flask_restful import Resource
from typing import Dict
from restmon import state

class Live(Resource):
    def get(self) -> Dict[str, str]:
        return {"status": "alive"}


class Ready(Resource):
    def get(self):
        if state.shutdown_event.is_set():
            return {"status": "not_ready"}, 503
        return {"status": "ready"}, 200
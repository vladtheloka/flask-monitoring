from flask_restful import Resource
from restmon.state import shutdown_event

class Live(Resource):
    def get(self):
        return {"status": "alive"}, 200


class Ready(Resource):
    def get(self):
        if shutdown_event.is_set():
            return {"status": "not_ready"}, 503
        return {"status": "ready"}, 200
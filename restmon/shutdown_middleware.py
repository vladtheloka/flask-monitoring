from flask import jsonify, request
from restmon.state import shutdown_event

EXCLUDE_PATH = {
    "/health/live",
}

def shutdown_middleware():
    # live всегда отвечает
    if request.path in EXCLUDE_PATH:
        return None

    if shutdown_event.is_set():
        return jsonify({"status": "shutting_down"}), 503

    return None
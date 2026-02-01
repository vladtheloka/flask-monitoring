from flask import jsonify, request
from restmon.state import shutdown_event
from restmon.metrics_state import requests_rejected_total

EXCLUDE_PATH = {
    "/health/live", "/metrics"
}

def shutdown_middleware():
    # live всегда отвечает
    if request.path in EXCLUDE_PATH:
        return None

    if shutdown_event.is_set():
        requests_rejected_total.inc()
        return jsonify({"status": "shutting_down"}), 503

    return None
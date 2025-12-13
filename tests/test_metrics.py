# tests/test_metrics.py
from flask.testing import FlaskClient


def test_metrics_endpoint_exists(client: FlaskClient):
    r = client.get("/metrics")
    assert r.status_code == 200
    assert r.headers["Content-Type"].startswith("text/plain")


def test_metrics_contains_required_metrics(client: FlaskClient):
    data = client.get("/metrics").data.decode()

    required = [
        "process_uptime_seconds",
        "system_cpu_usage_percent",
        "system_memory_usage_percent",
        "system_memory_used_bytes",
        "system_disk_usage_percent",
        "process_count",
    ]

    for metric in required:
        assert metric in data
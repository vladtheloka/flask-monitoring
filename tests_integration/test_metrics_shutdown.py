import requests

BASE = "http://localhost:5000"

def test_shutdown_metrics_exposed():
    r = requests.get(f"{BASE}/metrics")
    assert "shutdown_in_progress" in r.text
    assert "requests_rejected_total" in r.text

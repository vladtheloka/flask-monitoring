import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    return app.test_client()

def test_health(client):
    rv = client.get('/api/health')
    assert rv.status_code == 200
    assert rv.get_json() == {"status": "ok"}

def test_stats(client):
    rv = client.get('/api/stats')
    json_data = rv.get_json()
    assert "cpu_percent" in json_data
    assert "memory_percent" in json_data
    assert "disk_percent" in json_data

def test_processes(client):
    rv = client.get('/api/processes')
    json_data = rv.get_json()
    assert "top_processes" in json_data

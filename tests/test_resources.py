from flask.testing import FlaskClient

def test_get_memory(client: FlaskClient):
    rv = client.get("/memory")
    assert rv.status_code == 200
    data = rv.json
    assert data is not None, "Response JSON is None"
    assert data["totalMemory"] >= 0
    assert data["freeMemory"] >= 0


def test_get_cpu(client: FlaskClient):
    rv = client.get("/cpu")
    assert rv.status_code == 200
    data = rv.json
    assert data is not None, "Response JSON is None"
    assert "cpuuser" in data
    assert "cpusystem" in data


def test_get_cpu_percent(client: FlaskClient):
    rv = client.get("/cpupercent")
    assert rv.status_code == 200
    data = rv.json
    assert data is not None, "Response JSON is None"
    assert "cpuuser" in data


def test_get_storage(client: FlaskClient):
    rv = client.get("/storage")
    assert rv.status_code == 200
    data = rv.json
    assert data is not None, "Response JSON is None"
    assert data["roottotal"] > 0

from flask.testing import FlaskClient

def test_front_page(client: FlaskClient):
    rv = client.get("/")
    assert rv.status_code == 200
    assert rv.json == {"Hello": "World"}


def test_memory(client: FlaskClient):
    rv = client.get("/memory")
    assert rv.status_code == 200
    assert rv.json is not None
    assert "totalMemory" in rv.json
    assert "availableMemory" in rv.json
    assert "freeMemory" in rv.json


def test_cpu(client: FlaskClient):
    rv = client.get("/cpu")
    assert rv.status_code == 200
    assert rv.json is not None
    assert "cpuuser" in rv.json
    assert "cpusystem" in rv.json
    assert "cpuidle" in rv.json


def test_cpu_percent(client: FlaskClient):
    rv = client.get("/cpupercent")
    assert rv.status_code == 200
    assert rv.json is not None
    assert "cpuuser" in rv.json
    assert "cpusystem" in rv.json
    assert "cpuidle" in rv.json


def test_storage(client: FlaskClient):
    rv = client.get("/storage")
    assert rv.status_code == 200
    assert rv.json is not None
    assert "roottotal" in rv.json
    assert "rootused" in rv.json
    assert "rootfree" in rv.json
    assert "rootfreepercent" in rv.json
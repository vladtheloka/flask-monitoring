def test_front_page(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert rv.json == {"Hello": "World"}


def test_memory(client):
    rv = client.get("/memory")
    assert rv.status_code == 200
    assert "totalMemory" in rv.json
    assert "availableMemory" in rv.json
    assert "freeMemory" in rv.json


def test_cpu(client):
    rv = client.get("/cpu")
    assert rv.status_code == 200
    assert "cpuuser" in rv.json
    assert "cpusystem" in rv.json
    assert "cpuidle" in rv.json


def test_cpu_percent(client):
    rv = client.get("/cpupercent")
    assert rv.status_code == 200
    assert "cpuuser" in rv.json
    assert "cpusystem" in rv.json
    assert "cpuidle" in rv.json


def test_storage(client):
    rv = client.get("/storage")
    assert rv.status_code == 200
    assert "roottotal" in rv.json
    assert "rootused" in rv.json
    assert "rootfree" in rv.json
    assert "rootfreepercent" in rv.json
    assert "homestotal" in rv.json
    assert "homeused" in rv.json
    assert "homefree" in rv.json
    assert "homefreepercent" in rv.json
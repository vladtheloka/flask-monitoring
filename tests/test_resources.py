def test_get_memory(client):
    rv = client.get("/memory")
    assert rv.status_code == 200
    data = rv.json
    assert data["totalMemory"] >= 0
    assert data["freeMemory"] >= 0


def test_get_cpu(client):
    rv = client.get("/cpu")
    assert rv.status_code == 200
    data = rv.json
    assert "cpuuser" in data
    assert "cpusystem" in data


def test_get_cpu_percent(client):
    rv = client.get("/cpupercent")
    assert rv.status_code == 200
    data = rv.json
    assert "cpuuser" in data


def test_get_storage(client):
    rv = client.get("/storage")
    assert rv.status_code == 200
    data = rv.json
    assert data["roottotal"] > 0

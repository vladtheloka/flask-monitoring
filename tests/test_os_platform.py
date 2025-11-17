def test_platform(client):
    rv = client.get("/platform")
    assert rv.status_code == 200

    json = rv.json

    assert "kernelversion" in json
    assert "operatingsystem" in json
    assert "hostname" in json
    assert "architecture" in json

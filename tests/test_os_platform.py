from flask.testing import FlaskClient

def test_platform(client: FlaskClient):
    rv = client.get("/platform")
    assert rv.status_code == 200

    json = rv.json

    assert json is not None
    assert "kernelversion" in json
    assert "operatingsystem" in json
    assert "hostname" in json
    assert "architecture" in json

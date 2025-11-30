from flask.testing import FlaskClient

def test_system_info_options(client: FlaskClient):
    resp = client.options("/system_info")
    assert resp.status_code in (200, 204)


def test_system_info_head(client: FlaskClient):
    resp = client.head("/system_info")
    assert resp.status_code == 200


def test_invalid_methods(client: FlaskClient):
    for method in ["put", "patch", "delete"]:
        resp = getattr(client, method)("/system_info")
        assert resp.status_code == 405
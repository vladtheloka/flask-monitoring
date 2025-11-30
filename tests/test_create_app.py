from restmon.api import create_app

def test_create_app_registers_route():
    app = create_app()
    client = app.test_client()

    resp = client.get("/system_info")
    assert resp.status_code in (200, 500)  # 500 значит что handler подключён
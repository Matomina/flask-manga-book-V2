def test_admin_requires_login(client):
    response = client.get("/admin")
    assert response.status_code == 302


def test_admin_dashboard(client, auth):
    auth.login()
    response = client.get("/admin")
    assert response.status_code == 200
def test_admin_requires_login(client):
    response = client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_admin_dashboard_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/admin/")

    assert response.status_code == 200


def test_admin_forbidden_for_regular_user(client, auth):
    auth.login_as_user()

    response = client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert "Location" in response.headers
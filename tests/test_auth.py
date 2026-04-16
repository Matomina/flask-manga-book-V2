def test_login_success(client, auth):
    response = auth.login_as_admin()

    assert response.status_code == 302
    assert "Location" in response.headers


def test_login_fail(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "wrong@test.com",
            "password": "wrong",
        },
    )

    assert response.status_code == 401


def test_logout(client, auth):
    auth.login_as_admin()
    response = auth.logout()

    assert response.status_code == 302
    assert "Location" in response.headers

    protected_response = client.get("/admin/", follow_redirects=False)
    assert protected_response.status_code == 302
    assert "/auth/login" in protected_response.headers["Location"]
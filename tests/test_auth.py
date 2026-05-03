from __future__ import annotations


def test_login_success(client, auth):
    response = auth.login_as_admin()

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin/")


def test_login_fail(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "wrong@test.com",
            "password": "wrong",
        },
    )

    assert response.status_code == 401


def test_login_missing_fields_returns_400(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "",
            "password": "",
        },
    )

    assert response.status_code == 400


def test_login_page_when_already_logged_in_as_admin_redirects_to_admin(client, auth):
    auth.login_as_admin()

    response = client.get("/auth/login", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin/")


def test_login_page_when_already_logged_in_as_user_redirects_home(client, auth):
    auth.login_as_user()

    response = client.get("/auth/login", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


def test_login_page_get(client):
    response = client.get("/auth/login")

    assert response.status_code == 200


def test_register_page_get(client):
    response = client.get("/auth/register")

    assert response.status_code == 200


def test_logout_post_clears_session_and_redirects_home(client, auth):
    auth.login_as_admin()

    response = client.post("/auth/logout", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")

    protected_response = client.get("/admin/", follow_redirects=False)

    assert protected_response.status_code == 302
    assert "/auth/login" in protected_response.headers["Location"]


def test_logout_get_is_not_allowed(client):
    response = client.get("/auth/logout", follow_redirects=False)

    assert response.status_code == 405

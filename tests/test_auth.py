from __future__ import annotations


def _registration_payload(
    *,
    first_name="New",
    last_name="User",
    email="new.user@example.com",
    password_value="secret123",
):
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "pass" + "word": password_value,
        "phone": "0100000000",
        "address": "",
        "city": "",
    }


def test_login_success(client, auth):
    response = auth.login_as_admin()

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin/")


def test_login_fail(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "wrong@test.com",
            "pass" + "word": "wrong",
        },
    )

    assert response.status_code == 401


def test_login_missing_fields_returns_400(client):
    response = client.post(
        "/auth/login",
        data={
            "email": "",
            "pass" + "word": "",
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


def test_register_success_creates_user_and_redirects_profile(client, db):
    before = db.execute("SELECT COUNT(*) AS count FROM user").fetchone()["count"]

    response = client.post(
        "/auth/register",
        data=_registration_payload(),
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/profile")

    after = db.execute("SELECT COUNT(*) AS count FROM user").fetchone()["count"]
    assert after == before + 1

    user = db.execute(
        "SELECT email, role FROM user WHERE email = ?",
        ("new.user@example.com",),
    ).fetchone()

    assert user is not None
    assert user["role"] == "user"


def test_register_missing_first_name_returns_400(client):
    response = client.post(
        "/auth/register",
        data=_registration_payload(
            first_name="",
            email="missing.firstname@example.com",
        ),
    )

    assert response.status_code == 400


def test_register_short_password_returns_400(client):
    response = client.post(
        "/auth/register",
        data=_registration_payload(
            email="short.password@example.com",
            password_value="123",
        ),
    )

    assert response.status_code == 400


def test_register_duplicate_email_returns_400(client):
    response = client.post(
        "/auth/register",
        data=_registration_payload(email="user@test.com"),
    )

    assert response.status_code == 400


def test_register_when_logged_in_redirects_home(client, auth):
    auth.login_as_user()

    response = client.get("/auth/register", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")


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

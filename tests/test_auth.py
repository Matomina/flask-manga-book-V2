def test_login_success(client, auth):
    response = auth.login()
    assert response.status_code == 302  # redirect


def test_login_fail(client):
    response = client.post("/auth/login", data={
        "email": "wrong@test.com",
        "password": "wrong"
    })
    assert b"incorrect" in response.data.lower()


def test_logout(client, auth):
    auth.login()
    response = auth.logout()
    assert response.status_code == 302
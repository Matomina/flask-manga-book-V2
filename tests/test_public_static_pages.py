from __future__ import annotations


def test_cart_redirects(client):
    assert client.get("/cart", follow_redirects=False).status_code == 302


def test_panier_redirects(client):
    assert client.get("/panier", follow_redirects=False).status_code == 302


def test_cart_ok(client, auth):
    auth.login_as_user()
    assert client.get("/cart").status_code == 200


def test_panier_ok(client, auth):
    auth.login_as_user()
    assert client.get("/panier").status_code == 200


def test_help_redirects_to_about_anchor(client):
    response = client.get("/help", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/a-propos#aide")


def test_aide_redirects_to_about_anchor(client):
    response = client.get("/aide", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/a-propos#aide")

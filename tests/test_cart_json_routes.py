from __future__ import annotations


def test_cart_data_requires_login(client):
    response = client.get("/cart/data", follow_redirects=False)

    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_cart_data_returns_backend_cart_state(client, auth):
    auth.login_as_user()
    client.post(
        "/cart/add/1",
        json={"quantity": 2},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )

    response = client.get(
        "/cart/data",
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["count"] == 2
    assert payload["total"] > 0
    assert payload["items"][0]["article_id"] == 1
    assert payload["items"][0]["quantity"] == 2
    assert payload["items"][0]["image"].startswith("/static/")


def test_cart_add_json_updates_backend_cart(client, auth):
    auth.login_as_user()

    response = client.post(
        "/cart/add/1",
        json={"quantity": 1},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["count"] == 1
    assert payload["items"][0]["article_id"] == 1


def test_cart_update_json_updates_backend_cart(client, auth):
    auth.login_as_user()
    client.post(
        "/cart/add/1",
        json={"quantity": 1},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )

    response = client.post(
        "/cart/update/1",
        json={"quantity": 3},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["count"] == 3
    assert payload["items"][0]["quantity"] == 3


def test_cart_remove_json_updates_backend_cart(client, auth):
    auth.login_as_user()
    client.post(
        "/cart/add/1",
        json={"quantity": 1},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )

    response = client.post(
        "/cart/remove/1",
        json={},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["count"] == 0
    assert payload["items"] == []


def test_cart_add_json_returns_error_for_invalid_quantity(client, auth):
    auth.login_as_user()

    response = client.post(
        "/cart/add/1",
        json={"quantity": 0},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    payload = response.get_json()

    assert response.status_code == 400
    assert payload["error"] == "Quantité invalide."

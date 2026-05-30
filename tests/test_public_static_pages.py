from __future__ import annotations


def test_cart(client):
    assert client.get("/cart").status_code == 200


def test_panier(client):
    assert client.get("/panier").status_code == 200


def test_help(client):
    assert client.get("/help").status_code == 200


def test_aide(client):
    assert client.get("/aide").status_code == 200

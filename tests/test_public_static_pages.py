from __future__ import annotations


PUBLIC_STATIC_PATHS = (
    "/cart",
    "/panier",
    "/help",
    "/aide",
)


def test_public_static_paths_are_available(client):
    for path in PUBLIC_STATIC_PATHS:
        response = client.get(path)

        assert response.status_code == 200

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_contact_requires_login(client):
    response = client.post("/contact")
    assert response.status_code == 302  # redirection login
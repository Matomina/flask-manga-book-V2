def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_articles_page(client):
    response = client.get("/articles")
    assert response.status_code == 200


def test_article_detail_page(client):
    response = client.get("/articles/1")
    assert response.status_code == 200


def test_favorites_requires_login(client):
    response = client.get("/favorites")
    assert response.status_code == 302


def test_history_requires_login(client):
    response = client.get("/history")
    assert response.status_code == 302


def test_history_page(client, auth):
    auth.login()
    response = client.get("/history")
    assert response.status_code == 200


def test_contact_requires_login(client):
    response = client.post("/contact", data={"sujet": "Test", "message": "Bonjour"})
    assert response.status_code == 302


def test_contact_authenticated(client, auth):
    auth.login()
    response = client.post(
        "/contact",
        data={
            "sujet": "Commande",
            "message": "Bonjour, j'ai une question.",
        },
    )
    assert response.status_code == 302
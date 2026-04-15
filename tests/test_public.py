def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_articles_page(client):
    response = client.get("/articles")
    assert response.status_code == 200


def test_article_detail_page(client):
    response = client.get("/articles/1")
    assert response.status_code == 200


def test_contact_requires_login(client):
    response = client.post("/contact")
    assert response.status_code == 302
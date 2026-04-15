def test_forum_page(client):
    response = client.get("/forum/")
    assert response.status_code == 200


def test_create_topic_requires_login(client):
    response = client.post("/forum/create")
    assert response.status_code == 302
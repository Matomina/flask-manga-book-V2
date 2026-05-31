from __future__ import annotations


def _create_topic(
    db,
    title: str = "Sujet live",
    message: str = "Contenu live",
) -> int:
    cursor = db.execute(
        "INSERT INTO topics (user_id, title, message) VALUES (?, ?, ?)",
        (1, title, message),
    )
    db.commit()
    return int(cursor.lastrowid)


def _create_reply(db, topic_id: int, message: str = "Réponse live") -> int:
    cursor = db.execute(
        "INSERT INTO replies (topic_id, user_id, message) VALUES (?, ?, ?)",
        (topic_id, 1, message),
    )
    db.commit()
    return int(cursor.lastrowid)


def test_forum_index_has_modern_live_markers(client, db):
    _create_topic(db)

    response = client.get("/forum/")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "MangaBook Community" in html
    assert "data-forum-live=\"index\"" in html
    assert "data-forum-topic-list" in html
    assert "forum-live.js" in html
    assert "forum.css" in html


def test_forum_detail_has_modern_live_markers(client, db):
    topic_id = _create_topic(db)
    _create_reply(db, topic_id)

    response = client.get(f"/forum/{topic_id}")
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "data-forum-live=\"detail\"" in html
    assert f"data-topic-id=\"{topic_id}\"" in html
    assert "data-forum-replies-list" in html
    assert "data-forum-reply-form" in html
    assert "forum-live.js" in html


def test_forum_api_topics_returns_live_payload(client, db):
    topic_id = _create_topic(db, title="API topic", message="API message")
    _create_reply(db, topic_id)

    response = client.get("/forum/api/topics")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["topic_count"] >= 1
    assert payload["reply_count"] >= 1
    assert payload["topics"][0]["id"] == topic_id
    assert payload["topics"][0]["title"] == "API topic"
    assert payload["topics"][0]["url"].endswith(f"/forum/{topic_id}")


def test_forum_api_topic_returns_replies(client, db):
    topic_id = _create_topic(db)
    reply_id = _create_reply(db, topic_id, message="Réponse API")

    response = client.get(f"/forum/api/topics/{topic_id}")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["topic"]["id"] == topic_id
    assert payload["reply_count"] == 1
    assert payload["replies"][0]["id"] == reply_id
    assert payload["replies"][0]["message"] == "Réponse API"


def test_forum_create_topic_json_success(client, auth):
    auth.login_as_user()

    response = client.post(
        "/forum/create",
        json={"title": "JSON topic", "message": "JSON body"},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["topic"]["title"] == "JSON topic"
    assert payload["topic"]["message"] == "JSON body"
    assert payload["topic"]["reply_count"] == 0


def test_forum_reply_json_success(client, auth, db):
    topic_id = _create_topic(db)
    auth.login_as_user()

    response = client.post(
        f"/forum/{topic_id}/reply",
        json={"message": "Réponse JSON"},
        headers={"X-Requested-With": "XMLHttpRequest"},
    )
    payload = response.get_json()

    assert response.status_code == 201
    assert payload["reply"]["message"] == "Réponse JSON"
    assert payload["reply_count"] == 1
    assert payload["replies"][0]["message"] == "Réponse JSON"
